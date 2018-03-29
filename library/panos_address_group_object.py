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
module: panos_address_group_object
short_description: Create address group objects on PAN-OS devices.
description:
    - Create address group objects on PAN-OS devices.
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
            - Name of address group to create.
        required: true
    type:
        description:
            - Whether the group is static or dynamic.
        choices: ['static', 'dynamic']
        default: 'static'
    static_value:
        description:
            - List of address objects to be included in the group.  Required if type is 'static'.
        type: list
    dynamic_value:
        description:
            - Registered IP tags for a dynamic address group.  Required if type is 'dynamic'.
        type: string
    description:
        description:
            - Descriptive name for this address group.
    tag:
        description:
            - List of tags to add to this address group.
    state:
        description:
            - Create or remove address group object.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create object group 'Prod'
  panos_address_group_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod'
    static_value: ['Test-One', 'Test-Three']
    tag: ['Prod']

- name: Create object group 'SI'
  panos_address_group_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'SI'
    type: 'dynamic'
    dynamic_value: "'SI_Instances'"
    tag: ['SI']

- name: Delete object group 'SI'
  panos_address_group_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'SI'
    state: 'absent'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import objects
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def find_object(device, obj_name, obj_type):
    obj_type.refreshall(device)

    if isinstance(device, firewall.Firewall):
        return device.find(obj_name, obj_type)
    else:
        return None


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        name=dict(type='str', required=True),
        type=dict(default='static', choices=['static', 'dynamic']),
        static_value=dict(type='list'),
        dynamic_value=dict(type='str'),
        description=dict(type='str'),
        tag=dict(type='list'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    name = module.params['name']
    type = module.params['type']
    static_value = module.params['static_value']
    dynamic_value = module.params['dynamic_value']
    description = module.params['description']
    tag = module.params['tag']
    state = module.params['state']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        objects.AddressGroup.refreshall(device)

        if state == 'present':
            existing_obj = device.find(name, objects.AddressGroup)

            if type == 'static':
                if not static_value:
                    module.fail_json(msg='Must specify \'static_value\' if \'type\' is \'static\' '
                                         'and \'state\' is \'present.')

                new_obj = objects.AddressGroup(name, static_value=static_value,
                                               description=description, tag=tag)

            elif type == 'dynamic':
                if not dynamic_value:
                    module.fail_json(msg='Must specify \'dynamic_value\' if \'type\' is '
                                         '\'dynamic\' and \'state\' is \'present\'.')

                new_obj = objects.AddressGroup(name, dynamic_value=dynamic_value,
                                               description=description, tag=tag)

            if not existing_obj:
                device.add(new_obj)
                new_obj.create()
                changed = True
            elif not existing_obj.equal(new_obj):
                if type == 'static':
                    existing_obj.static_value = static_value
                elif type == 'dynamic':
                    existing_obj.dynamic_value = dynamic_value

                existing_obj.description = description
                existing_obj.tag = tag
                existing_obj.apply()
                changed = True

        elif state == 'absent':
            existing_obj = device.find(name, objects.AddressGroup)

            if existing_obj:
                existing_obj.delete()
                changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
