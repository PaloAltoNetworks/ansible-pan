---
title: panos_admpwd
---
# panos_admpwd

_(versionadded:: 2.3)_


## Synopsis

Change the admin password of PAN-OS via SSH using a SSH key for authentication.
Useful for AWS instances where the first login should be done via SSH.


## Requirements (on host that executes module)

- paramiko

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device |
| key_filename | yes |  |  | filename of the SSH Key to use for authentication |
| newpassword | yes |  |  | password to configure for admin on the PAN-OS device |
| username |  | admin |  | username for initial authentication |

## Examples

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
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | Last login: Fri Sep 16 11:09:20 2016 from 10.35.34.56.....Configuration committed successfully |




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

