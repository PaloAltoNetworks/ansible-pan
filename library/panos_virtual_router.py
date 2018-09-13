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
module: panos_virtual_router
short_description: Create a virtual router on the device.
description:
    - Create static routes on PAN-OS devices.
author: "Ken Celenza (@itdependsnetworks)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is not supported.
    - IPv6 is not supported.
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
            - Name of the virtual router.
        required: true
    state:
        description:
            - Create or remove static route.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create the zone trust'
  panos_virtual_router:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'trust'
    state: 'present'

- name: Create the zone dmz'
  panos_virtual_router:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'dmz'
    state: 'present'

- name: Delete the zone web_app'
  panos_virtual_router:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'web_app'
    state: 'present'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import network
    from pandevice.panorama import Template
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
        devicegroup=dict(type='str', required=False),
        panorama_template=dict(),
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
    devicegroup = module.params['devicegroup']
    state = module.params['state']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

        dev_group = None
        if devicegroup and isinstance(device, panorama.Panorama):
            dev_group = get_devicegroup(device, devicegroup)
            if dev_group:
                device.add(dev_group)
            else:
                module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

        network.VirtualRouter(name)
        active_virtual_routers = network.VirtualRouter.refreshall(device)

        found = False 
        for current_vr in active_virtual_routers:
            if current_vr.name == name:
                found = True
                del_obj = current_vr
                break

        # only change when present, and does not already exist
        if state == 'present' and not found:
            changed = True
            vr = network.VirtualRouter(name=name)
            device.add(vr)
            vr.create()

        # only change when absent, and does already exist
        elif state == 'absent' and found:
            changed = True
            device.add(del_obj)
            del_obj.delete()

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
