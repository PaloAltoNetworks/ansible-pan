---
title: panos_tunnel
---
# panos_tunnel

_(versionadded:: 2.9)_


## Synopsis

Configure tunnel network interface.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| comment |  |  |  | Interface comment. |
| commit |  | True |  | Commit if changed |
| if_name | yes |  |  | Name of the interface to configure. |
| ip |  |  |  | List of static IP addresses. |
| ipv6_enabled |  |  |  | Enable IPv6. |
| management_profile |  |  |  | Interface management profile name. |
| mtu |  |  |  | MTU for layer3 interface. |
| netflow_profile |  |  |  | Netflow profile for layer3 interface. |
| state |  | present |  | The state.  Can be either *present*/*absent*. |
| username |  | admin |  | Username credentials to use for auth. |
| vr_name |  | None |  | Name of the virtual router; it must already exist. |
| vsys_dg |  | vsys1 |  | Name of the vsys (if firewall) or device group (if panorama) to put this object. |
| zone_name |  | None |  | Name of the zone for the interface. If the zone does not exist it is created. If the zone exists and it is not of the correct mode the operation will fail. |

## Examples

```yaml
  - name: Create Tunnel Interface 'tunnel.1'
    panos_tunnel:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      if_name: tunnel.1

  - name: Create Tunnel Interface 'tunnel.2'
    panos_tunnel:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      if_name: tunnel.2
      ip: 192.168.27.21/30
      vr_name: default
      zone_name: ipsec_tunnel
      comment: IPSec connection to remote site
      management_profile: allow-ping
```

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

