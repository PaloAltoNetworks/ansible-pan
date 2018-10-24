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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_api_key
short_description: retrieve api_key for username/password combination
description:
    - This module will allow retrieval of the api_key for a given username/password
author: "Joshua Colson (@freakinhippie)"
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is NOT supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device or Panorama management console being configured.
        required: true
    username:
        description:
            - Username credentials to use for authentication.
        required: false
        default: "admin"
    password:
        description:
            - Password credentials to use for authentication.
        required: true
'''

EXAMPLES = '''
- name: retrieve api_key
  panos_op:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
  register: auth

- name: show system info
  panos_op:
    ip_address: '{{ ip_address }}'
    api_key: '{{ auth.api_key }}'
    cmd: show system info

'''

RETURN = '''
api_key:
    description: output of the api_key
    returned: success
    type: string
    sample: "LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBOWl6TGM9bXcwM3JHUGVhRlNiY0dCR0srNERUQT09"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pandevice.base import PanDevice
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(required=True, no_log=True),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password')]

    # Create the device with the appropriate pandevice type
    try:
        dev = PanDevice.create_from_device(*auth)
    except PanDeviceError as e:
        module.fail_json(msg='Failed to connect: {0}'.format(e))

    api_key = ''
    try:
        api_key = dev.api_key
    except PanDeviceError:
        e = get_exception()
        module.fail_json(msg='Failed to retrieve api_key: {0}'.format(e))

    module.exit_json(changed=False, msg="Done",
                     api_key=api_key)


if __name__ == '__main__':
    main()
