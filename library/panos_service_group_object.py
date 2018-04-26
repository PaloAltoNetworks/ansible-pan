#!/usr/bin/env python

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
module: panos_service_group_object
short_description: Create service group objects on PAN-OS devices.
description:
    - Create service group objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is not supported.
options:
    ip_address:
        description:
            - IP address or hostname of PAN-OS device.
        required: true
    username:
        description:
            - Username for authentication for PAN-OS device.  Optional if I(api_key) is used.
        default: 'admin'
    password:
        description:
            - Password for authentication for PAN-OS device.  Optional if I(api_key) is used.
    api_key:
        description:
            - API key to be used instead of I(username) and I(password).
    name:
        description:
            - Name of service group.
        required: true
    value:
        description:
            - List of service objects to be included in the group.  Must specify if state is
              present.
        type: list
        required: true
    tag:
        description:
            - List of tags for this service group.
        type: list
    device_group:
        description:
            - If I(ip_address) is a Panorama device, create object in this device group.
    state:
        description:
            - Create or remove service group object.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create service group 'Prod-Services'
  panos_service_group_object: 
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod-Services'
    value: ['ssh-tcp-22', 'mysql-tcp-3306']

- name: Delete service group 'Prod-Services'
  panos_service_group_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod-Services'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

try:
    from pandevice import objects
    from pandevice.errors import PanDeviceError

    HAS_PANOS_LIB = True
except ImportError:
    HAS_PANOS_LIB = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos import PanOSAnsibleModule


PANOS_SERVICE_GROUP_OBJECT_ARGSPEC = {
    'name': dict(type='str', required=True),
    'value': dict(type='list'),
    'tag': dict(type='list'),
    'device_group': dict(type='str'),
    'state': dict(default='present', choices=['present', 'absent'])
}

PANOS_SERVICE_GROUP_OBJECT_REQUIRED_IF_ARGS = [
    # If 'state' is 'present', require 'value'.
    ['state', 'present', ['value']]
]


def main():

    module = PanOSAnsibleModule(
        argument_spec=PANOS_SERVICE_GROUP_OBJECT_ARGSPEC,
        required_if=PANOS_SERVICE_GROUP_OBJECT_REQUIRED_IF_ARGS
    )

    name = module.params['name']
    value = module.params['value']
    tag = module.params['tag']
    device_group = module.params['device_group']
    state = module.params['state']

    changed = False

    try:
        if device_group:
            module.device_group = device_group

        if state == 'present':
            new_obj = objects.ServiceGroup(name=name, value=value, tag=tag)
            changed = module.create_or_update_object(name, objects.ServiceGroup, new_obj)

        elif state == 'absent':
            changed = module.delete_object(name, objects.ServiceGroup)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()