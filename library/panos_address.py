#!/usr/bin/env python

# Copyright (c) 2014, Palo Alto Networks <techbizdev@paloaltonetworks.com>
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
module: panos_address
short_description: create an address object
description:
    - Create an address object
author: 
    - Network to Code
    - Ken Celenza (itdependsnetworks)
version_added: "0.0"
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
    address:
        description:
            - IP address with or without mask, range, or fqdn
        required: true
        default: None
    address_name:
        description:
            - name of the address
        required: true
        default: None
    type:
        description:
            - ip-netmask, fqdn, ip-range
        required: false
        default: ip-nemask
    description:
        description:
            - description of address object
        required: false
        default: None
    tag:
        description:
            - tag of address object 
        required: false
        default: None
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# Creates service for port 22
  - name: create IP-Netmask Object
    panos_address:
      ip_address: "192.168.1.1"
      password: 'admin'
      address_name: 'google_dns'
      address: '8.8.8.8/32'
      description: 'Google DNS'
      tag: 'Outbound'
      commit: False

  - name: create IP-Range Object
    panos_address:
      ip_address: "192.168.1.1"
      password: 'admin'
      type: 'ip-range'
      address_name: 'apple-range'
      address: '17.0.0.0-17.255.255.255'
      commit: False

  - name: create FQDN Object
    panos_address:
      ip_address: "192.168.1.1"
      password: 'admin'
      type: 'fqdn'
      address_name: 'google.com'
      address: 'www.google.com'
'''

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_ADDRESS_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
                 "/vsys/entry[@name='vsys1']" +\
                 "/address/entry[@name='%s']"


def address_exists(xapi, address_name):
    xapi.get(_ADDRESS_XPATH % address_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_address(xapi, module, address, address_name, description, type, tag):
    if address_exists(xapi, address_name):
        return False

    exml = []
    exml.append('<%s>' % type)
    exml.append('%s' % address)
    exml.append('</%s>' % type)

    if description:
        exml.append('<description>')
        exml.append('%s' % description)
        exml.append('</description>')

    if tag:
        exml.append('<tag>')
        exml.append('<member>%s</member>' % tag)
        exml.append('</tag>')

    exml = ''.join(exml)

    xapi.set(xpath=_ADDRESS_XPATH % address_name, element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        address_name=dict(default=None),
        address=dict(default=None),
        description=dict(default=None),
        tag=dict(default=None),
        type=dict(default='ip-netmask', choices=['ip-netmask', 'ip-range', 'fqdn']),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    ip_address = module.params["ip_address"]
    if not ip_address:
        module.fail_json(msg="ip_address should be specified")
    password = module.params["password"]
    if not password:
        module.fail_json(msg="password is required")
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )


    address_name = module.params['address_name']
    if not address_name:
        module.fail_json(msg='address_name is required')
    address = module.params['address']
    if not address:
        module.fail_json(msg='address is required')
    commit = module.params['commit']

    description = module.params['description']
    tag = module.params['tag']
    type = module.params['type']

    changed = False
    changed = add_address(xapi, module,
                          address,
                          address_name,
                          description,
                          type,
                          tag)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
