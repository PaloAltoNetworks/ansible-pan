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
    dhgroup:
        description:
            - Specify the priority for Diffie-Hellman (DH) groups.
        default: group2
    authentication:
        description:
            - Specify the priority for hash algorithms.
        default: sha1
    encryption:
        description:
            - Select the appropriate Encapsulating Security Payload (ESP) authentication options.
        default: ['aes-256-cbc', '3des']
    lifetime_hrs:
        description:
            - Select units and enter the length of time (default is 1hr) that the negotiated key will stay effective.
        default: 1
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
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import base
    from pandevice import panorama
    from pandevice.errors import PanDeviceError
    from pandevice import network

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


# def get_devicegroup(device, devicegroup):
#     dg_list = device.refresh_devices()
#     for group in dg_list:
#         if isinstance(group, pandevice.panorama.DeviceGroup):
#             if group.name == devicegroup:
#                 return group
#     return False


class IPSecProfile:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.authentication = kwargs.get('authentication')
        self.encryption = kwargs.get('encryption')
        self.dh_group = kwargs.get('dh_group')
        self.lifetime_hrs = kwargs.get('lifetime_hrs')


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        name=dict(required=True),
        encryption=dict(type='list', default=['aes-256-cbc', '3des']),
        authentication=dict(default='sha1'),
        dhgroup=dict(default='group2'),
        lifetime_hrs=dict(type='int', default=1),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params['ip_address']
    password = module.params['password']
    username = module.params['username']
    api_key = module.params['api_key']
    state = module.params['state']
    profile_name = module.params['name']
    encryption = module.params['encryption']
    authentication = module.params['authentication']
    dhgroup = module.params['dhgroup']
    lifetime_hrs = module.params['lifetime_hrs']
    commit = module.params['commit']

    # If Panorama, validate the devicegroup
    # dev_group = None
    # if devicegroup and isinstance(device, panorama.Panorama):
    #     dev_group = get_devicegroup(device, devicegroup)
    #     if dev_group:
    #         device.add(dev_group)
    #     else:
    #         module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    ipsecProfile = IPSecProfile(name=profile_name, encryption=encryption,
                                authentication=authentication, dhgroup=dhgroup,
                                lifetime_hrs=lifetime_hrs)

    ipsec_crypto_prof = network.IpsecCryptoProfile(name=ipsecProfile.name, esp_encryption=ipsecProfile.encryption,
                                                   esp_authentication=ipsecProfile.authentication,
                                                   ah_authentication=None, dh_group=ipsecProfile.dh_group,
                                                   lifetime_hours=ipsecProfile.lifetime_hrs)

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    changed = False
    try:
        # fetch all IpsecCryptoProfiles
        crypto_profiles = network.IpsecCryptoProfile.refreshall(device)
        if state == "present":
            device.add(ipsec_crypto_prof)
            for p in crypto_profiles:
                if p.name == ipsec_crypto_prof.name:
                    if not ipsec_crypto_prof.equal(p):
                        ipsec_crypto_prof.apply()
                        changed = True
                    break
            else:
                ipsec_crypto_prof.create()
                changed = True
        elif state == "absent":
            ipsec_crypto_prof = device.find(ipsecProfile.name, network.IpsecCryptoProfile)
            if ipsec_crypto_prof:
                ipsec_crypto_prof.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except PanDeviceError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True)

    module.exit_json(msg='IPSec crypto profile config successful.', changed=changed)


if __name__ == '__main__':
    main()
