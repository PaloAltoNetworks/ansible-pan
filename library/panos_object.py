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
module: panos_object
short_description: Create objects on PAN-OS devices.
description:
    - Create objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.6"
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
    object_type:
        description:
            - Type of object to create.
        choices: ['address', 'address-group', 'service', 'service-group', 'tag']
        required: true
    name:
        description:
            - Name of object to create.
        required: true
    address_value:
        description:
            - If I(object_type) is I(address), this is the IP address, IP range, or FQDN for the
              object.  Required if state is I(present).
    address_type:
        description:
            - If I(object_type) is I(address), this is the type of address object.
        choices: ['ip-netmask', 'ip-range', 'fqdn']
        default: 'ip-netmask'
    address_group_type:
        description:
            - If I(object_type) is I(address_group), this is whether the group is static or
              dynamic.
        choices: ['static', 'dynamic']
        default: 'static'
    static_value:
        description:
            - List of address objects to be included in the group.  Required if 
              I(address_group_type) is 'static'.
        type: list
    dynamic_value:
        description:
            - Registered IP tags for a dynamic address group.  Required if I(address_group_type)
              is 'dynamic'.
        type: string
    protocol:
        description:
            - If I(object_type) is I(service), this is the protocol of the service.
        choices: ['tcp', 'udp']
        default: 'tcp'
    source_port:
        description
            - If I(object_type) is I(service), this is the source port of the service object.
    destination_port:
        description:
            - If I(object_type) is I(service), this is the destination port of the service 
              object.  Required if state is I(present).
    service_group_value:
        description:
            - If I(object_type) is I(service-group), this is the list of service objects to be 
              included in the group.  Required if I(state) is 'present'.
        type: list
        required: true
    color:
        description:
            - If I(object_type) is I(tag), this is the color for the tag.
        choices: ['red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray',
                  'light green', 'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold',
                  'brown']
    comments:
        description:
            - If I(object_type) is I(tag), this is comments for the tag.
    description:
        description:
            - Descriptive name for this object.
    tag:
        description:
            - List of tags to add to this object.
    device_group:
        description:
            - If I(ip_address) is a Panorama device, create object in this device group.
    state:
        description:
            - Create or remove object.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create object 'Test-One'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address'
    name: 'Test-One'
    address_value: '1.1.1.1'
    description: 'Description One'
    tag: ['Prod']

- name: Create object 'Test-Two'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address'
    name: 'Test-Two'
    address_type: 'ip-range'
    address_value: '1.1.1.1-2.2.2.2'
    description: 'Description Two'
    tag: ['SI']

- name: Create object 'Test-Three'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address'
    name: 'Test-Three'
    address_type: 'fqdn'
    address_value: 'foo.bar.baz'
    description: 'Description Three'

- name: Delete object 'Test-Two'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address'
    name: 'Test-Two'
    state: 'absent'

- name: Create object group 'Prod'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address-group'
    name: 'Prod'
    static_value: ['Test-One', 'Test-Three']
    tag: ['Prod']

- name: Create object group 'SI'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address-group'
    name: 'SI'
    type: 'dynamic'
    dynamic_value: "'SI_Instances'"
    tag: ['SI']

- name: Delete object group 'SI'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'address-group'
    name: 'SI'
    state: 'absent'

- name: Create service object 'ssh-tcp-22'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'service'
    name: 'ssh-tcp-22'
    destination_port: '22'
    description: 'SSH on tcp/22'
    tag: ['Prod']

- name: Create service object 'mysql-tcp-3306'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'service'
    name: 'mysql-tcp-3306'
    destination_port: '3306'
    description: 'MySQL on tcp/3306'

- name: Delete service object 'mysql-tcp-3306'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'service'
    name: 'mysql-tcp-3306'
    state: 'absent'

- name: Create service group 'Prod-Services'
  panos_object: 
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'service-group'
    name: 'Prod-Services'
    value: ['ssh-tcp-22', 'mysql-tcp-3306']

- name: Delete service group 'Prod-Services'
  panos_service_group_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'service-group'
    name: 'Prod-Services'
    state: 'absent'

- name: Create tag object 'Prod'
  panos_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'tag'
    name: 'Prod'
    color: 'red'
    comments: 'Prod Environment'

- name: Remove tag object 'Prod'
  panos_tag_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    object_type: 'tag'
    name: 'Prod'
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

try:
    from module_utils.network.panos import PanOSAnsibleModule
except ImportError:
    from ansible.module_utils.network.panos import PanOSAnsibleModule

COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]

