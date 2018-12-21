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
module: panos_ike_gateway
short_description: Configures IKE gateway on the firewall with subset of settings.
description:
    - Use this to manage or define a gateway, including the configuration information necessary to perform Internet Key
    - Exchange (IKE) protocol negotiation with a peer gateway. This is the Phase 1 portion of the IKE/IPSec VPN setup.
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
    protocol_version:
        description:
            - Specify the priority for Diffie-Hellman (DH) groups.
        default: ike2
    interface:
        description:
            - Specify the outgoing firewall interface to the VPN tunnel.
        default: 'ethernet1/1'
    passive_mode:
        description:
            - True to have the firewall only respond to IKE connections and never initiate them.
        default: True
    nat_traversal:
        description:
            - True to NAT Traversal mode
        default: False
    fragmentation:
        description:
            - True to enable IKE fragmentation
            - Incompatible with pre-shared keys, or 'aggressive' exchange mode
        default: False
    liveness_check:
        description:
            - The IKEv2 Liveness Check is always on; all IKEv2 packets serve the purpose of a liveness check. Use
            - this to have the system send empty informational packets after the peer has been idle for a number of sec.
        default: 5
    peer_ip_value:
        description:
            - IPv4 address of the peer gateway.
        default: '127.0.0.1'
    dead_peer_detection:
        description:
            - True to enable Dead Peer Detection on the gateway.
        default: false
    dead_peer_detection_interval:
        description:
            - Time in seconds to check for a dead peer.
        default: 99
    dead_peer_detection_retry:
        description:
            - Retry attempts before peer is marked dead.
        default: 10
    local_ip_address:
        description:
            - Bind IKE gateway to the specified interface IP address
            - It should include the mask, eg: '192.168.1.1/24'
        default: None
    local_ip_address_type:
        description:
            - The address type of the bound interface IP address
            - Valid options: 'ip' | 'floating-ip'
        default: None
    psk:
        description:
            - Specify pre-shared key.
        default: 'CHANGEME'
    crypto_profile_name:
        description:
            - Select an existing profile or keep the default profile.
        default: 'default'
    ikev1_exchange_mode:
        description:
            - The IKE exchange mode to use
            - Valid options: 'auto' | 'main' | 'aggressive'
        default: None
'''

EXAMPLES = '''
- name: Add IKE gateway config to the firewall
    panos_ike_gateway:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: 'IKEGW-Ansible'
      protocol_version: 'ikev2'
      interface: 'ethernet1/1'
      passive_mode: 'True'
      liveness_check: '5'
      peer_ip_value: '1.2.3.4'
      psk: 'CHANGEME'
      crypto_profile_name: 'IKE-Ansible'
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


