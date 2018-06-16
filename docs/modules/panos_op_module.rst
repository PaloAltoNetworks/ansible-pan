.. _panos_op:


panos_op
++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* This module will allow user to pass and execute any supported OP command on the PANW device.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
  * pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice


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
                <tr><td>api_key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div>        </td></tr>
                <tr><td>cmd<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The OP command to be performed.</div>        </td></tr>
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address (or hostname) of PAN-OS device or Panorama management console being configured.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Password credentials to use for authentication.</div>        </td></tr>
                <tr><td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td></td>
        <td><div>Username credentials to use for authentication.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: show list of all interfaces
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show interfaces all'
    
    - name: show system info
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show system info'

Return Values
-------------

The following are the fields unique to this module:

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
        <td> stdout_xml </td>
        <td> output of the given OP command as JSON formatted string </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> <response status=success><result><system><hostname>fw2</hostname> </td>
    </tr>
            <tr>
        <td> stdout </td>
        <td> output of the given OP command as JSON formatted string </td>
        <td align=center> success </td>
        <td align=center> string </td>
        <td align=center> {system: {app-release-date: 2017/05/01  15:09:12}} </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Checkmode is NOT supported.
    - Panorama is NOT supported.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

