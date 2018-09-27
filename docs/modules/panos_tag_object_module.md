---
title: panos_tag_object
---
# panos_tag_object

_(versionadded:: 2.8)_


## Synopsis

Create tag objects on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| color |  |  | red, green, blue, yellow, copper, orange, purple, gray, light green, cyan, light gray, blue gray, lime, black, gold, brown | Color for the tag. |
| comments |  |  |  | Comments for the tag. |
| device_group |  |  |  | If *ip_address* is a Panorama device, create tag in this device group. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| name | yes |  |  | Name of the tag. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove tag object. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| vsys |  | vsys1 |  | If *ip_address* is a firewall, create object in this virtual system. |

## Examples

    - name: Create tag object 'Prod'
      panos_tag_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Prod'
        color: 'red'
        comments: 'Prod Environment'
    
    - name: Remove tag object 'Prod'
      panos_tag_object:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Prod'
        state: 'absent'

#### Notes

- Panorama is supported.
- Check mode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

