.. _panos_cert_gen_ssh:


panos_cert_gen_ssh - generates a self-signed certificate using SSH protocol with SSH key
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.


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
                <tr><td>cert_cn<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Certificate CN (common name) embeded in the certificate signature.</div>        </td></tr>
                <tr><td>cert_friendly_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Human friendly certificate name (not CN but just a friendly name).</div>        </td></tr>
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address (or hostname) of PAN-OS device being configured.</div>        </td></tr>
                <tr><td>key_filename<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Location of the filename that is used for the auth. Either <em>key_filename</em> or <em>password</em> is required.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Password credentials to use for auth. Either <em>key_filename</em> or <em>password</em> is required.</div>        </td></tr>
                <tr><td>rsa_nbits<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>2048</td>
        <td></td>
        <td><div>Number of bits used by the RSA algorithm for the certificate generation.</div>        </td></tr>
                <tr><td>signed_by<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Undersigning authority (CA) that MUST already be presents on the device.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    # Generates a new self-signed certificate using ssh
    - name: generate self signed certificate
      panos_cert_gen_ssh:
        ip_address: "192.168.1.1"
        password: "paloalto"
        cert_cn: "1.1.1.1"
        cert_friendly_name: "test123"
        signed_by: "root-ca"





Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.
