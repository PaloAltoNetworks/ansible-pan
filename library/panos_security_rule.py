#!/usr/bin/env python

#  Copyright 2018 Palo Alto Networks, Inc
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
short_description: Create security rules on PAN-OS devices.
description:
    - Create security rules on PAN-OS devices.
author: "Ivan Bojer (@ivanbojer), Robert Hagen (@rnh556), Michael Richardson (@mrichardson03)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
options:
    ip_address:
        description:
            - IP address or hostname of PAN-OS device.
        required: true
    username:
        description:
            - Username for authentication for PAN-OS device.  Optional if I(api_key) is used.
        default: 'admin'
    password:
        description:
            - Password for authentication for PAN-OS device.  Optional if I(api_key) is used.
    api_key:
        description:
            - API key to be used instead of I(username) and I(password).
    name:
        description:
            - Name of security policy.
        required: true
    fromzone:
        description:
            - From zones.  Required if state is present.
        type: list
    tozone:
        description:
            - To zones.  Required if state is present.
        type: list
    source:
        description:
            - Source IP addresses.
        type: list
        default: ['any']
    destination:
        description:
            - Destination IP addresses.
        type: list
        default: ['any']
    application:
        description:
            - Applications.
        type: list
        default: ['any']
    service:
        description:
            - Destination services (ports).
        type: list
        default: ['application-default']
    category:
        description:
            - Destination URL categories.
        type: list
    action:
        description:
            - Action to take.  Note: not all options are available on all PAN-OS versions.
        choices: ['deny', 'allow', 'drop', 'reset-client', 'reset-server', 'reset-both']
        default: 'allow'
    icmp_unreachable:
        description:
            - Whether to send ICMP unreachable responses for drop actions.
        type: bool
        default: False
    log_setting:
        description:
            - Log forwarding profile.
        type: string
    log_start:
        description:
            - Log at session start
        type: boolean
        default: False
    log_end:
        description:
            - Log at session end
        type: bool
        default: True
    description:
        description:
            - Description of this rule.
        type: str
    type:
        description:
            - Type of policy: universal, interzone, or intrazone.
        choices: ['universal', 'interzone', 'intrazone']
        default: 'universal'
    negate_source:
        description:
            - Match on the reverse of the 'source' attribute.
        type: bool
        default: False
    negate_destination:
        description:
            - Match on the reverse of the 'destination' attribute.
        type: bool
        default: False
    schedule:
        description:
            - Schedule profile.
        type: str
    disable_server_response_inspection:
        description:
            - Disable server response inspection.
        type: bool
        default: False
    group:
        description:
            - Security Profile group name.
        type: str
    virus:
        description:
            - Antivirus security profile name.
        type: str
    spyware:
        description:
            - Anti-Spyware security profile name.
        type: str
    vulnerability:
        description:
            - Vulnerability Protection security profile name.
        type: str
    url_filtering:
        description:
            - URL Filtering security profile name.
        type: str
    file_blocking:
        description:
            - File Blocking security profile name.
        type: str
    wildfire_analysis:
        description:
            - Wildfire Analysis security profile name.
        type: str
    data_filtering:
        description:
            - Data Filtering security profile name.
        type: str
    negate_target:
        description:
            - I(Panorama only.) Target all but the listed target firewalls.  Requires that
              I(target) also be set.
        type: bool
        default: False
    target:
        description:
            - I(Panorama only.) Apply this policy to the listed firewalls only.
        type: list
    tag:
        description:
            - List of tags to add to this security policy.
    location:
        description:
            - Position to place the created rule in the rule base.
        choices: ['top', 'bottom', 'before', 'after']
    existing_rule:
        description:
            - If 'location' is set to 'before' or 'after', this option specifies an existing
              rule name.  The new rule will be created in the specified position relative to this
              rule.  If 'location' is set to 'before' or 'after', this option is required.
    device_group:
        description:
            - If I(ip_address) is a Panorama device, create policy in this device group.
        type: str
    panorama_loc:
        description:
            - If I(ip_address) is a Panorama device and I(device_group) is specified, create
              policy in either the pre or post rules.
        choices: ['pre', 'post']
        default: 'pre'
    state:
        description:
            - Create, remove, or disable security policy.
        choices: ['present', 'absent', 'disabled']
        default: 'present'
'''

EXAMPLES = '''
- name: Create Prod SSH Inbound policy
  panos_security_policy:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Prod SSH Inbound'
    fromzone: ['untrust']
    tozone: ['trust']
    source: ['any']
    destination: 'Prod-Instances'
    application: ['ssh']
    service: ['application-default']
    action: 'allow'
    tag: ['Prod']
