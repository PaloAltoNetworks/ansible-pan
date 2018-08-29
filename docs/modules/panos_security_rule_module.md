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

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |

NOT suboptions
|action|no||
Action to apply once rules maches.
 |
NOT suboptions
|antivirus|no||
Name of the already defined antivirus profile.
 |
NOT suboptions
|api_key|no||
API key that can be used instead of <em>username</em>/<em>password</em> credentials.
 |
NOT suboptions
|application|no||
List of applications.
 |
NOT suboptions
|commit|no||
Commit configuration if changed.
 |
NOT suboptions
|data_filtering|no||
Name of the already defined data_filtering profile.
 |
NOT suboptions
|description|no||
Description for the security rule.
 |
NOT suboptions
|destination_ip|no||
List of destination addresses.
 |
NOT suboptions
|destination_zone|no||
List of destination zones.
 |
NOT suboptions
|devicegroup|no||
- Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
    
 |
NOT suboptions
|existing_rule|no||
If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required.
 |
NOT suboptions
|file_blocking|no||
Name of the already defined file_blocking profile.
 |
NOT suboptions
|group_profile|no||
- Security profile group that is already defined in the system. This property supersedes antivirus, vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
    
 |
NOT suboptions
|hip_profiles|no||
- If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy on information collected by GlobalProtect. For example, the user access level can be determined HIP that notifies the firewall about the user's local configuration.
    
 |
NOT suboptions
|ip_address|yes||
IP address (or hostname) of PAN-OS device being configured.
 |
NOT suboptions
|location|no||
Position to place the created rule in the rule base.  Supported values are <em>top</em>/<em>bottom</em>/<em>before</em>/<em>after</em>.
 |
NOT suboptions
|log_end|no||
Whether to log at session end.
 |
NOT suboptions
|log_setting|no||
Log forwarding profile
 |
NOT suboptions
|log_start|no||
Whether to log at session start.
 |
NOT suboptions
|operation|no||
The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.
 |
NOT suboptions
|panorama_post_rule|no||
If the security rule is applied against panorama, set this to True in order to inject it into post rule.
 |
NOT suboptions
|password|yes||
Password credentials to use for auth unless <em>api_key</em> is set.
 |
NOT suboptions
|rule_name|yes||
Name of the security rule.
 |
NOT suboptions
|rule_type|no||
Type of security rule (version 6.1 of PanOS and above).
 |
NOT suboptions
|service|no||
List of services.
 |
NOT suboptions
|source_ip|no||
List of source addresses.
 |
NOT suboptions
|source_user|no||
Use users to enforce policy for individual users or a group of users.
 |
NOT suboptions
|source_zone|no||
List of source zones.
 |
NOT suboptions
|spyware|no||
Name of the already defined spyware profile.
 |
NOT suboptions
|tag_name|no||
Administrative tags that can be added to the rule. Note, tags must be already defined.
 |
NOT suboptions
|url_filtering|no||
Name of the already defined url_filtering profile.
 |
NOT suboptions
|username|no||
Username credentials to use for auth unless <em>api_key</em> is set.
 |
NOT suboptions
|vulnerability|no||
Name of the already defined vulnerability profile.
 |
NOT suboptions
|wildfire_analysis|no||
Name of the already defined wildfire_analysis profile.
 |

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

