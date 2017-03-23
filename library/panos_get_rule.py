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
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: panos_searchpolicy
short_description: retrieve security rule policy
description: >
    Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
    The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
    the traffic is applied, the more specific rules must precede the more general ones.
author: "Bob Hagen (@rnh556)"
version_added: "1.0"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth.
        required: false
        default: "admin"
    password:
        description:
            - Password credentials to use for auth.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    rule_name:
        description:
            - Name of the security rule.
        required: true
    devicegroup:
        description: >
            Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.
            If device group is not define we assume that we are contacting Firewall.
        required: false
        default: None
'''

EXAMPLES = '''
- name: search for firewall security rule
  panos_searchpolicy:
    ip_address: '10.0.0.1'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'SSH permit'

- name: search for  devicegroup rule
  panos_searchpolicy:
    ip_address: '10.0.0.1'
    password: 'paloalto'
    rule_name: 'SSH permit'
    devicegroup: 'DeviceGroupA'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    import pan.xapi
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import policies
    from pandevice import base
    import xmltodict
    import json
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def devicegroup_exists(device, devicegroup):
    dev_grps = device.refresh_devices()
    for grp in dev_grps:
        if isinstance(grp, panorama.DeviceGroup):
            if grp.name == devicegroup:
                return True
    return False


def get_rulebase(device, devicegroup):
    # Build the rulebase
    if isinstance(device, firewall.Firewall):
        rulebase = policies.Rulebase()
        device.add(rulebase)
    elif isinstance(device, panorama.Panorama):
        dg = panorama.DeviceGroup(devicegroup)
        device.add(dg)
        rulebase = policies.PreRulebase()
        dg.add(rulebase)
    else:
        return False
    policies.SecurityRule.refreshall(rulebase)
    return rulebase


def get_rule(rulebase, rule_name):
    # Search for the rule name
    rule = rulebase.find(rule_name)
    if rule:
        return rule
    else:
        return False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        rule_name=dict(required=True),
        devicegroup=dict()
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    rule_name = module.params['rule_name']
    devicegroup = module.params['devicegroup']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    if isinstance(device, panorama.Panorama):
        if devicegroup_exists(device, devicegroup):
            pass
        else:
            module.fail_json(
                failed=1,
                msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup
            )

    # Build the rulebase and search for the rule
    rulebase = get_rulebase(device, devicegroup)
    rule = get_rule(rulebase, rule_name)

    # If the rule exists, format and display it
    if rule:
        rule_dict = xmltodict.parse(rule.element_str())
        module.exit_json(
            stdout_lines=json.dumps(rule_dict, indent=2),
            msg='Rule matched'
        )
    else:
        module.fail_json(msg='\'%s\' rule not found. Is the name correct?' % rule_name)

if __name__ == '__main__':
    main()
