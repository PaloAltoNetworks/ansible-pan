#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: panos_bgp_policy_filter
short_description: Configures a BGP Policy Import/Export Rule
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.full_template_support
options:
    state:
        description:
            - Add or remove BGP Policy Filter.
            - I(state=return-object) is deprecated and will be removed in 2.12.
        choices:
            - present
            - absent
            - return-object
        default: 'present'
    commit:
        description:
            - Commit configuration if changed.
        default: True
        type: bool
    filter_type:
        description:
            - The type of filter.
        choices:
            - non-exist
            - advertise
            - suppress
        required: True
    policy_name:
        description:
            - The name of the policy object.
    policy_type:
        description:
            - The type of policy object.
        choices:
            - conditional-advertisement
            - aggregate
        required: True
    name:
        description:
            - Name of filter.
        required: True
    enable:
        description:
            - Enable filter.
        default: True
        type: bool
    address_prefix:
        description:
            - List of address prefix strings or dicts with "name"/"exact" keys.
            - Using the dict form for address prefixes should only be used with
              I(policy_type=aggregate).
        type: list
    match_afi:
        description:
            - Address Family Identifier.
        choices:
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
        choices:
            - unicast
            - multicast
            - both
    match_safi:
        description:
            - Subsequent Address Family Identifier.
        choices:
            - ip
            - ipv6
    vr_name:
        description:
            - Name of the virtual router; it must already exist and have BGP configured.
            - See M(panos_virtual_router).
        default: default
'''

EXAMPLES = '''

'''

RETURN = '''
# Default return values
panos_obj:
    description: a serialized policy filter is returned when state == 'return-object'
    returned: success
    type: string
    sample: "LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBOWl6TGM9bXcwM3JHUGVhRlNiY0dCR0srNERUQT09"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection
from ansible.module_utils._text import to_text


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import VirtualRouter
    from pandevice.network import Bgp
    from pandevice.network import BgpPolicyAggregationAddress
    from pandevice.network import BgpPolicyConditionalAdvertisement
    from pandevice.network import BgpPolicyNonExistFilter
    from pandevice.network import BgpPolicyAdvertiseFilter
    from pandevice.network import BgpPolicySuppressFilter
    from pandevice.network import BgpPolicyAddressPrefix
except ImportError:
    pass


def purge_stale_prefixes(cur_filter, new_prefixes):
    if cur_filter is None:
        return

    new_names = set(p.get('name') for p in new_prefixes if 'name' in p)
    cur_names = set(p.name for p in cur_filter.findall(network.BgpPolicyAddressPrefix))

    stale_prefixes = cur_names - new_names

    for name in stale_prefixes:
        cur_filter.find(name, network.BgpPolicyAddressPrefix).delete()


def setup_args():
    return dict(
        # TODO(gfreeman) - remove this later on and use the default state.
        state=dict(
            default='present', choices=['present', 'absent', 'return-object'],
            help='Add or remove BGP Policy Filter'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
        policy_type=dict(
            type='str', required=True, choices=['conditional-advertisement', 'aggregate'],
            help='The type of policy object'),
        policy_name=dict(
            type='str',
            help='The name of the policy object'),
        filter_type=dict(
            type='str', required=True, choices=['non-exist', 'advertise', 'suppress'],
            help='The type of filter'),

        name=dict(
            type='str', required=True,
            help='Name of filter'),
        enable=dict(
            default=True, type='bool',
            help='Enable filter'),
        match_afi=dict(
            type='str', choices=['ip', 'ipv6'],
            help='Address Family Identifier'),
        match_safi=dict(
            type='str', choices=['ip', 'ipv6'],
            help='Subsequent Address Family Identifier'),
        match_route_table=dict(
            type='str', default='unicast', choices=['unicast', 'multicast', 'both'],
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
        address_prefix=dict(
            type='list',
            help='List of Address Prefix objects'),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    vr = VirtualRouter(module.params['vr_name'])
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    bgp = vr.find('', Bgp)
    if bgp is None:
        module.fail_json(msg='BGP is not configured for virtual router {0}'.format(vr.name))

    policy = None
    if module.params['policy_type'] == 'conditional-advertisement':
        policy_cls = BgpPolicyConditionalAdvertisement
    else:
        policy_cls = BgpPolicyAggregationAddress
    policy = bgp.find_or_create(module.params['policy_name'], policy_cls)

    obj_type = None
    if module.params['filter_type'] == 'non-exist':
        obj_type = BgpPolicyNonExistFilter
    elif module.params['filter_type'] == 'advertise':
        obj_type = BgpPolicyAdvertiseFilter
    elif module.params['filter_type'] == 'suppress':
        obj_type = BgpPolicySuppressFilter
    else:
        module.fail_json(msg='Unknown filter_type: {0}'.format(module.params['filter_type']))
    listing = policy.findall(obj_type)

    spec = {
        'name': module.params['name'],
        'enable': module.params['enable'],
        'match_afi': module.params['match_afi'],
        'match_safi': module.params['match_safi'],
        'match_route_table': module.params['match_route_table'],
        'match_nexthop': module.params['match_nexthop'],
        'match_from_peer': module.params['match_from_peer'],
        'match_med': module.params['match_med'],
        'match_as_path_regex': module.params['match_as_path_regex'],
        'match_community_regex': module.params['match_community_regex'],
        'match_extended_community_regex': module.params['match_extended_community_regex'],
    }
    obj = obj_type(**spec)
    policy.add(obj)

    # Handle address prefixes.
    for x in module.params['address_prefix']:
        if isinstance(x, dict):
            if 'name' not in x:
                module.fail_json(msg='Address prefix dict requires "name": {0}'.format(x))
            obj.add(BgpPolicyAddressPrefix(
                to_text(x['name'], encoding='utf-8', errors='surrogate_or_strict'),
                None if x.get('exact') is None else module.boolean(x['exact']),
            ))
        else:
            obj.add(BgpPolicyAddressPrefix(to_text(x, encoding='utf-8', errors='surrogate_or_strict')))

    if module.params['state'] == 'return-object':
        module.deprecate('state=return-object is deprecated', '2.12')
        import pickle
        from base64 import b64encode
        obj.parent = None
        panos_obj = b64encode(pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
        module.exit_json(msg='returning serialized object', panos_obj=panos_obj)

    changed = helper.apply_state(obj, listing, module)
    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
