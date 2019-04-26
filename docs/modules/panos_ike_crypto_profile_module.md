---
title: panos_ike_crypto_profile
---
# panos_ike_crypto_profile

_(versionadded:: 2.8)_


## Synopsis

Use the IKE Crypto Profiles page to specify protocols and algorithms for identification, authentication, and
encryption (IKEv1 or IKEv2, Phase 1).


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| state |  | present | present, absent | Create or remove IKE profile. |
| commit |  | True |  | Commit configuration if changed. |
| name | yes |  |  | Name for the profile. |
| dh_group |  | ['group2'] | group1, group2, group5, group14, group19, group20 | Specify the priority for Diffie-Hellman (DH) groups. |
| authentication |  | ['sha1'] | md5, sha1, sha256, sha384, sha512 | Authentication hashes used for IKE phase 1 proposal. |
| encryption |  | ['aes-256-cbc', '3des'] | des, 3des, aes-128-cbc, aes-192-cbc, aes-256-cbc | Encryption algorithms used for IKE phase 1 proposal. |
| lifetime_seconds |  |  |  | IKE phase 1 key lifetime in seconds. |
| lifetime_minutes |  |  |  | IKE phase 1 key lifetime in minutes. |
| lifetime_hours |  | 8 |  | IKE phase 1 key lifetime in hours. If no other key lifetime is specified, default to 8 hours. |
| lifetime_days |  |  |  | IKE phase 1 key lifetime in days. |

## Examples

    - name: Add IKE crypto config to the firewall
        panos_ike_crypto_profile:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'vpn-0cc61dd8c06f95cfd-0'
          dh_group: ['group2']
          authentication: ['sha1']
          encryption: ['aes-128-cbc']
          lifetime_seconds: '28800'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

