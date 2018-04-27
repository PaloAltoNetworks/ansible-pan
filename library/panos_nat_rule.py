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
module: panos_nat_rules
short_description: Create NAT rules on PAN-OS devices.
description:
    - Create NAT rules on PAN-OS devices.
author: "Luigi Mori (@jtschichold),Ivan Bojer (@ivanbojer),Robert Hagen (@rnh556),Michael Richardson (@mrichardson03)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Check mode is not supported.
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
            - Name of NAT policy.
        required: true
    description:
        description:
            - Description of NAT policy.
    nat_type:
        description:
            - Type of NAT.
        choices: ['ipv4', 'nat64', 'npt6']
        default: 'ipv4'
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
    source_translation_type:
        description:
            - Type of source address translation
        type: str
        choices: ['dynamic-ip', 'dynamic-ip-and-port', 'static-ip']
    source_translation_address_type:
        description:
            - Address type for Dynamic IP and Port or Dynamic IP source translation types.
        type: str
    source_translation_interface:
        description:
            - Interface of the source address translation for Dynamic IP and Port or Dynamic IP
              source translation types.
        type: str
    source_translation_ip_address:
        description:
            - IP address of the source address translation for Dynamic IP and Port or Dynamic IP
              source translation types.
        type: str
    source_translation_translated_addresses:
        description:
            - Translated addresses of the source address translation for Dynamic IP and Port or
              Dynamic IP source translation types.
        type: list
    source_translation_fallback_type:
        description:
            - Type of fallback for Dynamic IP source translation types.
        choices: ['interface-address', 'translated-address']
    source_translation_fallback_translated_addresses:
        description:
            - Fallback translated addresses for Dynamic IP source translation.
    source_translation_fallback_interface:
        description:
            - Fallback interface for Dynamic IP source translation.
        type: str
    source_translation_fallback_ip_type:
        description:
            - The type of the IP address for the fallback source translation IP address.
        type: str
    source_translation_fallback_ip_address:
        description:
            - The IP address of the fallback source translation
        type: str
    source_translation_static_translated_address:
        description:
            - The IP address of for the static source translation.
        type: str
    source_translation_static_bi_directional:
        description:
            - Allow reverse translation from translated address to original address
        type: bool
    destination_translated_address:
        description:
            - Translated destination IP address
        type: str
    destination_translated_port:
        description:
            - Translated destination port number
        type: int
        description:
            - List of tags to add to this NAT policy.
        type: list
    ha_binding:
        description:
            - Device binding configuration in HA Active-Active mode
    negate_target:
        description:
            - Target all but the listed target firewalls.  (Applies to Panorama/device groups
              only.)
        type: bool
    target:
        description:
            - Apply this policy to the listed firewalls only.  (Applies to Panorama/device groups
              only).
    location:
        description:
            - Position to place the created rule in the rule base.
        choices: ['top', 'bottom', 'before', 'after']
        default: 'bottom'
    existing_rule:
        description:
            - If 'location' is set to 'before' or 'after', this option specifies an existing
              rule name.  The new rule will be created in the specified position relative to this
              rule.  If 'location' is set to 'before' or 'after', this option is required.
        type: str
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
            - Create, remove, or disable NAT policy.
        choices: ['present', 'absent', 'disabled']
        default: 'present'
'''

EXAMPLES = '''
- name: Create Outbound NAT rule
  panos_nat_rule:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Outbound'
    fromzone: ['trust']
    tozone: ['untrust']
    source_translation_type: 'dynamic-ip-and-port'
    source_translation_address_type: 'translated-address'
    source_translation_translated_addresses: ['10.0.0.1']
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

