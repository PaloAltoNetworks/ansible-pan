# panos_cert_gen_ssh

_(versionadded:: 2.3)_


## Synopsis

This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.


## Requirements (on host that executes module)

- paramiko

## Options

| parameter | required | default | choices | comments |
| cert_cn<  |
| yes |
|  |
|  |
| Certificate CN (common name) embedded in the certificate signature. </td></tr>
| cert_friendly_name<  |
| yes |
|  |
|  |
| Human friendly certificate name (not CN but just a friendly name). </td></tr>
| ip_address<  |
| yes |
|  |
|  |
| IP address (or hostname) of PAN-OS device being configured. </td></tr>
| key_filename<  |
| yes |
|  |
|  |
| Location of the filename that is used for the auth. Either <em>key_filename</em> or <em>password</em> is required. </td></tr>
| password<  |
| yes |
|  |
|  |
| Password credentials to use for auth. Either <em>key_filename</em> or <em>password</em> is required. </td></tr>
| rsa_nbits<  |
| no |
| 2048 |
|  |
| Number of bits used by the RSA algorithm for the certificate generation. </td></tr>
| signed_by<  |
| yes |
|  |
|  |
| Undersigning authority (CA) that MUST already be presents on the device. </td></tr>
| username<  |
| no |
| admin |
|  |
| User name to use for auth. Default is admin. </td></tr>
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

