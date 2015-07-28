.. _panos_swinstall:

panos_swinstall
``````````````````````````````

Install PAN-OS software image 
The image should have been already imported on the device 

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
    <td>version</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>version to install</td>
    </tr>
        <tr>
    <td>file</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>file to install</td>
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
    <td>job_timeout</td>
    <td>no</td>
    <td>240</td>
    <td><ul></ul></td>
    <td>timeout for download and install jobs in seconds</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # install PanOS_vm-6.1.1 image
    - name: install software
      panos_swinstall:
        ip_address: 192.168.1.1
        username: admin
        password: admin
        file: PanOS_vm-6.1.1
