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

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>address<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The IP address of the host or network in CIDR notation.</div></td></tr>
<tr><td>address_type<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The type of address object definition.  Valid types are <em>ip-netmask</em> and <em>ip-range</em>.</div></td></tr>
<tr><td>addressgroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>A static group of address objects or dynamic address group.</div></td></tr>
<tr><td>addressobject<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The name of the address object.</div></td></tr>
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>color<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>- The color of the tag object.  Valid values are <em>red, green, blue, yellow, copper, orange, purple, gray, light green, cyan, light gray, blue gray, lime, black, gold, and brown</em>.
    </div></td></tr>
<tr><td>description<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The description of the object.</div></td></tr>
<tr><td>destination_port<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The destination port to be used in a service object definition.</div></td></tr>
<tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>- The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.
    </div></td></tr>
<tr><td>dynamic_value<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The filter match criteria to be used in a dynamic addressgroup definition.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device or Panorama management console being configured.</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>The operation to be performed.  Supported values are <em>add</em>/<em>delete</em>/<em>find</em>.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Password credentials to use for authentication.</div></td></tr>
<tr><td>protocol<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The IP protocol to be used in a service object definition.  Valid values are <em>tcp</em> or <em>udp</em>.</div></td></tr>
<tr><td>servicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>A group of service objects.</div></td></tr>
<tr><td>serviceobject<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The name of the service object.</div></td></tr>
<tr><td>services<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The group of service objects used in a servicegroup definition.</div></td></tr>
<tr><td>source_port<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The source port to be used in a service object definition.</div></td></tr>
<tr><td>static_value<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>A group of address objects to be used in an addressgroup definition.</div></td></tr>
<tr><td>tag_name<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The name of an object or rule tag.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for authentication.</div></td></tr>
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

