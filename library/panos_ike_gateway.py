#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    - NOTE: The modules in this role are deprecated in favour of the modules in the collection U(https://paloaltonetworks.github.io/pan-os-ansible)
    - Use this to manage or define a gateway, including the configuration information
      necessary to perform Internet Key Exchange (IKE) protocol negotiation with a
      peer gateway. This is the Phase 1 portion of the IKE/IPSec VPN setup.
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.full_template_support
options:
    name:
        description:
            - Name for the profile.
        required: true
    version:
        description:
            - Specify the priority for Diffie-Hellman (DH) groups.
        default: 'ike2'
        choices:
            - ikev1
            - ikev2
            - ikev2-preferred
        aliases: 'protocol_version'
    interface:
        description:
            - Specify the outgoing firewall interface to the VPN tunnel.
        default: 'ethernet1/1'
    enable_passive_mode:
        description:
            - True to have the firewall only respond to IKE connections and never initiate them.
        type: bool
        default: True
        aliases: 'passive_mode'
    enable_nat_traversal:
        description:
            - True to NAT Traversal mode
        type: bool
        default: False
        aliases: 'nat_traversal'
    enable_fragmentation:
        description:
            - True to enable IKE fragmentation
            - Incompatible with pre-shared keys, or 'aggressive' exchange mode
        type: bool
        default: False
        aliases: 'fragmentation'
    enable_liveness_check:
        description:
            - Enable sending empty information liveness check message.
        type: bool
        default: True
    liveness_check_interval:
        description:
            - Delay interval before sending probing packets (in seconds).
        type: int
        default: 5
        aliases: 'liveness_check'
    peer_ip_value:
        description:
            - IPv4 address of the peer gateway.
        default: '127.0.0.1'
    enable_dead_peer_detection:
        description:
            - True to enable Dead Peer Detection on the gateway.
        type: bool
        default: false
        aliases: 'dead_peer_detection'
    dead_peer_detection_interval:
        description:
            - Time in seconds to check for a dead peer.
        type: int
        default: 99
    dead_peer_detection_retry:
        description:
            - Retry attempts before peer is marked dead.
        type: int
        default: 10
    local_ip_address:
        description:
            - Bind IKE gateway to the specified interface IP address
            - It should include the mask, such as '192.168.1.1/24'
        default: None
    local_ip_address_type:
        description:
            - The address type of the bound interface IP address
        choices: ['ip', 'floating-ip']
        default: None
    pre_shared_key:
        description:
            - Specify pre-shared key.
        default: 'CHANGEME'
        aliases: 'psk'
    local_id_type:
        description:
            - Specify the type of local ID.
        choices: ['ipaddr', 'fwdn', 'ufqdn', 'keyid', 'dn']
        default: None
    local_id_value:
        description:
            - The value for the local_id.  (See also local_id_type, above.)
        default: None
    peer_id_type:
        description:
            - Specify the type of peer ID.
        choices: ['ipaddr', 'fwdn', 'ufqdn', 'keyid', 'dn']
        default: None
    peer_id_value:
        description:
            - The value for the peer_id.  (See also peer_id_type, above.)
        default: None
    peer_id_check:
        description:
            - Type of checking to do on peer_id.
        choices: ['exact', 'wildcard']
    ikev1_crypto_profile:
        description:
            - Crypto profile for IKEv1.
        default: 'default'
        aliases: 'crypto_profile_name'
    ikev1_exchange_mode:
        description:
            - The IKE exchange mode to use
        choices:
            - auto
            - main
            - aggressive
        default: None
    ikev2_crypto_profile:
        description:
            - Crypto profile for IKEv2.
        default: 'default'
        aliases: 'crypto_profile_name'
    commit:
        description:
            - Commit configuration if changed.
        type: bool
        default: true
'''

EXAMPLES = '''
- name: Add IKE gateway config to the firewall
  panos_ike_gateway:
    provider: '{{ provider }}'
    state: 'present'
    name: 'IKEGW-Ansible'
    version: 'ikev2'
    interface: 'ethernet1/1'
    enable_passive_mode: True
    enable_liveness_check: True
    liveness_check_interval: '5'
    peer_ip_value: '1.2.3.4'
    pre_shared_key: 'CHANGEME'
    ikev2_crypto_profile: 'IKE-Ansible'
    commit: False
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection

