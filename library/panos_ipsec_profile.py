#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_ipsec_profile
short_description: Configures IPSec Crypto profile on the firewall with subset of settings.
description:
    - IPSec Crypto profiles specify protocols and algorithms for authentication and encryption in VPN tunnels based on
    - IPSec SA negotiation (Phase 2).
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is NOT supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Create or remove static route.
        choices: ['present', 'absent']
        default: 'present'
    commit:
        description:
            - Commit configuration if changed.
        default: true
    name:
        description:
            - Name for the profile.
        required: true
    esp_encryption:
        description:
        default: ['aes-256-cbc', '3des']
        aliases: encryption
    esp_authentication:
        description:
        default: sha1
        aliases: authentication
    ah_authentication:
        description:
        default:
    dh_group:
        description:
            - Diffie-Hellman (DH) groups.
        default: group2
        aliases: dhgroup
    lifetime_seconds:
        description:
            -  IPSec SA lifetime in seconds.
    lifetime_minutes:
        description:
            - IPSec SA lifetime in minutes.
    lifetime_hours:
        description:
            - IPSec SA lifetime in hours.
        aliases: lifetime_hrs
    lifetime_days:
        description:
            - IPSec SA lifetime in days.
    lifesize_kb:
        description:
            -  IPSec SA lifetime in kilobytes.
    lifesize_mb:
        description:
            - IPSec SA lifetime in megabytes.
    lifesize_gb:
        description:
            - IPSec SA lifetime in gigabytes.
    lifesize_tb:
        description:
            - IPSec SA lifetime in terabytes.
'''

EXAMPLES = '''
- name: Add IPSec crypto config to the firewall
    panos_ipsec_profile:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: 'IPSec-Ansible'
      encryption: ['aes-256-cbc', '3des']
      authentication: 'sha1'
      dhgroup: 'group2'
      lifetime_hrs: '1'
      commit: 'False'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import network
    from pandevice.errors import PanDeviceError

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def add_object(device, obj):
    if isinstance(device, firewall.Firewall):
        return device.add(obj)

    return None


def find_object(device, obj_name, obj_type, device_group=None):
    obj_type.refreshall(device)

    if isinstance(device, firewall.Firewall):
        return device.find(obj_name, obj_type)

    return None


def perform_commit(module, device):
    if isinstance(device, firewall.Firewall):
        result = device.commit(sync=True)

        if result:
            check_commit_result(module, result)


def check_commit_result(module, result):
    if result['result'] == 'FAIL':
        module.fail_json(msg='Commit failed')


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        name=dict(required=True),
        esp_encryption=dict(type='list', aliases=['encryption']),
        esp_authentication=dict(type='list', aliases=['authentication']),
        ah_authentication=dict(type='list'),
        dh_group=dict(default='group2', aliases=['dhgroup']),
        lifetime_seconds=dict(type='int'),
        lifetime_minutes=dict(type='int'),
        lifetime_hours=dict(type='int', aliases=['lifetime_hrs']),
        lifetime_days=dict(type='int'),
        lifesize_kb=dict(type='int'),
        lifesize_mb=dict(type='int'),
        lifesize_gb=dict(type='int'),
        lifesize_tb=dict(type='int'),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=False,
        required_one_of=[
            ['api_key', 'password'],
            ['lifetime_seconds', 'lifetime_minutes', 'lifetime_hours', 'lifetime_days']
        ],
        mutually_exclusive=[
            ['esp_encryption', 'ah_authentication'],
            ['esp_authentication', 'ah_authentication'],
            ['lifetime_seconds', 'lifetime_minutes', 'lifetime_hours', 'lifetime_days'],
            ['lifesize_kb', 'lifesize_mb', 'lifesize_gb', 'lifesize_tb']
        ]
    )

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params['ip_address']
    password = module.params['password']
    username = module.params['username']
    api_key = module.params['api_key']
    state = module.params['state']
    name = module.params['name']
    esp_encryption = module.params['esp_encryption']
    esp_authentication = module.params['esp_authentication']
    ah_authentication = module.params['ah_authentication']
    dh_group = module.params['dh_group']
    lifetime_seconds = module.params['lifetime_seconds']
    lifetime_minutes = module.params['lifetime_minutes']
    lifetime_hours = module.params['lifetime_hours']
    lifetime_days = module.params['lifetime_days']
    lifesize_kb = module.params['lifesize_kb']
    lifesize_mb = module.params['lifesize_mb']
    lifesize_gb = module.params['lifesize_gb']
    lifesize_tb = module.params['lifesize_tb']
    commit = module.params['commit']

    changed = False

    try:
        device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

        if state == 'present':
            existing_obj = find_object(device, name, network.IpsecCryptoProfile)
            new_obj = network.IpsecCryptoProfile(
                name=name,
                esp_encryption=esp_encryption,
                esp_authentication=esp_authentication,
                ah_authentication=ah_authentication,
                dh_group=dh_group,
                lifetime_seconds=lifetime_seconds,
                lifetime_minutes=lifetime_minutes,
                lifetime_hours=lifetime_hours,
                lifetime_days=lifetime_days,
                lifesize_kb=lifesize_kb,
                lifesize_mb=lifesize_mb,
                lifesize_gb=lifesize_gb,
                lifesize_tb=lifesize_tb
            )

            if not existing_obj:
                add_object(device, new_obj)
                new_obj.create()
                changed = True
            elif not existing_obj.equal(new_obj):
                existing_obj.esp_encryption = esp_encryption
                existing_obj.esp_authentication = esp_authentication
                existing_obj.ah_authentication = ah_authentication
                existing_obj.dh_group = dh_group
                existing_obj.lifetime_seconds = lifetime_seconds
                existing_obj.lifetime_minutes = lifetime_minutes
                existing_obj.lifetime_hours = lifetime_hours
                existing_obj.lifetime_days = lifetime_days
                existing_obj.lifesize_kb = lifesize_kb
                existing_obj.lifesize_mb = lifesize_mb
                existing_obj.lifesize_gb = lifesize_gb
                existing_obj.lifesize_tb = lifesize_tb
                existing_obj.apply()
                changed = True

        elif state == 'absent':
            existing_obj = find_object(device, name, network.IpsecCryptoProfile)

            if existing_obj:
                existing_obj.delete()
                changed = True

        if commit and changed:
            perform_commit(module, device)

    except PanDeviceError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    module.exit_json(msg='IPSec crypto profile config successful.', changed=changed)


if __name__ == '__main__':
    main()
