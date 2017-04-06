.. _panos_commit:


panos_commit - commit firewall's candidate configuration
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

PanOS module that will commit firewall's candidate configuration on
the device. The new configuration will become active immediately.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python


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
    <td>interval<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>0.5</td>
        <td><ul></ul></td>
        <td><div>interval for checking commit job</div></td></tr>
            <tr>
    <td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>password for authentication</div></td></tr>
            <tr>
    <td>sync<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>if commit should be synchronous</div></td></tr>
            <tr>
    <td>timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>timeout for commit job</div></td></tr>
            <tr>
    <td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td><ul></ul></td>
        <td><div>username for authentication</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    # Commit candidate config on 192.168.1.1 in sync mode
    - panos_commit:
        ip_address: "192.168.1.1"
        username: "admin"
        password: "admin"

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
        <td align=center> okey dokey </td>
    </tr>
        
    </table>
    </br></br>


