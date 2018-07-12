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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

DOCUMENTATION = '''
---
module: panos_lic
short_description: apply authcode to a device/instance
description:
    - Apply an authcode to a device.
    - The authcode should have been previously registered on the Palo Alto Networks support portal.
    - The device should have Internet access.
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
    auth_code:
        description:
            - authcode to be applied
        required: true
    force:
        description:
            - whether to apply authcode even if device is already licensed
        required: false
        default: "false"
'''

EXAMPLES = '''
    - hosts: localhost
      connection: local
      tasks:
        - name: fetch license
          panos_lic:
            ip_address: "192.168.1.1"
            password: "paloalto"
            auth_code: "IBADCODE"
          register: result
    - name: Display serialnumber (if already registered)
      debug:
        var: "{{result.serialnumber}}"
'''

RETURN = '''
serialnumber:
    description: serialnumber of the device in case that it has been already registered
    returned: success
    type: string
    sample: 007200004214
'''

from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_serial(xapi, module):
    xapi.op(cmd="show system info", cmd_xml=True)
    r = xapi.element_root
    serial = r.find('.//serial')
    if serial is None:
        module.fail_json(msg="No <serial> tag in show system info")

    serial = serial.text

    return serial


def apply_authcode(xapi, module, auth_code):
    try:
        xapi.op(cmd='request license fetch auth-code "%s"' % auth_code,
                cmd_xml=True)
    except pan.xapi.PanXapiError:
        if hasattr(xapi, 'xml_document'):
            if 'Successfully' in xapi.xml_document:
                return

        if 'Invalid Auth Code' in xapi.xml_document:
            module.fail_json(msg="Invalid Auth Code")

        raise

    return


def fetch_authcode(xapi, module):
    try:
        xapi.op(cmd='request license fetch', cmd_xml=True)
    except pan.xapi.PanXapiError:
        if hasattr(xapi, 'xml_document'):
            if 'Successfully' in xapi.xml_document:
                return

        if 'Invalid Auth Code' in xapi.xml_document:
            module.fail_json(msg="Invalid Auth Code")

        raise

    return


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        auth_code=dict(),
        username=dict(default='admin'),
        force=dict(type='bool', default=False)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    auth_code = module.params["auth_code"]
    force = module.params['force']
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    if not force:
        serialnumber = get_serial(xapi, module)
        if serialnumber != 'unknown':
            return module.exit_json(changed=False, serialnumber=serialnumber)
    if auth_code:
        apply_authcode(xapi, module, auth_code)
    else:
        fetch_authcode(xapi, module)

    module.exit_json(changed=True, msg="okey dokey")


if __name__ == '__main__':
    main()
