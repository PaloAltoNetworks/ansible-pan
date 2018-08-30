---
title: panos_userid
---
# panos_userid

_(versionadded:: 2.6)_


## Synopsis

Userid allows for user to IP mapping that can be used in the policy rules.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| operation |  | register |  | The action to be taken.  Supported values are *login*/*logout*. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| register_ip | yes |  |  | ip of the user's machine that needs to be registered with userid. |
| userid | yes |  |  | User UPN |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

      - name: register user ivanb to 10.0.1.101
        panos_userid:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'login'
          userid: 'ACMECORP\ivanb'
          register_ip: '10.0.1.101'

#### Notes

- Checkmode is not supported.
- Panorama is not supported.
- This operation is runtime and does not require explicit commit of the firewall configuration.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

