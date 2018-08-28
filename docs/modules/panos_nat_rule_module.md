# panos_nat_rule

_(versionadded:: 2.4)_


## Synopsis

-
 
C
r
e
a
t
e
 
a
 
p
o
l
i
c
y
 
n
a
t
 
r
u
l
e
.
 
K
e
e
p
 
i
n
 
m
i
n
d
 
t
h
a
t
 
w
e
 
c
a
n
 
e
i
t
h
e
r
 
e
n
d
 
u
p
 
c
o
n
f
i
g
u
r
i
n
g
 
s
o
u
r
c
e
 
N
A
T
,
 
d
e
s
t
i
n
a
t
i
o
n
 
N
A
T
,
 
o
r
 
b
o
t
h
.
 
I
n
s
t
e
a
d
 
o
f
 
s
p
l
i
t
t
i
n
g
 
i
t
 
i
n
t
o
 
t
w
o
 
w
e
 
w
i
l
l
 
m
a
k
e
 
a
 
f
a
i
r
 
a
t
t
e
m
p
t
 
t
o
 
d
e
t
e
r
m
i
n
e
 
w
h
i
c
h
 
o
n
e
 
t
h
e
 
u
s
e
r
 
w
a
n
t
s
.




## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| api_key<  |
| no |
|  |
|  |
| API key that can be used instead of <em>username</em>/<em>password</em> credentials. </td></tr>
| commit<  |
| no |
| True |
|  |
| Commit configuration if changed. </td></tr>
| destination_ip<  |
| no |
| [u'any'] |
|  |
| list of destination addresses </td></tr>
| destination_zone<  |
| yes |
|  |
|  |
| destination zone </td></tr>
| dnat_address<  |
| no |
| None |
|  |
| dnat translated address </td></tr>
| dnat_port<  |
| no |
| None |
|  |
| dnat translated port </td></tr>
| existing_rule<  |
| no |
|  |
|  |
| If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required. </td></tr>
| ip_address<  |
| yes |
|  |
|  |
| IP address (or hostname) of PAN-OS device being configured. </td></tr>
| location<  |
| no |
|  |
|  |
| Position to place the created rule in the rule base.  Supported values are <em>top</em>/<em>bottom</em>/<em>before</em>/<em>after</em>. </td></tr>
| operation<  |
| no |
|  |
|  |
| The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>/<em>disable</em>. </td></tr>
| password<  |
| yes |
|  |
|  |
| Password credentials to use for auth unless <em>api_key</em> is set. </td></tr>
| rule_name<  |
| yes |
|  |
|  |
| name of the SNAT rule </td></tr>
| service<  |
| no |
| any |
|  |
| service </td></tr>
| snat_address_type<  |
| no |
| translated-address |
|  |
| type of source translation. Supported values are <em>translated-address</em>/<em>interface-address</em>. </td></tr>
| snat_bidirectional<  |
| no |
| false |
|  |
| bidirectional flag </td></tr>
| snat_dynamic_address<  |
| no |
| None |
|  |
| Source NAT translated address. Used with Dynamic-IP and Dynamic-IP-and-Port. </td></tr>
| snat_interface<  |
| no |
| None |
|  |
| snat interface </td></tr>
| snat_interface_address<  |
| no |
| None |
|  |
| snat interface address </td></tr>
| snat_static_address<  |
| no |
| None |
|  |
| Source NAT translated address. Used with Static-IP translation. </td></tr>
| snat_type<  |
| no |
| None |
|  |
| type of source translation </td></tr>
| source_ip<  |
| no |
| [u'any'] |
|  |
| list of source addresses </td></tr>
| source_zone<  |
| yes |
|  |
|  |
| list of source zones </td></tr>
| username<  |
| no |
| admin |
|  |
| Username credentials to use for auth unless <em>api_key</em> is set. </td></tr>
</table>
</br>



## Examples

    # Create a source and destination nat rule
      - name: Create NAT SSH rule for 10.0.1.101
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          rule_name: "Web SSH"
          source_zone: ["external"]
          destination_zone: "external"
          source: ["any"]
          destination: ["10.0.0.100"]
          service: "service-tcp-221"
          snat_type: "dynamic-ip-and-port"
          snat_interface: "ethernet1/2"
          dnat_address: "10.0.1.101"
          dnat_port: "22"
    
      - name: disable a specific security rule
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'disable'
          rule_name: 'Prod-Legacy 1'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

