# panos_query_rules

_(versionadded:: 2.5)_


## Synopsis

-
 
S
e
c
u
r
i
t
y
 
p
o
l
i
c
i
e
s
 
a
l
l
o
w
 
y
o
u
 
t
o
 
e
n
f
o
r
c
e
 
r
u
l
e
s
 
a
n
d
 
t
a
k
e
 
a
c
t
i
o
n
,
 
a
n
d
 
c
a
n
 
b
e
 
a
s
 
g
e
n
e
r
a
l
 
o
r
 
s
p
e
c
i
f
i
c
 
a
s
 
n
e
e
d
e
d
.
 
T
h
e
 
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
r
e
 
c
o
m
p
a
r
e
d
 
a
g
a
i
n
s
t
 
t
h
e
 
i
n
c
o
m
i
n
g
 
t
r
a
f
f
i
c
 
i
n
 
s
e
q
u
e
n
c
e
,
 
a
n
d
 
b
e
c
a
u
s
e
 
t
h
e
 
f
i
r
s
t
 
r
u
l
e
 
t
h
a
t
 
m
a
t
c
h
e
s
 
t
h
e
 
t
r
a
f
f
i
c
 
i
s
 
a
p
p
l
i
e
d
,
 
t
h
e
 
m
o
r
e
 
s
p
e
c
i
f
i
c
 
r
u
l
e
s
 
m
u
s
t
 
p
r
e
c
e
d
e
 
t
h
e
 
m
o
r
e
 
g
e
n
e
r
a
l
 
o
n
e
s
.




## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice
- xmltodict can be obtains from PyPi https://pypi.python.org/pypi/xmltodict

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key  |
| no |
|  |
| |  |
| API key that can be used instead of <em>username</em>/<em>password</em> credentials.  |
</td></tr>
| application  |
| no |
| None |
| |  |
| Name of the application or application group to be queried.  |
</td></tr>
| destination_ip  |
| no |
| None |
| |  |
| The destination IP address to be queried.  |
</td></tr>
| destination_port  |
| no |
| None |
| |  |
| The destination port to be queried.  |
</td></tr>
| destination_zone  |
| no |
| None |
| |  |
| Name of the destination security zone to be queried.  |
</td></tr>
| devicegroup  |
| no |
| None |
| |  |
| The Panorama device group in which to conduct the query.  |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS firewall or Panorama management console being queried.  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| Password credentials to use for authentication.  |
</td></tr>
| protocol  |
| no |
| None |
| |  |
| The protocol used to be queried.  Must be either <em>tcp</em> or <em>udp</em>.  |
</td></tr>
| source_ip  |
| no |
| None |
| |  |
| The source IP address to be queried.  |
</td></tr>
| source_port  |
| no |
| None |
| |  |
| The source port to be queried.  |
</td></tr>
| source_zone  |
| no |
| None |
| |  |
| Name of the source security zone to be queried.  |
</td></tr>
| tag_name  |
| no |
| None |
| |  |
| Name of the rule tag to be queried.  |
</td></tr>
| username  |
| no |
| admin |
| |  |
| Username credentials to use for authentication.  |
</td></tr>
</table>
</br>



## Examples

    - name: search for rules with tcp/3306
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        source_zone: 'DevNet'
        destination_zone: 'DevVPC'
        destination_port: '3306'
        protocol: 'tcp'
    
    - name: search devicegroup for inbound rules to dmz host
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        destination_zone: 'DMZ'
        destination_ip: '10.100.42.18'
        address: 'DeviceGroupA'
    
    - name: search for rules containing a specified rule tag
      panos_query_rules:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        tag_name: 'ProjectX'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

