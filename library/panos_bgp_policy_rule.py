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
module: panos_bgp_policy_rule
short_description: Configures a BGP Policy Import/Export Rule
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
            - Add or remove BGP Policy Import/Export Rule.
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
                - allow
                - deny
    action_as_path_limit:
        description:
            - Add AS path limit attribute if it does not exist.
    action_as_path_prepend_times:
        description:
            - Prepend local AS for specified number of times.
    action_as_path_type:
        description:
            - AS path update options.
                - none
                - remove
                - prepend
                - remove-and-prepend
    action_community_argument:
        description:
            - Argument to the action community value if needed.
    action_community_type:
        description:
            - Community update options.
                - none
                - remove-all
                - remove-regex
                - append
                - overwrite
    action_dampening:
        description:
            - Route flap dampening profile; only with "import" type.
    action_extended_community_argument:
        description:
            - Argument to the action extended community value if needed.
    action_extended_community_type:
        description:
            - Extended community update options.
    action_local_preference:
        description:
            - New local preference value.
    action_med:
        description:
            - New MED value.
    action_nexthop:
        description:
            - Nexthop address.
    action_origin:
        description:
            - New route origin.
                - igp
                - egp
                - incomplete
    action_weight:
        description:
            - New weight value; only with "import" type.
    address_prefix:
        description:
            - List of Address Prefix dicts with "name"/"exact" keys.
    enable:
        description:
            - Enable rule.
            default: True
    match_afi:
        description:
            - Address Family Identifier.
                - ip
                - ipv6
    match_as_path_regex:
        description:
            - AS-path regular expression.
    match_community_regex:
        description:
            - Community AS-path regular expression.
    match_extended_community_regex:
        description:
            - Extended Community AS-path regular expression.
    match_from_peer:
        description:
            - Filter by peer that sent this route.
    match_med:
        description:
            - Multi-Exit Discriminator.
    match_nexthop:
        description:
            - Next-hop attributes.
    match_route_table:
        description:
            - Route table to match rule.
                - unicast
                - multicast
                - both
    match_safi:
        description:
            - Subsequent Address Family Identifier.
                - ip
                - ipv6
    name:
        description:
            - Name of filter.
            required: True
    type:
        description:
            - The type of rule.
                - import
                - export
            required: True
    used_by:
        description:
            - Peer-groups that use this rule.
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default

