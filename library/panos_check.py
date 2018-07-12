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
module: panos_check
short_description: check if PAN-OS device is ready for configuration
description:
    - Check if PAN-OS device is ready for being configured (no pending jobs).
    - The check could be done once or multiple times until the device is ready.
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
    timeout:
        description:
            - timeout of API calls
        required: false
        default: "0"
    interval:
        description:
            - time waited between checks
        required: false
        default: "0"
'''

EXAMPLES = '''
# single check on 192.168.1.1 with credentials admin/admin
- name: check if ready
  panos_check:
    ip_address: "192.168.1.1"
    password: "admin"

# check for 10 times, every 30 seconds, if device 192.168.1.1
# is ready, using credentials admin/admin
- name: wait for reboot
  panos_check:
    ip_address: "192.168.1.1"
    password: "admin"
  register: result
  until: not result|failed
  retries: 10
  delay: 30
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


from ansible.module_utils.basic import AnsibleModule
import time

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def check_jobs(jobs, module):
    job_check = False
    for j in jobs:
        status = j.find('.//status')
        if status is None:
            return False
        if status.text != 'FIN':
            return False
        job_check = True
    return job_check


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        timeout=dict(default=0, type='int'),
        interval=dict(default=0, type='int')
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    timeout = module.params['timeout']
    interval = module.params['interval']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password,
        timeout=60
    )

    checkpnt = time.time() + timeout
    while True:
        try:
            xapi.op(cmd="show jobs all", cmd_xml=True)
        except Exception:
            pass
        else:
            jobs = xapi.element_root.findall('.//job')
            if check_jobs(jobs, module):
                module.exit_json(changed=True, msg="okey dokey")

        if time.time() > checkpnt:
            break

        time.sleep(interval)

    module.fail_json(msg="Timeout")


if __name__ == '__main__':
    main()
