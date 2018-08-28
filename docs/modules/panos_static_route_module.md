# panos_static_route

_(versionadded:: 2.6)_


## Synopsis

Create static routes on PAN-OS devices.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| admin_dist<  |
| no |
|  |
|  |
| Administrative distance for static route. </td></tr>
| api_key<  |
| no |
|  |
|  |
| API key to be used instead of <em>username</em> and <em>password</em>. </td></tr>
| destination<  |
| no |
|  |
|  |
| Destination network.  Required if <em>state</em> is <em>present</em>. </td></tr>
| ip_address<  |
| yes |
|  |
|  |
| IP address or hostname of PAN-OS device. </td></tr>
| metric<  |
| no |
| 10 |
|  |
| Metric for route. </td></tr>
| name<  |
| yes |
|  |
|  |
| Name of static route. </td></tr>
| nexthop<  |
| no |
|  |
|  |
| Next hop IP address.  Required if <em>state</em> is <em>present</em>. </td></tr>
| nexthop_type<  |
| no |
| ip-address |
|  ip-address discard  |
| Type of next hop. </td></tr>
| password<  |
| no |
|  |
|  |
| Password for authentication for PAN-OS device.  Optional if <em>api_key</em> is used. </td></tr>
| state<  |
| no |
| present |
|  present absent  |
| Create or remove static route. </td></tr>
| username<  |
| no |
| admin |
|  |
| Username for authentication for PAN-OS device.  Optional if <em>api_key</em> is used. </td></tr>
| virtual_router<  |
| no |
| default |
|  |
| Virtual router to use. </td></tr>
</table>
</br>



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

#### Notes

- Panorama is not supported.
- IPv6 is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

