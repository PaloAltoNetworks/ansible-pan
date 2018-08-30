---
title: panos_loadcfg
---
# panos_loadcfg

_(versionadded:: 2.3)_


## Synopsis

Load configuration on PAN-OS device


## Requirements (on host that executes module)

- pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| commit |  | True |  | commit if changed |
| file |  | None |  | configuration file to load |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device |
| password | yes |  |  | password for authentication |
| username |  | admin |  | username for authentication |

## Examples

    # Import and load config file from URL
      - name: import configuration
        panos_import:
          ip_address: "192.168.1.1"
          password: "admin"
          url: "{{ConfigURL}}"
          category: "configuration"
        register: result
      - name: load configuration
        panos_loadcfg:
          ip_address: "192.168.1.1"
          password: "admin"
          file: "{{result.filename}}"




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

