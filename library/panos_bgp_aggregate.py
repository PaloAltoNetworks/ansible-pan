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
module: panos_bgp_aggregate
short_description: Configures a BGP Aggregation Prefix Policy
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
    as_set:
        description:
            - Generate AS-set attribute.
            default: False
    attr_as_path_limit:
        description:
            - Add AS path limit attribute if it does not exist.
    attr_as_path_prepend_times:
        description:
            - Prepend local AS for specified number of times.
    attr_as_path_type:
        description:
            - AS path update options.
                - none
                - remove
                - prepend
                - remove-and-prepend
            default: none
    attr_community_argument:
        description:
            - Argument to the action community value if needed.
    attr_community_type:
        description:
            - Community update options.
                - none
                - remove-all
                - remove-regex
                - append
                - overwrite
            default: none
    attr_extended_community_argument:
        description:
            - Argument to the action extended community value if needed.
    attr_extended_community_type:
        description:
            - Extended community update options.
                - none
                - remove-all
                - remove-regex
                - append
                - overwrite
            default: none
    attr_local_preference:
        description:
            - New Local Preference value.
    attr_med:
        description:
            - New Multi-Exit Discriminator value.
    attr_nexthop:
        description:
            - Next-hop address.
    attr_origin:
        description:
            - New route origin.
                - igp
                - egp
                - incomplete
            default: incomplete
    attr_weight:
        description:
            - New weight value.
    enable:
        description:
            - Enable policy.
            default: True
    name:
        description:
            - Name of policy.
            required: True
    prefix:
        description:
            - Aggregating address prefix.
    summary:
        description:
            - Summarize route.
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default
'''

EXAMPLES = '''
    - name: Create BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        name: aggr-rule-01
        prefix: 10.0.0.0/24
        enable: true
        summary: true

    - name: Remove BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: aggr-rule-01
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


def main():
    argument_spec = dict(
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
            help='Name of policy'),
        enable=dict(
            default=True, type='bool',
            help='Enable policy'),
        prefix=dict(
            type='str',
            help='Aggregating address prefix'),
        summary=dict(
            type='bool',
            help='Summarize route'),
        as_set=dict(
            type='bool', default=False,
            help='Generate AS-set attribute'),
        attr_local_preference=dict(
            type='int',
            help='New Local Preference value'),
        attr_med=dict(
            type='int',
            help='New Multi-Exit Discriminator value'),
        attr_weight=dict(
            type='int',
            help='New weight value'),
        attr_nexthop=dict(
            type='list',
            help='Next-hop address'),
        attr_origin=dict(
            type='str', default='incomplete', choices=['igp', 'egp', 'incomplete'],
            help='New route origin'),
        attr_as_path_limit=dict(
            type='int',
            help='Add AS path limit attribute if it does not exist'),
        attr_as_path_type=dict(
            type='str', default='none', choices=['none', 'remove', 'prepend', 'remove-and-prepend'],
            help='AS path update options'),
        attr_as_path_prepend_times=dict(
            type='int',
            help='Prepend local AS for specified number of times'),
        attr_community_type=dict(
            type='str', default='none', choices=['none', 'remove-all', 'remove-regex', 'append', 'overwrite'],
            help='Community update options'),
        attr_community_argument=dict(
            type='str',
            help='Argument to the action community value if needed'),
        attr_extended_community_type=dict(
            type='str', default='none', choices=['none', 'remove-all', 'remove-regex', 'append', 'overwrite'],
            help='Extended community update options'),
        attr_extended_community_argument=dict(
            type='str',
            help='Argument to the action extended community value if needed'),
    )
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

    attr_as_path_type = module.params['attr_as_path_type']
    attr_as_path_prepend_times = module.params['attr_as_path_prepend_times']
    attr_community_type = module.params['attr_community_type']
    attr_community_argument = module.params['attr_community_argument']
    attr_extended_community_type = module.params['attr_extended_community_type']
    attr_extended_community_argument = module.params['attr_extended_community_argument']

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

        new_obj = network.BgpPolicyAggregationAddress(**obj_spec)
        cur_obj = vr.find(name, network.BgpPolicyAggregationAddress, recursive=True)

        # compare differences between the current state vs desired state
        if state == 'present':
            # confirm values are set as needed
            if attr_as_path_type in ['prepend', 'remove-and-prepend']:
                if attr_as_path_prepend_times is None:
                    raise ValueError(
                        "An attr_as_path_type of 'prepend'|'remove-and-prepend' " +
                        'requires attr_as_path_prepend_times be set')
            if attr_community_type in ['remove-regex', 'append', 'overwrite']:
                if attr_community_argument is None:
                    raise ValueError(
                        "An attr_community_type of 'remove-regex'|'append'|'overwrite' " +
                        'requires attr_community_argument be set')
            if attr_extended_community_type in ['remove-regex', 'append', 'overwrite']:
                if attr_extended_community_argument is None:
                    raise ValueError(
                        "An attr_extended_community_type of 'remove-regex'|'append'|'overwrite' " +
                        'requires attr_extended_community_argument be set')

            # it seems all is well, preceed with update
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=True):
                bgp.add(new_obj)
                vr.add(bgp)
                new_obj.create()
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
        module.exit_json(msg='BGP aggregation address update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
