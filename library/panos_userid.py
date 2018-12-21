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

DOCUMENTATION = '''
---
module: panos_userid
short_description: Allow for registration and de-registration of userid
description:
    - Userid allows for user to IP mapping that can be used in the policy rules.
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is not supported.
    - This operation is runtime and does not require explicit commit of the firewall configuration.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    operation:
        description:
            - The action to be taken.  Supported values are I(login)/I(logout).
        default: 'register'
    userid:
        description:
            - User UPN
        required: true
    register_ip:
        description:
            - ip of the user's machine that needs to be registered with userid.
        required: true
'''

EXAMPLES = '''
  - name: register user ivanb to 10.0.1.101
    panos_userid:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      operation: 'login'
      userid: 'ACMECORP\\ivanb'
      register_ip: '10.0.1.101'
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


from ansible.module_utils.basic import get_exception, AnsibleModule

try:
    from pan.xapi import PanXapiError
    from pandevice import base
    from pandevice import panorama

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(required=True, no_log=True),
        api_key=dict(no_log=True),
        operation=dict(default='login', choices=['login', 'logout']),
        userid=dict(required=True),
        register_ip=dict(required=True)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    operation = module.params['operation']
    userid = module.params['userid']
    register_ip = module.params['register_ip']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    if isinstance(device, panorama.Panorama):
        module.fail_json(msg='Connected to a Panorama, but user-id API is not possible on Panorama.  Exiting.')

    # Which action shall we take on the object?
    try:
        if operation == "login":
            device.userid.login(userid, register_ip)
            module.exit_json(changed=True, msg='User \'%s\' successfully registered' % userid)
        elif operation == "logout":
            try:
                device.userid.logout(userid, register_ip)
                module.exit_json(changed=True, msg='User \'%s\' successfully unregistered' % userid)
            except PanXapiError:
                exc = get_exception()
                if exc.message in 'No multiusersystem configured name':
                    module.fail_json(msg=exc.message)
                else:
                    module.exit_json(changed=True, msg='User \'%s\' successfully unregistered' % userid)
    except PanXapiError:
        exc = get_exception()
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
