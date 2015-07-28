.. _panos_gpp_gateway:

panos_gpp_gateway
``````````````````````````````

Configure a GlobalProtect Portal gateway list 

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
    <td>config_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the client config</td>
    </tr>
        <tr>
    <td>gateway_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name address of the gateway</td>
    </tr>
        <tr>
    <td>description</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>description of the gateway</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>portal_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the GlobalProtect portal</td>
    </tr>
        <tr>
    <td>manual</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>manual gateway</td>
    </tr>
        <tr>
    <td>state</td>
    <td>no</td>
    <td>present</td>
    <td><ul><li>absent</li><li>present</li></ul></td>
    <td>state of the gateway</td>
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
    <td>type</td>
    <td>no</td>
    <td>external</td>
    <td><ul><li>internal</li><li>external</li></ul></td>
    <td>internal or external gateway</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Adds gateway to portal config on 192.168.1.1
      - name: add gateway to portal
        panos_gpp_gateway:
          username: "admin"
          ip_address: "192.168.1.1"
          password: "admin"
          portal_name: "GP-Portal"
          config_name: "GPClientConfig"
          type: "external"
          gateway_address: "{{elastic_ip0}}"
          description: "{{device_name}}"
          manual: true
          state: "present"
    
    # Removes gateway from portal config
      - name: delete gateway from portal
        panos_gpp_gateway:
          username: "admin"
          ip_address: "192.168.1.1"
          password: "admin"
          portal_name: "GP-Portal"
          config_name: "GPClientConfig"
          type: "external"
          gateway_address: "{{elastic_ip0}}"
          state: "absent"
