---
title: panos_bgp_aggregate
---
# panos_bgp_aggregate

_(versionadded:: 2.9)_


## Synopsis

PanOS module for configuring a BGP Aggregation Rules.


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
| as_set | bool |  | False |  | Generate AS-set attribute |
| attr_as_path_limit | int |  |  |  | Add AS path limit attribute if it does not exist |
| attr_as_path_prepend_times | int |  |  |  | Prepend local AS for specified number of times |
| attr_as_path_type | str |  | none | ['none', 'remove', 'prepend', 'remove-and-prepend'] | AS path update options |
| attr_community_argument | str |  |  |  | Argument to the action community value if needed |
| attr_community_type | str |  | none | ['none', 'remove-all', 'remove-regex', 'append', 'overwrite'] | Community update options |
| attr_extended_community_argument | str |  |  |  | Argument to the action extended community value if needed |
| attr_extended_community_type | str |  | none | ['none', 'remove-all', 'remove-regex', 'append', 'overwrite'] | Extended community update options |
| attr_local_preference | int |  |  |  | New Local Preference value |
| attr_med | int |  |  |  | New Multi-Exit Discriminator value |
| attr_nexthop | list |  |  |  | Next-hop address |
| attr_origin | str |  | incomplete | ['igp', 'egp', 'incomplete'] | New route origin |
| attr_weight | int |  |  |  | New weight value |
| enable | bool |  | True |  | Enable policy |
| name | str | True |  |  | Name of policy |
| prefix | str |  |  |  | Aggregating address prefix |
| summary | bool |  |  |  | Summarize route |
| | | | | | |

## Examples

    - name: Create BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        name: aggr-rule-01
        prefix: 10.0.0.0/24
        enable: true
        summary: true

    - name: Update BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        name: aggr-rule-01
        prefix: 10.0.0.0/24
        enable: true
        summary: true
        attr_med: 10
        attr_as_path_type: prepend
        attr_as_path_prepend_times: 1

    - name: Disable BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        vr_name: default
        name: aggr-rule-01
        prefix: 10.0.0.0/24
        enable: false
        summary: true
        attr_med: 10
        attr_as_path_type: prepend
        attr_as_path_prepend_times: 1

    - name: Remove BGP Aggregation Rule
      panos_bgp_aggregate:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: aggr-rule-01


#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

