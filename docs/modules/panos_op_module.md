---
title: panos_op
---
# panos_op

_(versionadded:: 2.5)_


## Synopsis

This module will allow user to pass and execute any supported OP command on the PANW device.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| cmd | yes |  |  | The OP command to be performed. |
| cmd_is_xml |  |  |  | The cmd is already given in XML format, so don't convert it. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device or Panorama management console being configured. |
| password | yes |  |  | Password credentials to use for authentication. |
| username |  | admin |  | Username credentials to use for authentication. |

## Examples

    - name: show list of all interfaces
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show interfaces all'
    
    - name: show system info
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show system info'
    
    - name: show system info as XML command
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: '<show><system><info/></system></show>'
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| stdout_xml | output of the given OP command as JSON formatted string | success | string | <response status=success><result><system><hostname>fw2</hostname> |
| stdout | output of the given OP command as JSON formatted string | success | string | {system: {app-release-date: 2017/05/01  15:09:12}} |

#### Notes

- Checkmode is NOT supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

