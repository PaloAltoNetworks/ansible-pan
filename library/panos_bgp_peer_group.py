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
module: panos_bgp_peer_group
short_description: Configures a BGP Peer Group
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
            required: True
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
            default: admin
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Add or remove BGP Peer Group configuration.
                - present
                - absent
            default: present
    commit:
        description:
            - Commit configuration if changed.
            default: True
    aggregated_confed_as_path:
        description:
            - The peers understand Aggregated Confederation AS Path.
    enable:
        description:
            - Enable BGP peer group.
            default: True
    export_nexthop:
        description:
            - Export locally resolved nexthop I("resolve")/I("use-self").
                - resolve
                - use-self
            default: resolve
    import_nexthop:
        description:
            - Override nexthop with peer address I("original")/I("use-peer"), only with "ebgp".
                - original
                - use-peer
            default: original
    name:
        description:
            - Name of the BGP peer group.
            required: True
    remove_private_as:
        description:
            - Remove private AS when exporting route, only with "ebgp".
    soft_reset_with_stored_info:
        description:
            - Enable soft reset with stored info.
    type:
        description:
            - Peer group type I("ebgp")/I("ibgp")/I("ebgp-confed")/I("ibgp-confed").
                - ebgp
                - ibgp
                - ebgp-confed
                - ibgp-confed
            default: ebgp
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default
'''

EXAMPLES = '''
- name: Create BGP Peer Group
    panos_bgp_peer_group:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: peer-group-1
      enable: true
      aggregated_confed_as_path: true
      soft_reset_with_stored_info: false
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
            help='Add or remove BGP Peer Group configuration'),
        name=dict(
            type='str', required=True,
            help='Name of the BGP peer group'),
        enable=dict(
            default=True, type='bool',
            help='Enable BGP peer group'),
        aggregated_confed_as_path=dict(
            type='bool',
            help='The peers understand Aggregated Confederation AS Path'),
        soft_reset_with_stored_info=dict(
            type='bool',
            help='Enable soft reset with stored info'),
        type=dict(
            type='str', default='ebgp', choices=['ebgp', 'ibgp', 'ebgp-confed', 'ibgp-confed'],
            help='Peer group type I("ebgp")/I("ibgp")/I("ebgp-confed")/I("ibgp-confed")'),
        export_nexthop=dict(
            type='str', default='resolve', choices=['resolve', 'use-self'],
            help='Export locally resolved nexthop I("resolve")/I("use-self")'),
        import_nexthop=dict(
            type='str', default='original', choices=['original', 'use-peer'],
            help='Override nexthop with peer address I("original")/I("use-peer"), only with "ebgp"'),
        remove_private_as=dict(
            type='bool',
            help='Remove private AS when exporting route, only with "ebgp"'),
        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
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

    # exclude the default items from kwargs passed to the object
    exclude_list = ['ip_address', 'username', 'password', 'api_key', 'state', 'commit']
    # exclude these items from the kwargs passed to the object
    exclude_list += ['vr_name']

    # generate the kwargs for network.BgpPeer
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    # # generate the kwargs for network.BgpPeerGroup
    # group_params = [
    #     'name', 'enable', 'aggregated_confed_as_path', 'soft_reset_with_stored_info',
    #     'type', 'export_nexthop', 'import_nexthop', 'remove_private_as'
    # ]
    # group_spec = dict((k, module.params[k]) for k in group_params)

    name = module.params['name']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    # create the new state object
    group = network.BgpPeerGroup(**obj_spec)

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
        bgp = vr.find('', network.Bgp) or network.Bgp()
        current_group = vr.find(name, network.BgpPeerGroup, recursive=True)

        # compare differences between the current state vs desired state
        if not group.equal(current_group, compare_children=False):
            changed = True

        if state == 'present':
            if current_group is None or not group.equal(current_group, compare_children=False):
                bgp.add(group)
                vr.add(bgp)
                group.create()
                changed = True
        elif state == 'absent':
            if current_group is not None:
                current_group.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='BGP peer group update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
