.. _panos_cert_gen_ssh:

panos_cert_gen_ssh
``````````````````````````````

Synopsis
--------

Added in version 2.3

This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.


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
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      password to use for authentication (either key or password is required)<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">rsa_nbits</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">1024</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      number of bits used by the RSA alg<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">cert_cn</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      certificate cn<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">cert_friendly_name</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      certificate name (not CN but just a friendly name)<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">key_filename</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      filename of the SSH Key to use for authentication (either key or password is required)<br></td>
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
    <td style="vertical-align:middle">signed_by</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      undersigning authorithy which MUST be presents on the device already<br></td>
    </tr>
        </table><br>


.. important:: Requires paramiko


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
