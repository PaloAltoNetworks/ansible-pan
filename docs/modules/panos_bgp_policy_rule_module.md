---
title: panos_bgp_policy_rule
---
# panos_bgp_policy_rule

_(versionadded:: 2.9)_

## Synopsis

PanOS module for configuring BGP Policy Import and Export rules

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
| vr_name | str |  | default |  | Name of the virtual router; it must already exist; see panos_virtual_router |
| | | | | | |
| action | str |  |  | ['allow', 'deny'] | Rule action |
| action_as_path_limit | int |  |  |  | Add AS path limit attribute if it does not exist |
| action_as_path_prepend_times | int |  |  |  | Prepend local AS for specified number of times |
| action_as_path_type | str |  |  | ['none', 'remove', 'prepend', 'remove-and-prepend'] | AS path update options |
| action_community_argument | str |  |  |  | Argument to the action community value if needed |
| action_community_type | str |  |  | ['none', 'remove-all', 'remove-regex', 'append', 'overwrite'] | Community update options |
| action_dampening | str |  |  |  | Route flap dampening profile; only with "import" type |
| action_extended_community_argument | str |  |  |  | Argument to the action extended community value if needed |
| action_extended_community_type | str |  |  |  | Extended community update options |
| action_local_preference | int |  |  |  | New local preference value |
| action_med | int |  |  |  | New MED value |
| action_nexthop | str |  |  |  | Nexthop address |
| action_origin | str |  |  | ['igp', 'egp', 'incomplete'] | New route origin |
| action_weight | int |  |  |  | New weight value; only with "import" type |
| address_prefix | list |  |  |  | List of Address Prefix dicts with "name"/"exact" keys |
| enable | bool |  | True |  | Enable rule |
| match_afi | str |  |  | ['ip', 'ipv6'] | Address Family Identifier |
| match_as_path_regex | str |  |  |  | AS-path regular expression |
| match_community_regex | str |  |  |  | Community AS-path regular expression |
| match_extended_community_regex | str |  |  |  | Extended Community AS-path regular expression |
| match_from_peer | list |  |  |  | Filter by peer that sent this route |
| match_med | int |  |  |  | Multi-Exit Discriminator |
| match_nexthop | list |  |  |  | Next-hop attributes |
| match_route_table | str |  |  | ['unicast', 'multicast', 'both'] | Route table to match rule |
| match_safi | str |  |  | ['ip', 'ipv6'] | Subsequent Address Family Identifier |
| name | str | True |  |  | Name of filter |
| type | str | True |  | ['import', 'export'] | The type of rule |
| used_by | list |  |  |  | Peer-groups that use this rule |
| | | | | | |

## Examples

    - name: Create BGP Policy Import Rule
      panos_bgp_policy_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: present
        vr_name: default
        name: import-rule-001
        type: import
        enable: true
        action: allow
        action_dampening: dampening-profile

    - name: Create BGP Policy Export Rule
      panos_bgp_policy_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: present
        vr_name: default
        name: export-rule-001
        type: export
        enable: true
        action: allow

    - name: Disable BGP Import Rule
      panos_bgp_policy_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: present
        vr_name: default
        name: import-rule-001
        type: import
        enable: false

    - name: Remove BGP Export Rule
      panos_bgp_policy_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: export-rule-001
        type: export

#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.

#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.
