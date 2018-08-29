# panos_pg

_(versionadded:: 2.3)_


## Synopsis

Create a security profile group


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |

NOT suboptions
|commit|no||
commit if changed
 |
NOT suboptions
|data_filtering|no||
name of the data filtering profile
 |
NOT suboptions
|file_blocking|no||
name of the file blocking profile
 |
NOT suboptions
|ip_address|yes||
IP address (or hostname) of PAN-OS device
 |
NOT suboptions
|password|yes||
password for authentication
 |
NOT suboptions
|pg_name|yes||
name of the security profile group
 |
NOT suboptions
|spyware|no||
name of the spyware profile
 |
NOT suboptions
|url_filtering|no||
name of the url filtering profile
 |
NOT suboptions
|username|no||
username for authentication
 |
NOT suboptions
|virus|no||
name of the anti-virus profile
 |
NOT suboptions
|vulnerability|no||
name of the vulnerability profile
 |
NOT suboptions
|wildfire|no||
name of the wildfire analysis profile
 |

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

