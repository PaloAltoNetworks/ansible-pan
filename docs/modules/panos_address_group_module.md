---
title: panos_address_group
---
# panos_address_group

_(versionadded:: 2.8)_


## Synopsis

Create address group objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| commit |  | True |  | Commit changes after creating object.  If *ip_address* is a Panorama device, and *device_group* is also set, perform a commit to Panorama and a commit-all to the device group. |
| description |  |  |  | Descriptive name for this address group. |
| device_group |  |  |  | If *ip_address* is a Panorama device, create object in this device group. |
| dynamic_value |  |  |  | Registered IP tags for a dynamic address group. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of address group to create. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove address group object. |
| static_value |  |  |  | List of address objects to be included in the group. |
| tag |  |  |  | List of tags to add to this address group. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| vsys |  | vsys1 |  | If *ip_address* is a firewall, create object in this virtual system. |

## Examples

    - name: Create object group 'Prod'
      panos_address_group:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'Prod'
        static_value: ['Test-One', 'Test-Three']
        tag: ['Prod']
    
    - name: Create object group 'SI'
      panos_address_group:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'SI'
        dynamic_value: "'SI_Instances'"
        tag: ['SI']
    
    - name: Delete object group 'SI'
      panos_address_group:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'SI'
        state: 'absent'

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