'''

EXAMPLES = '''
# Add a BGP Policy
  - name: Create Policy Import Rule
    panos_bgp_policy_rule:
      ip_address: "192.168.1.1"
      password: "admin"
      state: present
      vr_name: default
      name: import-rule-001
      type: import
      enable: true
      action: allow
      action_dampening: dampening-profile

  - name: Create Policy Export Rule
    panos_bgp_policy_rule:
      ip_address: "192.168.1.1"
      password: "admin"
      state: present
      vr_name: default
      name: export-rule-001
      type: export
      enable: true
      action: allow

  - name: Disable Import Rule
    panos_bgp_policy_rule:
      ip_address: "192.168.1.1"
      password: "admin"
      state: present
      vr_name: default
      name: import-rule-001
      type: import
      enable: false

  - name: Remove Export Rule
    panos_bgp_policy_rule:
      ip_address: "192.168.1.1"
      password: "admin"
      state: absent
      vr_name: default
      name: export-rule-001
      type: export
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
            help='Add or remove BGP Policy Import/Export Rule'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),

        type=dict(
            type='str', required=True, choices=['import', 'export'],
            help='The type of rule'),
        name=dict(
            type='str', required=True,
            help='Name of filter'),
        enable=dict(
            default=True, type='bool',
            help='Enable rule'),
        used_by=dict(
            type='list',
            help='Peer-groups that use this rule'),
        match_afi=dict(
            type='str', choices=['ip', 'ipv6'],
            help='Address Family Identifier'),
        match_safi=dict(
            type='str', choices=['ip', 'ipv6'],
            help='Subsequent Address Family Identifier'),
        match_route_table=dict(
            type='str', choices=['unicast', 'multicast', 'both'],
            help='Route table to match rule'),
        match_nexthop=dict(
            type='list',
            help='Next-hop attributes'),
        match_from_peer=dict(
            type='list',
            help='Filter by peer that sent this route'),
        match_med=dict(
            type='int',
            help='Multi-Exit Discriminator'),
        match_as_path_regex=dict(
            type='str',
            help='AS-path regular expression'),
        match_community_regex=dict(
            type='str',
            help='Community AS-path regular expression'),
        match_extended_community_regex=dict(
            type='str',
            help='Extended Community AS-path regular expression'),
        action=dict(
            type='str', choices=['allow', 'deny'],
            help='Rule action'),
        action_dampening=dict(
            type='str',
            help='Route flap dampening profile; only with "import" type'),
        action_weight=dict(
            type='int',
            help='New weight value; only with "import" type'),
        action_local_preference=dict(
            type='int',
            help='New local preference value'),
        action_med=dict(
            type='int',
            help='New MED value'),
        action_nexthop=dict(
            type='str',
            help='Nexthop address'),
        action_origin=dict(
            type='str', choices=['igp', 'egp', 'incomplete'],
            help='New route origin'),
        action_as_path_limit=dict(
            type='int',
            help='Add AS path limit attribute if it does not exist'),
        action_as_path_type=dict(
            type='str', choices=['none', 'remove', 'prepend', 'remove-and-prepend'],
            help='AS path update options'),
        action_as_path_prepend_times=dict(
            type='int',
            help='Prepend local AS for specified number of times'),
        action_community_type=dict(
            type='str', choices=['none', 'remove-all', 'remove-regex', 'append', 'overwrite'],
            help='Community update options'),
        action_community_argument=dict(
            type='str',
            help='Argument to the action community value if needed'),
        action_extended_community_type=dict(
            type='str',
            help='Extended community update options'),
        action_extended_community_argument=dict(
            type='str',
            help='Argument to the action extended community value if needed'),
        address_prefix=dict(
            type='list',
            help='List of Address Prefix dicts with "name"/"exact" keys'),
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
    exclude_list += ['type', 'vr_name', 'address_prefix']

    # export rules don't support action_weight or action_dampening
    if module.params['type'] == 'export':
        exclude_list += ['action_weight', 'action_dampening']

    # generate the kwargs for network.BgpPolicyRule
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    prefixes = module.params['address_prefix']
    rule_type = module.params['type']
    name = module.params['name']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    action_as_path_type = module.params['action_as_path_type']
    action_as_path_prepend_times = module.params['action_as_path_prepend_times']
    action_community_type = module.params['action_community_type']
    action_community_argument = module.params['action_community_argument']
    action_extended_community_type = module.params['action_extended_community_type']
    action_extended_community_argument = module.params['action_extended_community_argument']

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

        # create the new state object
        if rule_type == 'import':
            new_obj = network.BgpPolicyImportRule(**obj_spec)
            cur_obj = vr.find(name, network.BgpPolicyImportRule, recursive=True)
        elif rule_type == 'export':
            new_obj = network.BgpPolicyExportRule(**obj_spec)
            cur_obj = vr.find(name, network.BgpPolicyExportRule, recursive=True)
        else:
            raise ValueError('Policy rule type {0} is not supported'.format(rule_type))

        # add the prefix children
        if isinstance(prefixes, list):
            for prefix in prefixes:
                if prefix.get('name'):
                    pfx = network.BgpPolicyAddressPrefix(**prefix)
                    new_obj.add(pfx)

        # compare differences between the current state vs desired state
        if state == 'present':
            # confirm values are set as needed
            if action_as_path_type in ['prepend', 'remove-and-prepend']:
                if action_as_path_prepend_times is None:
                    raise ValueError(
                        "An action_as_path_type of 'prepend'|'remove-and-prepend' " +
                        'requires action_as_path_prepend_times be set')
            if action_community_type in ['remove-regex', 'append', 'overwrite']:
                if action_community_argument is None:
                    raise ValueError(
                        "An action_community_type of 'remove-regex'|'append'|'overwrite' " +
                        'requires action_community_argument be set')
            if action_extended_community_type in ['remove-regex', 'append', 'overwrite']:
                if action_extended_community_argument is None:
                    raise ValueError(
                        "An action_extended_community_type of 'remove-regex'|'append'|'overwrite' " +
                        'requires action_extended_community_argument be set')

            # it seems all is well, preceed with update
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
        module.exit_json(msg='BGP policy rule update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