PANOS_ADDRESS_OBJECT_ARGSPEC = {
    'name': dict(type='str', required=True),
    'object_type': dict(
        choices=['address', 'address-group', 'service', 'service-group', 'tag'],
        required=True
    ),

    'address_value': dict(type='str'),
    'address_type': dict(default='ip-netmask', choices=['ip-netmask', 'ip-range', 'fqdn']),

    'address_group_type': dict(default='static', choices=['static', 'dynamic']),
    'static_value': dict(type='list'),
    'dynamic_value': dict(type='str'),

    'protocol': dict(default='tcp', choices=['tcp', 'udp']),
    'source_port': dict(type='str'),
    'destination_port': dict(type='str'),

    'service_group_value': dict(type='list'),

    'color': dict(choices=COLOR_NAMES),
    'comments': dict(type='str'),

    'description': dict(type='str'),
    'tag': dict(type='list'),
    'device_group': dict(type='str'),
    'state': dict(default='present', choices=['present', 'absent'])
}

PANOS_OBJECT_REQUIRED_IF_COMPLEX_ARGSPEC = [
    # If 'state' is 'present' and 'object_type' is 'address', require 'address_value'.
    [{'state': 'present', 'object_type': 'address'}, ['address_value']],

    # If 'state' is 'present', 'object_type' is 'address-group', and 'address_group_type' is
    # 'static', require 'static_value'.
    [
        {'state': 'present', 'object_type': 'address-group', 'address_group_type': 'static'},
        ['static_value']
    ],

    # If 'state' is 'present', 'object_type' is 'address-group', and 'address_group_type' is
    # 'dynamic', require 'dynamic_value'.
    [
        {'state': 'present', 'object_type': 'address-group', 'address_group_type': 'dynamic'},
        ['dynamic_value']
    ],

    # If 'state' is 'present' and 'object_type' is 'service', require 'destination_port'.
    [{'state': 'present', 'object_type': 'service'}, ['destination_port']],

    [{'state': 'present', 'object_type': 'service-group'}, ['service_group_value']]
]


def main():
    module = PanOSAnsibleModule(
        argument_spec=PANOS_ADDRESS_OBJECT_ARGSPEC
    )

    name = module.params['name']
    object_type = module.params['object_type']

    address_value = module.params['address_value']
    address_type = module.params['address_type']

    address_group_type = module.params['address_group_type']
    static_value = module.params['static_value']
    dynamic_value = module.params['dynamic_value']

    protocol = module.params['protocol']
    source_port = module.params['source_port']
    destination_port = module.params['destination_port']

    service_group_value = module.params['service_group_value']

    color = module.params['color']
    comments = module.params['comments']

    description = module.params['description']
    tag = module.params['tag']
    device_group = module.params['device_group']
    state = module.params['state']

    changed = False

    for (param_dict, requirements) in PANOS_OBJECT_REQUIRED_IF_COMPLEX_ARGSPEC:
        and_op = False
        criteria = []
        for key in sorted(param_dict.keys()):
            if module.params[key] and module.params[key] == param_dict[key]:
                and_op = True
            else:
                and_op = False
                break
            criteria.append('\'%s\' is \'%s\'' % (key, param_dict[key]))
        if and_op == True:
            missing = []
            for requirement in requirements:
                if not module.params[requirement] or module.params[requirement] == '':
                    missing.append(requirement)
            if len(missing) > 0:
                module.fail_json(msg='%s but the following are missing: %s' % 
                    ((', '.join(criteria)), (', '.join(missing))))

    try:
        if device_group:
            module.device_group = device_group

        obj_type = None

        if object_type == 'address':
            obj_type = objects.AddressObject
        elif object_type == 'address-group':
            obj_type = objects.AddressGroup
        elif object_type == 'service':
            obj_type = objects.ServiceObject
        elif object_type == 'service-group':
            obj_type = objects.ServiceGroup
        elif object_type == 'tag':
            obj_type = objects.Tag

        if state == 'present':
            new_obj = None

            if object_type == 'address':
                new_obj = objects.AddressObject(
                    name, address_value, type=address_type, description=description, tag=tag
                )
            elif object_type == 'address-group' and address_group_type == 'static':
                new_obj = objects.AddressGroup(
                    name, static_value=static_value, description=description, tag=tag
                )
            elif object_type == 'address-group' and address_group_type == 'dynamic':
                new_obj = objects.AddressGroup(
                    name, dynamic_value=dynamic_value, description=description, tag=tag
                )
            elif object_type == 'service':
                new_obj = objects.ServiceObject(
                    name=name, protocol=protocol, source_port=source_port,
                    destination_port=destination_port, description=description, tag=tag
                )
            elif object_type == 'service-group':
                new_obj = objects.ServiceGroup(name=name, value=service_group_value, tag=tag)
            elif object_type == 'tag':
                color_id = objects.Tag.color_code(color) if color else None
                new_obj = objects.Tag(name=name, color=color_id, comments=comments)

            changed = module.create_or_update_object(name, obj_type, new_obj)

        elif state == 'absent':
            changed = module.delete_object(name, obj_type)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()