'''

RETURN = '''
# Default return values
'''

try:
    from pandevice import policies
    from pandevice.errors import PanDeviceError

    HAS_PANOS_LIB = True
except ImportError:
    HAS_PANOS_LIB = False

from ansible.module_utils.network.panos import PanOSAnsibleModule

PANOS_SECURITY_RULE_ARGSPEC = {
    'name': dict(type='str', required=True),
    'fromzone': dict(type='list'),
    'tozone': dict(type='list'),
    'source': dict(type='list', default=['any']),
    'destination': dict(type='list', default=['any']),
    'application': dict(type='list', default=['any']),
    'service': dict(type='list', default=['application-default']),
    'category': dict(type='list'),
    'action': dict(
        choices=['deny', 'allow', 'drop', 'reset-client', 'reset-server', 'reset-both'],
        default='allow'
    ),
    'icmp_unreachable': dict(type='bool', default=False),
    'log_setting': dict(type='string'),
    'log_start': dict(type='bool', default=False),
    'log_end': dict(type='bool', default=True),
    'description': dict(type='str'),
    'type': dict(choices=['universal', 'interzone', 'intrazone'], default='universal'),
    'negate_source': dict(type='bool', default=False),
    'negate_destination': dict(type='bool', default=False),
    'schedule': dict(type='str'),
    'disable_server_response_inspection': dict(type='bool', default=False),
    'group': dict(type='str'),
    'virus': dict(type='str'),
    'spyware': dict(type='str'),
    'vulnerability': dict(type='str'),
    'url_filtering': dict(type='str'),
    'file_blocking': dict(type='str'),
    'wildfire_analysis': dict(type='str'),
    'data_filtering': dict(type='str'),
    'negate_target': dict(type='bool', default=False),
    'target': dict(type='list'),
    'tag': dict(type='list'),
    'location': dict(choices=['top', 'bottom', 'before', 'after']),
    'existing_rule': dict(type='str'),
    'device_group': dict(type='str'),
    'panorama_loc': dict(choices=['pre', 'post']),
    'state': dict(default='present', choices=['present', 'absent', 'disabled'])
}

PANOS_SECURITY_RULE_REQUIRED_IF_ARGS = [
    # If 'state' is 'present', require 'fromzone' and 'tozone'.
    ['state', 'present', ['fromzone', 'tozone']],

    # If 'location' is 'before', require 'existing_rule'.
    ['location', 'before', ['existing_rule']],

    # If 'location' is 'after', require 'existing_rule'.
    ['location', 'after', ['existing_rule']],

    # If 'panorama_loc' is 'pre', require 'device_group'.
    ['panorama_loc', 'pre', ['device_group']],

    # If 'panorama_loc' is 'post', require 'device_group'.
    ['panorama_loc', 'post', ['device_group']]
]


def main():
    module = PanOSAnsibleModule(
        argument_spec=PANOS_SECURITY_RULE_ARGSPEC,
        required_if=PANOS_SECURITY_RULE_REQUIRED_IF_ARGS
    )

    name = module.params['name']
    fromzone = module.params['fromzone']
    tozone = module.params['tozone']
    source = module.params['source']
    destination = module.params['destination']
    application = module.params['application']
    service = module.params['service']
    category = module.params['category']
    action = module.params['action']
    log_setting = module.params['log_setting']
    log_start = module.params['log_start']
    log_end = module.params['log_end']
    description = module.params['description']
    type = module.params['type']
    negate_source = module.params['negate_source']
    negate_destination = module.params['negate_destination']
    schedule = module.params['schedule']
    disable_server_response_inspection = module.params['disable_server_response_inspection']
    group = module.params['group']
    virus = module.params['virus']
    spyware = module.params['spyware']
    vulnerability = module.params['vulnerability']
    url_filtering = module.params['url_filtering']
    file_blocking = module.params['file_blocking']
    wildfire_analysis = module.params['wildfire_analysis']
    data_filtering = module.params['data_filtering']
    negate_target = module.params['negate_target']
    target = module.params['target']
    tag = module.params['tag']
    location = module.params['location']
    existing_rule = module.params['existing_rule']
    device_group = module.params['device_group']
    state = module.params['state']

    changed = False

    try:
        if device_group:
            module.device_group = device_group

            if module.params['panorama_loc'] == 'post':
                module.rulebase = policies.PostRulebase

        if state == 'present':
            new_obj = policies.SecurityRule(
                name=name, fromzone=fromzone, tozone=tozone, source=source,
                destination=destination, application=application, service=service,
                category=category, action=action, log_setting=log_setting, log_start=log_start,
                log_end=log_end, description=description, type=type, negate_source=negate_source,
                negate_destination=negate_destination, schedule=schedule,
                disable_server_response_inspection=disable_server_response_inspection,
                group=group, virus=virus, spyware=spyware, vulnerability=vulnerability,
                url_filtering=url_filtering, file_blocking=file_blocking,
                wildfire_analysis=wildfire_analysis, data_filtering=data_filtering,
                tag=tag
            )

            # ICMP Unreachable only applies if we're dropping the traffic or sending resets.
            # if action in ['drop', 'reset-client', 'reset-server', 'reset-both']:
            #     new_obj.icmp_unreachable = module.params['icmp_unreachable']

            # Target and negate target only apply if we're talking to Panorama.
            if device_group:
                new_obj.negate_target = negate_target
                new_obj.target = target

            changed = module.create_or_update_rule(
                name, policies.SecurityRule, new_obj, location=location,
                existing_rule_name=existing_rule
            )

        elif state == 'absent':
            changed = module.delete_rule(name, policies.SecurityRule)

        elif state == 'disabled':
            changed = module.disable_rule(name, policies.SecurityRule)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
