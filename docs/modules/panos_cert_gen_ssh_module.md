# panos_cert_gen_ssh

_(versionadded:: 2.3)_


## Synopsis

This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.


## Requirements (on host that executes module)

- paramiko

## Options

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
<td><div>Certificate CN (common name) embedded in the certificate signature.</div></td></tr>
<tr><td>cert_friendly_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Human friendly certificate name (not CN but just a friendly name).</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
<tr><td>key_filename<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Location of the filename that is used for the auth. Either <em>key_filename</em> or <em>password</em> is required.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth. Either <em>key_filename</em> or <em>password</em> is required.</div></td></tr>
<tr><td>rsa_nbits<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>2048</td>
<td></td>
<td><div>Number of bits used by the RSA algorithm for the certificate generation.</div></td></tr>
<tr><td>signed_by<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Undersigning authority (CA) that MUST already be presents on the device.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>User name to use for auth. Default is admin.</div></td></tr>
</table>
</br>



## Examples

    # Generates a new self-signed certificate using ssh
    - name: generate self signed certificate
      panos_cert_gen_ssh:
        ip_address: "192.168.1.1"
        username: "admin"
        password: "paloalto"
        cert_cn: "1.1.1.1"
        cert_friendly_name: "test123"
        signed_by: "root-ca"

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

