---
title: panos_bgp_conditional_advertisement
---
# panos_bgp_conditional_advertisement

_(versionadded:: 2.9)_

## Synopsis

PanOS module for configuring a BGP Conditional Advertisement Rules.

## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP Conditional Advertisement Policy |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| advertisement_filter | str |  |  |  | Advertisement filter object returned by panos_bgp_policy_filter; only needed on creation |
| non_exist_filter | str |  |  |  | Non-Exist filter object returned by panos_bgp_policy_filter; only needed on creation |
| | | | | | |
| enable | bool |  |  |  | Enable this policy |
| name | str | True |  |  | Name of Conditional Advertisement policy |
| used_by | list |  |  |  | List of Peer Groups using this policy |
| | | | | | |

## Special Requirements

This module has some special requirements when creating a new rule. Filters are child items which are managed by the *[panos_bgp_policy_filter](panos_bgp_policy_filter_module.md)* module, while this module requires two child filters to be defined at creation time. This creates a catch-22 situation where the rule cannot be created until the children are, but the children cannot be created because there is no parent object. To work around this situation, the *panos_bgp_policy_filter* module supports a special state of *return-object*. Calling *panos_bgp_policy_filter* with that state will return a serialized version of the pandevice filter object. The *panos_bgp_conditional_advertisement* accepts two arguments which allow passing those serialized filter objects for inclusion as the children during the creation phase.

## Examples

    # Creating a Conditional Advertisement Rule requires at least one Non Exist Filter
    # and one Advertisement Filter. Use the 'return-object' state of the *panos_bgp_policy_filter*
    # module to create a placeholder object to pass into the *panos_bgp_conditional_advertisement* module

    - name: Create BGP Non-Exist Filter for Conditional Advertisement
      panos_bgp_policy_filter:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: return-object
        vr_name: default
        name: ne-filter-01
        policy_name: cond-rule-01
        policy_type: conditional-advertisement
        filter_type: non-exist
        enable: true
        address_prefix:
          - name: 10.0.0.0/24
      register: non_exist

    - name: Create BGP Advertise Filter for Conditional Advertisement
      panos_bgp_policy_filter:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: return-object
        vr_name: default
        name: ad-filter-01
        policy_name: cond-rule-01
        policy_type: conditional-advertisement
        filter_type: advertise
        enable: true
        address_prefix:
          - name: 10.0.1.0/24
      register: advertise

    - name: Create BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: cond-rule-01
        enable: true
        non_exist_filter: '{{ non_exist.panos_obj }}'
        advertise_filter: '{{ advertise.panos_obj }}'

    - name: Update BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: cond-rule-01
        enable: false

    - name: Remove BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: cond-rule-01

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.
