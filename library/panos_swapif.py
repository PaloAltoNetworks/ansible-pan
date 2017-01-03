#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage PaloAltoNetworks Firewall
# (c) 2016, techbizdev <techbizdev@paloaltonetworks.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: panos_swapif
short_description: swap mgmt interface from eth0 to eth1
description:
    - Swap password interface from eth0 to eth1. This operation requires reboot.
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - pan.xapi
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
        default: null
    password:
        description:
            - password for authentication
        required: true
        default: null
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    swap:
        description:
            - password to configure for admin on the PAN-OS device
        required: true
        default: "no"
'''

EXAMPLES = '''
- name: swap management interface
  panos_swapif:
    ip_address: "192.168.1.1"
    password: "changeme"
    swap: "yes"
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

from ansible.module_utils.basic import *  # noqa

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True),
        username=dict(default='admin'),
        swap=dict(default='no')
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    if not ip_address:
        module.fail_json(msg="ip_address should be specified")
    password = module.params["password"]
    if not password:
        module.fail_json(msg="password is required")
    username = module.params['username']
    swap = module.params['swap']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    try:
        if swap == 'yes':
            print('swapping')
            xapi.op(cmd="<set><system><setting><mgmt-interface-swap><enable><yes></yes></enable></mgmt-interface-swap></setting></system></set>")
        else:
            print('NOT swapping')
            xapi.op(cmd="<set><system><setting><mgmt-interface-swap><enable><no></no></enable></mgmt-interface-swap></setting></system></set>")
    except pan.xapi.PanXapiError, msg:
        if 'succeeded' in str(msg):
            module.exit_json(changed=True, msg=str(msg))

        raise

    module.exit_json(changed=True, msg="okey dokey")

if __name__ == '__main__':
    main()
