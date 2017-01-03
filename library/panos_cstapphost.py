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
module: panos_cstapphost
short_description: create a custom application based on the Host header
description:
    - Create a custom application for internal website based on the Host header
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
    app_name:
        description:
            - name of the new custom application
        required: true
    host_regex:
        description:
            - regex to match against the Host header
        required: true
    convert_hostname:
        description:
            - wheter convert string given as regex in a real regex
        required: false
        default: "false"
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# create a custom application for traffic for test.example.com
- name: setup custom application
  panos_cstapphost:
    ip_address: "192.168.1.1"
    password: "admin"
    username: "admin"
    app_name: "test"
    host_regex: "test\\.example\\.com"
'''

import sys

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_CUSTOM_APP_XPATH = "/config/devices/entry[@name='localhost.localdomain']/" +\
                    "vsys/entry[@name='vsys1']/application/entry[@name='%s']"

_CUSTOM_APP_TEMPLATE = """<default><port><member>tcp/80</member></port></default>
<signature>
<entry name="%s">
<and-condition>
<entry name="And Condition 1">
<or-condition>
<entry name="Or Condition 1">
<operator>
<pattern-match>
<pattern>
%s
</pattern>
<context>http-req-host-header</context>
</pattern-match>
</operator>
</entry>
</or-condition>
</entry>
</and-condition>
<scope>protocol-data-unit</scope>
<order-free>no</order-free>
</entry>
</signature>
<subcategory>web-posting</subcategory>
<category>collaboration</category>
<technology>browser-based</technology>
<risk>1</risk>
<able-to-transfer-file>yes</able-to-transfer-file>
<has-known-vulnerability>yes</has-known-vulnerability>
<file-type-ident>yes</file-type-ident>
<virus-ident>yes</virus-ident>
<parent-app>web-browsing</parent-app>
"""


def custom_app_exists(xapi, app_name):
    xapi.get(_CUSTOM_APP_XPATH % app_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_custom_app(xapi, app_name, host_regex):
    if custom_app_exists(xapi, app_name):
        return False

    xapi.set(xpath=_CUSTOM_APP_XPATH % app_name,
             element=_CUSTOM_APP_TEMPLATE % (app_name, host_regex))

    return True


def convert_to_regex(hname):
    # just subst '.' with '\.'
    return hname.replace('.', '\.')


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        app_name=dict(default=None),
        host_regex=dict(default=None),
        convert_hostname=dict(type='bool', default=False),
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

    app_name = module.params['app_name']
    if not app_name:
        module.fail_json(msg='app_name is required')
    host_regex = module.params['host_regex']
    if not host_regex:
        module.fail_json(msg='host_regex is required')
    convert_hostname = module.params['convert_hostname']
    if convert_hostname:
        host_regex = convert_to_regex(host_regex)
    commit = module.params['commit']

    changed = add_custom_app(xapi, app_name, host_regex)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
