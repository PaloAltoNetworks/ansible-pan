.. _panos_pg:

panos_pg
``````````````````````````````

Create a security profile group 

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
    <td>data_filtering</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the data filtering profile</td>
    </tr>
        <tr>
    <td>file_blocking</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the file blocking profile</td>
    </tr>
        <tr>
    <td>pg_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the security profile group</td>
    </tr>
        <tr>
    <td>vulnerability</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the vulnerability profile</td>
    </tr>
        <tr>
    <td>spyware</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the spyware profile</td>
    </tr>
        <tr>
    <td>url_filtering</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the url filtering profile</td>
    </tr>
        <tr>
    <td>virus</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the anti-virus profile</td>
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

    
    - name: setup security profile group
      panos_pg:
        ip_address: "192.168.1.1"
        password: "admin"
        username: "admin"
        pg_name: "pg-default"
        virus: "default"
        spyware: "default"
        vulnerability: "default"
