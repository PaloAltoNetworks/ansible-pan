# panos_pg

_(versionadded:: 2.3)_


## Synopsis

Create a security profile group


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| commit  |
| no |
| True |
| |  |
| commit if changed  |
</td></tr>
| data_filtering  |
| no |
| None |
| |  |
| name of the data filtering profile  |
</td></tr>
| file_blocking  |
| no |
| None |
| |  |
| name of the file blocking profile  |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS device  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| password for authentication  |
</td></tr>
| pg_name  |
| yes |
|  |
| |  |
| name of the security profile group  |
</td></tr>
| spyware  |
| no |
| None |
| |  |
| name of the spyware profile  |
</td></tr>
| url_filtering  |
| no |
| None |
| |  |
| name of the url filtering profile  |
</td></tr>
| username  |
| no |
| admin |
| |  |
| username for authentication  |
</td></tr>
| virus  |
| no |
| None |
| |  |
| name of the anti-virus profile  |
</td></tr>
| vulnerability  |
| no |
| None |
| |  |
| name of the vulnerability profile  |
</td></tr>
| wildfire  |
| no |
| None |
| |  |
| name of the wildfire analysis profile  |
</td></tr>
</table>
</br>



## Examples

    - name: setup security profile group
      panos_pg:
        ip_address: "192.168.1.1"
        password: "admin"
        username: "admin"
        pg_name: "pg-default"
        virus: "default"
        spyware: "default"
        vulnerability: "default"




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

