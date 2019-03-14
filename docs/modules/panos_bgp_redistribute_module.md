---
title: panos_bgp_redistribute
---
# panos_bgp_redistribute

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring a BGP Redistribution Rules.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP Aggregate Policy |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| | | | | | |
| address_family_identifier | str |  | ipv4 | ['ipv4', 'ipv6'] | Address Family Identifier |
| enable | bool |  | True |  | Enable rule |
| metric | int |  |  |  | Metric value |
| name | str | True |  |  | Name of rule; must match a defined Redistribution Profile in the virtual router |
| route_table | str |  | unicast | ['unicast', 'multicast', 'both'] | Summarize route |
| set_as_path_limit | int |  |  |  | Add the AS_PATHLIMIT path attribute |
| set_community | list |  |  |  | Add the COMMUNITY path attribute |
| set_extended_community | list |  |  |  | Add the EXTENDED COMMUNITY path attribute |
| set_local_preference | int |  |  |  | Add the LOCAL_PREF path attribute |
| set_med | int |  |  |  | Add the MULTI_EXIT_DISC path attribute |
| set_origin | str |  | incomplete | ['igp', 'egp', 'incomplete'] | New route origin |
| | | | | | |

## Examples

    - name: Create BGP Redistribution Rule
      panos_bgp_redistribute:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: redist-rule-01
        enable: false

    - name: Update BGP Redistribution Rule
      panos_bgp_redistribute:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: redist-rule-01
        enable: true
        set_as_path_limit: 255

    - name: Remove BGP Redistribution Rule
      panos_bgp_redistribute:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: redist-rule-01

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