class IKEGateway:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.protocol_version = kwargs.get('protocol_version')
        self.interface = kwargs.get('interface')
        self.local_ip_address_type = kwargs.get('local_ip_address_type')
        self.local_ip_address = kwargs.get('local_ip_address')
        self.ikev1_exchange_mode = kwargs.get('ikev1_exchange_mode')
        self.auth_type = 'pre-shared-key'
        self.enable_passive_mode = kwargs.get('enable_passive_mode')
        self.enable_nat_traversal = kwargs.get('enable_nat_traversal')
        self.enable_fragmentation = kwargs.get('enable_fragmentation')
        self.liveness_check = kwargs.get('liveness_check')
        self.peer_ip_type = 'ip'
        self.peer_ip_value = kwargs.get('peer_ip_value')
        self.dead_peer_detection = kwargs.get('dead_peer_detection')
        self.dead_peer_detection_interval = kwargs.get('dead_peer_detection_interval')
        self.dead_peer_detection_retry = kwargs.get('dead_peer_detection_retry')
        self.psk = kwargs.get('psk')


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        name=dict(required=True),
        protocol_version=dict(default='ikev2'),
        interface=dict(default='ethernet1/1'),
        local_ip_address_type=dict(default=None, choices=['ip', 'floating-ip']),
        local_ip_address=dict(default=None),
        # auth_type=dict(default='pre-shared-key'),
        # pasive_mode=dict(type='bool', default=True),
        passive_mode=dict(type='bool', default=True),
        nat_traversal=dict(type='bool', default=False),
        fragmentation=dict(type='bool', default=False),
        liveness_check=dict(type='int', default=5),
        peer_ip_value=dict(default='127.0.0.1'),
        dead_peer_detection=dict(type='bool', default=False),
        dead_peer_detection_interval=dict(type='int', default=99),
        dead_peer_detection_retry=dict(type='int', default=10),
        psk=dict(default='CHANGEME'),
        crypto_profile_name=dict(default='default'),
        ikev1_exchange_mode=dict(default=None, choices=['auto', 'main', 'aggressive']),
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
    protocol_version = module.params['protocol_version']
    interface = module.params['interface']
    local_ip_address_type = module.params['local_ip_address_type']
    local_ip_address = module.params['local_ip_address']
    # auth_type = module.params['auth_type']
    passive_mode = module.params['passive_mode']
    nat_traversal = module.params['nat_traversal']
    fragmentation = module.params['fragmentation']
    liveness_check = module.params['liveness_check']
    peer_ip_value = module.params['peer_ip_value']
    dead_peer_detection = module.params['dead_peer_detection']
    dead_peer_detection_interval = module.params['dead_peer_detection_interval']
    dead_peer_detection_retry = module.params['dead_peer_detection_retry']
    psk = module.params['psk']
    crypto_profile_name = module.params['crypto_profile_name']
    ikev1_exchange_mode = module.params['ikev1_exchange_mode']
    commit = module.params['commit']

    # If Panorama, validate the devicegroup
    # dev_group = None
    # if devicegroup and isinstance(device, panorama.Panorama):
    #     dev_group = get_devicegroup(device, devicegroup)
    #     if dev_group:
    #         device.add(dev_group)
    #     else:
    #         module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    ikeGtwy = IKEGateway(name=name, protocol_version=protocol_version, ikev1_exchange_mode=ikev1_exchange_mode,
                         interface=interface, local_ip_address_type=local_ip_address_type,
                         local_ip_address=local_ip_address, enable_nat_traversal=nat_traversal,
                         dead_peer_detection=dead_peer_detection,
                         dead_peer_detection_interval=dead_peer_detection_interval, enable_fragmentation=fragmentation,
                         dead_peer_detection_retry=dead_peer_detection_retry, enable_passive_mode=passive_mode,
                         liveness_check=liveness_check, peer_ip_value=peer_ip_value, psk=psk)

    ike_gateway = network.IkeGateway(name=ikeGtwy.name, version=ikeGtwy.protocol_version, enable_ipv6=False,
                                     disabled=False,
                                     peer_ip_type=ikeGtwy.peer_ip_type, peer_ip_value=ikeGtwy.peer_ip_value,
                                     interface=ikeGtwy.interface,
                                     local_ip_address_type=ikeGtwy.local_ip_address_type,
                                     local_ip_address=ikeGtwy.local_ip_address,
                                     auth_type=ikeGtwy.auth_type, pre_shared_key=ikeGtwy.psk,
                                     local_id_type=None, local_id_value=None, peer_id_type=None, peer_id_value=None,
                                     peer_id_check=None,
                                     local_cert=None, cert_enable_hash_and_url=False, cert_base_url=None,
                                     cert_use_management_as_source=False, cert_permit_payload_mismatch=False,
                                     cert_profile=None, cert_enable_strict_validation=False,
                                     enable_passive_mode=ikeGtwy.enable_passive_mode,
                                     enable_nat_traversal=ikeGtwy.enable_nat_traversal,
                                     enable_fragmentation=ikeGtwy.enable_fragmentation,
                                     ikev1_crypto_profile=crypto_profile_name,
                                     ikev1_exchange_mode=ikeGtwy.ikev1_exchange_mode,
                                     enable_dead_peer_detection=ikeGtwy.dead_peer_detection,
                                     dead_peer_detection_interval=ikeGtwy.dead_peer_detection_interval,
                                     dead_peer_detection_retry=ikeGtwy.dead_peer_detection_retry,
                                     ikev2_crypto_profile=crypto_profile_name,
                                     ikev2_cookie_validation=False,
                                     ikev2_send_peer_id=False, enable_liveness_check=True,
                                     liveness_check_interval=ikeGtwy.liveness_check)

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    changed = False
    try:
        # fetch all IKE gateways
        gateways = network.IkeGateway.refreshall(device)
        if state == "present":
            device.add(ike_gateway)
            for g in gateways:
                if g.name == ike_gateway.name:
                    if not ike_gateway.equal(g):
                        ike_gateway.apply()
                        changed = True
                    break
            else:
                ike_gateway.create()
                changed = True
        elif state == "absent":
            ike_gateway = device.find(ikeGtwy.name, network.IkeGateway)
            if ike_gateway:
                ike_gateway.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except PanDeviceError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True)

    module.exit_json(msg='IKE gateway config successful.', changed=changed)


if __name__ == '__main__':
    main()
