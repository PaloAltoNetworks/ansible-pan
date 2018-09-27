---
title: panos_service_group
---
# panos_service_group

_(versionadded:: 2.8)_


## Synopsis

Create service group objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| commit |  | True |  | Commit changes after creating object.  If *ip_address* is a Panorama device, and *device_group* is also set, perform a commit to Panorama and a commit-all to the device group. |
| device_group |  |  |  | If *ip_address* is a Panorama device, create object in this device group. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of service group. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove service group object. |
| tag |  |  |  | List of tags for this service group. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| value | yes |  |  | List of service objects to be included in the group.  Must specify if state is present. |
| vsys |  | vsys1 |  | If *ip_address* is a firewall, create object in this virtual system. |

## Examples

    - name: Create service group 'Prod-Services'
      panos_service_group:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'Prod-Services'
        value: ['ssh-tcp-22', 'mysql-tcp-3306']
    
    - name: Delete service group 'Prod-Services'
      panos_service_group:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        name: 'Prod-Services'
        state: 'absent'

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

