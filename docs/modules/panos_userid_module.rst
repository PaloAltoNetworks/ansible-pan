.. _panos_userid:


panos_userid
++++++++++++

.. versionadded:: 2.6


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Userid allows for user to IP mapping that can be used in the policy rules.


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
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address (or hostname) of PAN-OS device being configured.</div>        </td></tr>
                <tr><td>operation<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>register</td>
        <td></td>
        <td><div>The action to be taken.  Supported values are <em>login</em>/<em>logout</em>.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div>        </td></tr>
                <tr><td>register_ip<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>ip of the user's machine that needs to be registered with userid.</div>        </td></tr>
                <tr><td>userid<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>User UPN</div>        </td></tr>
                <tr><td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td></td>
        <td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

      - name: register user ivanb to 10.0.1.101
        panos_userid:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'login'
          userid: 'ACMECORP\ivanb'
          register_ip: '10.0.1.101'


Notes
-----

.. note::
    - Checkmode is not supported.
    - Panorama is not supported.
    - This operation is runtime and does not require explicit commit of the firewall configuration.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

