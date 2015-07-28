.. _panos_dhcpif:

panos_dhcpif
``````````````````````````````

Configure a DP network interface for DHCP 
Useful for configuring new AWS instances 

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
    <td>create_default_route</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether add default route with router learned via DHCP</td>
    </tr>
        <tr>
    <td>zone_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the zone for the interfaceif the zone does not exist it is created</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
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
        <tr>
    <td>if_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the interface to configure</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # enable DHCP client on ethernet1/1 in zone public
    - name: configure ethernet1/1
      panos_dhcpif:
        password: "admin"
        ip_address: "192.168.1.1"
        if_name: "ethernet1/1"
        zone_name: "public"
        create_default_route: "yes"
