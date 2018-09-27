---
title: panos_query_rules
---
# panos_query_rules

_(versionadded:: 2.5)_


## Synopsis

Security policies allow you to enforce rules and take action, and can be as general or specific as needed. The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches the traffic is applied, the more specific rules must precede the more general ones.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice
- xmltodict can be obtains from PyPI https://pypi.python.org/pypi/xmltodict

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| application |  | None |  | Name of the application or application group to be queried. |
| destination_ip |  | None |  | The destination IP address to be queried. |
| destination_port |  | None |  | The destination port to be queried. |
| destination_zone |  | None |  | Name of the destination security zone to be queried. |
| devicegroup |  | None |  | The Panorama device group in which to conduct the query. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS firewall or Panorama management console being queried. |
| password | yes |  |  | Password credentials to use for authentication. |
| protocol |  | None |  | The protocol used to be queried.  Must be either *tcp* or *udp*. |
| source_ip |  | None |  | The source IP address to be queried. |
| source_port |  | None |  | The source port to be queried. |
| source_zone |  | None |  | Name of the source security zone to be queried. |
| tag_name |  | None |  | Name of the rule tag to be queried. |
| username |  | admin |  | Username credentials to use for authentication. |

## Examples

    - name: search for rules with tcp/3306
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        source_zone: 'DevNet'
        destination_zone: 'DevVPC'
        destination_port: '3306'
        protocol: 'tcp'
    
    - name: search devicegroup for inbound rules to dmz host
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        destination_zone: 'DMZ'
        destination_ip: '10.100.42.18'
        address: 'DeviceGroupA'
    
    - name: search for rules containing a specified rule tag
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        tag_name: 'ProjectX'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

