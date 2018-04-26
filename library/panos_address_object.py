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
module: panos_address_object
short_description: Create address objects on PAN-OS devices.
description:
    - Create address objects on PAN-OS devices.
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
            - Name of object to create.
        required: true
    value:
        description:
            - IP address, IP range, or FQDN for the object.  Must specify if state is I(present).
        required: true
    type:
        description:
            - Type of address object.
        choices: ['ip-netmask', 'ip-range', 'fqdn']
        default: 'ip-netmask'
    description:
        description:
            - Descriptive name for this address object.
    tag:
        description:
            - List of tags to add to this address object.
    device_group:
        description:
            - If I(ip_address) is a Panorama device, create object in this device group.
    state:
        description:
            - Create or remove address object.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create object 'Test-One'
  panos_address_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-One'
    value: '1.1.1.1'
    description: 'Description One'
    tag: ['Prod']

- name: Create object 'Test-Two'
  panos_address_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Two'
    type: 'ip-range'
    value: '1.1.1.1-2.2.2.2'
    description: 'Description Two'
    tag: ['SI']

- name: Create object 'Test-Three'
  panos_address_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Three'
    type: 'fqdn'
    value: 'foo.bar.baz'
    description: 'Description Three'

- name: Delete object 'Test-Two'
  panos_address_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Two'
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

from ansible.module_utils.network.panos import PanOSAnsibleModule


PANOS_ADDRESS_OBJECT_ARGSPEC = {
    'name': dict(type='str', required=True),
    'value': dict(type='str'),
    'type': dict(default='ip-netmask', choices=['ip-netmask', 'ip-range', 'fqdn']),
    'description': dict(type='str'),
    'tag': dict(type='list'),
    'device_group': dict(type='str'),
    'state': dict(default='present', choices=['present', 'absent'])
}

PANOS_ADDRESS_OBJECT_REQUIRED_IF_ARGS = [
    # If 'state' is 'present', require 'value'.
    ['state', 'present', ['value']]
]


def main():
    module = PanOSAnsibleModule(
        argument_spec=PANOS_ADDRESS_OBJECT_ARGSPEC,
        required_if=PANOS_ADDRESS_OBJECT_REQUIRED_IF_ARGS
    )

    name = module.params['name']
    value = module.params['value']
    type = module.params['type']
    description = module.params['description']
    tag = module.params['tag']
    device_group = module.params['device_group']
    state = module.params['state']

    changed = False

    try:
        if device_group:
            module.device_group = device_group

        if state == 'present':
            new_obj = objects.AddressObject(
                name, value, type=type, description=description, tag=tag
            )
            changed = module.create_or_update_object(name, objects.AddressObject, new_obj)

        elif state == 'absent':
            changed = module.delete_object(name, objects.AddressObject)
    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
