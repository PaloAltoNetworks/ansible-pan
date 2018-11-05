#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2018 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_bgp
short_description: Configures Border Gateway Protocol (BGP)
description:
    - Use BGP to publish and consume routes from disparate networks.
author: "Joshua Colson (@freakinhippie)"
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is NOT supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Add or remove BGP configuration.
        choices: ['present', 'absent']
        default: 'present'
    commit:
        description:
            - Commit configuration if changed.
        default: true
    enable:
        description:
            - Enable BGP.
        default: true
    router_id:
        description:
            - Router ID in IP format (eg. 1.1.1.1)
        required: true
    reject_default_route:
        description:
            - Reject default route.
        default: true
    allow_redist_default_route:
        description:
            - Allow redistribute default route to BGP.
        default: false
    install_route:
        description:
            - Populate BGP learned route to global route table.
        default: false
    ecmp_multi_as:
        description:
            - Support multiple AS in ECMP.
        default: false
    enforce_first_as:
        description:
            - Enforce First AS for EBGP.
        default: true
    local_as:
        description:
            - Local Autonomous System (AS) number.
    as_format:
        description:
            - AS format I('2-byte')/I('4-byte').
        default: '2-byte'
    always_compare_med:
        description:
            - Always compare MEDs.
        default: false
    deterministic_med_comparison:
        description:
            - Deterministic MEDs comparison.
        default: true
    default_local_preference:
        description:
            - Default local preference.
        default: 100
    graceful_restart_enable:
        description:
            - Enable graceful restart.
        default: true
    gr_stale_route_time:
        description:
            - Time to remove stale routes after peer restart (in seconds).
    gr_local_restart_time:
        description:
            - Local restart time to advertise to peer (in seconds).
    gr_max_peer_restart_time:
        description:
            - Maximum of peer restart time accepted (in seconds).
    reflector_cluster_id:
        description:
            - Route reflector cluster ID.
    confederation_member_as:
        description:
            - Confederation requires member-AS number.
    aggregate_med:
        description:
            - Aggregate route only if they have same MED attributes.
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        default: "default"
'''

EXAMPLES = '''
- name: Configure and enable BGP
    panos_bgp:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      router_id: '1.1.1.1'
      local_as: '64512'
      commit: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import base
    from pandevice import panorama
    from pandevice.errors import PanDeviceError
    from pandevice import network

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def setup_args():
    return dict(
        ip_address=dict(
            required=True,
            help='IP address (or hostname) of PAN-OS device being configured'),
        password=dict(
            no_log=True,
            help='Password credentials to use for auth unless I(api_key) is set'),
        username=dict(
            default='admin',
            help='Username credentials to use for auth unless I(api_key) is set'),
        api_key=dict(
            no_log=True,
            help='API key that can be used instead of I(username)/I(password) credentials'),
        state=dict(
            default='present', choices=['present', 'absent'],
            help='Add or remove BGP configuration'),
        enable=dict(
            default=True, type='bool',
            help='Enable BGP'),
        router_id=dict(
            type='str',
            help='Router ID in IP format (eg. 1.1.1.1)'),
        reject_default_route=dict(
            type='bool', default=True,
            help='Reject default route'),
        allow_redist_default_route=dict(
            type='bool', default=False,
            help='Allow redistribute default route to BGP'),
        install_route=dict(
            type='bool', default=False,
            help='Populate BGP learned route to global route table'),
        ecmp_multi_as=dict(
            type='bool', default=False,
            help='Support multiple AS in ECMP'),
        enforce_first_as=dict(
            type='bool', default=True,
            help='Enforce First AS for EBGP'),
        local_as=dict(
            type='str',
            help='Local Autonomous System (AS) number'),
        as_format=dict(
            type='str', default='2-byte', choices=['2-byte', '4-byte'],
            help='AS format I("2-byte")/I("4-byte")'),
        always_compare_med=dict(
            type='bool', default=False,
            help='Always compare MEDs'),
        deterministic_med_comparison=dict(
            type='bool', default=True,
            help='Deterministic MEDs comparison'),
        default_local_preference=dict(
            type='int',
            help='Default local preference'),
        graceful_restart_enable=dict(
            type='bool', default=True,
            help='Enable graceful restart'),
        gr_stale_route_time=dict(
            type='int',
            help='Time to remove stale routes after peer restart (in seconds)'),
        gr_local_restart_time=dict(
            type='int',
            help='Local restart time to advertise to peer (in seconds)'),
        gr_max_peer_restart_time=dict(
            type='int',
            help='Maximum of peer restart time accepted (in seconds)'),
        reflector_cluster_id=dict(
            type='str',
            help='Route reflector cluster ID'),
        confederation_member_as=dict(
            type='str',
            help='Confederation requires member-AS number'),
        aggregate_med=dict(
            type='bool', default=True,
            help='Aggregate route only if they have same MED attributes'),
        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),
    )


def main():
    argument_spec = setup_args()
    
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get the firewall / panorama auth.
    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password', 'api_key')]

    # generate the kwargs for network.Bgp
    bgp_params = [
        'enable', 'router_id', 'reject_default_route', 'allow_redist_default_route',
        'install_route', 'ecmp_multi_as', 'enforce_first_as', 'local_as'
    ]

    bgp_spec = dict((k, module.params[k]) for k in bgp_params)

    # generate the kwargs for network.BgpRoutingOptions
    bgp_routing_options_params = [
        'as_format', 'always_compare_med', 'deterministic_med_comparison',
        'default_local_preference', 'graceful_restart_enable',
        'gr_stale_route_time', 'gr_local_restart_time', 'gr_max_peer_restart_time',
        'reflector_cluster_id', 'confederation_member_as', 'aggregate_med',
    ]
    bgp_routing_options_spec = dict((k, module.params[k]) for k in bgp_routing_options_params)

    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    bgp = network.Bgp(**bgp_spec)
    bgp_routing_options = network.BgpRoutingOptions(**bgp_routing_options_spec)

    changed = False
    try:
        # Create the device with the appropriate pandevice type
        device = base.PanDevice.create_from_device(*auth)
        network.VirtualRouter.refreshall(device)

        # grab the virtual router
        vr = device.find(vr_name, network.VirtualRouter)
        if vr is None:
            raise ValueError('Virtual router {0} does not exist'.format(vr_name))

        # fetch the current settings
        current_bgp = vr.find('', network.Bgp) or network.Bgp()
        current_options = current_bgp.find('', network.BgpRoutingOptions) or network.BgpRoutingOptions()

        # compare differences between the current state vs desired state
        changed |= not bgp.equal(current_bgp, compare_children=False)
        changed |= not bgp_routing_options.equal(current_options, compare_children=False)

        if state == 'present':
            if changed:
                bgp.add(bgp_routing_options)
                vr.add(bgp)
                bgp.create()
            else:
                module.exit_json(msg='no changes required.', changed=changed)
        elif state == 'absent':
            current_bgp.delete()
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    module.exit_json(msg='BGP configuration successful.', changed=changed)


if __name__ == '__main__':
    main()
