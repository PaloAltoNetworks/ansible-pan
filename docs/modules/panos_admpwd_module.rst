:source: panos_admpwd.py

:orphan:

.. _panos_admpwd_module:


panos_admpwd -- change admin password of PAN-OS device using SSH with SSH key
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Change the admin password of PAN-OS via SSH using a SSH key for authentication.
- Useful for AWS instances where the first login should be done via SSH.



Requirements
------------
The below requirements are needed on the host that executes this module.

- paramiko


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>IP address (or hostname) of PAN-OS device</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>key_filename</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>filename of the SSH Key to use for authentication</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>newpassword</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>password to configure for admin on the PAN-OS device</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>username</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">admin</div>
                                    </td>
                                                                <td>
                                                                        <div>username for initial authentication</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

    
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
Common return values are `documented here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <b>status</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>success</td>
                <td>
                                            <div>success status</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Last login: Fri Sep 16 11:09:20 2016 from 10.35.34.56.....Configuration committed successfully</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)


