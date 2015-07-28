.. _panos_mgtconfig:

panos_mgtconfig
``````````````````````````````

Configure management settings of device 

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
    <td>panorama_primary</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>address of primary Panorama server</td>
    </tr>
        <tr>
    <td>dns_server_secondary</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>address of secondary DNS server</td>
    </tr>
        <tr>
    <td>dns_server_primary</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>address of primary DNS server</td>
    </tr>
        <tr>
    <td>panorama_secondary</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>address of secondary Panorama server</td>
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

    
    - name: set dns and panorama
      panos_mgtconfig:
        ip_address: "192.168.1.1"
        password: "admin"
        dns_server_primary: "1.1.1.1"
        dns_server_secondary: "1.1.1.2"
        panorama_primary: "1.1.1.3"
        panorama_secondary: "1.1.1.4"
