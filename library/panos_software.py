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
module: panos_software
short_description: Install specific release of PAN-OS.
description:
    - Install specific release of PAN-OS.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported.
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
    version:
        description:
            - Desired PAN-OS release.
        required: true
    restart:
        description:
            - Restart device after installing desired version.  Use in conjunction with
              panos_check to determine when firewall is ready again.
        default: false
'''

EXAMPLES = '''
- name: Install PAN-OS 7.1.16 and restart
  panos_software:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    version: '7.1.16'
    restart: true
'''

RETURN = '''
version:
    description: After performing the software install, returns the version installed on the
        device.
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import PanOSVersion
    from pandevice.errors import PanDeviceError
    from pandevice import base

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        version=dict(type='str', required=True),
        restart=dict(type='bool', default=False)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    version = module.params['version']
    restart = module.params['restart']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        device.software.check()

        if PanOSVersion(version) != PanOSVersion(device.version):

            # Method only performs install if sync is set to true.
            device.software.download_install(version, sync=True)

            if restart:
                device.restart()

            changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, version=version)


if __name__ == '__main__':
    main()
