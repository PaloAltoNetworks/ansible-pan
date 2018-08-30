# panos_security_rule

_(versionadded:: 2.4)_


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
- xmltodict can be obtained from PyPi https://pypi.python.org/pypi/xmltodict

## Options

<table border=1 cellpadding=4>
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr><td>action<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>allow</td>
<td></td>
<td><div>Action to apply once rules maches.</div></td></tr>
<tr><td>antivirus<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined antivirus profile.</div></td></tr>
<tr><td>api_key<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
<tr><td>application<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>List of applications.</div></td></tr>
<tr><td>commit<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>Commit configuration if changed.</div></td></tr>
<tr><td>data_filtering<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined data_filtering profile.</div></td></tr>
<tr><td>description<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Description for the security rule.</div></td></tr>
<tr><td>destination_ip<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>List of destination addresses.</div></td></tr>
<tr><td>destination_zone<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>List of destination zones.</div></td></tr>
<tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>- Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
    </div></td></tr>
<tr><td>existing_rule<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required.</div></td></tr>
<tr><td>file_blocking<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined file_blocking profile.</div></td></tr>
<tr><td>group_profile<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>- Security profile group that is already defined in the system. This property supersedes antivirus, vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
    </div></td></tr>
<tr><td>hip_profiles<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>- If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy on information collected by GlobalProtect. For example, the user access level can be determined HIP that notifies the firewall about the user's local configuration.
    </div></td></tr>
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
<tr><td>log_end<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>True</td>
<td></td>
<td><div>Whether to log at session end.</div></td></tr>
<tr><td>log_setting<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Log forwarding profile</div></td></tr>
<tr><td>log_start<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Whether to log at session start.</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>add</td>
<td></td>
<td><div>The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.</div></td></tr>
<tr><td>panorama_post_rule<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>If the security rule is applied against panorama, set this to True in order to inject it into post rule.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
<tr><td>rule_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>Name of the security rule.</div></td></tr>
<tr><td>rule_type<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>universal</td>
<td></td>
<td><div>Type of security rule (version 6.1 of PanOS and above).</div></td></tr>
<tr><td>service<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>application-default</td>
<td></td>
<td><div>List of services.</div></td></tr>
<tr><td>source_ip<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>List of source addresses.</div></td></tr>
<tr><td>source_user<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>Use users to enforce policy for individual users or a group of users.</div></td></tr>
<tr><td>source_zone<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>any</td>
<td></td>
<td><div>List of source zones.</div></td></tr>
<tr><td>spyware<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined spyware profile.</div></td></tr>
<tr><td>tag_name<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Administrative tags that can be added to the rule. Note, tags must be already defined.</div></td></tr>
<tr><td>url_filtering<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined url_filtering profile.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
<tr><td>vulnerability<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined vulnerability profile.</div></td></tr>
<tr><td>wildfire_analysis<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>Name of the already defined wildfire_analysis profile.</div></td></tr>
</table>
</br>



## Examples

    - name: add an SSH inbound rule to devicegroup
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        rule_name: 'SSH permit'
        description: 'SSH rule test'
        tag_name: ['ProjectX']
        source_zone: ['public']
        destination_zone: ['private']
        source: ['any']
        source_user: ['any']
        destination: ['1.1.1.1']
        category: ['any']
        application: ['ssh']
        service: ['application-default']
        hip_profiles: ['any']
        action: 'allow'
        devicegroup: 'Cloud Edge'
    
    - name: add a rule to allow HTTP multimedia only from CDNs
      panos_security_rule:
        ip_address: '10.5.172.91'
        username: 'admin'
        password: 'paloalto'
        operation: 'add'
        rule_name: 'HTTP Multimedia'
        description: 'Allow HTTP multimedia only to host at 1.1.1.1'
        source_zone: ['public']
        destination_zone: ['private']
        source: ['any']
        source_user: ['any']
        destination: ['1.1.1.1']
        category: ['content-delivery-networks']
        application: ['http-video', 'http-audio']
        service: ['service-http', 'service-https']
        hip_profiles: ['any']
        action: 'allow'
    
    - name: add a more complex rule that uses security profiles
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        rule_name: 'Allow HTTP w profile'
        log_start: false
        log_end: true
        action: 'allow'
        antivirus: 'default'
        vulnerability: 'default'
        spyware: 'default'
        url_filtering: 'default'
        wildfire_analysis: 'default'
    
    - name: delete a devicegroup security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'delete'
        rule_name: 'Allow telnet'
        devicegroup: 'DC Firewalls'
    
    - name: find a specific security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        operation: 'find'
        rule_name: 'Allow RDP to DCs'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: add a rule at a specific location in the rulebase
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        rule_name: 'SSH permit'
        description: 'SSH rule test'
        source_zone: ['untrust']
        destination_zone: ['trust']
        source_ip: ['any']
        source_user: ['any']
        destination_ip: ['1.1.1.1']
        category: ['any']
        application: ['ssh']
        service: ['application-default']
        action: 'allow'
        location: 'before'
        existing_rule: 'Prod-Legacy 1'
    
    - name: disable a specific security rule
      panos_security_rule:
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

