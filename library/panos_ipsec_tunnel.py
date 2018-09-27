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
module: panos_ipsec_tunnel
short_description: Configures IPSec Tunnels on the firewall with subset of settings.
description:
    - Use IPSec Tunnels to establish and manage IPSec VPN tunnels between firewalls. This is the Phase 2 portion of the
    - IKE/IPSec VPN setup.
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
            - Name for the IPSec tunnel.
        required: true
    tunnel_interface:
        description:
            - Specify existing tunnel interface that will be used.
        default: 'tunnel.1'
    ike_gtw_name:
        description:
            - Name of the existing IKE gateway.
        default: 'default'
    ipsec_profile:
        description:
            - Name of the existing IPsec profile or use default.
        default: 'default'
'''

EXAMPLES = '''
- name: Add IPSec tunnel to IKE gateway profile
    panos_ipsec_tunnel:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: 'IPSecTunnel-Ansible'
      tunnel_interface: 'tunnel.2'
      ike_gtw_name: 'IKEGW-Ansible'
      ipsec_profile: 'IPSec-Ansible'
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


class IPSecTunnel:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.key_type = 'auto-key'
        self.tunnel_interface = kwargs.get('tunnel_interface')
        self.ike_gw = args[0]
        self.ipsec_profile = args[1]


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        name=dict(required=True),
        tunnel_interface=dict(default='tunnel.1'),
        ike_gtw_name=dict(default='default'),
        ipsec_profile=dict(default='default'),
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
    name = module.params['name']
    tunnel_interface = module.params['tunnel_interface']
    ike_gtw_name = module.params['ike_gtw_name']
    ipsec_profile = module.params['ipsec_profile']
    commit = module.params['commit']

    # If Panorama, validate the devicegroup
    # dev_group = None
    # if devicegroup and isinstance(device, panorama.Panorama):
    #     dev_group = get_devicegroup(device, devicegroup)
    #     if dev_group:
    #         device.add(dev_group)
    #     else:
    #         module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    ipsecTunnel = IPSecTunnel(ike_gtw_name, ipsec_profile, name=name,
                              tunnel_interface=tunnel_interface)

    ipsec_tunnel = network.IpsecTunnel(name=ipsecTunnel.name, tunnel_interface=ipsecTunnel.tunnel_interface,
                                       type=ipsecTunnel.key_type,
                                       ak_ike_gateway=ipsecTunnel.ike_gw,
                                       ak_ipsec_crypto_profile=ipsecTunnel.ipsec_profile,
                                       ipv6=False,
                                       enable_tunnel_monitor=False,
                                       disabled=False)

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    changed = False
    try:
        # fetch all Ipsec tunnels
        tunnels = network.IpsecTunnel.refreshall(device)
        if state == "present":
            device.add(ipsec_tunnel)
            for t in tunnels:
                if t.name == ipsec_tunnel.name:
                    if not ipsec_tunnel.equal(t):
                        ipsec_tunnel.apply()
                        changed = True
            else:
                ipsec_tunnel.create()
                changed = True
        elif state == "absent":
            ipsec_tunnel = device.find(ipsec_tunnel.name, network.IpsecTunnel)
            if ipsec_tunnel:
                ipsec_tunnel.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except PanDeviceError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True)

    module.exit_json(msg='ipsec tunnel config successful.', changed=changed)


if __name__ == '__main__':
    main()
