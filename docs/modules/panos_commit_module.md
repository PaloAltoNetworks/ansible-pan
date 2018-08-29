---
title: panos_commit
---
# panos_commit

_(versionadded:: 2.3)_


## Synopsis

PanOS module that will commit firewall's candidate configuration on
the device. The new configuration will become active immediately.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of <em>username</em>/<em>password</em> credentials. |
| devicegroup |  |  |  | The Panorama device group to be committed. |
| ip_address | yes |  |  | The IP address (or hostname) of the PAN-OS device or Panorama management console. |
| password | yes |  |  | Password credentials to use for authentication. |
| username |  | admin |  | Username credentials to use for authentication. |

## Examples

    - name: commit candidate config on firewall
      panos_commit:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
    
    - name: commit candidate config on Panorama using api_key
      panos_commit:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        devicegroup: 'Cloud-Edge'
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | Commit successful |




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

