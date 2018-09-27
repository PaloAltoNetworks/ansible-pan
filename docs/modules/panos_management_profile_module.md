---
title: panos_management_profile
---
# panos_management_profile

_(versionadded:: 2.6)_


## Synopsis

This module will allow you to manage interface management profiles on PAN-OS.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice
- xmltodict can be obtained from PyPI https://pypi.python.org/pypi/xmltodict

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | Perform a commit if a change is made. |
| http |  |  |  | Enable http |
| http_ocsp |  |  |  | Enable http-ocsp |
| https |  |  |  | Enable https |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device or Panorama management console being configured. |
| name | yes |  |  | The management profile name. |
| panorama_template |  |  |  | The template name (required if 'ip_address' is a Panorama); ignored if 'ip_address' is a firewall. |
| password |  |  |  | Password credentials to use for authentication. |
| permitted_ip |  |  |  | The list of permitted IP addresses |
| ping |  |  |  | Enable ping |
| response_pages |  |  |  | Enable response pages |
| snmp |  |  |  | Enable snmp |
| ssh |  |  |  | Enable ssh |
| state |  | present |  | The state.  Can be either *present*/*absent*. |
| telnet |  |  |  | Enable telnet |
| userid_service |  |  |  | Enable userid service |
| userid_syslog_listener_ssl |  |  |  | Enable userid syslog listener ssl |
| userid_syslog_listener_udp |  |  |  | Enable userid syslog listener udp |
| username |  | admin |  | Username credentials to use for authentication. |

## Examples

    - name: ensure mngt profile foo exists and allows ping and ssh and commit
      panos_management_profile:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'foo'
        ping: true
        ssh: true
    
    - name: make sure mngt profile bar does not exist without doing a commit
      panos_management_profile:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'bar'
        state: 'absent'
        commit: false

#### Notes

- Checkmode is NOT supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

