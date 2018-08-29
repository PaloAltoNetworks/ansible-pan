---
title: panos_pg
---
# panos_pg

_(versionadded:: 2.3)_


## Synopsis

Create a security profile group


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| commit |  | True |  | commit if changed |
| data_filtering |  | None |  | name of the data filtering profile |
| file_blocking |  | None |  | name of the file blocking profile |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device |
| password | yes |  |  | password for authentication |
| pg_name | yes |  |  | name of the security profile group |
| spyware |  | None |  | name of the spyware profile |
| url_filtering |  | None |  | name of the url filtering profile |
| username |  | admin |  | username for authentication |
| virus |  | None |  | name of the anti-virus profile |
| vulnerability |  | None |  | name of the vulnerability profile |
| wildfire |  | None |  | name of the wildfire analysis profile |

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

