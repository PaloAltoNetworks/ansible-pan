---
title: panos_api_key
---
# panos_admin

_(versionadded:: 2.3)_


## Synopsis

PanOS module that allows fetching the api_key for a user account by doing API calls to the Firewall using pan-api as the protocol.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |

## Examples

    # Get the api_key of user admin
      - name: retrieve admin api_key
        panos_admin:
          ip_address: "192.168.1.1"
          password: "admin"
        register: auth

      - name: show system info
        panos_op:
          ip_address: "192.168.1.1"
          api_key: '{{ auth.api_key }}'
          cmd: show system info
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |
| api_key | api key string | success | string | LUFRPT14MW5xOEo1R09KVlBZNnpnemh0VHRBOWl6TGM9bXcwM3JHUGVhRlNiY0dCR0srNERUQT09 |

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

