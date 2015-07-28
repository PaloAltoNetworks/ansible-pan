.. _panos_sshkey:

panos_sshkey
``````````````````````````````

Manage SSH keys of admins 

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
    <td>public_key</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>SSH public key to set</td>
    </tr>
        <tr>
    <td>state</td>
    <td>yes</td>
    <td></td>
    <td><ul><li>present</li><li>absent</li></ul></td>
    <td>if present module checks for presence of SSH key if absent module deletes SSH key if present</td>
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
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>username of the admin to operate on</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # delete SSH key of foo if present
    - panos_sshkey:
        ip_address: "192.168.1.1"
        password: "admin"
        admin_username: "foo"
        state: "absent"
