#!/usr/bin/env python

# Copyright (c) 2015, Palo Alto Networks <techbizdev@paloaltonetworks.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

DOCUMENTATION = '''
---
module: panos_swapif
short_description: swap mgmt interface from eth0 to eth1
description:
    - Swap password interface from eth0 to eth1. This operation requires reboot.
author: Palo Alto Networks - Ivan Bojer ibojer@paloaltonetworks.com
version_added: "0.1"
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

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None),
        username=dict(default='admin'),
        swap=dict(default='no')
    )
    module = AnsibleModule(argument_spec=argument_spec)

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

from ansible.module_utils.basic import *  # noqa

main()
