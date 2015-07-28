.. _panos_admpwd:

panos_admpwd
``````````````````````````````

Change the admin password of PAN-OS via SSH using a SSH key for authentication. 
Useful for AWS instances where the first login should be done via SSH. 

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
    <td>password to configure for admin on the PAN-OS device</td>
    </tr>
        <tr>
    <td>key_filename</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>filename of the SSH Key to use for authentication</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # Tries for 10 times to set the admin password of 192.168.1.1 to "badpassword"
    # via SSH, authenticating using key /tmp/ssh.key
    - name: set admin password
      panos_admpwd:
        ip_address: "192.168.1.1"
        key_filename: "/tmp/ssh.key"
        password: "badpassword"
      register: result
      until: not result|failed
      retries: 10
      delay: 30
