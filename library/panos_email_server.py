#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_email_server
short_description: Manage email servers in an email profile.
description:
    - Manages email servers in an email server profile.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.vsys_shared
    - panos.device_group
options:
    email_profile:
        description:
            - Name of the email server profile.
        required: True
    name:
        description:
            - Server name.
        required: True
    display_name:
        description:
            - Display name
    from_email:
        description:
            - From email address
    to_email:
        description:
            - Destination email address.
    also_to_email:
        description:
            - Additional destination email address
    email_gateway:
        description:
            - IP address or FQDN of email gateway to use.
'''

EXAMPLES = '''
# Create a profile
- name: Create email server in an email profile
  panos_email_server:
    provider: '{{ provider }}'
    email_profile: 'my-profile'
    name: 'my-email-server'
    from_email: 'alerts@example.com'
    to_email: 'notify@example.com'
    email_gateway: 'smtp.example.com'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.device import EmailServerProfile
    from pandevice.device import EmailServer
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(7, 1, 0),
        argument_spec=dict(
            email_profile=dict(required=True),
            name=dict(required=True),
            display_name=dict(),
            from_email=dict(),
            to_email=dict(),
            also_to_email=dict(),
            email_gateway=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = EmailServerProfile(module.params['email_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = sp.findall(EmailServer)

    spec = {
        'name': module.params['name'],
        'display_name': module.params['display_name'],
        'from': module.params['from_email'],
        'to': module.params['to_email'],
        'also_to': module.params['also_to_email'],
        'email_gateway': module.params['email_gateway'],
    }
    obj = EmailServer(**spec)
    sp.add(obj)

    changed = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
