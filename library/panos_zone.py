#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

DOCUMENTATION = '''
---
module: panos_zone
short_description: configure security zone
description:
    - Configure security zones on PAN-OS firewall or in Panorama template.
author: "Robert Hagen (@stealthllama)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
note:
    - Check mode is supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    zone:
        description:
            - Name of the security zone to configure.
        required: true
    mode:
        description:
            - The mode of the security zone. Must match the mode of the interface.
            - Possible values I(tap)/I(virtual-wire)/I(layer2)/I(layer3)/I(external)
        default: "layer3"
    interface:
        description:
            - List of member interfaces.
    zone_profile:
        description:
            - Zone protection profile.
    log_setting:
        description:
            - Log forwarding setting.
    enable_userid:
        description:
            - Enable user identification.
    include_acl:
        description:
            - User identification ACL include list.
    exclude_acl:
        description:
            - User identification ACL exclude list.
    vsys:
        description:
            - The firewall VSYS in which to create the zone.
        default: "vsys1"
    template:
        description:
            - The Panorama template in which to create the zone.
    state:
        description:
            - The state of the zone.
            - Possible values I(present)/I(absent).
'''

EXAMPLES = '''
# Create an L3 zone.
- name: create DMZ zone on a firewall
  panos_zone:
    ip_address: {{ ip_address }}
    api_key: {{ api_key }}
    zone: 'dmz'
    mode: 'layer3'
    zone_profile: 'strict'

# Add an interface to the zone.
- name: add ethernet1/2 to zone dmz
  panos_interface:
    ip_address: '192.168.1.1'
    username: 'ansible'
    password: 'secret'
    zone: 'dmz'
    mode: 'layer3'
    interface: ['ethernet1/2']
    zone_profile: 'strict'

# Delete the zone.
- name: delete the DMZ zone
  panos_interface:
    ip_address: '192.168.1.1'
    username: 'ansible'
    password: 'secret'
    zone: 'dmz'
    state: 'absent'

# Add a zone to a multi-VSYS Panorama template
- name: add Cloud zone to template
  panos_interface:
    ip_address: {{ ip_address }}
    api_key: {{ api_key }}
    zone: 'datacenter'
    mode: 'layer3'
    enable_userid: true
    exclude_ip: '10.0.200.0/24'
    template: 'Datacenter Template'
    vsys: 'vsys4'
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception


try:
    from pandevice.base import PanDevice
    from pandevice.network import Zone
    from pandevice.device import Vsys
    from pandevice.firewall import Firewall
    from pandevice.panorama import Panorama, Template
    from pandevice.errors import PanDeviceError
    from pandevice import ha
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_vsys(vsys, vsys_list):
    for v in vsys_list:
        if v.name == vsys:
            return v


def get_template(template, template_list):
    for t in template_list:
        if t.name == template:
            return t


def find_zone(zones, new_zone):
    for z in zones:
        if z.name == new_zone.name:
            return z


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        zone=dict(required=True),
        mode=dict(choices=['tap', 'virtual-wire', 'layer2', 'layer3', 'external'], default='layer3'),
        interface=dict(type='list'),
        zone_profile=dict(),
        log_setting=dict(),
        enable_userid=dict(type='bool', default=False),
        include_acl=dict(type='list'),
        exclude_acl=dict(type='list'),
        vsys=dict(default='vsys1'),
        template=dict(),
        state=dict(choices=['present', 'absent'], default='present')
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get the firewall / panorama auth.
    auth = (
        module.params['ip_address'],
        module.params['username'],
        module.params['password'],
        module.params['api_key'],
    )

    # Set the Zone object params
    zone_spec = {
        'name': module.params['zone'],
        'mode': module.params['mode'],
        'interface': module.params['interface'],
        'zone_profile': module.params['zone_profile'],
        'log_setting': module.params['log_setting'],
        'enable_user_identification': module.params['enable_userid'],
        'include_acl': module.params['include_acl'],
        'exclude_acl': module.params['exclude_acl']
    }

    # Get other info
    vsys = module.params['vsys']
    template = module.params['template']
    state = module.params['state']

    # Open the connection to the PAN-OS device
    device = None
    try:
        device = PanDevice.create_from_device(*auth)
    except PanDeviceError:
        e = get_exception()
        module.fail_json(msg=e.message)

    # Set the attachment point for the Zone object
    parent = None
    if isinstance(device, Firewall):
        parent = device
    elif isinstance(device, Panorama):
        if template is not None:
            template_list = Template.refreshall(device)
            parent = get_template(template, template_list)
            if parent is None:
                module.fail_json(msg='Template not found: {0}'.format(template))
        else:
            module.fail_json(msg='A template parameter is required when device type is Panorama')
    if vsys is not None:
        v = Vsys(vsys)
        parent.add(v)
        parent = v

    # Retrieve the current list of zones
    try:
        zones = Zone.refreshall(parent)
    except PanDeviceError:
        e = get_exception()
        module.fail_json(msg=e.message)

    # Build the zone and attach to the parent
    new_zone = Zone(**zone_spec)
    parent.add(new_zone)

    # Which action shall we take on the Zone object?
    changed = False
    if state == 'present':
        match = find_zone(zones, new_zone)
        if match:
            # Change an existing zone
            if not match.equal(new_zone):
                try:
                    if not module.check_mode:
                        new_zone.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed "present" create: {0}'.format(e))
                else:
                    changed = True
        else:
            # Add a new zone
            try:
                if not module.check_mode:
                    new_zone.apply()
            except PanDeviceError as e:
                module.fail_json(msg='Failed "present" apply: {0}'.format(e))
            else:
                changed = True
    elif state == 'absent':
        match = find_zone(zones, new_zone)
        if match:
            # Delete an existing zone
            try:
                if not module.check_mode:
                    new_zone.delete()
            except PanDeviceError as e:
                module.fail_json(msg='Failed "absent" delete: {0}'.format(e))
            else:
                changed = True

    # Done!
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
