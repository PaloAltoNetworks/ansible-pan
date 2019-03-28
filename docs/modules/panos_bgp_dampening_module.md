---
title: panos_bgp_dampening
---
# panos_bgp_dampening

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring a BGP Dampening Profile.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP Dampening Profile |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| cutoff | float |  |  |  | Cutoff threshold value |
| decay_half_life_reachable | int |  |  |  | Decay half-life while reachable (in seconds) |
| decay_half_life_unreachable | int |  |  |  | Decay half-life while unreachable (in seconds) |
| enable | bool |  | True |  | Enable profile |
| max_hold_time | int |  |  |  | Maximum of hold-down time (in seconds) |
| name | str | True |  |  | Name of Dampening Profile |
| reuse | float |  |  |  | Reuse threshold value |
| | | | | | |

## Examples

    - name: Create BGP Dampening Profile
      panos_bgp_dampening:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: damp-profile-01
        enable: true
        reuse: 1.0
        max_hold_time: 60

    - name: Update BGP Dampening Profile
      panos_bgp_dampening:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: damp-profile-01
        enable: true
        reuse: 0.5
        max_hold_time: 90

    - name: Disable BGP Dampening Profile
      panos_bgp_dampening:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: damp-profile-01
        enable: false
        reuse: 0.5
        max_hold_time: 90

    - name: Remove BGP Dampening Profile
      panos_bgp_dampening:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        state: absent
        name: damp-profile-01

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

