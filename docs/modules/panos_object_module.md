---
title: panos_object
---
# panos_object

_(versionadded:: 2.4)_


## Synopsis

-
 
P
o
l
i
c
y
 
o
b
j
e
c
t
s
 
f
o
r
m
 
t
h
e
 
m
a
t
c
h
 
c
r
i
t
e
r
i
a
 
f
o
r
 
p
o
l
i
c
y
 
r
u
l
e
s
 
a
n
d
 
m
a
n
y
 
o
t
h
e
r
 
f
u
n
c
t
i
o
n
s
 
i
n
 
P
A
N
-
O
S
.
 
T
h
e
s
e
 
m
a
y
 
i
n
c
l
u
d
e
 
a
d
d
r
e
s
s
 
o
b
j
e
c
t
,
 
a
d
d
r
e
s
s
 
g
r
o
u
p
s
,
 
s
e
r
v
i
c
e
 
o
b
j
e
c
t
s
,
 
s
e
r
v
i
c
e
 
g
r
o
u
p
s
,
 
a
n
d
 
t
a
g
.




## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| address |  |  |  | The IP address of the host or network in CIDR notation. |
| address_type |  |  |  | The type of address object definition.  Valid types are <em>ip-netmask</em> and <em>ip-range</em>. |
| addressgroup |  |  |  | A static group of address objects or dynamic address group. |
| addressobject |  |  |  | The name of the address object. |
| api_key |  |  |  | API key that can be used instead of <em>username</em>/<em>password</em> credentials. |
| color |  |  |  | - The color of the tag object.  Valid values are <em>red, green, blue, yellow, copper, orange, purple, gray, light green, cyan, light gray, blue gray, lime, black, gold, and brown</em>.
 |
| description |  |  |  | The description of the object. |
| destination_port |  |  |  | The destination port to be used in a service object definition. |
| devicegroup |  | None |  | - The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.
 |
| dynamic_value |  |  |  | The filter match criteria to be used in a dynamic addressgroup definition. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device or Panorama management console being configured. |
| operation | yes |  |  | The operation to be performed.  Supported values are <em>add</em>/<em>delete</em>/<em>find</em>. |
| password | yes |  |  | Password credentials to use for authentication. |
| protocol |  |  |  | The IP protocol to be used in a service object definition.  Valid values are <em>tcp</em> or <em>udp</em>. |
| servicegroup |  |  |  | A group of service objects. |
| serviceobject |  |  |  | The name of the service object. |
| services |  |  |  | The group of service objects used in a servicegroup definition. |
| source_port |  |  |  | The source port to be used in a service object definition. |
| static_value |  |  |  | A group of address objects to be used in an addressgroup definition. |
| tag_name |  |  |  | The name of an object or rule tag. |
| username |  | admin |  | Username credentials to use for authentication. |

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

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

