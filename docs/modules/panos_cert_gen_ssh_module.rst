:source: panos_cert_gen_ssh.py

:orphan:

.. _panos_cert_gen_ssh_module:


panos_cert_gen_ssh -- generates a self-signed certificate using SSH protocol with SSH key
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- **NOTE: The modules in this role are deprecated in favour of the modules in the collection U(https://paloaltonetworks.github.io/pan-os-ansible)**
- This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
- otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.



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
                    <b>cert_cn</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>Certificate CN (common name) embedded in the certificate signature.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>cert_friendly_name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>Human friendly certificate name (not CN but just a friendly name).</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>IP address (or hostname) of PAN-OS device being configured.</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>Location of the filename that is used for the auth. Either <em>key_filename</em> or <em>password</em> is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>Password credentials to use for auth. Either <em>key_filename</em> or <em>password</em> is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>rsa_nbits</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"2048"</div>
                                    </td>
                                                                <td>
                                                                        <div>Number of bits used by the RSA algorithm for the certificate generation.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>signed_by</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">null</div>
                                    </td>
                                                                <td>
                                                                        <div>Undersigning authority (CA) that MUST already be presents on the device.</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"admin"</div>
                                    </td>
                                                                <td>
                                                                        <div>User name to use for auth. Default is admin.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - Checkmode is not supported.



Examples
--------

.. code-block:: yaml+jinja

    
    # Generates a new self-signed certificate using ssh
    - name: generate self signed certificate
      panos_cert_gen_ssh:
        ip_address: "192.168.1.1"
        username: "admin"
        password: "paloalto"
        cert_cn: "1.1.1.1"
        cert_friendly_name: "test123"
        signed_by: "root-ca"





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)


