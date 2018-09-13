---
title: panos_ipsec_profile
---
# panos_ipsec_profile

_(versionadded:: 2.6)_


## Synopsis

IPSec Crypto profiles specify protocols and algorithms for authentication and encryption in VPN tunnels based on
IPSec SA negotiation (Phase 2).


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| authentication |  | sha1 |  | Specify the priority for hash algorithms. |
| commit |  | True |  | Commit configuration if changed. |
| dhgroup |  | group2 |  | Specify the priority for Diffie-Hellman (DH) groups. |
| encryption |  | [u'aes-256-cbc', u'3des'] |  | Select the appropriate Encapsulating Security Payload (ESP) authentication options. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| lifetime_hrs |  | 1 |  | Select units and enter the length of time (default is 1hr) that the negotiated key will stay effective. |
| name | yes |  |  | Name for the profile. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| state |  | present | present, absent | Create or remove static route. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

    - name: Add IPSec crypto config to the firewall
        panos_ipsec_profile:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'IPSec-Ansible'
          encryption: ['aes-256-cbc', '3des']
          authentication: 'sha1'
          dhgroup: 'group2'
          lifetime_hrs: '1'
          commit: 'False'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

