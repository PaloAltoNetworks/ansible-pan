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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_commit
short_description: Commit a PAN-OS device's candidate configuration.
description:
    - Module that will commit the candidate configuration of a PAN-OS device.
    - The new configuration will become active immediately.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.3"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
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
    device_group:
        description:
            - If I(ip_address) is a Panorama device, perform a commit-all to the devices in this
              device group in addition to commiting to Panorama.
        type: str
        aliases: ['devicegroup']
'''

EXAMPLES = '''
- name: commit candidate config on firewall
  panos_commit:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'

- name: commit candidate config on Panorama using api_key
  panos_commit:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    device_group: 'Cloud-Edge'
'''

RETURN = '''
# Default return values
'''
try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


from ansible.module_utils.basic import AnsibleModule


def get_devicegroup(device, device_group):
    if isinstance(device, panorama.Panorama):
        dgs = device.refresh_devices()

        for dg in dgs:
            if isinstance(dg, panorama.DeviceGroup):
                if dg.name == device_group:
                    return dg

    return None


def check_commit_result(module, result):
    if result['result'] == 'FAIL':
        if 'xml' in result:
            result.pop('xml')

        module.fail_json(msg='Commit failed', result=result)


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        device_group=dict(type='str', aliases=['devicegroup'])
    )

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=False,
        required_one_of=[['api_key', 'password']]
    )

    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    device_group = module.params['device_group']

    changed = False
    results = []

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

        if device_group:
            if device_group.lower() == 'shared':
                device_group = None
            else:
                if not get_devicegroup(device, device_group):
                    module.fail_json(msg='Could not find {} device group.'.format(device_group))

        if isinstance(device, firewall.Firewall):
            result = device.commit(sync=True)

            if result:
                check_commit_result(module, result)

                changed = True
                results.append(result)

        elif isinstance(device, panorama.Panorama):
            # Panorama commit is two potential steps, one to Panorama itself, and one to the
            # device group.
            result = device.commit(sync=True)

            if result:
                check_commit_result(module, result)

                changed = True
                results.append(result)

            if device_group:
                result = device.commit_all(
                    sync=True, sync_all=True, devicegroup=device_group
                )

                if result:
                    check_commit_result(module, result)

                    changed = True
                    results.append(result)

        # Clean XML out of results becasue Ansible doesn't like it.
        for result in results:
            if 'xml' in result:
                result.pop('xml')

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, result=results)


if __name__ == '__main__':
    main()
