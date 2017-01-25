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

DOCUMENTATION = '''
---
module: panos_security_policy
short_description: create security rule tuple
description:
    - This module will create a security rule based on provided tuples. The basic objects (zones, etc) must be already present.
author:
    - Palo Alto Networks
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
    rule_name:
        description:
            - name of the security rule
        required: true
    from_zone:
        description:
            - list of source zones
        required: false
        default: "any"
    to_zone:
        description:
            - list of destination zones
        required: false
        default: "any"
    source:
        description:
            - list of source addresses
        required: false
        default: "any"
    destination:
        description:
            - list of destination addresses
        required: false
        default: "any"
    application:
        description:
            - list of applications
        required: false
        default: "any"
    service:
        description:
            - list of services
        required: false
        default: "application-default"
    hip_profiles:
        description:
            - list of HIP profiles
        required: false
        default: "any"
    group_profile:
        description:
            - security profile group
        required: false
        default: None
    log_start:
        description:
            - whether to log at session start
        required: false
        default: "false"
    log_end:
        description:
            - whether to log at session end
        required: false
        default: true
    rule_type:
        description:
            - type of security rule (6.1+)
        required: false
        default: "universal"
    vulnprofile_name:
        description:
            - name of the vulnerability profile
        required: false
        default: None
    action:
        description:
            - action
        required: false
        default: "allow"
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# permit ssh to 1.1.1.1
- panos_security_policy:
    ip_address: "192.168.1.1"
    password: "admin"
    rule_name: "SSH permit"
    from_zone: ["public"]
    to_zone: ["private"]
    source: ["any"]
    source_user: ["any"]
    destination: ["1.1.1.1"]
    category: ["any"]
    application: ["ssh"]
    service: ["application-default"]
    hip_profiles: ["any"]
    action: "allow"
    commmit: False

# deny all
- panos_security_policy:
    ip_address: "192.168.1.1"
    password: "admin"
    username: "admin"
    rule_name: "DenyAll"
    log_start: true
    log_end: true
    action: "deny"
    rule_type: "interzone"
    commmit: False
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    import pan.xapi
    from pan.xapi import PanXapiError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_SRULE_XPATH = "/config/devices/entry[@name='localhost.localdomain']" + \
               "/vsys/entry[@name='vsys1']" + \
               "/rulebase/security/rules/entry[@name='%s']"


def security_rule_exists(xapi, rule_name):
    xapi.get(_SRULE_XPATH % rule_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_security_rule(xapi, **kwargs):
    if security_rule_exists(xapi, kwargs['rule_name']):
        return False

    # exml = ['<entry name="permit-server"%s">'%kwargs['rule_name']]
    exml = []

    exml.append('<to>')
    for t in kwargs['to_zone']:
        exml.append('<member>%s</member>' % t)
    exml.append('</to>')

    exml.append('<from>')
    for t in kwargs['from_zone']:
        exml.append('<member>%s</member>' % t)
    exml.append('</from>')

    exml.append('<source>')
    for t in kwargs['source']:
        exml.append('<member>%s</member>' % t)
    exml.append('</source>')

    exml.append('<destination>')
    for t in kwargs['destination']:
        exml.append('<member>%s</member>' % t)
    exml.append('</destination>')

    exml.append('<source-user>')
    for t in kwargs['source_user']:
        exml.append('<member>%s</member>' % t)
    exml.append('</source-user>')

    exml.append('<category>')
    for t in kwargs['category']:
        exml.append('<member>%s</member>' % t)
    exml.append('</category>')

    exml.append('<application>')
    for t in kwargs['application']:
        exml.append('<member>%s</member>' % t)
    exml.append('</application>')

    exml.append('<service>')
    for t in kwargs['service']:
        exml.append('<member>%s</member>' % t)
    exml.append('</service>')

    exml.append('<hip-profiles>')
    for t in kwargs['hip_profiles']:
        exml.append('<member>%s</member>' % t)
    exml.append('</hip-profiles>')

    if kwargs['group_profile'] is not None:
        exml.append('<profile-setting>'
                    '<group><member>%s</member></group>'
                    '</profile-setting>' % kwargs['group_profile'])

    if kwargs['log_start']:
        exml.append('<log-start>yes</log-start>')
    else:
        exml.append('<log-start>no</log-start>')

    if kwargs['log_end']:
        exml.append('<log-end>yes</log-end>')
    else:
        exml.append('<log-end>no</log-end>')

    if kwargs['rule_type'] != 'universal':
        exml.append('<rule-type>%s</rule-type>' % kwargs['rule_type'])

    exml.append('<action>%s</action>' % kwargs['action'])

    if kwargs['vulnprofile_name'] is not None:
        exml.append('<profile-setting>')
        exml.append('<profiles>')
        exml.append('<vulnerability>')
        exml.append('<member>%s</member>' % kwargs['vulnprofile_name'])
        exml.append('</vulnerability>')
        exml.append('</profiles>')
        exml.append('</profile-setting>')

    # exml.append('</entry>')

    exml = ''.join(exml)
    xapi.set(xpath=_SRULE_XPATH % kwargs['rule_name'], element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        rule_name=dict(required=True),
        from_zone=dict(type='list', default=['any']),
        to_zone=dict(type='list', default=['any']),
        source=dict(type='list', default=["any"]),
        source_user=dict(type='list', default=['any']),
        destination=dict(type='list', default=["any"]),
        category=dict(type='list', default=['any']),
        application=dict(type='list', default=['any']),
        service=dict(type='list', default=['application-default']),
        hip_profiles=dict(type='list', default=['any']),
        group_profile=dict(),
        vulnprofile_name=dict(),
        log_start=dict(type='bool', default=False),
        log_end=dict(type='bool', default=True),
        rule_type=dict(default='universal'),
        action=dict(default='allow'),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           mutually_exclusive=[['group_profile', 'vulnprofile_name']])

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    rule_name = module.params['rule_name']
    from_zone = module.params['from_zone']
    to_zone = module.params['to_zone']
    source = module.params['source']
    source_user = module.params['source_user']
    destination = module.params['destination']
    category = module.params['category']
    application = module.params['application']
    service = module.params['service']
    hip_profiles = module.params['hip_profiles']
    action = module.params['action']

    group_profile = module.params['group_profile']
    vulnprofile_name = module.params['vulnprofile_name']
    log_start = module.params['log_start']
    log_end = module.params['log_end']
    rule_type = module.params['rule_type']
    commit = module.params['commit']

    try:
        changed = add_security_rule(
            xapi,
            rule_name=rule_name,
            from_zone=from_zone,
            to_zone=to_zone,
            source=source,
            source_user=source_user,
            destination=destination,
            category=category,
            application=application,
            service=service,
            hip_profiles=hip_profiles,
            group_profile=group_profile,
            log_start=log_start,
            log_end=log_end,
            rule_type=rule_type,
            vulnprofile_name=vulnprofile_name,
            action=action
        )
    except PanXapiError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
