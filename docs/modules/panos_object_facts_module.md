---
title: panos_object_facts
---
# panos_object_facts

_(versionadded:: 2.8)_


## Synopsis

Retrieves tag information objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of object to retrieve. |
| object_type | yes | address | address, address-group, service, service-group, tag | Type of object to retrieve. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |

## Examples

    - name: Retrieve address group object 'Prod'
      panos_object_facts:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'Prod'
        object_type: 'address-group'
      register: result
    
    - name: Retrieve service group object 'Prod-Services'
      panos_object_facts:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'Prod-Services'
        object_type: 'service-group'
      register: result
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| results | Dict containing object attributes.  Empty if object is not found. | always | dict |  |

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

