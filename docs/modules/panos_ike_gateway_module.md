---
title: panos_ike_gateway
---
# panos_ike_gateway

_(versionadded:: 2.8)_


## Synopsis

Use this to manage or define a gateway, including the configuration information necessary to perform Internet Key
Exchange (IKE) protocol negotiation with a peer gateway. This is the Phase 1 portion of the IKE/IPSec VPN setup.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | Commit configuration if changed. |
| crypto_profile_name |  | default |  | Select an existing profile or keep the default profile. |
| interface |  | ethernet1/1 |  | Specify the outgoing firewall interface to the VPN tunnel. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| liveness_check |  | 5 |  | The IKEv2 Liveness Check is always on; all IKEv2 packets serve the purpose of a liveness check. Usethis to have the system send empty informational packets after the peer has been idle for a number of sec. |
| name | yes |  |  | Name for the profile. |
| pasive_mode |  | True |  | True to have the firewall only respond to IKE connections and never initiate them. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| peer_ip_value |  | 127.0.0.1 |  | IPv4 address of the peer gateway. |
| protocol_version |  | ike2 |  | Specify the priority for Diffie-Hellman (DH) groups. |
| psk |  | CHANGEME |  | Specify pre-shared key. |
| state |  | present | present, absent | Create or remove static route. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

    - name: Add IKE gateway config to the firewall
        panos_ike_gateway:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'IKEGW-Ansible'
          protocol_version: 'ikev2'
          interface: 'ethernet1/1'
          pasive_mode: 'True'
          liveness_check: '5'
          peer_ip_value: '1.2.3.4'
          psk: 'CHANGEME'
          crypto_profile_name: 'IKE-Ansible'
          commit: 'False'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

