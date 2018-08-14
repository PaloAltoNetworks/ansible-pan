.. _panos_static_route:


panos_static_route
++++++++++++++++++

.. versionadded:: 2.6


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Create static routes on PAN-OS devices.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
  * pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>admin_dist<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Administrative distance for static route.</div>        </td></tr>
                <tr><td>api_key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>API key to be used instead of <em>username</em> and <em>password</em>.</div>        </td></tr>
                <tr><td>destination<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Destination network.  Required if <em>state</em> is <em>present</em>.</div>        </td></tr>
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address or hostname of PAN-OS device.</div>        </td></tr>
                <tr><td>metric<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>10</td>
        <td></td>
        <td><div>Metric for route.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of static route.</div>        </td></tr>
                <tr><td>nexthop<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Next hop IP address.  Required if <em>state</em> is <em>present</em>.</div>        </td></tr>
                <tr><td>nexthop_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>ip-address</td>
        <td><ul><li>ip-address</li><li>discard</li></ul></td>
        <td><div>Type of next hop.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Password for authentication for PAN-OS device.  Optional if <em>api_key</em> is used.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Create or remove static route.</div>        </td></tr>
                <tr><td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td></td>
        <td><div>Username for authentication for PAN-OS device.  Optional if <em>api_key</em> is used.</div>        </td></tr>
                <tr><td>virtual_router<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>default</td>
        <td></td>
        <td><div>Virtual router to use.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

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


Notes
-----

.. note::
    - Panorama is not supported.
    - IPv6 is not supported.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

