---
title: panos_bgp_peer_group
---
# panos_bgp_peer_group

_(versionadded:: 2.9)_

## Synopsis

PanOS module for configuring a BGP Peer Group.

## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP Peer Group configuration |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| | | | | | |
| aggregated_confed_as_path | bool |  |  |  | The peers understand Aggregated Confederation AS Path |
| enable | bool |  | True |  | Enable BGP peer group |
| export_nexthop | str |  | resolve | ['resolve', 'use-self'] | Export locally resolved nexthop I("resolve")/I("use-self") |
| import_nexthop | str |  | original | ['original', 'use-peer'] | Override nexthop with peer address I("original")/I("use-peer"), only with "ebgp" |
| name | str | True |  |  | Name of the BGP peer group |
| remove_private_as | bool |  |  |  | Remove private AS when exporting route, only with "ebgp" |
| soft_reset_with_stored_info | bool |  |  |  | Enable soft reset with stored info |
| type | str |  | ebgp | ['ebgp', 'ibgp', 'ebgp-confed', 'ibgp-confed'] | Peer group type I("ebgp")/I("ibgp")/I("ebgp-confed")/I("ibgp-confed") |
| | | | | | |

## Examples

    # Create a BGP peer group
      - name: Add peer group
        panos_bgp_peer_group:
          ip_address: "192.168.1.1"
          password: "admin"
          state: present
          vr_name: default
          name: peer-group-1
          enable: true
          aggregated_confed_as_path: true
          soft_reset_with_stored_info: false

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.
