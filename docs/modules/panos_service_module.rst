.. _panos_service:


panos_service - create a service object
+++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create a service object. Service objects are fundamental representation of the applications given src/dst ports and protocol


Requirements (on host that executes module)
-------------------------------------------

  * pan-python


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
            <tr>
    <td>commit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>commit if changed</div></td></tr>
            <tr>
    <td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>password for authentication</div></td></tr>
            <tr>
    <td>port<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>destination port</div></td></tr>
            <tr>
    <td>protocol<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>protocol for the service, should be tcp or udp</div></td></tr>
            <tr>
    <td>service_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>name of the service</div></td></tr>
            <tr>
    <td>source_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>source port</div></td></tr>
            <tr>
    <td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td><ul></ul></td>
        <td><div>username for authentication</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    # Creates service for port 22
      - name: create SSH service
        panos_service:
          ip_address: "192.168.1.1"
          password: "admin"
          service_name: "service-tcp-22"
          protocol: "tcp"
          port: "22"



