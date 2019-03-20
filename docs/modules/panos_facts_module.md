---
title: panos_facts
---
# panos_facts

_(versionadded:: 2.8)_


## Synopsis

Collects facts from Palo Alto Networks device


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| gather_subset |  | !config | all, system, session, interfaces, ha, vr, vsys and config | Scopes what information is gathered from the device. |
| host | yes |  |  | IP address or hostname of PAN-OS device. |
| username |  | admin |  | Username for authentication for PAN-OS device.  If the value is not specified in the task, the value of environment variable ANSIBLE_NET_USERNAME will be used instead. |
| password |  |  |  | Password for authentication for PAN-OS device. If the value is not specified in the task, the value of environment variable ANSIBLE_NET_PASSWORD will be used instead. |


## Examples

    - name: Get configuration from device
      panos_facts:
        host: myfw.company.com
        username: admin
        password: mysecret
        gather_subset: config
    
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |
| --- | --- | --- | --- | --- |
| net_hostname | Hostname of the local node. | When **system** is specified in **gather_subset**. | str |  |
| net_serial | Serial number of the local node. | When **system** is specified in **gather_subset**. | str |  |
| net_model | Device model of the local node. | When **system** is specified in **gather_subset**. | str |  |
| net_version | PanOS version of the local node. | When **system** is specified in **gather_subset**. | str |  |
| net_uptime | Uptime of the local node. | When **system** is specified in **gather_subset**. | str | 469 days, 19:30:16 |
| net_full_commit_required | Specifies whether full commit is required to apply changes. | When **system** is specified in **gather_subset**. | bool |  |
| net_uncommitted_changes | Specifies if commit is required to apply changes. | When **system** is specified in **gather_subset**. | bool |  |
| net_multivsys | Specifies whether multivsys mode is enabled on local node. | When **system** is specified in **gather_subset**. | str |  |
| net_session_usage | Current number of active sessions on local node. | When **session** is specified in **gather_subset**. | int |  |
| net_session_max | Maximum number of sessions on local node. | When **session** is specified in **gather_subset**. | int |  |
| net_pps | Current packets/s throughput. | When **session** is specified in **gather_subset**. | int |  |
| net_kbps | Current kb/s throughput. | When **session** is specified in **gather_subset**. | int |  |
| net_ha_enabled | Specifies whether HA is enabled or not. | When **ha** is specified in **gather_subset**. | bool |  |
| net_ha_localmode | Specifies the HA mode on local node. | When **ha** is specified in **gather_subset**. | str | Active-Passive |
| net_ha_localstate | Specifies the HA state on local node. | When **ha** is specified in **gather_subset**. | str | active |
| net_config | Device confiration in XML format. | When **config** is specified in **gather_subset**. | str |  |
| net_interfaces | Network interface information (name, comment, ip, ipv6, tag). | When **interface** is specified in **gather_subset**. | dict |  |
| net_virtual-routers | Virtual Router information (vr_name, vr_routerid, vr_asn, vr_iflist). | When **vr** is specified in **gather_subset**. | dict |  |
| net_virtual-systems | Virtual System information (vsys_description, vsys_id, vsys_name, vsys_currentsessions, vsys_vsys_maxsessions, vsys_vrlist, vsys_iflist, vsys_zonelist). | When **vsys** is specified in **gather_subset**. | dict |  |


#### Notes

- Panorama is not supported, though some **gather_subset** values can be collected from Panorama.


#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


