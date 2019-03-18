---
title: panos_ipsec_profile
---
# panos_ipsec_profile

_(versionadded:: 2.8)_


## Synopsis

IPSec Crypto profiles specify protocols and algorithms for authentication and encryption in VPN tunnels based on
IPSec SA negotiation (Phase 2).


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
| name | yes |  |  | Name for the profile. |
| esp_encryption |  | [u'aes-256-cbc', u'3des'] | des, 3des, null, aes-128-cbc, aes-192-cbc, aes-256-cbc, aes-128-gcm, aes-256-gcm | Encryption algorithms for ESP mode. |
| esp_authentication |  | sha1 | none, md5, sha1, sha256, sha384, or sha512 | Authentication algorithms for ESP mode. |
| ah_authentication |  |  | md5, sha1, sha256, sha384, or sha512 | Authentication algorithms for AH mode. |
| dh_group |  | group2 | no-pfs, group1, group2, group5, group14, group19, group20 | Diffie-Hellman (DH) groups. |
| lifetime_seconds |  |  |  | IPSec SA lifetime in seconds. |
| lifetime_minutes |  |  |  | IPSec SA lifetime in minutes. |
| lifetime_hours |  |  |  | IPSec SA lifetime in hours.  If no other key lifetimes are specified, default to 1 hour. |
| lifetime_days |  |  |  | IPSec SA lifetime in days. |
| lifesize_kb |  |  |  | IPSec SA lifetime in kilobytes. |
| lifesize_mb |  |  |  | IPSec SA lifetime in megabytes. |
| lifesize_gb |  |  |  | IPSec SA lifetime in gigabytes. |
| lifesize_tb |  |  |  | IPSec SA lifetime in terabytes. |
| state |  | present | present, absent | Create or remove IPsec profile. |
| commit |  | True |  | Commit configuration if changed. |

## Examples

    - name: Add IPSec crypto config to the firewall
        panos_ipsec_profile:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'ipsec-vpn-0cc61dd8c06f95cfd-0'
          esp_authentication: 'sha1'
          esp_encryption: 'aes-128-cbc'
          lifetime_seconds: '3600'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

