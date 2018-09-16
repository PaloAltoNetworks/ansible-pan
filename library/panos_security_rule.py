#!/usr/bin/env python

#  Copyright 2017 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_security_rule
short_description: Create security rule policy on PAN-OS devices or Panorama management console.
description:
    - Security policies allow you to enforce rules and take action, and can be as general or specific as needed. 
    - The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches 
    - the traffic is applied, the more specific rules must precede the more general ones.
author: "Ivan Bojer (@ivanbojer), Robert Hagen (@stealthllama), Michael Richardson (@mrichardson03)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
    - xmltodict can be obtained from PyPi U(https://pypi.python.org/pypi/xmltodict)
notes:
    - Checkmode is not supported.
    - Panorama is supported.
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
    source_zone:
        description:
            - List of source zones.
        default: "any"
    source_ip:
        description:
            - List of source addresses.
        default: "any"
    source_user:
        description:
            - Use users to enforce policy for individual users or a group of users.
        default: "any"
    hip_profiles:
        description: >
            - If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy
            on information collected by GlobalProtect. For example, the user access level can be determined HIP that
            notifies the firewall about the user's local configuration.
        default: "any"
    destination_zone:
        description:
            - List of destination zones.
        default: "any"
    destination_ip:
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
    category:
        description:
            - Destination URL categories
    action:
        description:
            - Action to apply once rules matches.
        default: "allow"
    log_setting:
        description:
            - Log forwarding profile
    log_start:
        description:
            - Whether to log at session start.
        default: false
    log_end:
        description:
            - Whether to log at session end.
        default: true
    description:
        description:
            - Description for the security rule.
        default: "None"
    rule_type:
        description:
            - Type of security rule (version 6.1 of PanOS and above).
        default: "universal"
    tag_name:
        description:
            - Administrative tags that can be added to the rule. Note, tags must be already defined.
        default: "None"
    negate_source:
        description:
            - Match on the reverse of the 'source' attribute
        default: false
    negate_destination:
        description:
            - Match on the reverse of the 'destination' attribute
        default: false
    disabled:
        description:
            - Disable this rule
        default: false
    schedule:
        description:
            - Schedule profile
    icmp_unreachable:
        description:
            - Send 'ICMP Unreachable'. Used with 'deny', 'drop', and 'reset' actions.
        default: false
    disable_server_response_inspection:
        description:
            - Disables packet inspection from the server to the client. Useful under heavy server load conditions.
        default: false
    group_profile:
        description: >
            - Security profile group that is already defined in the system. This property supersedes antivirus,
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
    location:
        description:
            - Position to place the created rule in the rule base.  Supported values are
              I(top)/I(bottom)/I(before)/I(after).
        default: "bottom"
    existing_rule:
        description:
            - If 'location' is set to 'before' or 'after', this option specifies an existing
              rule name.  The new rule will be created in the specified position relative to this
              rule.  If 'location' is set to 'before' or 'after', this option is required.
    devicegroup:
        description: >
            - Device groups are logical groups of firewalls in Panorama.
            - If the device group is not defined actions will affect the Shared Panorama context.
        default: None
    pre_rule:
        description:
            - If the security rule is applied against Panorama, set this to True to create a pre-rule.
        default: True
    post_rule:
        description:
            - If the security rule is applied against Panorama, set this to True to create a post-rule.
        default: False
    target:
        description:
            - Apply this rule exclusively to the listed firewalls in Panorama.
    negate_target:
        description:
            - Exclude this rule from the listed firewalls in Panorama.
    state:
        description:
            - The state of the rule.  Can be either I(present)/I(absent).
    operation:
        description:
            - The action to be taken.  Supported values are I(add)/I(update)/I(find)/I(delete).
            - I(Deprecated - use 'state' instead.) 
        default: 'add'
    commit:
        description:
            - Commit configuration if changed.
        default: false
'''

EXAMPLES = '''
- name: add an SSH inbound rule to devicegroup
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    tag_name: ['ProjectX']
    source_zone: ['public']
    destination_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    hip_profiles: ['any']
    action: 'allow'
    devicegroup: 'Cloud Edge'
    rulebase: true


- name: add a rule to allow HTTP multimedia only from CDNs
  panos_security_rule:
    ip_address: '10.5.172.91'
    username: 'admin'
    password: 'paloalto'
    rule_name: 'HTTP Multimedia'
    description: 'Allow HTTP multimedia only to host at 1.1.1.1'
    source_zone: ['public']
    destination_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    category: ['content-delivery-networks']
    application: ['http-video', 'http-audio']
    service: ['service-http', 'service-https']
    hip_profiles: ['any']
    action: 'allow'

- name: add a more complex rule that uses security profiles
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    rule_name: 'Allow HTTP'
    log_start: false
    log_end: true
    action: 'allow'
    antivirus: 'default'
    vulnerability: 'default'
    spyware: 'default'
    url_filtering: 'default'
    wildfire_analysis: 'default'
    
- name: disable a Panorama pre-rule 
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    rule_name: 'Allow telnet'
    source_zone: ['public']
    destination_zone: ['private']
    source: ['any']
    source_user: ['any']
    destination: ['1.1.1.1']
    log_start: false
    log_end: true
    action: 'allow'
    devicegroup: 'Production edge'
    rulebase: 'pre'
    disabled: true


- name: delete a devicegroup security rule
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    api_key: '{{ api_key }}'
    operation: 'delete'
    rule_name: 'Allow telnet'
    devicegroup: 'DC Firewalls'
    rulebase: 'pre'
    state: absent

- name: add a rule at a specific location in the rulebase
  panos_security_rule:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    operation: 'add'
    rule_name: 'SSH permit'
    description: 'SSH rule test'
    source_zone: ['untrust']
    destination_zone: ['trust']
    source_ip: ['any']
    source_user: ['any']
    destination_ip: ['1.1.1.1']
    category: ['any']
    application: ['ssh']
    service: ['application-default']
    action: 'allow'
    location: 'before'
    existing_rule: 'Allow MySQL'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pandevice.base import PanDevice
    from pandevice.policies import Rulebase, SecurityRule, PreRulebase, PostRulebase
    from pandevice.device import Vsys
    from pandevice.firewall import Firewall
    from pandevice.panorama import Panorama, DeviceGroup
    from pandevice.errors import PanDeviceError
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

ACCEPTABLE_MOVE_ERRORS = (
    'already at the top',
    'already at the bottom',
)


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def get_rulebase(device, devicegroup, rulebase):
    # Determine the rulebase type and attach it to the device
    if isinstance(device, Firewall):
        rb = Rulebase()
        device.add(rb)
    elif isinstance(device, Panorama):
        dg = DeviceGroup(devicegroup)
        device.add(dg)
        if rulebase == 'pre':
            rb = PreRulebase()
        elif rulebase == 'post':
            rb = PostRulebase()
        dg.add(rb)
    return rb


def find_rule(rules, new_rule):
    for r in rules:
        if r.name == new_rule.name:
            return r


# TODO: Remove operation parameter and all associated code
def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        rule_name=dict(required=True),
        source_zone=dict(type='list', default=['any']),
        source_ip=dict(type='list', default=["any"]),
        source_user=dict(type='list', default=['any']),
        hip_profiles=dict(type='list', default=['any']),
        destination_zone=dict(type='list', default=['any']),
        destination_ip=dict(type='list', default=["any"]),
        application=dict(type='list', default=['any']),
        service=dict(type='list', default=['application-default']),
        category=dict(type='list', default=['any']),
        action=dict(default='allow', choices=['allow', 'deny', 'drop', 'reset-client', 'reset-server', 'reset-both']),
        log_setting=dict(),
        log_start=dict(type='bool', default=False),
        log_end=dict(type='bool', default=True),
        description=dict(default=''),
        rule_type=dict(default='universal', choices=['universal', 'intrazone', 'interzone']),
        tag_name=dict(type='list'),
        negate_source=dict(type='bool', default=False),
        negate_destination=dict(type='bool', default=False),
        disabled=dict(type='bool', default=False),
        schedule=dict(),
        icmp_unreachable=dict(type='bool', default=False),
        disable_server_response_inspection=dict(type=bool, default=False),
        group_profile=dict(),
        antivirus=dict(),
        spyware=dict(),
        vulnerability=dict(),
        url_filtering=dict(),
        file_blocking=dict(),
        wildfire_analysis=dict(),
        data_filtering=dict(),
        target=dict(type='list'),
        negate_target=dict(type='bool', default=False),
        location=dict(choices=['top', 'bottom', 'before', 'after']),
        existing_rule=dict(),
        devicegroup=dict(),
        rulebase=dict(default='pre', choices=['pre', 'post']),
        state=dict(default='present', choices=['present', 'absent']),
        operation=dict(default='add', choices=['add', 'update', 'delete', 'find']),
        commit=dict(type='bool', default=False)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                           required_one_of=[['api_key', 'password']])

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')
    elif not hasattr(SecurityRule, 'move'):
        module.fail_json(msg='Python library pandevice needs to be updated.')

    # Get the firewall / panorama auth.
    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password', 'api_key')]

    # Create the device with the appropriate pandevice type
    device = PanDevice.create_from_device(*auth)

    # If Panorama, validate the devicegroup if its defined
    devicegroup = module.params['devicegroup']
    dg = None
    if devicegroup and isinstance(device, Panorama):
        dg = get_devicegroup(device, devicegroup)
        if dg:
            device.add(dg)
        else:
            module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    # Get the params needed to build the rule object
    rule_spec = {
        'name': module.params['rule_name'],
        'fromzone': module.params['source_zone'],
        'tozone': module.params['destination_zone'],
        'source': module.params['source_ip'],
        'source_user': module.params['source_user'],
        'hip_profiles': module.params['hip_profiles'],
        'destination': module.params['destination_ip'],
        'application': module.params['application'],
        'service': module.params['service'],
        'category': module.params['category'],
        'action': module.params['action'],
        'log_setting': module.params['log_setting'],
        'log_start': module.params['log_start'],
        'log_end': module.params['log_end'],
        'description': module.params['description'],
        'type': module.params['rule_type'],
        'tag': module.params['tag_name'],
        'negate_source': module.params['negate_source'],
        'negate_destination': module.params['negate_destination'],
        'disabled': module.params['disabled'],
        'schedule': module.params['schedule'],
        'icmp_unreachable': module.params['icmp_unreachable'],
        'disable_server_response_inspection': module.params['disable_server_response_inspection'],
        'group': module.params['group_profile'],
        'virus': module.params['antivirus'],
        'spyware': module.params['spyware'],
        'vulnerability': module.params['vulnerability'],
        'url_filtering': module.params['url_filtering'],
        'file_blocking': module.params['file_blocking'],
        'wildfire_analysis': module.params['wildfire_analysis'],
        'data_filtering': module.params['data_filtering'],
    }

    # Add additional rule params if Panorama
    if isinstance(device, Panorama):
        rule_spec['target'] = module.params['target']
        rule_spec['negate_target'] = module.params['negate_target']

    # Get additional rule info
    location = module.params['location']
    existing_rule = module.params['existing_rule']
    rulebase = module.params['rulebase']
    state = module.params['state']
    operation = module.params['operation']
    commit = module.params['commit']

    # Sanity check the location / existing_rule params.
    if location in ('before', 'after') and not existing_rule:
        module.fail_json(msg="'existing_rule' must be specified if location is 'before' or 'after'.")

    # Get the rulebase and grab its security rules
    parent = get_rulebase(device, dg, rulebase)
    rules = SecurityRule.refreshall(parent)

    # Create new rule object from the params and add to rulebase
    new_rule = SecurityRule(**rule_spec)
    if not new_rule:
        module.fail_json(msg='Incorrect rule parameters specified; quitting')
    parent.add(new_rule)

    # Which action shall we take on the rule object?
    changed = False
    if state == 'present':
        match = find_rule(rules, new_rule)
        if match:
            # Change an existing rule
            if not match.equal(new_rule):
                # Change existing rule values
                try:
                    if not module.check_mode:
                        new_rule.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed "present" create: {0}'.format(e))
                else:
                    changed = True
        else:
            # Add a new rule
            try:
                if not module.check_mode:
                    new_rule.apply()
            except PanDeviceError as e:
                module.fail_json(msg='Failed "present" apply: {0}'.format(e))
            else:
                changed = True
        # Move the rule if location is defined
        if location:
            try:
                if not module.check_mode:
                    new_rule.move(location, existing_rule)
            except PanDeviceError as e:
                if '{0}'.format(e) not in ACCEPTABLE_MOVE_ERRORS:
                    module.fail_json(msg='Failed move: {0}'.format(e))
            else:
                changed = True
    elif state == 'absent':
        match = find_rule(rules, new_rule)
        if match:
            # Delete an existing rule
            try:
                if not module.check_mode:
                    new_rule.delete()
            except PanDeviceError as e:
                module.fail_json(msg='Failed "absent" delete: {0}'.format(e))
            else:
                changed = True
    elif operation == "find":
        # Search for the rule
        match = find_rule(rules, new_rule)
        # If found, format and return the result
        if match:
            module.exit_json(
                stdout_lines=match.about(),
                msg='Rule matched'
            )
        else:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % new_rule.name)
    elif operation == "delete":
        # Search for the object
        match = find_rule(rules, new_rule)
        if match is None:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % new_rule.name)
        try:
            if not module.check_mode:
                new_rule.delete()
        except PanDeviceError as e:
            module.fail_json(msg='Failed "delete" delete: {0}'.format(e))
        else:
            changed = True
    elif operation == "add":
        # Search for the rule. Fail if found.
        match = find_rule(rules, new_rule)
        if match:
            module.fail_json(msg='Rule \'%s\' already exists. Use operation: \'update\' to change it.' % new_rule.name)
        try:
            if not module.check_mode:
                new_rule.create()
        except PanDeviceError as e:
            module.fail_json(msg='Failed "add" create: {0}'.format(e))
        else:
            changed = True
            if location:
                try:
                    if not module.check_mode:
                        new_rule.move(location, existing_rule)
                except PanDeviceError as e:
                    if '{0}'.format(e) not in ACCEPTABLE_MOVE_ERRORS:
                        module.fail_json(msg='Failed move: {0}'.format(e))
    elif operation == 'update':
        # Search for the rule. Update if found.
        match = find_rule(rulebase, new_rule.name)
        if not match:
            module.fail_json(msg='Rule \'%s\' does not exist. Use operation: \'add\' to add it.' % new_rule.name)
        try:
            if not module.check_mode:
                new_rule.apply()
        except PanDeviceError as e:
            module.fail_json(msg='Failed "update" apply: {0}'.format(e))
        else:
            changed = True
            if location:
                try:
                    if not module.check_mode:
                        new_rule.move(location, existing_rule)
                except PanDeviceError as e:
                    if '{0}'.format(e) not in ACCEPTABLE_MOVE_ERRORS:
                        module.fail_json(msg='Failed move: {0}'.format(e))

    # Optional commit.
    # FIXME: Commits should be done using the separate commit module
    if changed and commit:
        try:
            device.commit(sync=True)
        except PanDeviceError as e:
            module.fail_json(msg='Failed commit: {0}'.format(e))

    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
