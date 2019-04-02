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
module: panos_bgp_redistribute
short_description: Configures a BGP Redistribution Rule
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
            - Add or remove BGP Aggregate Policy.
                - present
                - absent
        default: present
    commit:
        description:
            - Commit configuration if changed.
        default: True
    address_family_identifier:
        description:
            - Address Family Identifier.
                - ipv4
                - ipv6
        default: ipv4
    enable:
        description:
            - Enable rule.
        default: True
    metric:
        description:
            - Metric value.
    name:
        description:
            - Name of rule; must match a defined Redistribution Profile in the virtual router.
        required: True
    route_table:
        description:
            - Summarize route.
                - unicast
                - multicast
                - both
        default: unicast
    set_as_path_limit:
        description:
            - Add the AS_PATHLIMIT path attribute.
    set_community:
        description:
            - Add the COMMUNITY path attribute.
    set_extended_community:
        description:
            - Add the EXTENDED COMMUNITY path attribute.
    set_local_preference:
        description:
            - Add the LOCAL_PREF path attribute.
    set_med:
        description:
            - Add the MULTI_EXIT_DISC path attribute.
    set_origin:
        description:
            - New route origin.
                - igp
                - egp
                - incomplete
        default: incomplete
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
        default: default
'''

EXAMPLES = '''
- name: Create BGP Peer Group
    panos_bgp_policy_rule:
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
            help='Add or remove BGP Aggregate Policy'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),

        name=dict(
            type='str', required=True,
            help='Name of rule; must match a defined Redistribution Profile in the virtual router'),
        enable=dict(
            default=True, type='bool',
            help='Enable rule'),
        address_family_identifier=dict(
            type='str', default='ipv4', choices=['ipv4', 'ipv6'],
            help='Address Family Identifier'),
        route_table=dict(
            type='str', default='unicast', choices=['unicast', 'multicast', 'both'],
            help='Summarize route'),
        set_origin=dict(
            type='str', default='incomplete', choices=['igp', 'egp', 'incomplete'],
            help='New route origin'),
        set_med=dict(
            type='int',
            help='Add the MULTI_EXIT_DISC path attribute'),
        set_local_preference=dict(
            type='int',
            help='Add the LOCAL_PREF path attribute'),
        set_as_path_limit=dict(
            type='int',
            help='Add the AS_PATHLIMIT path attribute'),
        set_community=dict(
            type='list',
            help='Add the COMMUNITY path attribute'),
        set_extended_community=dict(
            type='list',
            help='Add the EXTENDED COMMUNITY path attribute'),
        metric=dict(
            type='int',
            help='Metric value'),
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

    # generate the kwargs for network.BgpPolicyRule
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

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

        new_obj = network.BgpRedistributionRule(**obj_spec)
        cur_obj = vr.find(name, network.BgpRedistributionRule, recursive=True)

        # compare differences between the current state vs desired state
        if state == 'present':
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=True):
                bgp.add(new_obj)
                vr.add(bgp)
                new_obj.apply()
                changed = True
        elif state == 'absent':
            if cur_obj is not None:
                cur_obj.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='BGP redistribution rule update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
