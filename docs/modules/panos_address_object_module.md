---
title: panos_address_object
---
# panos_address_object

_(versionadded:: 2.8)_


## Synopsis

Create address objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| address_type |  | ip-netmask | ip-netmask, ip-range, fqdn | Type of address object. |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| commit |  | True |  | Commit changes after creating object.  If *ip_address* is a Panorama device, and *device_group* is also set, perform a commit to Panorama and a commit-all to the device group. |
| description |  |  |  | Descriptive name for this address object. |
| device_group |  |  |  | If *ip_address* is a Panorama device, create object in this device group. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of object to create. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove address object. |
| tag |  |  |  | List of tags to add to this address object. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| value | yes |  |  | IP address, IP range, or FQDN for the object.  Must specify if state is *present*. |
| vsys |  | vsys1 |  | If *ip_address* is a firewall, create object in this virtual system. |

## Examples

    - name: Create object 'Test-One'
      panos_address_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-One'
        value: '1.1.1.1'
        description: 'Description One'
        tag: ['Prod']
    
    - name: Create object 'Test-Two'
      panos_address_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Two'
        address_type: 'ip-range'
        value: '1.1.1.1-2.2.2.2'
        description: 'Description Two'
        tag: ['SI']
    
    - name: Create object 'Test-Three'
      panos_address_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Three'
        address_type: 'fqdn'
        value: 'foo.bar.baz'
        description: 'Description Three'
    
    - name: Delete object 'Test-Two'
      panos_address_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Two'
        state: 'absent'

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

