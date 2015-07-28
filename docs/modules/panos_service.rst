.. _panos_service:

panos_service
``````````````````````````````

Create a service object 

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
    <td>protocol</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>protocol for the service, should be tcp or udp</td>
    </tr>
        <tr>
    <td>service_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the service</td>
    </tr>
        <tr>
    <td>source_port</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>source port</td>
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
    <td>port</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>destination port</td>
    </tr>
        </table>

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
