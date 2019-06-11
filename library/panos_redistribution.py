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
module: panos_redistribution
short_description: Configures a Redistribution Profile on a virtual router
description:
    - Configures a Redistribution Profile on a virtual router
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.full_template_support
options:
    name:
        description:
            - Name of rule.
        required: True
    priority:
        description:
            - Priority ID.
        type: int
    action:
        description:
            - Rule action.
        choices:
            - no-redist
            - redist
        default: 'no-redist'
    filter_type:
        description:
            - Any of 'static', 'connect', 'rip', 'ospf', or 'bgp'.
    filter_interface:
        description:
            - Filter interface.
    filter_destination:
        description:
            - Filter destination.
    filter_nexthop:
        description:
            - Filter nexthop.
    ospf_filter_pathtype:
        description:
            - Any of 'intra-area', 'inter-area', 'ext-1', or 'ext-2'.
    ospf_filter_area:
        description:
            - OSPF filter on area.
    ospf_filter_tag:
        description:
            - OSPF filter on tag.
    bgp_filter_community:
        description:
            - BGP filter on community.
    bgp_filter_extended_community:
        description:
            - BGP filter on extended community.
    type:
        description:
            - Name of rule.
        choices:
            - ipv4
            - ipv6
        default: 'ipv4'
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
        default: 'default'
    commit:
        description:
            - Commit configuration if changed.
        default: True
        type: bool
'''

EXAMPLES = '''
- name: Create Redistribution Profile
  panos_redistribution:
    provider: '{{ provider }}'
    name: 'my-profile'
    priority: 42
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import VirtualRouter
    from pandevice.network import RedistributionProfile
    from pandevice.network import RedistributionProfileIPv6
except ImportError:
    pass


def setup_args():
    return dict(
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
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
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

    spec = {
        'name': module.params['name'],
        'priority': module.params['priority'],
        'action': module.params['action'],
        'filter_type': module.params['filter_type'],
        'filter_interface': module.params['filter_interface'],
        'filter_destination': module.params['filter_destination'],
        'filter_nexthop': module.params['filter_nexthop'],
        'ospf_filter_pathtype': module.params['ospf_filter_pathtype'],
        'ospf_filter_area': module.params['ospf_filter_area'],
        'ospf_filter_tag': module.params['ospf_filter_tag'],
        'bgp_filter_community': module.params['bgp_filter_community'],
        'bgp_filter_extended_community': module.params['bgp_filter_extended_community'],
    }

    if module.params['type'] == 'ipv4':
        obj = RedistributionProfile(**spec)
    else:
        obj = RedistributionProfileIPv6(**spec)

    listing = vr.findall(obj.__class__)
    vr.add(obj)

    changed = helper.apply_state(obj, listing, module)
    if changed and module.params['commit']:
        helper.commit(module)

    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
