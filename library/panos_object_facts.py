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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
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
            - Name of object to retrieve.
        required: true
    object_type:
        description:
            - Type of object to retrieve.
        choices: ['address', 'address-group', 'service', 'service-group', 'tag']
        default: 'address'
        required: true
'''

EXAMPLES = '''
- name: Retrieve address group object 'Prod'
  panos_object_facts:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    name: 'Prod'
    object_type: 'address-group'
  register: result

- name: Retrieve service group object 'Prod-Services'
  panos_object_facts:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    name: 'Prod-Services'
    object_type: 'service-group'
  register: result
'''

RETURN = '''
results:
    description: Dict containing object attributes.  Empty if object is not found.
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import objects
    from pandevice import panorama
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]


def find_object(device, obj_name, obj_type, device_group=None):
    obj_type.refreshall(device)

    if isinstance(device, firewall.Firewall):
        return device.find(obj_name, obj_type)
    elif isinstance(device, panorama.Panorama):
        if device_group:
            dg = get_devicegroup(device, device_group)
            device.add(dg)
            obj_type.refreshall(dg)
            return dg.find(obj_name, obj_type)
        else:
            return device.find(obj_name, obj_type)

    return None


def get_devicegroup(device, device_group):

    if isinstance(device, panorama.Panorama):
        dgs = device.refresh_devices()

        for dg in dgs:
            if isinstance(dg, panorama.DeviceGroup):
                if dg.name == device_group:
                    return dg

    return None


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        name=dict(type='str', required=True),
        object_type=dict(
            type='str',
            choices=['address', 'address-group', 'service', 'service-group', 'tag'],
            required=True
        ),
        device_group=dict(type='str')
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    object_type = module.params['object_type']
    name = module.params['name']
    device_group = module.params['device_group']

    results = {}

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

        if device_group:
            if device_group.lower() == 'shared':
                device_group = None
            else:
                if not get_devicegroup(device, device_group):
                    module.fail_json(msg='Could not find {} device group.'.format(device_group))

        obj = None
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

        obj = find_object(device, name, obj_type, device_group)

        if obj:
            results = obj.about()

            # If the object type was a tag, convert the color id back into the name.
            if object_type == 'tag':
                color_index = int(results['entry']['color'][5:]) - 1
                results['entry']['color'] = COLOR_NAMES[color_index]

        module.exit_json(changed=False, results=results)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
