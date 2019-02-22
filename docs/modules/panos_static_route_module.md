---
title: panos_static_route
---
# panos_static_route

_(versionadded:: 2.6)_


## Synopsis

Create static routes on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| admin_dist |  |  |  | Administrative distance for static route. |
| api_key |  |  |  | API key to be used instead of *username* and *password*. |
| destination |  |  |  | Destination network.  Required if *state* is *present*. |
| ip_address | yes |  |  | IP address or hostname of PAN-OS device. |
| metric |  | 10 |  | Metric for route. |
| name | yes |  |  | Name of static route. |
| nexthop |  |  |  | Next hop IP address.  Required if *state* is *present*. |
| nexthop_type |  | ip-address | ip-address, discard, none | Type of next hop. |
| password |  |  |  | Password for authentication for PAN-OS device.  Optional if *api_key* is used. |
| state |  | present | present, absent | Create or remove static route. |
| username |  | admin |  | Username for authentication for PAN-OS device.  Optional if *api_key* is used. |
| virtual_router |  | default |  | Virtual router to use. |

## Examples

    - name: Create route 'Test-One'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-One'
        destination: '1.1.1.0/24'
        nexthop: '10.0.0.1'

    - name: Create route 'Test-Two'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Two'
        destination: '2.2.2.0/24'
        nexthop: '10.0.0.1'

    - name: Create route 'Test-Three'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Three'
        destination: '3.3.3.0/24'
        nexthop: '10.0.0.1'

    - name: Delete route 'Test-Two'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Two'
        state: 'absent'

    - name: Create route 'Test-Four'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Four'
        destination: '4.4.4.0/24'
        nexthop: '10.0.0.1'
        virtual_router: 'VR-Two'

    - name: Create route 'Test-Five'
      panos_static_route:
        ip_address: '{{ fw_ip_address }}'
        username: '{{ fw_username }}'
        password: '{{ fw_password }}'
        name: 'Test-Five'
        destination: '5.5.5.0/24'
        nexthop_type: 'none'

#### Notes

- Panorama is not supported.
- IPv6 is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

