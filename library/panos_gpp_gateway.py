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
module: panos_gpp_gateway
short_description: configure a GlobalProtect Portal gateway list
description:
    - Configure a GlobalProtect Portal gateway list
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
    portal_name:
        description:
            - name of the GlobalProtect portal
        required: true
    config_name:
        description:
            - name of the client config
        required: true
    gateway_address:
        description:
            - name address of the gateway
        required: true
    type:
        description:
            - internal or external gateway
        required: false
        choices: [ "internal", "external" ]
        default: external
    state:
        description:
            - state of the gateway
        required: false
        default: "present"
        choices: [ "absent", "present" ]
        default: present
    manual:
        description:
            - manual gateway
        required: false
        default: true
    description:
        description:
            - description of the gateway
        required: false
        default: None
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# Adds gateway to portal config on 192.168.1.1
  - name: add gateway to portal
    panos_gpp_gateway:
      username: "admin"
      ip_address: "192.168.1.1"
      password: "admin"
      portal_name: "GP-Portal"
      config_name: "GPClientConfig"
      type: "external"
      gateway_address: "{{elastic_ip0}}"
      description: "{{device_name}}"
      manual: true
      state: "present"

# Removes gateway from portal config
  - name: delete gateway from portal
    panos_gpp_gateway:
      username: "admin"
      ip_address: "192.168.1.1"
      password: "admin"
      portal_name: "GP-Portal"
      config_name: "GPClientConfig"
      type: "external"
      gateway_address: "{{elastic_ip0}}"
      state: "absent"
'''

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_GW_PATH = "/config/devices/entry[@name='localhost.localdomain']" +\
           "/vsys/entry[@name='vsys1']" +\
           "/global-protect/global-protect-portal/entry[@name='%s']" +\
           "/client-config/configs/entry[@name='%s']" +\
           "/gateways/%s/list/entry[@name='%s']"


def get_gpp_gateway(xapi, module, portal_name, config_name,
                    type_, gateway_address):
    xapi.get(_GW_PATH % (portal_name, config_name, type_, gateway_address))
    e = xapi.element_root.find('.//entry')
    return e


def delete_gpp_gateway(xapi, module, portal_name, config_name,
                       type_, gateway_address):
    xapi.delete(xpath=_GW_PATH % (portal_name, config_name,
                                  type_, gateway_address))
    return True


def modify_gpp_gateway(cgw, xapi, module, portal_name, config_name,
                       type_, gateway_address, manual, description):
    result = False

    if manual is not None:
        cmanual = cgw.find('manual')
        if cmanual is None:
            raise Exception('No manual value tag')
        if cmanual.text not in ['yes', 'no']:
            raise Exception('Invalid manual value: %s' % cmanual.text)

        if bool(cmanual == 'yes') ^ bool(manual):
            xapi.edit(xpath=(_GW_PATH+"/manual") %
                      (portal_name, config_name, type_, gateway_address),
                      element="<manual>%s</manual>" %
                      ('yes' if manual else 'no'))
            result = True

    if description is not None:
        cdescription = cgw.find('description')
        if cdescription is not None and \
           cdescription.text is not None and \
           cdescription.text == description:
            return result
        xapi.edit(xpath=(_GW_PATH+"/description") %
                  (portal_name, config_name, type_, gateway_address),
                  element="<description>%s</description>" %
                  description)
        result = True

    return result


def create_gpp_gateway(xapi, module, portal_name, config_name,
                       type_, gateway_address, manual, description, exists):
    entry = []
    # entry.append("<entry name='%s'>"%gateway_address)
    entry.append("<manual>%s</manual>" % ('yes' if manual else 'no'))
    entry.append("<priority>1</priority>")
    if description:
        entry.append("<description>%s</description>" % description)
    # entry.append("<entry/>")

    if exists:
        xapi.set(xpath=_GW_PATH %
                 (portal_name, config_name, type_, gateway_address),
                 element=''.join(entry))
    else:
        xapi.set(xpath=_GW_PATH %
                 (portal_name, config_name, type_, gateway_address),
                 element=''.join(entry))
    return True


def check_gpp_gateway(xapi, module, portal_name, config_name, gateway_address,
                      type_, state, manual, description):
    cgw = get_gpp_gateway(
        xapi,
        module,
        portal_name,
        config_name,
        type_,
        gateway_address
    )

    if state == 'absent':
        # we don't want the gw and the gw does not exists. Fair enough
        if cgw is None:
            return False

        return delete_gpp_gateway(xapi, module, portal_name, config_name,
                                  type_, gateway_address)

    # state 'present'
    if cgw is not None:
        # we want the gw and the gw exists. Check if matches our desiderata
        return modify_gpp_gateway(cgw, xapi, module, portal_name, config_name,
                                  type_, gateway_address, manual, description)

    return create_gpp_gateway(xapi, module, portal_name, config_name,
                              type_, gateway_address, manual, description,
                              cgw is not None)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        portal_name=dict(default=None),
        config_name=dict(default=None),
        gateway_address=dict(default=None),
        type=dict(default="external", choices=['internal', 'external']),
        state=dict(default="present", choices=['absent', 'present']),
        manual=dict(type='bool', default=None),
        description=dict(default=None),
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

    portal_name = module.params['portal_name']
    if portal_name is None:
        module.fail_json(msg='portal_name is required')
    config_name = module.params['config_name']
    if config_name is None:
        module.fail_json(msg='config_name is required')
    gateway_address = module.params['gateway_address']
    if gateway_address is None:
        module.fail_json(msg='gateway_address is required')
    type_ = module.params['type']
    state = module.params['state']
    manual = module.params['manual']
    description = module.params['description']
    commit = module.params['commit']

    changed = False
    changed = check_gpp_gateway(
        xapi,
        module,
        portal_name,
        config_name,
        gateway_address,
        type_,
        state,
        manual,
        description
    )

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
