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
module: panos_bgp_policy_filter
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
            - Add or remove BGP Policy Filter.
                - present
                - absent
                - return-object
            default: present
    commit:
        description:
            - Commit configuration if changed.
            default: True
    filter_type:
        description:
            - The type of filter.
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
    address_prefix:
        description:
            - List of Address Prefix objects.
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
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
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
    exclude_list += ['vr_name', 'policy_type', 'policy_name', 'filter_type', 'address_prefix']

    # generate the kwargs for network.BgpPolicyRule
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    # fetch the standard settings
    state = module.params['state']
    commit = module.params['commit']

    prefixes = module.params['address_prefix']
    # make sure the prefixes are a list
    if prefixes is None:
        prefixes = []
    elif not isinstance(prefixes, list):
        prefixes = [prefixes]

    name = module.params['name']
    vr_name = module.params['vr_name']
    policy_type = module.params['policy_type']
    policy_name = module.params['policy_name']
    filter_type = module.params['filter_type']

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
        bgp = vr.find('', network.Bgp)

        # find the parent object
        if policy_type == 'conditional-advertisement':
            # make sure that we've got at least one prefix
            if len(prefixes) < 1:
                raise ValueError('Conditional Advertisement policies require at least one prefix')
            cur_policy = vr.find(policy_name, network.BgpPolicyConditionalAdvertisement, recursive=True)
        elif policy_type == 'aggregate':
            cur_policy = vr.find(policy_name, network.BgpPolicyAggregationAddress, recursive=True)
        else:
            raise ValueError('Policy type {0} is not supported'.format(policy_type))

        # find the current state object
        if cur_policy is None and state != 'return-object':
            raise ValueError("Policy {0} '{1}' not found".format(policy_type, policy_name))

        # create the new state object
        if filter_type == 'non-exist':
            new_obj = network.BgpPolicyNonExistFilter(**obj_spec)
            cur_obj = cur_policy.find(name, network.BgpPolicyNonExistFilter) if cur_policy is not None else None
        elif filter_type == 'advertise':
            new_obj = network.BgpPolicyAdvertiseFilter(**obj_spec)
            cur_obj = cur_policy.find(name, network.BgpPolicyAdvertiseFilter) if cur_policy is not None else None
        elif filter_type == 'suppress':
            new_obj = network.BgpPolicySuppressFilter(**obj_spec)
            cur_obj = cur_policy.find(name, network.BgpPolicySuppressFilter) if cur_policy is not None else None

        # add the address prefixes
        for prefix in prefixes:
            if prefix.get('name'):
                pfx = network.BgpPolicyAddressPrefix(**prefix)
                new_obj.add(pfx)

        # compare differences between the current state vs desired state
        if state == 'present':
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=True):
                # purge_stale_prefixes(cur_obj, prefixes)
                cur_policy.add(new_obj)
                new_obj.apply()
                changed = True
        elif state == 'absent':
            if cur_obj is not None:
                cur_obj.delete()
                changed = True
        elif state == 'return-object':
            import pickle
            from base64 import b64encode
            panos_obj = b64encode(pickle.dumps(new_obj, protocol=pickle.HIGHEST_PROTOCOL))
            module.exit_json(msg='returning serialized object', panos_obj=panos_obj)
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='BGP policy filter update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
