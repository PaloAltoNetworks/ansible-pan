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
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| authentication |  | sha1 |  | Specify the priority for hash algorithms. |
| commit |  | True |  | Commit configuration if changed. |
| dhgroup |  | group2 |  | Specify the priority for Diffie-Hellman (DH) groups. |
| encryption |  | [u'aes-256-cbc', u'3des'] |  | Select the appropriate Encapsulating Security Payload (ESP) authentication options. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| lifetime_sec |  | 28800 |  | Select unit of time and enter the length of time that the negotiated IKE Phase 1 key will be effective. |
| name | yes |  |  | Name for the profile. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| state |  | present | present, absent | Create or remove static route. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

    - name: Add IKE crypto config to the firewall
        panos_ike_crypto_profile:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          state: 'present'
          name: 'IKE-Ansible'
          dhgroup: 'group2'
          authentication: 'sha1'
          encryption: ['aes-256-cbc', '3des']
          lifetime_sec: '28800'
          commit: 'False'

#### Notes

- Checkmode is not supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

