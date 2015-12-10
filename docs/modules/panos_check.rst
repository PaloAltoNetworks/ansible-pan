.. _panos_check:

panos_check
``````````````````````````````

Synopsis
--------


Check if PAN-OS device is ready for being configured (no pending jobs).
The check could be done once or multiple times until the device is ready.


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
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      username for authentication<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      password for authentication<br></td>
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
    <td style="vertical-align:middle">timeout</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">0</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      timeout of API calls<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">interval</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">0</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      time waited between checks<br></td>
    </tr>
        </table><br>


.. important:: Requires pan-python


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
