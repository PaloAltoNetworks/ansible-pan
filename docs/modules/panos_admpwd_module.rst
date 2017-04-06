.. _panos_admpwd:


panos_admpwd - change admin password of PAN-OS device using SSH with SSH key
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Change the admin password of PAN-OS via SSH using a SSH key for authentication.
Useful for AWS instances where the first login should be done via SSH.


Requirements (on host that executes module)
-------------------------------------------

  * paramiko


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
            <tr>
    <td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
            <tr>
    <td>key_filename<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>filename of the SSH Key to use for authentication</div></td></tr>
            <tr>
    <td>newpassword<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>password to configure for admin on the PAN-OS device</div></td></tr>
            <tr>
    <td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td><ul></ul></td>
        <td><div>username for initial authentication</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    # Tries for 10 times to set the admin password of 192.168.1.1 to "badpassword"
    # via SSH, authenticating using key /tmp/ssh.key
    - name: set admin password
      panos_admpwd:
        ip_address: "192.168.1.1"
        username: "admin"
        key_filename: "/tmp/ssh.key"
        newpassword: "badpassword"
      register: result
      until: not result|failed
      retries: 10
      delay: 30

Return Values
-------------

Common return values are documented here :doc:`common_return_values`, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> status </td>
        <td> success status </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> Last login: Fri Sep 16 11:09:20 2016 from 10.35.34.56.....Configuration committed successfully </td>
    </tr>
        
    </table>
    </br></br>


