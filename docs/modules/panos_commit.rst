.. _panos_commit:

panos_commit
``````````````````````````````

Commit config on a device 

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
    <td>password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for authentication</td>
    </tr>
        <tr>
    <td>timeout</td>
    <td>no</td>
    <td>none</td>
    <td><ul></ul></td>
    <td>timeout for commit job</td>
    </tr>
        <tr>
    <td>interval</td>
    <td>no</td>
    <td>0.5</td>
    <td><ul></ul></td>
    <td>interval for checking commit job</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>sync</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>if commit should be synchronous</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Commit candidate config on 192.168.1.1 in sync mode
    - panos_commit:
        ip_address: "192.168.1.1"
        username: "admin"
        password: "admin"
