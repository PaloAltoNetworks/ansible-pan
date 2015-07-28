.. _panos_import:

panos_import
``````````````````````````````

Import file on PAN-OS device 

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
    <td>category</td>
    <td>no</td>
    <td>software</td>
    <td><ul></ul></td>
    <td>category of file</td>
    </tr>
        <tr>
    <td>file</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>file to import</td>
    </tr>
        <tr>
    <td>url</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>url to file to import</td>
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

    
    # import software image PanOS_vm-6.1.1 on 192.168.1.1
    - name: import software image into PAN-OS
      panos_import:
        ip_address: 192.168.1.1
        username: admin
        password: admin
        file: /tmp/PanOS_vm-6.1.1
        category: software
