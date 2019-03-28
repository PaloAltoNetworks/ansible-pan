---
title: panos_bgp_auth
---
# panos_bgp_auth

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring a BGP Authentication Profiles.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP Authentication Profile |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| replace | bool |  | False |  | The secret is encrypted so the state cannot be compared; this option forces removal of a matching item before applying the new config |
| | | | | | |
| name | str | True |  |  | Name of Authentication Profile |
| secret | str |  |  |  | Secret |
| | | | | | |

## Examples

    - name: Create BGP Auth Profile
      panos_bgp_auth:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        name: auth-profile-01
        secret: '{{ bgp_auth_secret }}'

    - name: Update BGP Auth Profile
      panos_bgp_auth:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        replace: true
        name: auth-profile-01
        secret: '{{ bgp_auth_secret }}'

    - name: Remove BGP Auth Profile
      panos_bgp_auth:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: auth-profile-01


#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