try:
    from pandevice.network import IkeGateway
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(required=True),
            version=dict(default='ikev2', choices=['ikev1', 'ikev2', 'ikev2-preferred'], aliases=['protocol_version']),
            interface=dict(default='ethernet1/1'),
            local_ip_address_type=dict(default=None, choices=['ip', 'floating-ip']),
            local_ip_address=dict(default=None),
            enable_passive_mode=dict(type='bool', default=True, aliases=['passive_mode']),
            enable_nat_traversal=dict(type='bool', default=False, aliases=['nat_traversal']),
            enable_fragmentation=dict(type='bool', default=False, aliases=['fragmentation']),
            enable_liveness_check=dict(type='bool', default=True),
            liveness_check_interval=dict(type='int', default=5, aliases=['liveness_check']),
            peer_ip_value=dict(default='127.0.0.1'),
            enable_dead_peer_detection=dict(type='bool', default=False, aliases=['dead_peer_detection']),
            dead_peer_detection_interval=dict(type='int', default=99),
            dead_peer_detection_retry=dict(type='int', default=10),
            pre_shared_key=dict(no_log=True, default='CHANGEME', aliases=['psk']),
            local_id_type=dict(default=None, choices=['ipaddr', 'fqdn', 'ufqdn', 'keyid', 'dn']),
            local_id_value=dict(default=None),
            peer_id_type=dict(default=None, choices=['ipaddr', 'fqdn', 'ufqdn', 'keyid', 'dn']),
            peer_id_value=dict(default=None),
            peer_id_check=dict(choices=['exact', 'wildcard']),
            ikev1_crypto_profile=dict(default='default', aliases=['crypto_profile_name']),
            ikev1_exchange_mode=dict(default=None, choices=['auto', 'main', 'aggressive']),
            ikev2_crypto_profile=dict(default='default', aliases=['crypto_profile_name']),
            commit=dict(type='bool', default=True),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
        required_together=[
            ['peer_id_value', 'peer_id_type'],
            ['local_id_value', 'local_id_type'],
        ],
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        'name': module.params['name'],
        'version': module.params['version'],
        'interface': module.params['interface'],
        'local_ip_address_type': module.params['local_ip_address_type'],
        'local_ip_address': module.params['local_ip_address'],
        'auth_type': 'pre-shared-key',
        'enable_passive_mode': module.params['enable_passive_mode'],
        'enable_nat_traversal': module.params['enable_nat_traversal'],
        'enable_fragmentation': module.params['enable_fragmentation'],
        'enable_liveness_check': module.params['enable_liveness_check'],
        'liveness_check_interval': module.params['liveness_check_interval'],
        'peer_ip_value': module.params['peer_ip_value'],
        'enable_dead_peer_detection': module.params['enable_dead_peer_detection'],
        'dead_peer_detection_interval': module.params['dead_peer_detection_interval'],
        'dead_peer_detection_retry': module.params['dead_peer_detection_retry'],
        'pre_shared_key': module.params['pre_shared_key'],
        'local_id_type': module.params['local_id_type'],
        'local_id_value': module.params['local_id_value'],
        'peer_id_type': module.params['peer_id_type'],
        'peer_id_value': module.params['peer_id_value'],
        'peer_id_check': module.params['peer_id_check'],
        'ikev1_crypto_profile': module.params['ikev1_crypto_profile'],
        'ikev1_exchange_mode': module.params['ikev1_exchange_mode'],
        'ikev2_crypto_profile': module.params['ikev2_crypto_profile'],
    }

    # Other info.
    commit = module.params['commit']

    # Retrieve current info.
    try:
        listing = IkeGateway.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = IkeGateway(**spec)
    parent.add(obj)

    # Apply the state.
    changed = helper.apply_state(obj, listing, module)

    # Commit.
    if commit and changed:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
