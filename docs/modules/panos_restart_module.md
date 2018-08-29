# panos_restart

_(versionadded:: 2.3)_


## Synopsis

Restart a device either through Panorama or going directly to a firewall.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of <em>username</em>/<em>password</em> credentials. |
| devicegroup |  | None |  | Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.If device group is not define we assume that we are contacting Firewall. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| password |  |  |  | Password credentials to use for auth unless <em>api_key</em> is set. |
| username |  | admin |  | Username credentials to use for auth unless <em>api_key</em> is set. |

## Examples

    - panos_restart:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

