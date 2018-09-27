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
module: panos_tag_object
short_description: Create tag objects on PAN-OS devices.
description:
    - Create tag objects on PAN-OS devices.
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
            - Name of the tag.
        required: true
    color:
        description:
            - Color for the tag.
        choices: ['red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray',
                  'light green', 'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold',
                  'brown']
    comments:
        description:
            - Comments for the tag.
    device_group:
        description:
            - If I(ip_address) is a Panorama device, create tag in this device group.
    vsys:
        description:
            - If I(ip_address) is a firewall, create object in this virtual system.
        type: string
        default: 'vsys1'
    state:
        description:
            - Create or remove tag object.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create tag object 'Prod'
  panos_tag_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod'
    color: 'red'
    comments: 'Prod Environment'

- name: Remove tag object 'Prod'
  panos_tag_object:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod'
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
    from pandevice import panorama
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]


def add_object(device, obj, device_group=None):
    if isinstance(device, firewall.Firewall):
        return device.add(obj)
    elif isinstance(device, panorama.Panorama):
        if device_group:
            return get_devicegroup(device, device_group).add(obj)
        else:
            return device.add(obj)

    return None


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


def perform_commit(module, device, device_group):
    if isinstance(device, firewall.Firewall):
        result = device.commit(sync=True)

        if result:
            check_commit_result(module, result)

    elif isinstance(device, panorama.Panorama):
        result = device.commit(sync=True)

        if result:
            check_commit_result(module, result)

        if device_group:
            result = device.commit_all(sync=True, sync_all=True, devicegroup=device_group)

            if result:
                check_commit_result(module, result)


def check_commit_result(module, result):
    if result['result'] == 'FAIL':
        module.fail_json(msg='Commit failed')


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        name=dict(type='str', required=True),
        color=dict(choices=COLOR_NAMES),
        comments=dict(type='str'),
        device_group=dict(type='str'),
        vsys=dict(type='str', default='vsys1'),
        state=dict(default='present', choices=['present', 'absent']),
        commit=dict(type='bool', default=True)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    name = module.params['name']
    color = module.params['color']
    comments = module.params['comments']
    device_group = module.params['device_group']
    vsys = module.params['vsys']
    state = module.params['state']
    commit = module.params['commit']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

        if isinstance(device, firewall.Firewall):
            device.vsys = vsys

        if device_group:
            if device_group.lower() == 'shared':
                device_group = None
            else:
                if not get_devicegroup(device, device_group):
                    module.fail_json(msg='Could not find {} device group.'.format(device_group))

        if state == 'present':
            existing_obj = find_object(device, name, objects.Tag, device_group)
            color_id = objects.Tag.color_code(color) if color else None
            new_obj = objects.Tag(name=name, color=color_id, comments=comments)

            if not existing_obj:
                add_object(device, new_obj, device_group)
                new_obj.create()
                changed = True
            elif not existing_obj.equal(new_obj):
                existing_obj.color = objects.Tag.color_code(color)
                existing_obj.comments = comments
                existing_obj.apply()
                changed = True

        elif state == 'absent':
            existing_obj = find_object(device, name, objects.Tag, device_group)

            if existing_obj:
                existing_obj.delete()
                changed = True

        if commit and changed:
            perform_commit(module, device, device_group)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
