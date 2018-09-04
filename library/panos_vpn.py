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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_vpn
short_description: Configures VPN on the firewall.
description:
    - VPN configuration requires ...
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
    - xmltodict can be obtained from PyPi U(https://pypi.python.org/pypi/xmltodict)
notes:
    - Checkmode is not supported.
    - Panorama is not supported.
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
    operation:
        description:
            - The action to be taken.  Supported values are I(add)/I(update)/I(find)/I(delete).
        default: 'add'
    commit:
        description:
            - Commit configuration if changed.
        default: true
'''

EXAMPLES = '''
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


class IKEProfile:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.authentication = kwargs.get('authentication')
        self.encryption = kwargs.get('encryption')
        self.dh_group = kwargs.get('dh_group')
        self.lifetime_secs = kwargs.get('lifetime_secs')


class IPSecProfile:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.authentication = kwargs.get('authentication')
        self.encryption = kwargs.get('encryption')
        self.dh_group = kwargs.get('dh_group')
        self.lifetime_hrs = kwargs.get('lifetime_hrs')


class IKEGateway:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.protocol_version = kwargs.get('protocol_version')
        self.interface = kwargs.get('interface')
        self.auth_type = kwargs.get('auth_type')
        self.enable_passive_mode = kwargs.get('enable_passive_mode')
        self.liveness_check = kwargs.get('liveness_check')
        self.peer_ip_value = kwargs.get('peer_ip_value')
        self.psk = kwargs.get('psk')


class IPSecTunnel:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.key_type = kwargs.get('key_type')
        self.tunnel_interface = kwargs.get('tunnel_interface')
        self.ike_gw = args[0]
        self.ipsec_profile = args[1]


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        operation=dict(default='add', choices=['add', 'delete']),
        ike_profile_name=dict(required=True),
        ike_dhgroup=dict(default='group2'),
        ike_authentication=dict(default='sha1'),
        ike_encryption=dict(default=['aes-256-cbc', '3des']),
        ike_lifetime_sec=dict(type='int', default=28800),
        ipsec_profile_name=dict(required=True),
        ipsec_encryption=dict(default=['aes-256-cbc', '3des']),
        ipsec_authentication=dict(default='sha1'),
        ipsec_dhgroup=dict(default='group2'),
        ipsec_lifetime_hrs=dict(type='int', default=1),
        ike_gw_name=dict(required=True),
        ike_gw_protocol_version=dict(default='ikev2'),
        ike_gw_interface=dict(default='ethernet1/1'),
        ike_gw_auth_type=dict(default='pre-shared-key'),
        ike_gw_pasive_mode=dict(type='bool', default=True),
        ike_gw_liveness_check=dict(type='int', default=5),
        ike_gw_peer_ip_value=dict(required=True),
        ike_gw_psk=dict(required=True),
        ipsec_tunnel_name=dict(required=True),
        ipsec_tunnel_interface=dict(required=True),
        ipsec_key_type=dict(default='auto-key'),
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
    operation = module.params['operation']
    ike_profile_name = module.params['ike_profile_name']
    ike_dhgroup = module.params['ike_dhgroup']
    ike_authentication = module.params['ike_authentication']
    ike_encryption = module.params['ike_encryption']
    ike_lifetime_sec = module.params['ike_lifetime_sec']
    ipsec_profile_name = module.params['ipsec_profile_name']
    ipsec_encryption = module.params['ipsec_encryption']
    ipsec_authentication = module.params['ipsec_authentication']
    ipsec_dhgroup = module.params['ipsec_dhgroup']
    ipsec_lifetime_hrs = module.params['ipsec_lifetime_hrs']
    ike_gw_name = module.params['ike_gw_name']
    ike_gw_protocol_version = module.params['ike_gw_protocol_version']
    ike_gw_interface = module.params['ike_gw_interface']
    ike_gw_auth_type = module.params['ike_gw_auth_type']
    ike_gw_pasive_mode = module.params['ike_gw_pasive_mode']
    ike_gw_liveness_check = module.params['ike_gw_liveness_check']
    ike_gw_peer_ip_value = module.params['ike_gw_peer_ip_value']
    ike_gw_psk = module.params['ike_gw_psk']
    ipsec_tunnel_name = module.params['ipsec_tunnel_name']
    ipsec_tunnel_interface = module.params['ipsec_tunnel_interface']
    ipsec_key_type = module.params['ipsec_key_type']
    commit = module.params['commit']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    # dev_group = None
    # if devicegroup and isinstance(device, panorama.Panorama):
    #     dev_group = get_devicegroup(device, devicegroup)
    #     if dev_group:
    #         device.add(dev_group)
    #     else:
    #         module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    ikeProfile = IKEProfile(name=ike_profile_name,
                            authentication=ike_authentication,
                            encryption=ike_encryption,
                            dh_group=ike_dhgroup, lifetime_secs=ike_lifetime_sec)

    ipsecProfile = IPSecProfile(name=ipsec_profile_name, ipsec_encryption=ipsec_encryption,
                                ipsec_authentication=ipsec_authentication, ipsec_dhgroup=ipsec_dhgroup,
                                ipsec_lifetime_hrs=ipsec_lifetime_hrs)
    ikeGtwy = IKEGateway(name=ike_gw_name, protocol_version=ike_gw_protocol_version, ike_gw_interface=ike_gw_interface,
                         ike_gw_auth_type=ike_gw_auth_type, ike_gw_pasive_mode=ike_gw_pasive_mode,
                         ike_gw_liveness_check=ike_gw_liveness_check, peer_ip_value=ike_gw_peer_ip_value, psk=ike_gw_psk)

    ipsecTunnel = IPSecTunnel(name=ipsec_tunnel_name, tunnel_interface=ipsec_tunnel_interface,
                              ipsec_key_type=ipsec_key_type)

    ####

    ike_crypto_prof = network.IkeCryptoProfile(ikeProfile.name, ikeProfile.dh_group, ikeProfile.authentication,
                                                ikeProfile.encryption, ikeProfile.lifetime_secs,
                                                None, None, None, 0)

    ipsec_crypto_prof = network.IpsecCryptoProfile(name=ipsecProfile.name, esp_encryption=ipsecProfile.encryption,
                                                   esp_authentication=ipsecProfile.authentication,
                                                   ah_authentication=None, dh_group=ipsecProfile.dh_group,
                                                   lifetime_hours=ipsecProfile.lifetime_hrs)

    ike_gateway = network.IkeGateway(name=ikeGtwy.name, version=ikeGtwy.protocol_version, enable_ipv6=False,
                                     disabled=False,
                                     peer_ip_type="ip", peer_ip_value=ikeGtwy.peer_ip_value,
                                     interface=ikeGtwy.interface,
                                     auth_type=ikeGtwy.auth_type, pre_shared_key=ikeGtwy.psk,
                                     local_id_type=None, local_id_value=None, peer_id_type=None, peer_id_value=None,
                                     peer_id_check=None,
                                     local_cert=None, cert_enable_hash_and_url=False, cert_base_url=None,
                                     cert_use_management_as_source=False, cert_permit_payload_mismatch=False,
                                     cert_profile=None, cert_enable_strict_validation=False,
                                     enable_passive_mode=True,
                                     enable_fragmentation=False,
                                     ikev1_exchange_mode=None, ikev1_crypto_profile=None,
                                     enable_dead_peer_detection=False, dead_peer_detection_interval=99,
                                     dead_peer_detection_retry=10,
                                     ikev2_crypto_profile=ikeProfile.name,
                                     ikev2_cookie_validation=False,
                                     ikev2_send_peer_id=False, enable_liveness_check=True,
                                     liveness_check_interval=ikeGtwy.liveness_check)

    ipsec_tunnel = network.IpsecTunnel(name=ipsecTunnel.name, tunnel_interface=ipsecTunnel. tunnel_interface,
                                       type=ipsecTunnel.key_type,
                                       ak_ike_gateway=ikeGtwy.name,
                                       ak_ipsec_crypto_profile=ipsecTunnel.ipsec_profile,
                                       ipv6=False,
                                       enable_tunnel_monitor=False,
                                       disabled=False)

    if operation == "add":
        try:
            device.add(ike_crypto_prof)
            ike_crypto_prof.create()
            device.add(ipsec_crypto_prof)
            ipsec_crypto_prof.create()
            device.add(ike_gateway)
            ike_gateway.create()
            device.add(ipsec_tunnel)
            ipsec_tunnel.create()

            device.commit(sync=True)
        except PanDeviceError:
            exc = get_exception()
            module.fail_json(msg=exc.message)

        if commit:
            module.exit_json(msg='VPN config successful.')
        else:
            module.fail_json(msg='That operation is not implemented yet')


if __name__ == '__main__':
    main()
