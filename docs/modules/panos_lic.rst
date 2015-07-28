.. _panos_lic:

panos_lic
``````````````````````````````

Apply an authcode to a device. 
The authcode should have been previously registered on the Palo Alto Networks support portal. 
The device should have Internet access. 

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
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for authentication</td>
    </tr>
        <tr>
    <td>force</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether to apply authcode even if device is already licensed</td>
    </tr>
        <tr>
    <td>auth_code</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>authcode to be applied</td>
    </tr>
        </table>

Examples
--------

 ::

    
      - name: fetch license
        panos_lic:
            ip_address: "192.168.1.1"
            password: "admin"
            auth_code: "IBADCODE"
