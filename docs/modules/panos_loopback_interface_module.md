---
title: panos_interface
---
# panos_interface

_(versionadded:: 2.0.2)_


## Synopsis

Configure loopback interfaces on a PaloAlto device.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| adjust_tcp_mss |  |  |  | Adjust TCP MSS for loopback interface. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| comment |  |  |  | Interface comment. |
| commit |  | True |  | Commit if changed |
| if_name | yes |  |  | Name of the interface to configure. |
| ip |  |  |  | List of static IP addresses. |
| ipv4_mss_adjust |  |  |  | (7.1+) TCP MSS adjustment for IPv4. |
| ipv6_enabled |  |  |  | Enable IPv6. |
| ipv6_mss_adjust |  |  |  | (7.1+) TCP MSS adjustment for IPv6. |
| management_profile |  |  |  | Interface management profile name. |
| mtu |  |  |  | MTU for layer3 interface. |
| netflow_profile |  |  |  | Netflow profile for loopback interface. |
| password |  |  |  | Password credentials to use for auth. |
| state |  |  |  | The state.  Can be either *present*/*absent*.If this is defined, then "operation" is ignored. |
| username |  | admin |  | Username credentials to use for auth. |
| vr_name |  | default |  | Name of the virtual router; it must already exist. |
| vsys_dg |  | vsys1 |  | Name of the vsys (if firewall) or device group (if panorama) to put this object. |
| zone_name | yes |  |  | Name of the zone for the interface. If the zone does not exist it is created.If the zone exists and it is not of the correct mode the operation will fail. |

## Examples

   # Delete loopback.1
   - name: delete loopback.1
    panos_loopback_interface:
      ip_address: "192.168.1.1"
      username: "ansible"
      password: "secret"
      if_name: "loopback.1"
      state: absent
    
    # Update/create loopback comment.
    - name: update loopback.1 comment
    panos_loopback_interface:
      ip_address: "192.168.1.1"
      username: "ansible"
      password: "secret"
      if_name: "loopback.1"
      ip: ["10.1.1.1/32"]
      comment: "Loopback iterface"
      state: present

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

