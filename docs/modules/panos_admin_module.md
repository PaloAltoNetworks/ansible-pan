---
title: panos_admin
---
# panos_admin

_(versionadded:: 2.3)_


## Synopsis

PanOS module that allows changes to the user account passwords by doing API calls to the Firewall using pan-api as the protocol.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| admin_password | yes |  |  | New password for *admin_username* user |
| admin_username |  | admin |  | Username that needs password change. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | Commit configuration if changed. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| role |  |  |  | role for admin user |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |

## Examples

    # Set the password of user admin to "badpassword"
    # Doesn't commit the candidate config
      - name: set admin password
        panos_admin:
          ip_address: "192.168.1.1"
          password: "admin"
          admin_username: admin
          admin_password: "badpassword"
          commit: False
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

