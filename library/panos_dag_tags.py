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
module: panos_dag_tags
short_description: Create tags for DAG's on PAN-OS devices.
description:
    - Create the ip address to tag associations. Tags will in turn be used to create DAG's
author: "Vinay Venkataraghavan @vinayvenkat"
version_added: "2.4"
requirements:
    - pan-python
    - pan-device
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
        default: null
    password:
        description:
            - password for authentication
        required: true
        default: null
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    description:
        description:
            - The purpose / objective of the static Address Group
        required: false
        default: null
    commit:
        description:
            - commit if changed
        required: false
        default: true
    
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule, get_exception

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import objects

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, panorama.DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def register_ip_to_tag_map(device, ip_addresses, tag):
    """
    
    :param device: 
    :param ip_addresses: 
    :param tag: 
    :return: 
    """

    exc = None
    try:
        device.userid.register(ip_addresses, tag)
    except Exception, e:
            exc = get_exception()

    if exc:
        return (False, exc)
    else:
        return (True, exc)

def get_all_address_group_mapping(device):
    """
    Retrieve all the tag to IP address mappings
    :param device: 
    :return: 
    """
    exc = None
    ret = None
    try:
        ret = device.userid.get_registered_ip()
    except Exception, e:
        exc = get_exception()

    if exc:
        return (False, exc)
    else:
        return (ret, exc)

def delete_address_from_mapping(device, ip_address, tags):
    """
    Delete an IP address from a tag mapping. 
    :param device: 
    :param ip_address:
    :param tags: 
    :return: 
    """

    exc = None
    try:
        ret = device.userid.unregister(ip_address, tags)
    except Exception, e:
        exc = get_exception()

    if exc:
        return (False, exc)
    else:
        return (True, exc)

def main():

    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        devicegroup=dict(default=None),
        description=dict(default=None),
        ip_to_register=dict(type='str', required=False),
        tag_names=dict(type='list', required=True),
        commit=dict(type='bool', default=True),
        operation=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    api_key = module.params['api_key']
    commit = module.params['commit']
    devicegroup = module.params['devicegroup']
    operation = module.params['operation']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    result = None
    if operation == 'add':
        result, exc = register_ip_to_tag_map(device,
                               ip_addresses=module.params.get('ip_to_register', None),
                               tag=module.params.get('tag_names', None)
                      )
    elif operation == 'list':
        result, exc = get_all_address_group_mapping(device)
    elif operation == 'delete':
        result, exc = delete_address_from_mapping(device,
                                                  ip_address=module.params.get('ip_to_register', None),
                                                  tags=module.params.get('tag_names', [])
                      )
    else:
        module.fail_json(msg="Unsupported option")

    if not result:
        module.fail_json(msg=exc)

    if commit:
        try:
            device.commit(sync=True)
        except Exception, e:
            module.fail_json(get_exception())

    module.exit_json(changed=True, msg=result)

if __name__ == "__main__":
    main()