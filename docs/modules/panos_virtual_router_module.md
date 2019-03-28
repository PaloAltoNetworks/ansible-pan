---
title: panos_virtual_router
---
# panos_virtual_router

_(versionadded:: 2.9)_


## Synopsis

PanOS module that allows managing a Virtual Router instance.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | type | required | default | choices | comments |
| --- | --- | --- | --- | --- | --- |
| ip_address | str | True |  |  | IP address (or hostname) of PAN-OS device being configured |
| username | str |  | admin |  | Username credentials to use for auth unless I(api_key) is set |
| password | str |  |  |  | Password credentials to use for auth unless I(api_key) is set |
| api_key | str |  |  |  | API key that can be used instead of I(username)/I(password) credentials |
| state | str |  | present | ['present', 'absent'] | Add or remove BGP peer configuration |
| commit | bool |  | True |  | Commit configuration if changed |
| | | | | | |
| name | str |  | default |  | Name of virtual router |
| interface | list |  |  |  | List of interface names |
| ad_ebgp | int |  |  |  | Administrative distance for this protocol |
| ad_ibgp | int |  |  |  | Administrative distance for this protocol |
| ad_ospf_ext | int |  |  |  | Administrative distance for this protocol |
| ad_ospf_int | int |  |  |  | Administrative distance for this protocol |
| ad_ospfv3_ext | int |  |  |  | Administrative distance for this protocol |
| ad_ospfv3_int | int |  |  |  | Administrative distance for this protocol |
| ad_rip | int |  |  |  | Administrative distance for this protocol |
| ad_static | int |  |  |  | Administrative distance for this protocol |
| ad_static_ipv6 | int |  |  |  | Administrative distance for this protocol |

## Examples

    # Create a new virtual router instance
      - name: create virtual router
        panos_virtual_router:
          ip_address: "192.168.1.1"
          password: "admin"
          state: present
          name: vr-1
          interface: ['ethernet1/1']
          ad_rip: 150

    # Remove virtual router instance
      - name: create virtual router
        panos_virtual_router:
          ip_address: "192.168.1.1"
          password: "admin"
          state: absent
          name: vr-1


#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| status | success status | success | string | okey dokey |

#### Notes

- Checkmode is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

