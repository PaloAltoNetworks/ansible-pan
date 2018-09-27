---
title: panos_object
---
# panos_object

_(versionadded:: 2.4)_


## Synopsis

Policy objects form the match criteria for policy rules and many other functions in PAN-OS. These may include
address object, address groups, service objects, service groups, and tag.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| address |  |  |  | The IP address of the host or network in CIDR notation. |
| address_type |  |  |  | The type of address object definition.  Valid types are *ip-netmask* and *ip-range*. |
| addressgroup |  |  |  | A static group of address objects or dynamic address group. |
| addressobject |  |  |  | The name of the address object. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| color |  |  |  | - The color of the tag object.  Valid values are *red, green, blue, yellow, copper, orange, purple, gray, light green, cyan, light gray, blue gray, lime, black, gold, and brown*.
 |
| commit |  |  |  | Commit the config change. |
| description |  |  |  | The description of the object. |
| destination_port |  |  |  | The destination port to be used in a service object definition. |
| devicegroup |  | None |  | The name of the (preexisting) Panorama device group.If undefined and ip_address is Panorama, this defaults to shared. |
| dynamic_value |  |  |  | The filter match criteria to be used in a dynamic addressgroup definition. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device or Panorama management console being configured. |
| operation | yes |  |  | The operation to be performed.  Supported values are *add*/*delete*/*find*. |
| password | yes |  |  | Password credentials to use for authentication. |
| protocol |  |  |  | The IP protocol to be used in a service object definition.  Valid values are *tcp* or *udp*. |
| servicegroup |  |  |  | A group of service objects. |
| serviceobject |  |  |  | The name of the service object. |
| services |  |  |  | The group of service objects used in a servicegroup definition. |
| source_port |  |  |  | The source port to be used in a service object definition. |
| static_value |  |  |  | A group of address objects to be used in an addressgroup definition. |
| tag_name |  |  |  | The name of an object or rule tag. |
| username |  | admin |  | Username credentials to use for authentication. |
| vsys |  | vsys1 |  | The vsys to put the object into.Firewall only. |

## Examples

    - name: search for shared address object
      panos_object:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'find'
        address: 'DevNet'
    
    - name: create an address group in devicegroup using API key
      panos_object:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'add'
        addressgroup: 'Prod_DB_Svrs'
        static_value: ['prod-db1', 'prod-db2', 'prod-db3']
        description: 'Production DMZ database servers'
        tag_name: 'DMZ'
        devicegroup: 'DMZ Firewalls'
    
    - name: create a global service for TCP 3306
      panos_object:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'add'
        serviceobject: 'mysql-3306'
        destination_port: '3306'
        protocol: 'tcp'
        description: 'MySQL on tcp/3306'
    
    - name: create a global tag
      panos_object:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        tag_name: 'ProjectX'
        color: 'yellow'
        description: 'Associated with Project X'
    
    - name: delete an address object from a devicegroup using API key
      panos_object:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'delete'
        addressobject: 'Win2K test'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **deprecated** which means that .

