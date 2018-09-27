---
title: panos_administrator
---
# panos_administrator

_(versionadded:: 2.8)_


## Synopsis

Manages PAN-OS administrator user accounts.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| admin_password |  |  |  | New plain text password for the *admin_username* user.If this is not specified, then the password is left as-is. |
| admin_username |  | admin |  | Admin name. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| authentication_profile |  |  |  | The authentication profile. |
| commit |  | True |  | Commit configuration if changed. |
| device_admin |  |  |  | Admin type - device admin |
| device_admin_read_only |  |  |  | Admin type - device admin, read only |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| panorama_admin |  |  |  | This is for Panorama only.Make the user a Panorama admin only |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| password_profile |  |  |  | The password profile for this user. |
| role_profile |  |  |  | The role based profile. |
| ssh_public_key |  |  |  | Use public key authentication (ssh) |
| state |  | present |  | The state.  Can be either *present*/*absent*. |
| superuser |  |  |  | Admin type - superuser |
| superuser_read_only |  |  |  | Admin type - superuser, read only |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| vsys |  |  |  | This is for multi-vsys physical firewalls only.The list of vsys this admin should manage. |
| vsys_read_only |  |  |  | This is for multi-vsys physical firewalls only.The list of vsys this read only admin should manage. |
| web_client_cert_only |  |  |  | Use only client certificate authenciation (Web) |

## Examples

    # Configure user "foo"
    # Doesn't commit the candidate config
      - name: configure foo administrator
        panos_administrator:
          ip_address: "192.168.1.1"
          password: "admin"
          admin_username: 'foo'
          admin_password: 'secret'
          superuser: true
          commit: false
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | done |

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

