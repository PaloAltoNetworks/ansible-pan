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

DOCUMENTATION = '''
---
module: panos_nat_rule
short_description: create a policy NAT rule
description:
    - Create a policy nat rule. Keep in mind that we can either end up configuring source NAT, destination NAT, or both. Instead of splitting it into two we will make a fair attempt to determine which one the user wants.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Robert Hagen (@rnh556)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported.
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
            - name of the SNAT rule
        required: true
    source_zone:
        description:
            - list of source zones
        required: true
    destination_zone:
        description:
            - destination zone
        required: true
    source_ip:
        description:
            - list of source addresses
        required: false
        default: ["any"]
    destination_ip:
        description:
            - list of destination addresses
        required: false
        default: ["any"]
    service:
        description:
            - service
        required: false
        default: "any"
    snat_type:
        description:
            - type of source translation
        required: false
        default: None
    snat_address:
        description:
            - snat translated address
        required: false
        default: None
    snat_interface:
        description:
            - snat interface
        required: false
        default: None
    snat_interface_address:
        description:
            - snat interface address
        required: false
        default: None
    snat_bidirectional:
        description:
            - bidirectional flag
        required: false
        default: "false"
    dnat_address:
        description:
            - dnat translated address
        required: false
        default: None
    dnat_port:
        description:
            - dnat translated port
        required: false
        default: None
    override:
        description:
            - attempt to override rule if one with the same name already exists
        required: false
        default: "false"
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# Create a source and destination nat rule
  - name: create nat SSH221 rule for 10.0.1.101
    panos_nat_rule:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      rule_name: "Web SSH"
      from_zone: ["external"]
      to_zone: "external"
      source: ["any"]
      destination: ["10.0.0.100"]
      service: "service-tcp-221"
      snat_type: "dynamic-ip-and-port"
      snat_interface: "ethernet1/2"
      dnat_address: "10.0.1.101"
      dnat_port: "22"
      commit: False
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
    import pandevice
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import objects
    from pandevice import policies
    import xmltodict
    import json

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, pandevice.panorama.DeviceGroup):
            if group.name == devicegroup:
                return group
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
    policies.NatRule.refreshall(rulebase)
    return rulebase


def find_rule(rulebase, rule_name):
    # Search for the rule name
    rule = rulebase.find(rule_name)
    if rule:
        return rule
    else:
        return False


def create_nat_rule(**kwargs):
    nat_rule = policies.NatRule(
        name=kwargs['rule_name'],
        description=kwargs['description'],
        fromzone=kwargs['source_zone'],
        source=kwargs['source_ip'],
        tozone=kwargs['destination_zone'],
        destination=kwargs['destination_ip'],
        service=kwargs['service'],
        to_interface=kwargs['to_interface'],
        nat_type=kwargs['nat_type']
    )

    # Source translation: Static IP
    if kwargs['snat_type'] in ['static-ip'] and kwargs['snat_static_address']:
        nat_rule.source_translation_type = kwargs['snat_type']
        nat_rule.source_translation_static_translated_address = kwargs['snat_static_address']
        # Bi-directional flag set?
        if kwargs['snat_bidirectional']:
            nat_rule.source_translation_static_bi_directional = kwargs['snat_bidirectional']

    # Source translation: Dynamic IP and port
    elif kwargs['snat_type'] in ['dynamic-ip-and-port']:
        nat_rule.source_translation_type = kwargs['snat_type']
        # Interface address?
        if kwargs['snat_interface']:
            nat_rule.source_translation_interface = kwargs['snat_interface']
            # Interface IP?
            if kwargs['snat_interface_address']:
                nat_rule.source_translation_ip_address = kwargs['snat_interface_address']
        else:
            nat_rule.source_translation_translated_addresses = kwargs['snat_dynamic_address']

    # Source translation: Dynamic IP
    elif kwargs['snat_type'] in ['dynamic-ip']:
        if kwargs['snat_dynamic_address']:
            nat_rule.source_translation_type = kwargs['snat_type']
            nat_rule.source_translation_translated_addresses = kwargs['snat_dynamic_address']
        else:
            return False

    # Destination translation
    if kwargs['dnat_address']:
        nat_rule.destination_translated_address = kwargs['dnat_address']
        if kwargs['dnat_port']:
            nat_rule.destination_translated_port = kwargs['dnat_port']

    # Any tags?
    if 'tag_name' in kwargs:
        nat_rule.tag = kwargs['tag_name']

    return nat_rule


def add_rule(rulebase, nat_rule):
    if rulebase:
        rulebase.add(nat_rule)
        nat_rule.create()
        return True
    else:
        return False


def update_rule(rulebase, nat_rule):
    if rulebase:
        rulebase.add(nat_rule)
        nat_rule.apply()
        return True
    else:
        return False

def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(required=True, no_log=True),
        api_key=dict(no_log=True),
        operation=dict(required=True, choices=['add','update','delete','find']),
        rule_name=dict(required=True),
        description=dict(),
        tag_name=dict(),
        source_zone=dict(type='list', required=True),
        source_ip=dict(type='list', default=['any']),
        destination_zone=dict(required=True),
        destination_ip=dict(type='list', default=['any']),
        service=dict(default='any'),
        to_interface=dict(default='any'),
        snat_type=dict(choices=['static-ip','dynamic-ip-and-port','dynamic-ip']),
        snat_static_address=dict(),
        snat_dynamic_addresses=dict(type='list'),
        snat_interface=dict(),
        snat_interface_address=dict(),
        snat_bidirectional=dict(type='bool', default=False),
        dnat_address=dict(),
        dnat_port=dict(),
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
    operation = module.params['operation']
    rule_name = module.params['rule_name']
    description = module.params['description']
    tag_name = module.params['tag_name']
    source_zone = module.params['source_zone']
    source_ip = module.params['source_ip']
    destination_zone = module.params['destination_zone']
    destination_ip = module.params['destination_ip']
    service = module.params['service']
    to_interface = module.params['to_interface']
    nat_type = 'ipv4'
    snat_type = module.params['snat_type']
    snat_static_address = module.params['snat_static_address']
    snat_dynamic_address = module.params['snat_dynamic_address']
    snat_interface = module.params['snat_interface']
    snat_interface_address = module.params['snat_interface_address']
    snat_bidirectional = module.params['snat_bidirectional']
    dnat_address = module.params['dnat_address']
    dnat_port = module.params['dnat_port']
    devicegroup = module.params['devicegroup']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(
                failed=1,
                msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup
            )

    # Get the rulebase
    rulebase = get_rulebase(device, dev_group)

    # Which action shall we take on the object?
    if operation == "find":
        # Search for the rule
        match = find_rule(rulebase, rule_name)
        # If found, format and return the result
        if match:
            match_dict = xmltodict.parse(match.element_str())
            module.exit_json(
                stdout_lines=json.dumps(match_dict, indent=2),
                msg='Rule matched'
            )
        else:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % rule_name)
    elif operation == "delete":
        # Search for the object
        match = find_rule(rulebase, rule_name)
        # If found, delete it
        if match:
            try:
                match.delete()
            except PanXapiError:
                exc = get_exception()
                module.fail_json(msg=exc.message)

            module.exit_json(changed=True, msg='Rule \'%s\' successfully deleted.' % rule_name)
        else:
            module.fail_json(msg='Rule \'%s\' not found. Is the name correct?' % rule_name)
    elif operation == "add":
        # Search for the rule. Fail if found.
        match = find_rule(rulebase, rule_name)
        if match:
            module.fail_json(msg='Rule already exists. Use operation: \'update\' to change rule.')
        else:
            try:
                new_rule = create_nat_rule(
                    rule_name=rule_name,
                    description=description,
                    tag_name=tag_name,
                    source_zone=source_zone,
                    destination_zone=destination_zone,
                    source_ip=source_ip,
                    destination_ip=destination_ip,
                    service=service,
                    to_interface=to_interface,
                    nat_type=nat_type,
                    snat_type=snat_type,
                    snat_static_address=snat_static_address,
                    snat_dynamic_address=snat_dynamic_address,
                    snat_interface=snat_interface,
                    snat_interface_address=snat_interface_address,
                    snat_bidirectional=snat_bidirectional,
                    dnat_address=dnat_address,
                    dnat_port=dnat_port
                )
                changed = add_rule(rulebase, new_rule)
            except PanXapiError:
                exc = get_exception()
                module.fail_json(msg=exc.message)
            module.exit_json(changed=changed, msg="Rule \'%s\' successfully added." % rule_name)
    elif operation == 'update':
        # Search for the rule. Update if found.
        match = find_rule(rulebase, rule_name)
        if match:
            try:
                new_rule = create_nat_rule(
                    rule_name=rule_name,
                    description=description,
                    tag_name=tag_name,
                    source_zone=source_zone,
                    destination_zone=destination_zone,
                    source_ip=source_ip,
                    destination_ip=destination_ip,
                    service=service,
                    to_interface=to_interface,
                    nat_type=nat_type,
                    snat_type=snat_type,
                    snat_static_address=snat_static_address,
                    snat_dynamic_address=snat_dynamic_address,
                    snat_interface=snat_interface,
                    snat_interface_address=snat_interface_address,
                    snat_bidirectional=snat_bidirectional,
                    dnat_address=dnat_address,
                    dnat_port=dnat_port
                )
                changed = update_rule(rulebase, new_rule)
            except PanXapiError:
                exc = get_exception()
                module.fail_json(msg=exc.message)
            module.exit_json(changed=changed, msg="Rule \'%s\' successfully updated." % rule_name)
        else:
            module.fail_json(msg='Rule does not exist. Use operation: \'add\' to add rule.')


if __name__ == '__main__':
    main()

