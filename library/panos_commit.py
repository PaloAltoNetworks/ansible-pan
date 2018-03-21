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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_commit
short_description: commit firewall's candidate configuration
description:
    - PanOS module that will commit firewall's candidate configuration on
    - the device. The new configuration will become active immediately.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Robert Hagen (@rnh556)"
version_added: "2.3"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
options:
    ip_address:
        description:
            - The IP address (or hostname) of the PAN-OS device or Panorama management console.
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
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
        required: false
    devicegroup:
        description:
            - The Panorama device group to be committed.
        required: false
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
    devicegroup: 'Cloud-Edge'
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "Commit successful"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    import pandevice
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def devicegroup_exists(device, devicegroup):
    dev_grps = device.refresh_devices()
    for grp in dev_grps:
        if isinstance(grp, pandevice.panorama.DeviceGroup):
            if grp.name == devicegroup:
                return True
    return False


def do_commit(device, devicegroup):
    try:
        if isinstance(device, panorama.Panorama):
            result = device.commit_all(sync=True, sync_all=True, exception=True, devicegroup=devicegroup)
        else:
            result = device.commit(sync=True, exception=True)
        return result
    except:
        return False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        devicegroup=dict()
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    devicegroup = module.params['devicegroup']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    if isinstance(device, panorama.Panorama):
        if devicegroup_exists(device, devicegroup):
            pass
        else:
            module.fail_json(
                failed=1,
                msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup
            )

    # Commit the configs
    if do_commit(device, devicegroup):
        module.exit_json(changed=True, msg='Commit successful')
    else:
        module.fail_json(changed=False, msg='Commit failed')


if __name__ == '__main__':
    main()
