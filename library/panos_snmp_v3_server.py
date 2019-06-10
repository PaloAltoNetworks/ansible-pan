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
module: panos_snmp_v3_server
short_description: Manage SNMP v3 servers.
description:
    - Manages SNMP v3 servers.
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
    snmp_profile:
        description:
            - Name of the SNMP server profile.
        required: true
    name:
        description:
            - Name of the server.
        required: true
    manager:
        description:
            - IP address or FQDN of SNMP manager to use.
    user:
        description:
            - User
    engine_id:
        description:
            - A hex number
    auth_password:
        description:
            - Authentiation protocol password.
    priv_password:
        description:
            - Privacy protocol password.
'''

EXAMPLES = '''
# Create snmp v3 server
- name: Create snmp v3 server
  panos_snmp_v3_server:
    provider: '{{ provider }}'
    snmp_profile: 'my-profile'
    name: 'my-v3-server'
    manager: '192.168.55.10'
    user: 'jdoe'
    auth_password: 'password'
    priv_password: 'drowssap'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.device import SnmpServerProfile
    from pandevice.device import SnmpV3Server
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
            snmp_profile=dict(required=True),
            name=dict(required=True),
            manager=dict(),
            user=dict(),
            engine_id=dict(),
            auth_password=dict(no_log=True),
            priv_password=dict(no_log=True),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    sp = SnmpServerProfile(module.params['snmp_profile'])
    parent.add(sp)
    try:
        sp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    listing = sp.findall(SnmpV3Server)

    spec = {
        'name': module.params['name'],
        'manager': module.params['manager'],
        'user': module.params['user'],
        'engine_id': module.params['engine_id'],
        'auth_password': module.params['auth_password'],
        'priv_password': module.params['priv_password'],
    }
    obj = SnmpV3Server(**spec)
    sp.add(obj)

    changed = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
