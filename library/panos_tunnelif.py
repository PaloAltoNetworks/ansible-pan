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
module: panos_tunnelif
short_description: configure a tunnel interface
description:
    - Configure a tunnel interface
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
    tunnel_unit:
        description:
            - unit number of the tunnel interface
        required: true
    zone_name:
        description:
            - name of the zone for the interface
            - if the zone does not exist it is created
        required: true
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# create tunnel.2 interface on zone vpn-dc-zone
- name: configure tunnel if
  panos_tunnelif:
      ip_address: "192.168.1.1"
      password: "admin"
      username: "admin"
      tunnel_unit: 2
      zone_name: "vpn-dc-zone"
'''

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_TIF_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
             "/network/interface/tunnel/units/entry[@name='tunnel.%s']"

_ZONE_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
              "/vsys/entry/zone/entry"
_ZONE_XPATH_QUERY = _ZONE_XPATH+"[network/layer3/member/text()='%s']"
_ZONE_XPATH_IF = _ZONE_XPATH+"[@name='%s']/network/layer3/member[text()='%s']"
_VR_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
            "/network/virtual-router/entry"


def add_tunnel_if(xapi, tunnel_unit, zone_name):
    tif_xml = ['<entry name="tunnel.%s"></entry>']

    tif_xml = (''.join(tif_xml)) % (tunnel_unit)
    xapi.edit(xpath=_TIF_XPATH % tunnel_unit, element=tif_xml)

    xapi.set(xpath=_ZONE_XPATH+"[@name='%s']/network/layer3" % zone_name,
             element='<member>tunnel.%s</member>' % tunnel_unit)
    xapi.set(xpath=_VR_XPATH+"[@name='default']/interface",
             element='<member>tunnel.%s</member>' % tunnel_unit)

    return True


def if_exists(xapi, tunnel_unit):
    xpath = _TIF_XPATH % tunnel_unit
    xapi.get(xpath=xpath)
    network = xapi.element_root.find('.//entry')
    return (network is not None)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        tunnel_unit=dict(default=None),
        zone_name=dict(default=None),
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

    tunnel_unit = module.params['tunnel_unit']
    if not tunnel_unit:
        module.fail_json(msg="tunnel_unit required")
    zone_name = module.params['zone_name']
    if not zone_name:
        module.fail_json(msg="zone_name required")

    commit = module.params['commit']

    ifexists = if_exists(xapi, tunnel_unit)
    if ifexists:
        module.exit_json(changed=False, msg="tunnel unit exists, not changed")

    changed = add_tunnel_if(xapi, tunnel_unit, zone_name)
    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
