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

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>commit<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>Commit configuration if changed.</div></td></tr>
<tr><td>destination_ip<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>[u'any']</td>
<td></td>
<td><div>list of destination addresses</div></td></tr>
<tr><td>destination_zone<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>destination zone</div></td></tr>
<tr><td>dnat_address<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>dnat translated address</div></td></tr>
<tr><td>dnat_port<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>dnat translated port</div></td></tr>
<tr><td>existing_rule<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
<tr><td>location<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Position to place the created rule in the rule base.  Supported values are <em>top</em>/<em>bottom</em>/<em>before</em>/<em>after</em>.</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>/<em>disable</em>.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
<tr><td>rule_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>name of the SNAT rule</div></td></tr>
<tr><td>service<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>service</div></td></tr>
<tr><td>snat_address_type<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>translated-address</td>
<td></td>
<td><div>type of source translation. Supported values are <em>translated-address</em>/<em>interface-address</em>.</div></td></tr>
<tr><td>snat_bidirectional<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>false</td>
<td></td>
<td><div>bidirectional flag</div></td></tr>
<tr><td>snat_dynamic_address<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Source NAT translated address. Used with Dynamic-IP and Dynamic-IP-and-Port.</div></td></tr>
<tr><td>snat_interface<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>snat interface</div></td></tr>
<tr><td>snat_interface_address<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>snat interface address</div></td></tr>
<tr><td>snat_static_address<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Source NAT translated address. Used with Static-IP translation.</div></td></tr>
<tr><td>snat_type<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>type of source translation</div></td></tr>
<tr><td>source_ip<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>[u'any']</td>
<td></td>
<td><div>list of source addresses</div></td></tr>
<tr><td>source_zone<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>list of source zones</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
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