PANOS_NAT_RULE_ARGSPEC = {
    'name': dict(type='str', required=True),
    'description': dict(type='str'),
    'type': dict(default='ipv4', choices=['ipv4', 'nat64', 'nptv6']),
    'fromzone': dict(type='list'),
    'tozone': dict(type='list'),
    'source': dict(type='list', default=['any']),
    'destination': dict(type='list', default=['any']),
    'source_translation_type': dict(choices=['dynamic-ip', 'dynamic-ip-and-port', 'static-ip']),
    'source_translation_address_type': dict(type='str'),
    'source_translation_interface': dict(type='str'),
    'source_translation_ip_address': dict(type='str'),
    'source_translation_translated_addresses': dict(type='list'),
    'source_translation_fallback_type': dict(choices=['interface-address', 'translated-address']),
    'source_translation_fallback_translated_addresses': dict(type='list'),
    'source_translation_fallback_interface': dict(type='str'),
    'source_translation_fallback_ip_type': dict(type='str'),
    'source_translation_fallback_ip_address': dict(type='str'),
    'source_translation_static_translated_address': dict(type='str'),
    'source_translation_static_bi_directional': dict(type='bool'),
    'destination_translated_address': dict(type='str'),
    'destination_translated_port': dict(type='int'),
    'ha_binding': dict(type='str'),
    'negate_target': dict(type='bool'),
    'target': dict(type='list'),
    'tag': dict(type='list'),
    'location': dict(default='bottom', choices=['top', 'bottom', 'before', 'after']),
    'existing_rule': dict(type='str'),
    'device_group': dict(type='str'),
    'panorama_loc': dict(choices=['pre', 'post']),
    'state': dict(default='present', choices=['present', 'absent', 'disabled'])
}

PANOS_NAT_RULE_REQUIRED_IF_ARGS = [
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


def create_nat_rule(params):
    new_rule = policies.NatRule(
        name=params['name'],
        description=params['description'],
        nat_type=params['type'],
        fromzone=params['fromzone'],
        tozone=params['tozone'],
        source=params['source'],
        destination=params['destination'],
        source_translation_type=params['source_translation_type'],
        source_translation_address_type=params['source_translation_address_type'],
        source_translation_interface=params['source_translation_interface'],
        source_translation_ip_address=params['source_translation_ip_address'],
        source_translation_translated_addresses=params['source_translation_translated_addresses'],
        source_translation_fallback_type=params['source_translation_fallback_type'],
        source_translation_fallback_translated_addresses=params['source_translation_fallback_translated_addresses'],
        source_translation_fallback_interface=params['source_translation_fallback_interface'],
        source_translation_fallback_ip_type=params['source_translation_fallback_ip_type'],
        source_translation_fallback_ip_address=params['source_translation_fallback_ip_address'],
        source_translation_static_translated_address=params['source_translation_static_translated_address'],
        source_translation_static_bi_directional=params['source_translation_static_bi_directional'],
        destination_translated_address=params['destination_translated_address'],
        destination_translated_port=params['destination_translated_port'],
        ha_binding=params['ha_binding'],
        tag=params['tag']
    )

    return new_rule


def main():
    module = PanOSAnsibleModule(
        argument_spec=PANOS_NAT_RULE_ARGSPEC,
        required_if=PANOS_NAT_RULE_REQUIRED_IF_ARGS
    )

    changed = False

    name = module.params['name']
    location = module.params['location']
    existing_rule = module.params['existing_rule']
    device_group = module.params['device_group']
    state = module.params['state']

    try:
        if device_group:
            module.device_group = device_group

            if module.params['panorama_loc'] == 'post':
                module.rulebase = policies.PostRulebase

        if state == 'present':
            new_obj = create_nat_rule(module.params)

            # Target and negate target only apply if we're talking to Panorama.
            if device_group:
                new_obj.negate_target = module.params['negate_target']
                new_obj.target = module.params['target']

            changed = module.create_or_update_rule(
                name, policies.NatRule, new_obj, location=location,
                existing_rule_name=existing_rule
            )

        elif state == 'absent':
            changed = module.delete_rule(name, policies.NatRule)

        elif state == 'disabled':
            changed = module.disable_rule(name, policies.NatRule)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
