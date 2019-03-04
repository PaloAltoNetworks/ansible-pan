---
title: panos_redistribution
---
# panos_redistribution

_(versionadded:: 2.9)_

## Synopsis

PanOS module for configuring a Redistribution Profile.

## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove Route Redistribution Rule |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| type | str |  | ipv4 | ['ipv4', 'ipv6'] | Name of rule |
| | | | | | |
| action | str |  | no-redist | ['no-redist', 'redist'] | Rule action |
| bgp_filter_community | list |  |  |  | BGP filter on community |
| bgp_filter_extended_community | list |  |  |  | BGP filter on extended community |
| filter_destination | list |  |  |  | Filter destination |
| filter_interface | list |  |  |  | Filter interface |
| filter_nexthop | list |  |  |  | Filter nexthop |
| filter_type | list |  |  |  | Any of 'static', 'connect', 'rip', 'ospf', or 'bgp' |
| name | str | True |  |  | Name of rule |
| ospf_filter_area | list |  |  |  | OSPF filter on area |
| ospf_filter_pathtype | list |  |  |  | Any of 'intra-area', 'inter-area', 'ext-1', or 'ext-2' |
| ospf_filter_tag | list |  |  |  | OSPF filter on tag |
| priority | int |  |  |  | Priority ID |
| | | | | | |

## Examples

    - name: Create Redistribution Profile
      panos_redistribution:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: redist-01
        priority: 10
        filter_type:
          - static
          - rip

    - name: Remove Redistribution Profile
      panos_redistribution:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: redist-01

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

