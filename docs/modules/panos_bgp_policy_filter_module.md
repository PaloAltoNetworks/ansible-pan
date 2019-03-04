---
title: panos_bgp_policy_filter
---
# panos_bgp_policy_filter

_(versionadded:: 2.9)_

## Synopsis

PanOS module for configuring BGP Policy *Non-Exist*, *Advertise*, and *Suppress* Filters

## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent', 'return-object'] | Add or remove BGP Policy Filter |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| filter_type | str | True |  | ['non-exist', 'advertise', 'suppress'] | The type of filter |
| policy_name | str |  |  |  | The name of the policy object |
| policy_type | str | True |  | ['conditional-advertisement', 'aggregate'] | The type of policy object |
| | | | | | |
| address_prefix | list |  |  |  | List of Address Prefix objects |
| enable | bool |  | True |  | Enable filter |
| match_afi | str |  |  | ['ip', 'ipv6'] | Address Family Identifier |
| match_as_path_regex | str |  |  |  | AS-path regular expression |
| match_community_regex | str |  |  |  | Community AS-path regular expression |
| match_extended_community_regex | str |  |  |  | Extended Community AS-path regular expression |
| match_from_peer | list |  |  |  | Filter by peer that sent this route |
| match_med | int |  |  |  | Multi-Exit Discriminator |
| match_nexthop | list |  |  |  | Next-hop attributes |
| match_route_table | str |  | unicast | ['unicast', 'multicast', 'both'] | Route table to match rule |
| match_safi | str |  |  | ['ip', 'ipv6'] | Subsequent Address Family Identifier |
| name | str | True |  |  | Name of filter |
| | | | | | |

## Special Accomodations

This module has an extra choice for the state argument called *return-object*. Passing this state will cause the module to generate a filter object matching the given arguments, then return it as a serialized string in the *panos_obj* key of the return object. See [panos_bgp_conditional_advertisement](panos_bgp_conditional_advertisement_module.md) for examples.

## Examples

    - name: Return BGP Advertise Policy Filter Object
      panos_bgp_policy_filter:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: return-object
        vr_name: default
        name: ad-filter-01
        enable: false
        filter_type: advertise
        policy_type: conditional-advertisement
        policy_name: cond-advert-01
        address_prefix:
          - name: 10.1.1.0/24
      register: ad_filter
        
    - name: Create BGP Advertise Policy Filter
      panos_bgp_policy_filter:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: present
        vr_name: default
        name: ad-filter-02
        enable: false
        filter_type: advertise
        policy_type: conditional-advertisement
        policy_name: cond-advert-01
        address_prefix:
          - name: 10.2.1.0/24

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |
| panos_obj | serialized filter object | when state == 'return-object' | string | |

#### Notes

- Checkmode is not supported.

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

