#!/usr/bin/env python

#  Copyright 2017 Palo Alto Networks, Inc
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
module: panos_object_facts
short_description: Retrieve facts about objects on PAN-OS devices.
description:
    - Retrieves tag information objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is not supported.
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
            - Name of object to retrieve.
        required: true
    type:
        description:
            - Type of object to retrieve.
        choices: ['address', 'address-group', 'service', 'service-group', 'tag']
        default: 'address'
        required: true
'''

EXAMPLES = '''
- name: Retrieve address group object 'Prod'
  panos_object_facts:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod'
    type: 'address-group'
  register: result

- name: Retrieve service group object 'Prod-Services'
  panos_object_facts:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod-Services'
    type: 'service-group'
  register: result
'''

RETURN = '''
results:
    description: Dict containing object attributes.  Empty if object is not found.
    returned: always
    type: dict
'''

from ansible.module_utils.network.panos import PanOSAnsibleModule

try:
    from pandevice import objects
    from pandevice.errors import PanDeviceError

    HAS_PANOS_LIB = True
except ImportError:
    HAS_PANOS_LIB = False

try:
    import xmltodict

    HAS_XMLTODICT_LIB = True
except ImportError:
    HAS_XMLTODICT_LIB = False


COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]

PANOS_OBJECT_FACTS_ARGSPEC = {
    'name': dict(type='str', required=True),
    'type': dict(
        choices=['address', 'address-group', 'service', 'service-group', 'tag'],
        required=True
    ),
    'device_group': dict(type='str')
}


def main():
    module = PanOSAnsibleModule(argument_spec=PANOS_OBJECT_FACTS_ARGSPEC)

    type = module.params['type']
    name = module.params['name']
    device_group = module.params['device_group']

    results = {}

    if not HAS_XMLTODICT_LIB:
        module.fail_json(msg='xmltodict is required for this module.')

    try:
        obj = None
        obj_type = None

        if type == 'address':
            obj_type = objects.AddressObject
        elif type == 'address-group':
            obj_type = objects.AddressGroup
        elif type == 'service':
            obj_type = objects.ServiceObject
        elif type == 'service-group':
            obj_type = objects.ServiceGroup
        elif type == 'tag':
            obj_type = objects.Tag

        if device_group:
            module.device_group = device_group

        obj = module.find_object(name, obj_type)

        if obj:
            results = xmltodict.parse(obj.element_str())

            # If the object type was a tag, convert the color id back into the name.
            if type == 'tag':
                color_index = int(results['entry']['color'][5:]) - 1
                results['entry']['color'] = COLOR_NAMES[color_index]

        module.exit_json(changed=False, results=results)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
