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
module: panos_vulnprofile
short_description: create vulnerability profile
description:
    - Create custom vulnerability profile
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
    rule_tuples:
        description:
            - "a list of dictionaries that contains each rule definition. A rule is made of:"
            - "rule_name: required"
            - "threat_name: optional, deafult is 'any'"
            - "vendor_id: optional, deafult is 'any'"
            - "cve: optional, deafult is 'any'"
            - "host_type: optional, deafult is 'client'"
            - "severity: required"
            - "action: optional, deafult is 'default'"
            - "capture: optional, deafult is 'disable'"
        required: false
        default: None
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
panos_vulnprofile:
  ip_address: "10.0.0.43"
  password: "admin"
  vulnprofile_name: "SampleVRule"
  description: "some description"
  rule_tuples: [{'rule_name': 'simple-client-critical', 'threat_name': 'any', 'vendor_id': 'any', 'cve': '1.1.1.1', 'host_type': 'client', 'severity': 'critical', 'action': 'default', 'capture': 'disable'}, {'rule_name': 'simple-client-high', 'threat_name': 'any', 'cve': 'any', 'vendor_id': '1.1.1.1', 'host_type': 'client', 'severity': 'high', 'action': 'default', 'capture': 'disable'}]
  exception_ids: ["35931","35933"]
  commit: False
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

from ansible.module_utils.basic import AnsibleModule
import json
# import pydevd
# pydevd.settrace('localhost', port=62980, stdoutToServer=True, stderrToServer=True)


try:
    import pan.xapi
    from pan.xapi import PanXapiError
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_SERVICE_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
                 "/vsys/entry[@name='vsys1']" +\
                 "/profiles/vulnerability/entry[@name='%s']"


def debug(msg):
    print json.dumps({
        "DEBUG": msg
    })


def vulnerability_profile_exists(xapi, vulnprofile_name):
    xapi.get(_SERVICE_XPATH % vulnprofile_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_vulnerability_profile(xapi, **kwargs):
    if vulnerability_profile_exists(xapi, kwargs['vulnprofile_name']):
        return False

    exml = []

    if kwargs['rule_tuples'] is not None:
        exml.append('<rules>')
        for item in kwargs['rule_tuples']:
            cve = "any"
            vendor_id = "any"
            threat_name = "any"
            host_type = "client"
            action = "default"
            capture = "disable"
            category = "any"

            if 'cve' in item:
                cve = item['cve']
            if 'vendor_id' in item:
                vendor_id = item['vendor_id']
            if 'threat_name' in item:
                threat_name = item['threat_name']
            if 'host_type' in item:
                host_type = item['host_type']
            if 'action' in item:
                action = item['action']
            if 'capture' in item:
                capture = item['capture']
            if 'category' in item:
                category = item['category']

            exml.append('<entry name=\"%s\">' % item['rule_name'])
            exml.append('<cve><member>%s</member></cve>' % cve)
            exml.append('<vendor-id><member>%s</member></vendor-id>' %
                        vendor_id)
            exml.append('<severity><member>%s</member></severity>' %
                        item['severity'])
            exml.append('<threat-name>%s</threat-name>' %
                        threat_name)
            exml.append('<host>%s</host>' % host_type)
            exml.append('<category>%s</category>' % category)
            exml.append('<packet-capture>%s</packet-capture>' %
                        capture)
            exml.append('<action><%s/></action>' %
                        action)
            exml.append('</entry>')
        exml.append('</rules>')

    if kwargs['exception_ids'] is not None:
        exml.append('<threat-exception>')
        for t in kwargs['exception_ids']:
            exml.append('<entry name=\"%s\">'
                        '<action><reset-client/></action>'
                        '</entry>' % t)
        exml.append('</threat-exception>')

    if kwargs['description'] is not None:
        exml.append('<description>%s</description>' % kwargs['description'])

    exml = ''.join(exml)

# FOR DEBUGGING
#    print "element='%s'"%exml
    xapi.set(xpath=_SERVICE_XPATH % kwargs['vulnprofile_name'], element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        vulnprofile_name=dict(required=True),
        description=dict(default=None),
        rule_tuples=dict(default=None),
        exception_ids=dict(default=None),
        commit=dict(type='bool', default=True)
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

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    vulnprofile_name = module.params["vulnprofile_name"]
    if not vulnprofile_name:
        module.fail_json(msg="vulnprofile_name must be specified")

    description = module.params["description"]
    rule_tuples = module.params["rule_tuples"]
    rule_tuples = rule_tuples.replace('\'','"') #get rid of double-quotes
    rule_tuples = json.loads(rule_tuples)
    exception_ids = module.params["exception_ids"]

    if not rule_tuples and not exception_ids:
        module.fail_json(msg="You cannot have both exception and rules empty")

    commit = module.params['commit']

    try:
        changed = add_vulnerability_profile(xapi,
                                            vulnprofile_name=vulnprofile_name,
                                            description=description,
                                            rule_tuples=rule_tuples,
                                            exception_ids=exception_ids)

        if changed and commit:
            xapi.commit(cmd="<commit></commit>", sync=True, interval=1)
    except PanXapiError:
        import sys
        x = sys.exc_info()[1]
        module.fail_json(msg=x.message)

    module.exit_json(changed=changed, msg="okey dokey")

if __name__ == '__main__':
    main()
