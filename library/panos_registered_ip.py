#!/usr/bin/env python

#  Copyright 2016 Palo Alto Networks, Inc
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
module: panos_register_ip
short_description: Create tags for DAG's on PAN-OS devices.
description:
    - Create the ip address to tag associations. Tags will in turn be used to create DAG's
author: "Michael Richardson (@mrichardson03)"
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
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
    registered_ip:
        description:
            - IP address to register.
        required: true
    tag_names:
        description:
            - List of tags that the IP address will be registered to.
        required: true
    state:
        description:
            - Create or remove registered IP address.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Add 'First_Tag' tag to 1.1.1.1
  panos_registered_ip:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    registered_ip: '1.1.1.1'
    tag_names: ['First_Tag']
    state: 'present'

- name: Add 'First_Tag' tag to 1.1.1.2
  panos_registered_ip:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    registered_ip: '1.1.1.2'
    tag_names: ['First_Tag']
    state: 'present'

- name: Add 'Second_Tag' tag to 1.1.1.1
  panos_registered_ip:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    registered_ip: '1.1.1.1'
    tag_names: ['Second_Tag']
    state: 'present'

- name: Remove 'Second_Tag' from 1.1.1.1
  panos_registered_ip:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    registered_ip: '1.1.1.1'
    tag_names: ['Second_Tag']
    state: 'absent'

- name: Remove 'First_Tag' from 1.1.1.2 (will unregister entirely)
  panos_registered_ip:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    registered_ip: '1.1.1.2'
    tag_names: ['First_Tag']
    state: 'absent'
'''

RETURN = '''
results:
    description: After performing action, returns tags for registered IP.  IP addresses as keys,
        tags as values.
    returned: always
    type: dict
    sample: { '1.1.1.1': ['First_Tag', 'Second_Tag'] }
'''

from ansible.module_utils.basic import AnsibleModule, get_exception

try:
    from pandevice import base
    from pan.xapi import PanXapiError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        registered_ip=dict(type='str', required=True),
        tag_names=dict(type='list', required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    registered_ip = module.params['registered_ip']
    tag_names = module.params['tag_names']
    state = module.params['state']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        registered_ips = device.userid.get_registered_ip(tags=tag_names)

        if state == 'present':
            if registered_ip not in registered_ips:
                device.userid.register(registered_ip, tags=tag_names)
                changed = True

        elif state == 'absent':
            if registered_ip in registered_ips:
                device.userid.unregister(registered_ip, tags=tag_names)
                changed = True

        results = device.userid.get_registered_ip(tags=tag_names)

    except PanXapiError:
        module.fail_json(msg=get_exception())

    module.exit_json(changed=changed, results=results)


if __name__ == '__main__':
    main()
