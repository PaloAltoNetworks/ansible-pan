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
module: panos_static_route
short_description: Create static routes on PAN-OS devices.
description:
    - Create static routes on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is not supported.
    - IPv6 is not supported.
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
            - Name of static route.
        required: true
    destination:
        description:
            - Destination network.  Required if I(state) is I(present).
    nexthop_type:
        description:
            - Type of next hop.
        choices: ['ip-address', 'discard']
        default: 'ip-address'
    nexthop:
        description:
            - Next hop IP address.  Required if I(state) is I(present).
    admin_dist:
        description:
            - Administrative distance for static route.
    metric:
        description:
            - Metric for route.
        default: '10'
    virtual_router:
        description:
            - Virtual router to use.
        default: 'default'
    interface:
        description:
            - The Interface to use.
    state:
        description:
            - Create or remove static route.
        choices: ['present', 'absent']
        default: 'present'
'''

EXAMPLES = '''
- name: Create route 'Test-One'
  panos_static_route:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-One'
    destination: '1.1.1.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Two'
  panos_static_route:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Two'
    destination: '2.2.2.0/24'
    nexthop: '10.0.0.1'

- name: Create route 'Test-Three'
  panos_static_route:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Three'
    destination: '3.3.3.0/24'
    nexthop: '10.0.0.1'

- name: Delete route 'Test-Two'
  panos_static_route:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Two'
    state: 'absent'

- name: Create route 'Test-Four'
  panos_static_route:
    ip_address: '{{ fw_ip_address }}'
    username: '{{ fw_username }}'
    password: '{{ fw_password }}'
    name: 'Test-Four'
    destination: '4.4.4.0/24'
    nexthop: '10.0.0.1'
    virtual_router: 'VR-Two'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import network
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def find_object(device, obj_name, obj_type):
    obj_type.refreshall(device)

    if isinstance(device, firewall.Firewall):
        return device.find(obj_name, obj_type)
    else:
        return None


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        name=dict(type='str', required=True),
        destination=dict(type='str'),
        nexthop_type=dict(default='ip-address', choices=['ip-address', 'discard']),
        nexthop=dict(type='str'),
        admin_dist=dict(type='str'),
        metric=dict(default='10'),
        virtual_router=dict(default='default'),
        interface=dict(type='str'),
        state=dict(default='present', choices=['present', 'absent'])
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_LIB:
        module.fail_json(msg='pan-python and pandevice are required for this module.')

    ip_address = module.params['ip_address']
    username = module.params['username']
    password = module.params['password']
    api_key = module.params['api_key']
    name = module.params['name']
    destination = module.params['destination']
    nexthop_type = module.params['nexthop_type']
    nexthop = module.params['nexthop']
    admin_dist = module.params['admin_dist']
    metric = module.params['metric']
    virtual_router = module.params['virtual_router']
    state = module.params['state']
    interface = module.params['interface']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)
        network.VirtualRouter.refreshall(device)
        vr = device.find(virtual_router, network.VirtualRouter)

        if state == 'present':
            if not destination and not nexthop:
                module.fail_json(msg='Must specify \'destination\' and \'nexthop\' if state is \'present\'.')

            existing_route = vr.find(name, network.StaticRoute)
            new_route = network.StaticRoute(name, destination, nexthop=nexthop,
                                            nexthop_type=nexthop_type, admin_dist=admin_dist,
                                            metric=metric, interface=interface)

            if not existing_route:
                vr.add(new_route)
                new_route.create()
                changed = True
            elif not existing_route.equal(new_route):
                existing_route.destination = destination
                existing_route.nexthop = nexthop
                existing_route.nexthop_type = nexthop_type
                existing_route.admin_dist = admin_dist
                existing_route.metric = metric
                existing_route.interface = interface
                existing_route.apply()
                changed = True

        elif state == 'absent':
            existing_route = vr.find(name, network.StaticRoute)

            if existing_route:
                existing_route.delete()
                changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
