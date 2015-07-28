.. _panos_nat:

panos_nat
``````````````````````````````

Create a nat rule 

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
    <td>snat_bidirectional</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>bidirectional flag</td>
    </tr>
        <tr>
    <td>dnat_port</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>dnat translated port</td>
    </tr>
        <tr>
    <td>snat_interface_address</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>snat interface address</td>
    </tr>
        <tr>
    <td>rule_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the SNAT rule</td>
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
    <td>snat_address</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>snat translated address</td>
    </tr>
        <tr>
    <td>dnat_address</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>dnat translated address</td>
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
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>type of source translation</td>
    </tr>
        <tr>
    <td>destination</td>
    <td>no</td>
    <td>['any']</td>
    <td><ul></ul></td>
    <td>destination address</td>
    </tr>
        <tr>
    <td>from_zone</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>source zones</td>
    </tr>
        <tr>
    <td>source</td>
    <td>no</td>
    <td>['any']</td>
    <td><ul></ul></td>
    <td>source address</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
    </tr>
        <tr>
    <td>snat_interface</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>snat interface</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Create a source and destination nat rule
      - name: create nat SSH221 rule for 10.0.1.101
        panos_nat:
          ip_address: "192.168.1.1"
          password: "admin"
          rule_name: "Web SSH"
          from_zone: ["external"]
          to_zone: "external"
          source: ["any"]
          destination: ["10.0.0.100"]
          service: "service-tcp-221"
          snat_type: "dynamic-ip-and-port"
          snat_interface: "ethernet1/2"
          dnat_address: "10.0.1.101"
          dnat_port: "22"
          commit: False
