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
module: panos_dhcpif
short_description: configure a DP network interface for DHCP
description:
    - Configure a DP network interface for DHCP
author: 
    - Palo Alto Networks 
    - Luigi Mori (jtschichold)
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
    if_name:
        description:
            - name of the interface to configure
        required: true
    zone_name:
        description:
            - name of the zone for the interface
            - if the zone does not exist it is created
        required: true
    create_default_route:
        description:
            - whether add default route with router learned via DHCP
        required: false
        default: "false"
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# enable DHCP client on ethernet1/1 in zone public
- name: configure ethernet1/1
  panos_dhcpif:
    password: "admin"
    ip_address: "192.168.1.1"
    if_name: "ethernet1/1"
    zone_name: "public"
    create_default_route: "yes"
'''

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_IF_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
            "/network/interface/ethernet/entry[@name='%s']"

_ZONE_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
              "/vsys/entry/zone/entry"
_ZONE_XPATH_QUERY = _ZONE_XPATH+"[network/layer3/member/text()='%s']"
_ZONE_XPATH_IF = _ZONE_XPATH+"[@name='%s']/network/layer3/member[text()='%s']"
_VR_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
            "/network/virtual-router/entry"


def add_dhcp_if(xapi, if_name, zone_name, create_default_route):
    if_xml = [
        '<entry name="%s">',
        '<layer3>',
        '<dhcp-client>',
        '<create-default-route>%s</create-default-route>',
        '</dhcp-client>'
        '</layer3>'
        '</entry>'
    ]
    cdr = 'yes'
    if not create_default_route:
        cdr = 'no'
    if_xml = (''.join(if_xml)) % (if_name, cdr)
    xapi.edit(xpath=_IF_XPATH % if_name, element=if_xml)

    xapi.set(xpath=_ZONE_XPATH+"[@name='%s']/network/layer3" % zone_name,
             element='<member>%s</member>' % if_name)
    xapi.set(xpath=_VR_XPATH+"[@name='default']/interface",
             element='<member>%s</member>' % if_name)

    return True


def if_exists(xapi, if_name):
    xpath = _IF_XPATH % if_name
    xapi.get(xpath=xpath)
    network = xapi.element_root.find('.//layer3')
    return (network is not None)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        if_name=dict(default=None),
        zone_name=dict(default=None),
        create_default_route=dict(type='bool', default=False),
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

    if_name = module.params['if_name']
    if not if_name:
        module.fail_json(msg="if_name required")
    zone_name = module.params['zone_name']
    if not zone_name:
        module.fail_json(msg="zone_name required")
    create_default_route = module.params['create_default_route']
    commit = module.params['commit']

    ifexists = if_exists(xapi, if_name)
    if ifexists:
        module.exit_json(changed=False, msg="if exists, not changed")

    changed = add_dhcp_if(xapi, if_name, zone_name, create_default_route)
    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
