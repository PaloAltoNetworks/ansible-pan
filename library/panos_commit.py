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

DOCUMENTATION = '''
---
module: panos_commit
short_description: commit firewall's candidate configuration
description:
    - PanOS module that will commit firewall's candidate configuration on
    - the device. The new configuration will become active immediately.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
    password:
        description:
            - password for authentication
        required: true
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    interval:
        description:
            - interval for checking commit job
        required: false
        default: 0.5
    timeout:
        description:
            - timeout for commit job
        required: false
        default: None
    sync:
        description:
            - if commit should be synchronous
        required: false
        default: true
'''

EXAMPLES = '''
# Commit candidate config on 192.168.1.1 in sync mode
- panos_commit:
    ip_address: "192.168.1.1"
    username: "admin"
    password: "admin"
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "okey dokey"
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
    result = device.commit(sync=True)
    if isinstance(device, panorama.Panorama):
        result = device.commit_all(sync=True, sync_all=True, devicegroup=devicegroup)
    return result


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
    device = base.PanDevice.create_from_device(ip_address, username, password)

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