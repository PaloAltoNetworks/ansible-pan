#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2019 Palo Alto Networks, Inc
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

DOCUMENTATION = '''
---
module: panos_zone_facts
short_description: Retrieves zone information
description:
    - NOTE: The modules in this role are deprecated in favour of the modules in the collection U(https://paloaltonetworks.github.io/pan-os-ansible)
    - Retrieves information on zones from a firewall or Panorama.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.full_template_support
    - panos.vsys
options:
    name:
        description:
            - Name of the security zone.
'''

EXAMPLES = '''
# Get information on a specific zone
- name: Get zone3 info
  panos_zone_facts:
    provider: '{{ provider }}'
    name: 'zone3'
  register: ans

# Get the config of all zones
- name: Get all zones
  panos_zone_facts:
    provider: '{{ provider }}'
  register: zones
'''

RETURN = '''
spec:
    description: The spec of the specified virtual router.
    returned: When I(name) is specified.
    type: complex
    contains:
        zone:
            description: The name.
        mode:
            description: The mode of the zone.
        interface:
            description: List of interfaces.
            type: list
        zone_profile:
            description: Zone protection profile.
        log_setting:
            description: Log forwarding setting.
        enable_userid:
            description: Enable user identification.
            type: bool
        include_acl:
            description: User identification ACL include list.
            type: list
        exclude_acl:
            description: User identification ACL exclude list.
            type: list
zones:
    description: List of zone specs.
    returned: When I(name) is not specified.
    type: list
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.network import Zone
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            name=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    renames = (
        ('name', 'zone'),
        ('enable_user_identification', 'enable_userid'),
    )

    name = module.params['name']
    if name is None:
        try:
            listing = Zone.refreshall(parent)
        except PanDeviceError as e:
            module.fail_json(msg='Failed refreshall: {0}'.format(e))

        zones = helper.to_module_dict(listing, renames)
        module.exit_json(changed=False, zones=zones)

    zone = Zone(name)
    parent.add(zone)
    try:
        zone.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = helper.to_module_dict(zone, renames)
    module.exit_json(changed=False, spec=spec)


if __name__ == '__main__':
    main()
