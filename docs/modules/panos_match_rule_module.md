---
title: panos_match_rule
---
# panos_match_rule

_(versionadded:: 2.5)_


## Synopsis

Security policies allow you to enforce rules and take action, and can be as general or specific as needed.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| application |  |  |  | The application. |
| category |  |  |  | URL category |
| destination_ip |  |  |  | The destination IP address. |
| destination_port |  |  |  | The destination port. |
| destination_zone |  |  |  | The destination zone. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| protocol |  |  |  | The IP protocol number from 1 to 255. |
| rule_type |  | security |  | Type of rule. Valid types are *security* or *nat*. |
| source_ip | yes |  |  | The source IP address. |
| source_port |  |  |  | The source port. |
| source_user |  |  |  | The source user or group. |
| source_zone |  |  |  | The source zone. |
| to_interface |  |  |  | The inbound interface in a NAT rule. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| vsys_id | yes | vsys1 |  | ID of the VSYS object. |

## Examples

    - name: check security rules for Google DNS
      panos_match_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_type: 'security'
        source_ip: '10.0.0.0'
        destination_ip: '8.8.8.8'
        application: 'dns'
        destination_port: '53'
        protocol: '17'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: check security rules inbound SSH with user match
      panos_match_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_type: 'security'
        source_ip: '0.0.0.0'
        source_user: 'mydomain\jsmith'
        destination_ip: '192.168.100.115'
        destination_port: '22'
        protocol: '6'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: check NAT rules for source NAT
      panos_match_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_type: 'nat'
        source_zone: 'Prod-DMZ'
        source_ip: '10.10.118.50'
        to_interface: 'ethernet1/2'
        destination_zone: 'Internet'
        destination_ip: '0.0.0.0'
        protocol: '6'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: check NAT rules for inbound web
      panos_match_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_type: 'nat'
        source_zone: 'Internet'
        source_ip: '0.0.0.0'
        to_interface: 'ethernet1/1'
        destination_zone: 'Prod DMZ'
        destination_ip: '192.168.118.50'
        destination_port: '80'
        protocol: '6'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: check security rules for outbound POP3 in vsys4
      panos_match_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vsys_id: 'vsys4'
        rule_type: 'security'
        source_ip: '10.0.0.0'
        destination_ip: '4.3.2.1'
        application: 'pop3'
        destination_port: '110'
        protocol: '6'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    

#### Notes

- Checkmode is not supported.
- Panorama NOT is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

