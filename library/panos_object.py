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
module: panos_search_address
short_description: retrieve address object or address group
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
- name: search for shared address object
  panos_searchobject:
    ip_address: '10.0.0.1'
    username: 'admin'
    password: 'paloalto'
    address: 'DevNet'

- name: search for devicegroup address object
  panos_searchobject:
    ip_address: '10.0.0.1'
    password: 'paloalto'
    object: 'DevNet'
    address: 'DeviceGroupA'
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


def find_object(device, dev_group, obj_name, obj_type):
    # Get the firewall objects
    obj_type.refreshall(device)
    if isinstance(device, pandevice.firewall.Firewall):
        addr = device.find(obj_name, obj_type)
        return addr
    elif isinstance(device, pandevice.panorama.Panorama):
        addr = device.find(obj_name, obj_type)
        if addr is None:
            if dev_group:
                device.add(dev_group)
                obj_type.refreshall(dev_group)
                addr = dev_group.find(obj_name, obj_type)
        return addr
    else:
        return False

def create_object(**kwargs):
    if kwargs['addressobject']:
        newobject = objects.AddressObject(
            name=kwargs['addressobject'],
            value=kwargs['address'],
            type=kwargs['address_type'],
            description=kwargs['description'],
            tag=kwargs['tag']
        )
        if newobject.type and newobject.value:
            return newobject
        else:
            return False
    elif kwargs['addressgroup']:
        newobject = objects.AddressGroup(
            name=kwargs['addressgroup'],
            static_value=kwargs['static_value'],
            dynamic_value=kwargs['dynamic_value'],
            description=kwargs['description'],
            tag=kwargs['tag']
        )
        if newobject.static_value or newobject.dynamic_value:
            return newobject
        else:
            return False
    elif kwargs['serviceobject']:
        newobject = objects.ServiceObject(
            name=kwargs['serviceobject'],
            protocol=kwargs['protocol'],
            source_port=kwargs['source_port'],
            destination_port=kwargs['destination_port'],
            tag=kwargs['tag']
        )
        if newobject.protocol and newobject.destination_port:
            return newobject
        else:
            return False
    elif kwargs['servicegroup']:
        newobject = objects.ServiceGroup(
            name=kwargs['servicegroup'],
            value=kwargs['services'],
            tag=kwargs['tag']
        )
        if newobject.value:
            return newobject
        else:
            return False
    else:
        return False


def add_object(device, dev_group, new_object):
    if dev_group:
        dev_group.add(new_object)
    else:
        device.add(new_object)
    new_object.create()
    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        action=dict(required=True, choices=['add', 'delete', 'find']),
        addressobject=dict(default=None),
        addressgroup=dict(default=None),
        serviceobject=dict(default=None),
        servicegroup=dict(default=None),
        address=dict(default=None),
        address_type=dict(default='ip-netmask', choices=['ip-netmask', 'ip-range', 'fqdn']),
        static_value=dict(type='list', default=None),
        dynamic_value=dict(default=None),
        protocol=dict(default=None, choices=['tcp', 'udp']),
        source_port=dict(default=None),
        destination_port=dict(default=None),
        services=dict(type='list', default=None),
        description=dict(default=None),
        tag=dict(type='list', default=None),
        devicegroup=dict(default=None)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']],
                           mutually_exclusive=[['addressobject', 'addressgroup',
                                                'serviceobject', 'servicegroup',
                                                'tag']]
                           )
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    action = module.params['action']
    addressobject = module.params['addressobject']
    addressgroup = module.params['addressgroup']
    serviceobject = module.params['serviceobject']
    servicegroup = module.params['servicegroup']
    address = module.params['address']
    address_type = module.params['address_type']
    static_value = module.params['static_value']
    dynamic_value = module.params['dynamic_value']
    protocol = module.params['protocol']
    source_port = module.params['source_port']
    destination_port = module.params['destination_port']
    services = module.params['services']
    description = module.params['description']
    tag = module.params['tag']
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

    # What type of object are we talking about?
    if addressobject:
        obj_name = addressobject
        obj_type = objects.AddressObject
    elif addressgroup:
        obj_name = addressgroup
        obj_type = objects.AddressGroup
    elif serviceobject:
        obj_name = serviceobject
        obj_type = objects.ServiceObject
    elif servicegroup:
        obj_name = servicegroup
        obj_type = objects.ServiceGroup
    elif tag:
        obj_name = tag
        obj_type = objects.Tag
    else:
        module.fail_json(msg='No object type defined!')

    # Which action shall we take on the object?
    if action == "find":
        # Search for the object
        match = find_object(device, dev_group, obj_name, obj_type)

        # If found, format and return the result
        if match:
            match_dict = xmltodict.parse(match.element_str())
            module.exit_json(
                stdout_lines=json.dumps(match_dict, indent=2),
                msg='Object matched'
            )
        else:
            module.fail_json(msg='Object \'%s\' not found. Is the name correct?' % obj_name)
    elif action == "delete":
        # Search for the object
        match = find_object(device, dev_group, obj_name, obj_type)

        # If found, delete it
        if match:
            try:
                match.delete()
            except PanXapiError:
                exc = get_exception()
                module.fail_json(msg=exc.message)

            module.exit_json(changed=True, msg='Object \'%s\' successfully deleted' % obj_name)
        else:
            module.fail_json(msg='Object \'%s\' not found. Is the name correct?' % obj_name)
    elif action == "add":
        try:
            new_object = create_object(
                addressobject = addressobject,
                addressgroup = addressgroup,
                serviceobject = serviceobject,
                servicegroup = servicegroup,
                address = address,
                address_type = address_type,
                static_value = static_value,
                dynamic_value = dynamic_value,
                protocol = protocol,
                source_port = source_port,
                destination_port = destination_port,
                services = services,
                description = description,
                tag = tag
            )
            changed = add_object(device, dev_group, new_object)
        except PanXapiError:
            exc = get_exception()
            module.fail_json(msg=exc.message)
        module.exit_json(changed=changed, msg="Object \'%s\' successfully added" % obj_name)
    else:
        module.fail_json(msg='Invalid action')

if __name__ == '__main__':
    main()
