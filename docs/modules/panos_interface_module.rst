.. _panos_interface:


panos_interface
+++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python


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
                <tr><td>commit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td></td>
        <td><div>Commit if changed</div>        </td></tr>
                <tr><td>create_default_route<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>false</td>
        <td></td>
        <td><div>Whether or not to add default route with router learned via DHCP.</div>        </td></tr>
                <tr><td>if_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the interface to configure.</div>        </td></tr>
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address (or hostname) of PAN-OS device being configured.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Password credentials to use for auth.</div>        </td></tr>
                <tr><td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td></td>
        <td><div>Username credentials to use for auth.</div>        </td></tr>
                <tr><td>zone_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the zone for the interface. If the zone does not exist it is created but if the zone exists and it is not of the layer3 type the operation will fail.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: enable DHCP client on ethernet1/1 in zone public
      interface:
        password: "admin"
        ip_address: "192.168.1.1"
        if_name: "ethernet1/1"
        zone_name: "public"
        create_default_route: "yes"





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

