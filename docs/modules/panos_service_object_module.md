---
title: panos_service_object
---
# panos_service_object

_(versionadded:: 2.8)_


## Synopsis

Create service objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| commit |  | True |  | Commit changes after creating object.  If *ip_address* is a Panorama device, and *device_group* is also set, perform a commit to Panorama and a commit-all to the device group. |
| description |  |  |  | Descriptive name for this service object. |
| destination_port |  |  |  | Destination port of the service object.  Required if state is *present*. |
| device_group |  |  |  | If *ip_address* is a Panorama device, create object in this device group. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of service object. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| protocol |  | tcp | tcp, udp | Protocol of the service. |
| source_port |  |  |  | Source port of the service object. |
| state |  | present | present, absent | Create or remove service object. |
| tag |  |  |  | List of tags for this service object. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| vsys |  | vsys1 |  | If *ip_address* is a firewall, create object in this virtual system. |

## Examples

    - name: Create service object 'ssh-tcp-22'
      panos_service_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'ssh-tcp-22'
        destination_port: '22'
        description: 'SSH on tcp/22'
        tag: ['Prod']
    
    - name: Create service object 'mysql-tcp-3306'
      panos_service_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'mysql-tcp-3306'
        destination_port: '3306'
        description: 'MySQL on tcp/3306'
    
    - name: Delete service object 'mysql-tcp-3306'
      panos_service_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'mysql-tcp-3306'
        state: 'absent'

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

