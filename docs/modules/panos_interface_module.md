---
title: panos_interface
---
# panos_interface

_(versionadded:: 2.3)_


## Synopsis

Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| adjust_tcp_mss |  |  |  | Adjust TCP MSS for layer3 interface. |
| aggregate_group |  |  |  | Aggregate interface name. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| comment |  |  |  | Interface comment. |
| commit |  | True |  | Commit if changed |
| create_default_route |  | false |  | Whether or not to add default route with router learned via DHCP. |
| dhcp_default_route_metric |  |  |  | Metric for the DHCP default route. |
| enable_dhcp |  | true |  | Enable DHCP on this interface. |
| if_name | yes |  |  | Name of the interface to configure. |
| ip |  |  |  | List of static IP addresses. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| ipv4_mss_adjust |  |  |  | (7.1+) TCP MSS adjustment for IPv4. |
| ipv6_enabled |  |  |  | Enable IPv6. |
| ipv6_mss_adjust |  |  |  | (7.1+) TCP MSS adjustment for IPv6. |
| link_duplex |  |  |  | Link duplex.  Supported values are *auto*/*full*/*half*. |
| link_speed |  |  |  | Link speed.  Supported values are *auto*/*10*/*100*/*1000*. |
| link_state |  |  |  | Link state.  Supported values are *auto*/*up*/*down*. |
| lldp_enabled |  |  |  | Enable LLDP for layer2 interface. |
| lldp_profile |  |  |  | LLDP profile name for layer2 interface. |
| management_profile |  |  |  | Interface management profile name. |
| mode |  | layer3 |  | The interface mode.Supported values are *layer3*/*layer2*/*virtual-wire*/*tap*/*ha*/*decrypt-mirror*/*aggregate-group* |
| mtu |  |  |  | MTU for layer3 interface. |
| netflow_profile |  |  |  | Netflow profile for layer3 interface. |
| netflow_profile_l2 |  |  |  | Netflow profile name for layer2 interface. |
| operation |  | add |  | The action to be taken.  Supported values are *add*/*update*/*delete*.This is used only if "state" is unspecified. |
| password |  |  |  | Password credentials to use for auth. |
| state |  |  |  | The state.  Can be either *present*/*absent*.If this is defined, then "operation" is ignored. |
| username |  | admin |  | Username credentials to use for auth. |
| vr_name |  | default |  | Name of the virtual router; it must already exist. |
| vsys_dg |  | vsys1 |  | Name of the vsys (if firewall) or device group (if panorama) to put this object. |
| zone_name | yes |  |  | Name of the zone for the interface. If the zone does not exist it is created.If the zone exists and it is not of the correct mode the operation will fail. |

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

