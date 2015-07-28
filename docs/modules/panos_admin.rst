.. _panos_admin:

panos_admin
``````````````````````````````

Add or modify PAN-OS admin 

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
    <td>role</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>role for admin user</td>
    </tr>
        <tr>
    <td>admin_password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for admin user</td>
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
    <td>admin_username</td>
    <td>no</td>
    <td>admin</td>
    <td><ul></ul></td>
    <td>username for admin user</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Set the password of user admin to "badpassword"
    # Doesn't commit the candidate config
      - name: set admin password
        panos_admin:
          ip_address: "192.168.1.1"
          password: "admin"
          admin_username: admin
          admin_password: "badpassword"
          commit: False
