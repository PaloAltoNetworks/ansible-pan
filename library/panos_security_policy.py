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
module: panos_security_policy
short_description: Create security policies on PAN-OS devices.
description:
    - Create security policies on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is not supported.
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
    state:
        description:
            - Create, remove, or disable security policy.
        choices: ['present', 'absent', 'disabled']
        default: 'present'
'''

EXAMPLES = '''

'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import policies
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_rulebase(device, devicegroup=None):
    if isinstance(device, firewall.Firewall):
        rulebase = policies.Rulebase()
        device.add(rulebase)
    else:
        return None

    policies.SecurityRule.refreshall(rulebase)
    return rulebase


def find_rule_index(rulebase, rule_name):
    if rulebase:
        for num, child in enumerate(rulebase.children):
            if rule_name == child.name:
                return num
    return -1


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        name=dict(type='str', required=True),
        fromzone=dict(type='list'),
        tozone=dict(type='list'),
        source=dict(type='list', default=['any']),
        destination=dict(type='list', default=['any']),
        application=dict(type='list', default=['any']),
        service=dict(type='list', default=['application-default']),
        category=dict(type='list'),
        action=dict(
            choices=['deny', 'allow', 'drop', 'reset-client', 'reset-server', 'reset-both'],
            default='allow'
        ),
        log_setting=dict(type='string'),
        log_start=dict(type='bool', default=False),
        log_end=dict(type='bool', default=True),
        description=dict(type='str'),
        type=dict(choices=['universal', 'interzone', 'intrazone'], default='universal'),
        negate_source=dict(type='bool', default=False),
        negate_destination=dict(type='bool', default=False),
        schedule=dict(type='str'),
        disable_server_response_inspection=dict(type='bool', default=False),
        group=dict(type='str'),
        virus=dict(type='str'),
        spyware=dict(type='str'),
        vulnerability=dict(type='str'),
        url_filtering=dict(type='str'),
        file_blocking=dict(type='str'),
        wildfire_analysis=dict(type='str'),
        data_filtering=dict(type='str'),
        negate_target=dict(type='bool', default=False),
        target=dict(type='list'),
        tag=dict(type='list'),
        location=dict(choices=['top', 'bottom', 'before', 'after']),
        existing_rule=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent', 'disabled'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
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
    state = module.params['state']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        rulebase = get_rulebase(device)
        existing_obj = rulebase.find(name, policies.SecurityRule)

        if state == 'present':
            if not fromzone or not tozone:
                module.fail_json(msg='Must specify \'fromzone\' and \'tozone\' if \'state\' is \''
                                 'present\'.')

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

            # TODO: icmp_unreachable special handling

            # TODO: negate_target and target special handling (Panorama)

            if ((location == 'before') or (location == 'after')) and not existing_rule:
                module.fail_json(msg='Must specify \'existing_rule\' if \'location\' is '
                                 '\'before\' or \'after\'.')

            # Default is to add the rule at the bottom of the rulebase.
            new_rule_index = len(rulebase.children)

            if (location == 'before') or (location == 'after'):
                new_rule_index = find_rule_index(rulebase, existing_rule)

                if new_rule_index < 0:
                    module.fail_json(msg='Existing rule \'%s\' does not exist.' % existing_rule)

                if location == 'after':
                    new_rule_index = new_rule_index + 1

            elif location == 'top':
                new_rule_index = 0

            if not existing_obj:
                rulebase.insert(new_rule_index, new_obj)
                new_obj.create()
                rulebase.apply()
                changed = True

            elif not existing_obj.equal(new_obj):
                for param in new_obj._params:
                    setattr(existing_obj, param.name, getattr(new_obj, param.name))
                existing_obj.apply()
                rulebase.apply()
                changed = True

            # If we need to change the rule positioning for any reason, do it here.
            if location and new_rule_index != find_rule_index(rulebase, new_obj.name):
                rulebase.insert(new_rule_index, new_obj)
                new_obj.create()
                existing_obj.delete()
                rulebase.apply()
                changed = True

        elif state == 'absent' and existing_obj:
            existing_obj.delete()
            rulebase.apply()
            changed = True

        elif state == 'disabled' and existing_obj:
            existing_obj.disabled = True
            existing_obj.apply()
            changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
