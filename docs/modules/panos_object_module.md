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
| address<  |
| no |
|  |
|  |
| The IP address of the host or network in CIDR notation. </td></tr>
| address_type<  |
| no |
|  |
|  |
| The type of address object definition.  Valid types are <em>ip-netmask</em> and <em>ip-range</em>. </td></tr>
| addressgroup<  |
| no |
|  |
|  |
| A static group of address objects or dynamic address group. </td></tr>
| addressobject<  |
| no |
|  |
|  |
| The name of the address object. </td></tr>
| api_key<  |
| no |
|  |
|  |
| API key that can be used instead of <em>username</em>/<em>password</em> credentials. </td></tr>
| color<  |
| no |
|  |
|  |
| - The color of the tag object.  Valid values are <em>red, green, blue, yellow, copper, orange, purple, gray, light green, cyan, light gray, blue gray, lime, black, gold, and brown</em>.
     </td></tr>
| description<  |
| no |
|  |
|  |
| The description of the object. </td></tr>
| destination_port<  |
| no |
|  |
|  |
| The destination port to be used in a service object definition. </td></tr>
| devicegroup<  |
| no |
| None |
|  |
| - The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.
     </td></tr>
| dynamic_value<  |
| no |
|  |
|  |
| The filter match criteria to be used in a dynamic addressgroup definition. </td></tr>
| ip_address<  |
| yes |
|  |
|  |
| IP address (or hostname) of PAN-OS device or Panorama management console being configured. </td></tr>
| operation<  |
| yes |
|  |
|  |
| The operation to be performed.  Supported values are <em>add</em>/<em>delete</em>/<em>find</em>. </td></tr>
| password<  |
| yes |
|  |
|  |
| Password credentials to use for authentication. </td></tr>
| protocol<  |
| no |
|  |
|  |
| The IP protocol to be used in a service object definition.  Valid values are <em>tcp</em> or <em>udp</em>. </td></tr>
| servicegroup<  |
| no |
|  |
|  |
| A group of service objects. </td></tr>
| serviceobject<  |
| no |
|  |
|  |
| The name of the service object. </td></tr>
| services<  |
| no |
|  |
|  |
| The group of service objects used in a servicegroup definition. </td></tr>
| source_port<  |
| no |
|  |
|  |
| The source port to be used in a service object definition. </td></tr>
| static_value<  |
| no |
|  |
|  |
| A group of address objects to be used in an addressgroup definition. </td></tr>
| tag_name<  |
| no |
|  |
|  |
| The name of an object or rule tag. </td></tr>
| username<  |
| no |
| admin |
|  |
| Username credentials to use for authentication. </td></tr>
</table>
</br>



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

