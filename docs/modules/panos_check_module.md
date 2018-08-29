# panos_check

_(versionadded:: 2.3)_


## Synopsis

Check if PAN-OS device is ready for being configured (no pending jobs).
The check could be done once or multiple times until the device is ready.


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| interval |  | 0 |  | time waited between checks |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device |
| password | yes |  |  | password for authentication |
| timeout |  | 0 |  | timeout of API calls |
| username |  | admin |  | username for authentication |

## Examples

    # single check on 192.168.1.1 with credentials admin/admin
    - name: check if ready
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
    
    # check for 10 times, every 30 seconds, if device 192.168.1.1
    # is ready, using credentials admin/admin
    - name: wait for reboot
      panos_check:
        ip_address: "192.168.1.1"
        password: "admin"
      register: result
      until: not result|failed
      retries: 10
      delay: 30




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

