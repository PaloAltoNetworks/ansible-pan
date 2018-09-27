---
title: panos_dag_tags
---
# panos_dag_tags

_(versionadded:: 2.5)_


## Synopsis

Create the ip address to tag associations. Tags will in turn be used to create DAG's


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | commit if changed |
| description |  |  |  | The purpose / objective of the static Address Group |
| devicegroup |  |  |  | - Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
 |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device |
| ip_to_register |  |  |  | IP that will be registered with the given tag names. |
| operation |  |  |  | The action to be taken. Supported values are *add*/*update*/*find*/*delete*. |
| password | yes |  |  | password for authentication |
| tag_names |  |  |  | The list of the tags that will be added or removed from the IP address. |
| username |  | admin |  | username for authentication |

## Examples

    - name: Create the tags to map IP addresses
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Tags to allow certain IP's to access various SaaS Applications"
        operation: 'add'
      tags: "adddagip"
    
    - name: List the IP address to tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        tag_names: "{{ tag_names }}"
        description: "List the IP address to tag mapping"
        operation: 'list'
      tags: "listdagip"
    
    - name: Unregister an IP address from a tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Unregister IP address from tag mappings"
        operation: 'delete'
      tags: "deletedagip"

#### Notes

- Checkmode is not supported.
- Panorama is not supported.
- use panos_registered_ip from now on



#### Status

This module is flagged as **deprecated** which means that .

