---
title: panos_bgp
---
# panos_bgp

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring basic BGP in a virtual router.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP peer configuration |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist |
| | | | | | |
| aggregate_med | bool |  | True |  | Aggregate route only if they have same MED attributes |
| allow_redist_default_route | bool |  | False |  | Allow redistribute default route to BGP |
| always_compare_med | bool |  | False |  | Always compare MEDs |
| as_format | str |  | 2-byte | ['2-byte', '4-byte'] | AS format I("2-byte")/I("4-byte") |
| confederation_member_as | str |  |  |  | Confederation requires member-AS number |
| default_local_preference | int |  |  |  | Default local preference |
| deterministic_med_comparison | bool |  | True |  | Deterministic MEDs comparison |
| ecmp_multi_as | bool |  | False |  | Support multiple AS in ECMP |
| enable | bool |  | True |  | Enable BGP |
| enforce_first_as | bool |  | True |  | Enforce First AS for EBGP |
| gr_local_restart_time | int |  |  |  | Local restart time to advertise to peer (in seconds) |
| gr_max_peer_restart_time | int |  |  |  | Maximum of peer restart time accepted (in seconds) |
| gr_stale_route_time | int |  |  |  | Time to remove stale routes after peer restart (in seconds) |
| graceful_restart_enable | bool |  | True |  | Enable graceful restart |
| install_route | bool |  | False |  | Populate BGP learned route to global route table |
| local_as | str |  |  |  | Local Autonomous System (AS) number |
| reflector_cluster_id | str |  |  |  | Route reflector cluster ID |
| reject_default_route | bool |  | True |  | Reject default route |
| router_id | str |  |  |  | Router ID in IP format (eg. 1.1.1.1) |
| | | | | | |

## Examples

    # Turn on basic BGP routing
      - name: Enable BGP in Virtual Router
        panos_bgp:
          ip_address: "192.168.1.1"
          password: "admin"
          state: present
          vr_name: default
          enable: true
          router_id: 10.1.1.1
          local_as: 64555
          install_route: true

      - name: Disable BGP in Virtual Router
        panos_bgp:
          ip_address: "192.168.1.1"
          password: "admin"
          state: absent
          vr_name: default
          enable: false


#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

