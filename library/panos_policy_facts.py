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
module: panos_policy_facts
short_description: Retrieve facts about policies on PAN-OS devices.
description:
    - Retrieves information about policies on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
    - xmltodict can be obtained from PyPi U(https://pypi.python.org/pypi/xmltodict)
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
            - Name of the rule to retrieve.
        required: true
    type:
        description:
            - Type of rule to retrieve.
        choices: ['security', 'nat']
        default: 'security'
        required: true
    device_group:
        description:
            - If I(ip_address) is a Panorama device, look for policy in this device group.
        type: str
    panorama_loc:
        description:
            - If I(ip_address) is a Panorama device and I(device_group) is specified, look for
              policy in either the pre or post rules.
        choices: ['pre', 'post']
        default: 'pre'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos import PanOSAnsibleModule

try:
    from pandevice import policies
    from pandevice.errors import PanDeviceError

    HAS_PANOS_LIB = True
except ImportError:
    HAS_PANOS_LIB = False

try:
    import xmltodict

    HAS_XMLTODICT_LIB = True
except ImportError:
    HAS_XMLTODICT_LIB = False


PANOS_POLICY_FACTS_ARGSPEC = {
    'name': dict(type='str', required=True),
    'type': dict(choices=['security', 'nat'], required=True),
    'device_group': dict(type='str'),
    'panorama_loc': dict(choices=['pre', 'post'])
}

PANOS_POLICY_FACTS_REQUIRED_IF_ARGS = [
    # If 'panorama_loc' is 'pre', require 'device_group'.
    ['panorama_loc', 'pre', ['device_group']],

    # If 'panorama_loc' is 'post', require 'device_group'.
    ['panorama_loc', 'post', ['device_group']]
]


def main():
    module = PanOSAnsibleModule(
        argument_spec=PANOS_POLICY_FACTS_ARGSPEC,
        required_if=PANOS_POLICY_FACTS_REQUIRED_IF_ARGS
    )

    name = module.params['name']
    type = module.params['type']
    device_group = module.params['device_group']
    panorama_loc = module.params['panorama_loc']

    results = {}

    if not HAS_XMLTODICT_LIB:
        module.fail_json(msg='xmltodict is required for this module.')

    try:
        rule = None
        rule_type = None

        if device_group:
            module.device_group = device_group

            if panorama_loc == 'post':
                module.rulebase = policies.PostRulebase

        if type == 'security':
            rule_type = policies.SecurityRule
        elif type == 'nat':
            rule_type = policies.NatRule

        rule = module.find_rule(name, rule_type)

        if rule:
            results = xmltodict.parse(rule.element_str())

        module.exit_json(changed=False, results=results)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
