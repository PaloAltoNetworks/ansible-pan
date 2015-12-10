.. _panos_admpwd:

panos_admpwd
``````````````````````````````

Synopsis
--------


Change the admin password of PAN-OS via SSH using a SSH key for authentication.
Useful for AWS instances where the first login should be done via SSH.


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">ip_address</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      IP address (or hostname) of PAN-OS device<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      password to configure for admin on the PAN-OS device<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">key_filename</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      filename of the SSH Key to use for authentication<br></td>
    </tr>
        </table><br>


.. important:: Requires paramiko


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
