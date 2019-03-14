---
title: panos_ipsec_tunnel
---
# panos_ipsec_tunnel

_(versionadded:: 2.8)_


## Synopsis

Use IPSec Tunnels to establish and manage IPSec VPN tunnels between firewalls. This is the Phase 2 portion of the
IKE/IPSec VPN setup.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | Commit configuration if changed. |
| ike_gtw_name |  | default |  | Name of the existing IKE gateway. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| ipsec_profile |  | default |  | Name of the existing IPsec profile or use default. |
| name | yes |  |  | Name for the IPSec tunnel. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| state |  | present | present, absent | Create or remove static route. |
| tunnel_interface |  | tunnel.1 |  | Specify existing tunnel interface that will be used. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

    - name: Add IPSec tunnel to IKE gateway profile
        panos_ipsec_tunnel:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'IPSecTunnel-Ansible'
          tunnel_interface: 'tunnel.2'
          ike_gtw_name: 'IKEGW-Ansible'
          ipsec_profile: 'IPSec-Ansible'
          commit: 'False'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

