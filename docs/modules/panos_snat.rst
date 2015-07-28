.. _panos_snat:

panos_snat
``````````````````````````````

Create a source nat rule 
Note, only static SNAT rules are supported 
Superseded, use panos_nat module 

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
    <td>translated_address</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>translated address</td>
    </tr>
        <tr>
    <td>to_zone</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>destination zone</td>
    </tr>
        <tr>
    <td>service</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>service</td>
    </tr>
        <tr>
    <td>snat_type</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>type of SNAT</td>
    </tr>
        <tr>
    <td>rule_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the SNAT rule</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>interface_address_if</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>interface for dynamic-ip-and-port interface address NAT rules</td>
    </tr>
        <tr>
    <td>destination</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>destination address</td>
    </tr>
        <tr>
    <td>from_zone</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>source zone</td>
    </tr>
        <tr>
    <td>source</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>source address</td>
    </tr>
        <tr>
    <td>bidirectional</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether the SNAT should be bidirectional</td>
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
    <td>interface_address_ip</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address for dynamic-ip-and-port interface address NAT rules</td>
    </tr>
        </table>

Examples
--------

 ::

    
    - name: create bidirectional source nat rule
      panos_snat:
        ip_address: "192.168.1.1"
        password: "admin"
        rule_name: "static bidir snat"
        bidirectional: "true"
        snat_type: "static-ip"
        translated_address: "1.1.1.1"
        from_zone: "private"
        to_zone: "public"
        source: "10.1.1.1"
        destination: "any"
        service: "any"
