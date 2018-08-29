---
title: panos_import
---
# panos_import

_(versionadded:: 2.3)_


## Synopsis

Import file on PAN-OS device


## Requirements (on host that executes module)

- pan-python
- requests
- requests_toolbelt

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| category |  | software |  | Category of file uploaded. The default is software. |
| file |  | None |  | Location of the file to import into device. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device. |
| password | yes |  |  | Password for device authentication. |
| url |  | None |  | URL of the file that will be imported to device. |
| username |  | admin |  | Username for device authentication. |

## Examples

    # import software image PanOS_vm-6.1.1 on 192.168.1.1
    - name: import software image into PAN-OS
      panos_import:
        ip_address: 192.168.1.1
        username: admin
        password: admin
        file: /tmp/PanOS_vm-6.1.1
        category: software




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

