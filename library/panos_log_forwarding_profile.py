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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_log_forwarding_profile
short_description: Manage log forwarding profiles.
description:
    - Manages log forwarding profiles.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.vsys_shared
    - panos.device_group
options:
    name:
        description:
            - Name of the profile.
        required: true
    description:
        description:
            - Profile description
    enhanced_logging:
        description:
            - Valid for PAN-OS 8.1+
            - Enabling enhanced application logging.
        type: 'bool'
'''

EXAMPLES = '''
# Create a profile
- name: Create log forwarding profile
  panos_log_forwarding_profile
    provider: '{{ provider }}'
    name: 'my-profile'
    enhanced_logging: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.objects import LogForwardingProfile
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            name=dict(required=True),
            description=dict(),
            enhanced_logging=dict(type='bool'),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    try:
        listing = LogForwardingProfile.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = {
        'name': module.params['name'],
        'description': module.params['description'],
        'enhanced_logging': module.params['enhanced_logging'],
    }
    obj = LogForwardingProfile(**spec)
    parent.add(obj)

    changed = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
