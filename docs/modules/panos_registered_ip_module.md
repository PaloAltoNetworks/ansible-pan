---
title: panos_registered_ip
---
# panos_registered_ip

_(versionadded:: 2.7)_


## Synopsis

Registers tags for IP addresses that can be used to build dynamic address groups.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| ips | yes |  |  | List of IP addresses to register/unregister. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove registered IP addresses. |
| tags | yes |  |  | List of tags that the IP address will be registered to. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |

## Examples

    - name: Add 'First_Tag' tag to 1.1.1.1
      panos_registered_ip:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        ips: ['1.1.1.1']
        tags: ['First_Tag']
        state: 'present'
    
    - name: Add 'First_Tag' tag to 1.1.1.2
      panos_registered_ip:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        ips: ['1.1.1.2']
        tags: ['First_Tag']
        state: 'present'
    
    - name: Add 'Second_Tag' tag to 1.1.1.1
      panos_registered_ip:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        ips: ['1.1.1.1']
        tags: ['Second_Tag']
        state: 'present'
    
    - name: Remove 'Second_Tag' from 1.1.1.1
      panos_registered_ip:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        ips: ['1.1.1.1']
        tags: ['Second_Tag']
        state: 'absent'
    
    - name: Remove 'First_Tag' from 1.1.1.2 (will unregister entirely)
      panos_registered_ip:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        ips: ['1.1.1.2']
        tags: ['First_Tag']
        state: 'absent'
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| results | After performing action, returns tags for given IPs.  IP addresses as keys, tags as values. | always | dict | {'1.1.1.1': ['First_Tag', 'Second_Tag']} |

#### Notes

- Checkmode is not supported.
- Panorama is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

