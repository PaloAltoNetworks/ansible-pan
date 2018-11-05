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
module: panos_redistribution
short_description: Configures a Redistribution Profile on a virtual router
description:
    - Configures a Redistribution Profile on a virtual router
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
            - Add or remove Route Redistribution Rule.
                - present
                - absent
            default: present
    commit:
        description:
            - Commit configuration if changed.
            default: True
    action:
        description:
            - Rule action.
                - no-redist
                - redist
            default: no-redist
    bgp_filter_community:
        description:
            - BGP filter on community.
    bgp_filter_extended_community:
        description:
            - BGP filter on extended community.
    filter_destination:
        description:
            - Filter destination.
    filter_interface:
        description:
            - Filter interface.
    filter_nexthop:
        description:
            - Filter nexthop.
    filter_type:
        description:
            - Any of 'static', 'connect', 'rip', 'ospf', or 'bgp'.
    name:
        description:
            - Name of rule.
            required: True
    ospf_filter_area:
        description:
            - OSPF filter on area.
    ospf_filter_pathtype:
        description:
            - Any of 'intra-area', 'inter-area', 'ext-1', or 'ext-2'.
    ospf_filter_tag:
        description:
            - OSPF filter on tag.
    priority:
        description:
            - Priority ID.
    type:
        description:
            - Name of rule.
                - ipv4
                - ipv6
            default: ipv4
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default
'''

EXAMPLES = '''
- name: Create Redistribution Profile
    panos_redistribution:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
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
            help='Add or remove Route Redistribution Rule'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
        type=dict(
            type='str', default='ipv4', choices=['ipv4', 'ipv6'],
            help='Name of rule'),

        name=dict(
            type='str', required=True,
            help='Name of rule'),
        priority=dict(
            type='int',
            help='Priority ID'),
        action=dict(
            type='str', default='no-redist', choices=['no-redist', 'redist'],
            help='Rule action'),
        filter_type=dict(
            type='list',
            help="Any of 'static', 'connect', 'rip', 'ospf', or 'bgp'"),
        filter_interface=dict(
            type='list',
            help='Filter interface'),
        filter_destination=dict(
            type='list',
            help='Filter destination'),
        filter_nexthop=dict(
            type='list',
            help='Filter nexthop'),
        ospf_filter_pathtype=dict(
            type='list',
            help="Any of 'intra-area', 'inter-area', 'ext-1', or 'ext-2'"),
        ospf_filter_area=dict(
            type='list',
            help='OSPF filter on area'),
        ospf_filter_tag=dict(
            type='list',
            help='OSPF filter on tag'),
        bgp_filter_community=dict(
            type='list',
            help='BGP filter on community'),
        bgp_filter_extended_community=dict(
            type='list',
            help='BGP filter on extended community'),
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
    exclude_list += ['vr_name', 'type']

    # generate the kwargs for network.BgpPolicyRule
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']
    filter_type = module.params['type']

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

        if filter_type == 'ipv4':
            new_obj = network.RedistributionProfile(**obj_spec)
            cur_obj = vr.find(name, network.RedistributionProfile, recursive=True)
        elif filter_type == 'ipv6':
            new_obj = network.RedistributionProfileIPv6(**obj_spec)
            cur_obj = vr.find(name, network.RedistributionProfileIPv6, recursive=True)
        else:
            raise ValueError("Filter type '{0}' is unsupported".format(filter_type))

        # compare differences between the current state vs desired state
        if state == 'present':
            # it seems all is well, preceed with update
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=True):
                vr.add(new_obj)
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
        module.exit_json(msg='Redistribution policy rule update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
