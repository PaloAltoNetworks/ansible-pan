.. _panos_tunnelif:

panos_tunnelif
``````````````````````````````

Configure a tunnel interface 

.. raw:: html

    <table>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr>
    <td>username</td>
    <td>no</td>
    <td>admin</td>
    <td><ul></ul></td>
    <td>username for authentication</td>
    </tr>
        <tr>
    <td>tunnel_unit</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>unit number of the tunnel interface</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
    </tr>
        <tr>
    <td>zone_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the zone for the interfaceif the zone does not exist it is created</td>
    </tr>
        <tr>
    <td>password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for authentication</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # create tunnel.2 interface on zone vpn-dc-zone
    - name: configure tunnel if
      panos_tunnelif:
          ip_address: "192.168.1.1"
          password: "admin"
          username: "admin"
          tunnel_unit: 2
          zone_name: "vpn-dc-zone"
