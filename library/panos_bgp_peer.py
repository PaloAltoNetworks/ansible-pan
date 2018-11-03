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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_bgp_peer
short_description: Configures a BGP Peer
description:
    - Use BGP to publish and consume routes from disparate networks.
author: "Joshua Colson (@freakinhippie)"
version_added: "2.9"
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
            required: True
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
            default: admin
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Add or remove BGP peer configuration.
                - present
                - absent
            default: present
    commit:
        description:
            - Commit configuration if changed.
            default: True
    address_family_identifier:
        description:
            - Peer address family type.
                - ipv4
                - ipv6
    bfd_profile:
        description:
            - BFD profile configuration.
    connection_authentication:
        description:
            - BGP auth profile name.
    connection_hold_time:
        description:
            - Hold time (in seconds).
    connection_idle_hold_time:
        description:
            - Idle hold time (in seconds).
    connection_incoming_allow:
        description:
            - Allow incoming connections.
    connection_incoming_remote_port:
        description:
            - Restrict remote port for incoming BGP connections.
    connection_keep_alive_interval:
        description:
            - Keep-alive interval (in seconds).
    connection_min_route_adv_interval:
        description:
            - Minimum Route Advertisement Interval (in seconds).
    connection_multihop:
        description:
            - IP TTL value used for sending BGP packet. set to 0 means eBGP use 2, iBGP use 255.
    connection_open_delay_time:
        description:
            - Open delay time (in seconds).
    connection_outgoing_allow:
        description:
            - Allow outgoing connections.
    connection_outgoing_local_port:
        description:
            - Use specific local port for outgoing BGP connections.
    enable:
        description:
            - Enable BGP Peer.
            default: True
    enable_mp_bgp:
        description:
            - Enable MP-BGP extentions.
    enable_sender_side_loop_detection:
        description:
            - Enable sender side loop detection.
    local_interface:
        description:
            - Interface to accept BGP session.
    local_interface_ip:
        description:
            - Specify exact IP address if interface has multiple addresses.
    max_prefixes:
        description:
            - Maximum of prefixes to receive from peer.
    name:
        description:
            - Name of BGP Peer.
            required: True
    peer_address_ip:
        description:
            - IP address of peer.
    peer_as:
        description:
            - Peer AS number.
    peer_group:
        description:
            - Name of the peer group; it must already exist; see panos_bgp_peer_group.
            required: True
    peering_type:
        description:
            - Peering type.
                - unspecified
                - bilateral
    reflector_client:
        description:
            - Reflector client type.
                - non-client
                - client
                - meshed-client
    subsequent_address_multicast:
        description:
            - Select SAFI for this peer.
    subsequent_address_unicast:
        description:
            - Select SAFI for this peer.
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default
'''

EXAMPLES = '''
- name: Create BGP Peer
    panos_bgp_peer:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: peer-1
      enable: true
      local_interface: ethernet1/1
      local_interface_ip: 192.168.1.1
      peer_address_ip: 10.1.1.1
      peer_as: 64512
      commit: true
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


