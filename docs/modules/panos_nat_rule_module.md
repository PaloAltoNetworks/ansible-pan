---
title: panos_nat_rule
---
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
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of <em>username</em>/<em>password</em> credentials. |
| commit |  | True |  | Commit configuration if changed. |
| destination_ip |  | [u'any'] |  | list of destination addresses |
| destination_zone | yes |  |  | destination zone |
| dnat_address |  | None |  | dnat translated address |
| dnat_port |  | None |  | dnat translated port |
| existing_rule |  |  |  | If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| location |  |  |  | Position to place the created rule in the rule base.  Supported values are <em>top</em>/<em>bottom</em>/<em>before</em>/<em>after</em>. |
| operation |  |  |  | The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>/<em>disable</em>. |
| password | yes |  |  | Password credentials to use for auth unless <em>api_key</em> is set. |
| rule_name | yes |  |  | name of the SNAT rule |
| service |  | any |  | service |
| snat_address_type |  | translated-address |  | type of source translation. Supported values are <em>translated-address</em>/<em>interface-address</em>. |
| snat_bidirectional |  | false |  | bidirectional flag |
| snat_dynamic_address |  | None |  | Source NAT translated address. Used with Dynamic-IP and Dynamic-IP-and-Port. |
| snat_interface |  | None |  | snat interface |
| snat_interface_address |  | None |  | snat interface address |
| snat_static_address |  | None |  | Source NAT translated address. Used with Static-IP translation. |
| snat_type |  | None |  | type of source translation |
| source_ip |  | [u'any'] |  | list of source addresses |
| source_zone | yes |  |  | list of source zones |
| username |  | admin |  | Username credentials to use for auth unless <em>api_key</em> is set. |

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

