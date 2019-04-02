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
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.full_template_support
options:
    name:
        description:
            - Name for the IPSec tunnel.
        required: true
    tunnel_interface:
        description:
            - Specify existing tunnel interface that will be used.
        default: 'tunnel.1'
    ak_ike_gateway:
        description:
            - Name of the existing IKE gateway.
        default: 'default'
        aliases: 'ike_gtw_name'
    ak_ipsec_crypto_profile:
        description:
            - Name of the existing IPsec profile or use default.
        default: 'default'
        aliases: 'ipsec_profile'
    enable_tunnel_monitor:
        description:
            - Enable tunnel monitoring on this tunnel.
        default: False
    tunnel_monitor_dest_ip:
        description:
            - Destination IP to send ICMP probe.
    tunnel_monitor_proxy_id:
        description:
            - Which proxy-id (or proxy-id-v6) the monitoring traffic will use.
        default: None
    tunnel_monitor_profile:
        description:
            - Monitoring action.
        default: None
    disabled:
        description:
            - Disable the IPsec tunnel.
        default: False
    commit:
        description:
            - Commit configuration if changed.
        default: True
'''

EXAMPLES = '''
- name: Add IPSec tunnel to IKE gateway profile
  panos_ipsec_tunnel:
    provider: '{{ provider }}'
    name: 'IPSecTunnel-Ansible'
    tunnel_interface: 'tunnel.2'
    ak_ike_gateway: 'IKEGW-Ansible'
    ak_ipsec_crypto_profile: 'IPSec-Ansible'
    state: 'present'
    commit: False
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection

try:
    from pandevice.network import IpsecTunnel
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
            tunnel_interface=dict(default='tunnel.1'),
            ak_ike_gateway=dict(default='default', aliases=['ike_gtw_name']),
            ak_ipsec_crypto_profile=dict(default='default', aliases=['ipsec_profile']),
            enable_tunnel_monitor=dict(type='bool', default=False),
            tunnel_monitor_dest_ip=dict(type='str', default=None),
            tunnel_monitor_proxy_id=dict(type='str', default=None),
            tunnel_monitor_profile=dict(type='str', default=None),
            disabled=dict(type='bool', default=False),
            commit=dict(type='bool', default=True)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        'name': module.params['name'],
        'tunnel_interface': module.params['tunnel_interface'],
        'ak_ike_gateway': module.params['ak_ike_gateway'],
        'ak_ipsec_crypto_profile': module.params['ak_ipsec_crypto_profile'],
        'enable_tunnel_monitor': module.params['enable_tunnel_monitor'],
        'tunnel_monitor_dest_ip': module.params['tunnel_monitor_dest_ip'],
        'tunnel_monitor_proxy_id': module.params['tunnel_monitor_proxy_id'],
        'tunnel_monitor_profile': module.params['tunnel_monitor_profile'],
        'disabled': module.params['disabled']
    }

    # Other info.
    commit = module.params['commit']

    # Retrieve current info.
    try:
        listing = IpsecTunnel.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = IpsecTunnel(**spec)
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
