---
title: panos_registered_ip_facts
---
# panos_registered_ip_facts

_(versionadded:: 2.7)_


## Synopsis

Retrieves tag information about registered IPs on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| tags |  |  |  | List of tags to retrieve facts for.  If not specified, retrieve all tags. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |

## Examples

    - name: Get facts for all registered IPs
      panos_registered_ip_facts:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
      register: registered_ip_facts
    
    - name: Get facts for specific tag
      panos_registered_ip_facts:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        tags: ['First_Tag']
      register: first_tag_registered_ip_facts
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| results | IP addresses as keys, tags as values. | always | dict | {'1.1.1.1': ['First_Tag', 'Second_Tag']} |

#### Notes

- Panorama is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

