---
title: panos_bgp_peer
---
# panos_bgp_peer

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring a BGP Peer in a peer group.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP peer configuration |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| peer_group | str | True |  |  | Name of the peer group; it must already exist; see panos_bgp_peer_group |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| | | | | | |
| address_family_identifier | str |  |  | ['ipv4', 'ipv6'] | Peer address family type |
| bfd_profile | str |  |  |  | BFD profile configuration |
| connection_authentication | str |  |  |  | BGP auth profile name |
| connection_hold_time | int |  |  |  | Hold time (in seconds) |
| connection_idle_hold_time | int |  |  |  | Idle hold time (in seconds) |
| connection_incoming_allow | bool |  |  |  | Allow incoming connections |
| connection_incoming_remote_port | int |  |  |  | Restrict remote port for incoming BGP connections |
| connection_keep_alive_interval | int |  |  |  | Keep-alive interval (in seconds) |
| connection_min_route_adv_interval | int |  |  |  | Minimum Route Advertisement Interval (in seconds) |
| connection_multihop | int |  |  |  | IP TTL value used for sending BGP packet. set to 0 means eBGP use 2, iBGP use 255 |
| connection_open_delay_time | int |  |  |  | Open delay time (in seconds) |
| connection_outgoing_allow | bool |  |  |  | Allow outgoing connections |
| connection_outgoing_local_port | int |  |  |  | Use specific local port for outgoing BGP connections |
| enable | bool |  | True |  | Enable BGP Peer |
| enable_mp_bgp | bool |  |  |  | Enable MP-BGP extentions |
| enable_sender_side_loop_detection | bool |  |  |  | Enable sender side loop detection |
| local_interface | str |  |  |  | Interface to accept BGP session |
| local_interface_ip | str |  |  |  | Specify exact IP address if interface has multiple addresses |
| max_prefixes | int |  |  |  | Maximum of prefixes to receive from peer |
| name | str | True |  |  | Name of BGP Peer |
| peer_address_ip | str |  |  |  | IP address of peer |
| peer_as | str |  |  |  | Peer AS number |
| peering_type | str |  |  | ['unspecified', 'bilateral'] | Peering type |
| reflector_client | str |  |  | ['non-client', 'client', 'meshed-client'] | Reflector client type |
| subsequent_address_multicast | bool |  |  |  | Select SAFI for this peer |
| subsequent_address_unicast | bool |  |  |  | Select SAFI for this peer |

## Examples

    # Add a BGP peer to a group
      - name: Create BGP peer
        panos_bgp_peer:
          ip_address: "192.168.1.1"
          password: "admin"
          state: present
          vr_name: default
          name: peer-1
          enable: true
          local_interface: ethernet1/1
          peer_as: 64550


#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

