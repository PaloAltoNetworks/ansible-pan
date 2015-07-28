.. _panos_check:

panos_check
``````````````````````````````

Check if PAN-OS device is ready for being configured (no pending jobs) 
The check could be done once or multiple times until the device is ready 

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
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>timeout</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>timeout of API calls</td>
    </tr>
        <tr>
    <td>interval</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>time waited between checks</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # single check on 192.168.1.1 with credentials admin/admin
    - name: check if ready
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
    
    # check for 10 times, every 30 seconds, if device 192.168.1.1
    # is ready, using credentials admin/admin
    - name: wait for reboot
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
      register: result
      until: not result|failed
      retries: 10
      delay: 30