def main():
    argument_spec = dict(
        ip_address=dict(
            required=True,
            help='IP address (or hostname) of PAN-OS device being configured'),
        password=dict(
            no_log=True,
            help='Password credentials to use for auth unless I(api_key) is set'),
        username=dict(
            default='admin',
            help='Username credentials to use for auth unless I(api_key) is set'),
        api_key=dict(
            no_log=True,
            help='API key that can be used instead of I(username)/I(password) credentials'),
        state=dict(
            default='present', choices=['present', 'absent'],
            help='Add or remove BGP peer configuration'),

        name=dict(
            type='str', required=True,
            help='Name of BGP Peer'),
        enable=dict(
            default=True, type='bool',
            help='Enable BGP Peer'),
        peer_as=dict(
            type='str',
            help='Peer AS number'),
        enable_mp_bgp=dict(
            type='bool',
            help='Enable MP-BGP extentions'),
        address_family_identifier=dict(
            type='str', choices=['ipv4', 'ipv6'],
            help='Peer address family type'),
        subsequent_address_unicast=dict(
            type='bool',
            help='Select SAFI for this peer'),
        subsequent_address_multicast=dict(
            type='bool',
            help='Select SAFI for this peer'),
        local_interface=dict(
            type='str',
            help='Interface to accept BGP session'),
        local_interface_ip=dict(
            type='str',
            help='Specify exact IP address if interface has multiple addresses'),
        peer_address_ip=dict(
            type='str',
            help='IP address of peer'),
        connection_authentication=dict(
            type='str',
            help='BGP auth profile name'),
        connection_keep_alive_interval=dict(
            type='int',
            help='Keep-alive interval (in seconds)'),
        connection_min_route_adv_interval=dict(
            type='int',
            help='Minimum Route Advertisement Interval (in seconds)'),
        connection_multihop=dict(
            type='int',
            help='IP TTL value used for sending BGP packet. set to 0 means eBGP use 2, iBGP use 255'),
        connection_open_delay_time=dict(
            type='int',
            help='Open delay time (in seconds)'),
        connection_hold_time=dict(
            type='int',
            help='Hold time (in seconds)'),
        connection_idle_hold_time=dict(
            type='int',
            help='Idle hold time (in seconds)'),
        connection_incoming_allow=dict(
            type='bool',
            help='Allow incoming connections'),
        connection_outgoing_allow=dict(
            type='bool',
            help='Allow outgoing connections'),
        connection_incoming_remote_port=dict(
            type='int',
            help='Restrict remote port for incoming BGP connections'),
        connection_outgoing_local_port=dict(
            type='int',
            help='Use specific local port for outgoing BGP connections'),
        enable_sender_side_loop_detection=dict(
            type='bool',
            help='Enable sender side loop detection'),
        reflector_client=dict(
            type='str', choices=['non-client', 'client', 'meshed-client'],
            help='Reflector client type'),
        peering_type=dict(
            type='str', choices=['unspecified', 'bilateral'],
            help='Peering type'),
        # aggregated_confed_as_path=dict(
        #     type='bool',
        #     help='This peer understands aggregated confederation AS path'),
        max_prefixes=dict(
            type='int',
            help='Maximum of prefixes to receive from peer'),
        # max_orf_entries=dict(
        #     type='int',
        #     help='Maximum of ORF entries accepted from peer'),
        # soft_reset_with_stored_info=dict(
        #     type='bool',
        #     help='Enable soft reset with stored info'),
        bfd_profile=dict(
            type='str',
            help='BFD profile configuration'),

        peer_group=dict(
            required=True,
            help='Name of the peer group; it must already exist; see panos_bgp_peer_group'),
        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get the firewall / panorama auth.
    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password', 'api_key')]

    # exclude the default items from kwargs passed to the object
    exclude_list = ['ip_address', 'username', 'password', 'api_key', 'state', 'commit']
    # exclude these items from the kwargs passed to the object
    exclude_list += ['peer_group', 'vr_name']

    # generate the kwargs for network.BgpPeer
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    peer_group = module.params['peer_group']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    # create the new state object
    new_obj = network.BgpPeer(**obj_spec)

    changed = False
    try:
        # Create the device with the appropriate pandevice type
        device = base.PanDevice.create_from_device(*auth)
        network.VirtualRouter.refreshall(device)

        # grab the virtual router
        vr = device.find(vr_name, network.VirtualRouter)
        if vr is None:
            raise ValueError('Virtual router {0} does not exist'.format(vr_name))

        # grab the peer group
        pg = vr.find(peer_group, network.BgpPeerGroup, recursive=True)
        if pg is None and state == 'present':
            raise ValueError('Peer group {0} does not exist'.format(peer_group))

        # fetch the current settings
        cur_obj = None
        if pg is not None:
            cur_obj = pg.find(name, network.BgpPeer)

        # compare differences between the current state vs desired state
        if state == 'present':
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=False):
                pg.add(new_obj)
                new_obj.apply()
                changed = True
        elif state == 'absent':
            if cur_obj is not None:
                cur_obj.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='BGP peer update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
