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
module: panos_registered_ip_facts
short_description: Retrieve facts about registered IPs on PAN-OS devices.
description:
    - Retrieves tag information about registered IPs on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.7"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
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
    tags:
        description:
            - List of tags to retrieve facts for.  If not specified, retrieve all tags.
'''

EXAMPLES = '''
- name: Get facts for all registered IPs
  panos_registered_ip_facts:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
  register: registered_ip_facts

- name: Get facts for specific tag
  panos_registered_ip_facts:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    tags: ['First_Tag']
  register: first_tag_registered_ip_facts
'''

RETURN = '''
results:
    description: IP addresses as keys, tags as values.
    returned: always
    type: dict
    sample: { '1.1.1.1': ['First_Tag', 'Second_Tag'] }
'''

from ansible.module_utils.basic import AnsibleModule, get_exception

try:
    from pandevice import base
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        tags=dict(type='list')
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    tags = module.params['tags']

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        registered_ips = device.userid.get_registered_ip(tags=tags)

    except PanDeviceError:
        module.fail_json(msg=get_exception())

    module.exit_json(changed=False, results=registered_ips)


if __name__ == '__main__':
    main()
