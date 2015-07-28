.. _panos_dnat:

panos_dnat
``````````````````````````````

Create a destination nat rule 
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
    <td>rule_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the SNAT rule</td>
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
    <td>translated_port</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>translated port</td>
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
        </table>

Examples
--------

 ::

    
    # Create a destination nat rule dnat-ssh on 192.168.1.1
      - name: create destination nat rule for server
        panos_dnat:
          ip_address: "192.168.1.1"
          password: "admin"
          rule_name: "dnat-ssh"
          from_zone: "external"
          to_zone: "external"
          source: "any"
          destination: "{{PAVMAWSPublicIP}}"
          service: "service-tcp-22"
          translated_address: "{{ServerIP}}"
