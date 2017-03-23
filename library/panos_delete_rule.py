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
module: panos_security_policy
short_description: Create security rule policy on PanOS devices.
description: >
    Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
    The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
    the traffic is applied, the more specific rules must precede the more general ones.
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.3"
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
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    rule_name:
        description:
            - Name of the security rule.
        required: true
    rule_type:
        description:
            - Type of security rule (version 6.1 of PanOS and above).
        default: "universal"
    description:
        description:
            - Description for the security rule.
        default: "None"
    tag:
        description:
            - Administrative tags that can be added to the rule. Note, tags must be already defined.
        default: "None"
    from_zone:
        description:
            - List of source zones.
        default: "any"
    to_zone:
        description:
            - List of destination zones.
        default: "any"
    source:
        description:
            - List of source addresses.
        default: "any"
    source_user:
        description:
            - Use users to enforce policy for individual users or a group of users.
        default: "any"
    hip_profiles:
        description: >
            If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy
            on information collected by GlobalProtect. For example, the user access level can be determined HIP that
            notifies the firewall about the user's local configuration.
        default: "any"
    destination:
        description:
            - List of destination addresses.
        default: "any"
    application:
        description:
            - List of applications.
        default: "any"
    service:
        description:
            - List of services.
        default: "application-default"
    log_start:
        description:
            - Whether to log at session start.
        default: false
    log_end:
        description:
            - Whether to log at session end.
        default: true
    action:
        description:
            - Action to apply once rules maches.
        default: "allow"
    group_profile:
        description: >
            Security profile group that is already defined in the system. This property supersedes antivirus,
            vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
        default: None
    antivirus:
        description:
            - Name of the already defined antivirus profile.
        default: None
    vulnerability:
        description:
            - Name of the already defined vulnerability profile.
        default: None
    spyware:
        description:
            - Name of the already defined spyware profile.
        default: None
    url_filtering:
        description:
            - Name of the already defined url_filtering profile.
        default: None
    file_blocking:
        description:
            - Name of the already defined file_blocking profile.
        default: None
    data_filtering:
        description:
            - Name of the already defined data_filtering profile.
        default: None
    wildfire_analysis:
        description:
            - Name of the already defined wildfire_analysis profile.
        default: None
    devicegroup:
        description: >
            Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.
            If device group is not define we assume that we are contacting Firewall.
        default: None
'''

EXAMPLES = '''
- name: permit ssh to 1.1.1.1
  panos_security_policy:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    from_zone: ['public']
    to_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    hip_profiles: ['any']
    action: 'allow'

- name: Allow HTTP multimedia only from CDNs
  panos_security_policy:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'HTTP Multimedia'
    description: 'Allow HTTP multimedia only to host at 1.1.1.1'
    from_zone: ['public']
    to_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['content-delivery-networks']
    application: ['http-video', 'http-audio']
    service: ['service-http', 'service-https']
    hip_profiles: ['any']
    action: 'allow'

- name: more complex fictitious rule that uses profiles
  panos_security_policy:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'Allow HTTP w profile'
    log_start: false
    log_end: true
    action: 'allow'
    antivirus: 'default'
    vulnerability: 'default'
    spyware: 'default'
    url_filtering: 'default'
    wildfire_analysis: 'default'

- name: deny all
  panos_security_policy:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'DenyAll'
    log_start: true
    log_end: true
    action: 'deny'
    rule_type: 'interzone'

# permit ssh to 1.1.1.1 using panorama and pushing the configuration to firewalls
# that are defined in 'DeviceGroupA' device group
- name: permit ssh to 1.1.1.1 through Panorama
  panos_security_policy:
    ip_address: '10.5.172.92'
    password: 'paloalto'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    from_zone: ['public']
    to_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    hip_profiles: ['any']
    action: 'allow'
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
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import objects
    from pandevice import policies

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def devicegroup_exists(device, devicegroup):
    dev_grps = device.refresh_devices()
    for grp in dev_grps:
        if isinstance(grp, pandevice.panorama.DeviceGroup):
            if grp.name == devicegroup:
                return True
    return False


def get_rulebase(device, devicegroup):
    # Build the rulebase
    if isinstance(device, pandevice.firewall.Firewall):
        rulebase = pandevice.policies.Rulebase()
        device.add(rulebase)
    elif isinstance(device, pandevice.panorama.Panorama):
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


def delete_rule(rulebase, sec_rule):
    if rulebase:
        rulebase.add(sec_rule)
        sec_rule.create()
        return True
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

    # If the rule exists, delete it
    if rule:
        try:
            rule.delete()
        except PanXapiError:
            exc = get_exception()
            module.fail_json(msg=exc.message)
        module.exit_json(changed=True, msg="Rule \'%s\' successfully deleted" % rule_name)
    else:
        module.fail_json(changed=False, msg='Rule \'%s\' not found. Is the name correct?' % rule_name)


if __name__ == '__main__':
    main()