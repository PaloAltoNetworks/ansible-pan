# panos_interface

_(versionadded:: 2.3)_


## Synopsis

Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |

NOT suboptions
|adjust_tcp_mss|no||
Adjust TCP MSS for layer3 interface.
 |
NOT suboptions
|aggregate_group|no||
Aggregate interface name.
 |
NOT suboptions
|api_key|no||
API key that can be used instead of <em>username</em>/<em>password</em> credentials.
 |
NOT suboptions
|comment|no||
Interface comment.
 |
NOT suboptions
|commit|no||
Commit if changed
 |
NOT suboptions
|create_default_route|no||
Whether or not to add default route with router learned via DHCP.
 |
NOT suboptions
|dhcp_default_route_metric|no||
Metric for the DHCP default route.
 |
NOT suboptions
|enable_dhcp|no||
Enable DHCP on this interface.
 |
NOT suboptions
|if_name|yes||
Name of the interface to configure.
 |
NOT suboptions
|ip|no||
List of static IP addresses.
 |
NOT suboptions
|ip_address|yes||
IP address (or hostname) of PAN-OS device being configured.
 |
NOT suboptions
|ipv4_mss_adjust|no||
(7.1+) TCP MSS adjustment for IPv4.
 |
NOT suboptions
|ipv6_enabled|no||
Enable IPv6.
 |
NOT suboptions
|ipv6_mss_adjust|no||
(7.1+) TCP MSS adjustment for IPv6.
 |
NOT suboptions
|link_duplex|no||
Link duplex.  Supported values are <em>auto</em>/<em>full</em>/<em>half</em>.
 |
NOT suboptions
|link_speed|no||
Link speed.  Supported values are <em>auto</em>/<em>10</em>/<em>100</em>/<em>1000</em>.
 |
NOT suboptions
|link_state|no||
Link state.  Supported values are <em>auto</em>/<em>up</em>/<em>down</em>.
 |
NOT suboptions
|lldp_enabled|no||
Enable LLDP for layer2 interface.
 |
NOT suboptions
|lldp_profile|no||
LLDP profile name for layer2 interface.
 |
NOT suboptions
|management_profile|no||
Interface management profile name.
 |
NOT suboptions
|mode|no||
The interface mode.
Supported values are <em>layer3</em>/<em>layer2</em>/<em>virtual-wire</em>/<em>tap</em>/<em>ha</em>/<em>decrypt-mirror</em>/<em>aggregate-group</em>
 |
NOT suboptions
|mtu|no||
MTU for layer3 interface.
 |
NOT suboptions
|netflow_profile|no||
Netflow profile for layer3 interface.
 |
NOT suboptions
|netflow_profile_l2|no||
Netflow profile name for layer2 interface.
 |
NOT suboptions
|operation|no||
The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>delete</em>.
 |
NOT suboptions
|password|no||
Password credentials to use for auth.
 |
NOT suboptions
|username|no||
Username credentials to use for auth.
 |
NOT suboptions
|vr_name|no||
Name of the virtual router; it must already exist.
 |
NOT suboptions
|vsys_dg|no||
Name of the vsys (if firewall) or device group (if panorama) to put this object.
 |
NOT suboptions
|zone_name|yes||
Name of the zone for the interface. If the zone does not exist it is created.
If the zone exists and it is not of the correct mode the operation will fail.
 |

## Examples

    # Create ethernet1/1 as DHCP.
    - name: enable DHCP client on ethernet1/1 in zone public
      panos_interface:
        ip_address: "192.168.1.1"
        username: "ansible"
        password: "secret"
        if_name: "ethernet1/1"
        zone_name: "public"
        create_default_route: "yes"
    
    # Update ethernet1/2 with a static IP address in zone dmz.
    - name: ethernet1/2 as static in zone dmz
      panos_interface:
        ip_address: "192.168.1.1"
        username: "ansible"
        password: "secret"
        if_name: "ethernet1/2"
        mode: "layer3"
        ip: ["10.1.1.1/24"]
        enable_dhcp: false
        zone_name: "dmz"




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

