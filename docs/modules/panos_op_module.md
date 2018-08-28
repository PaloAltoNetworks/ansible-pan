# panos_op

_(versionadded:: 2.5)_


## Synopsis

T
h
i
s
 
m
o
d
u
l
e
 
w
i
l
l
 
a
l
l
o
w
 
u
s
e
r
 
t
o
 
p
a
s
s
 
a
n
d
 
e
x
e
c
u
t
e
 
a
n
y
 
s
u
p
p
o
r
t
e
d
 
O
P
 
c
o
m
m
a
n
d
 
o
n
 
t
h
e
 
P
A
N
W
 
d
e
v
i
c
e
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
| cmd<  |
| yes |
|  |
|  |
| The OP command to be performed. </td></tr>
| cmd_is_xml<  |
| no |
|  |
| yes / no |
| The cmd is already given in XML format, so don't convert it. </td></tr>
| ip_address<  |
| yes |
|  |
|  |
| IP address (or hostname) of PAN-OS device or Panorama management console being configured. </td></tr>
| password<  |
| yes |
|  |
|  |
| Password credentials to use for authentication. </td></tr>
| username<  |
| no |
| admin |
|  |
| Username credentials to use for authentication. </td></tr>
</table>
</br>



## Examples

    - name: show list of all interfaces
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show interfaces all'
    
    - name: show system info
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: 'show system info'
    
    - name: show system info as XML command
      panos_op:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        cmd: '<show><system><info/></system></show>'
#### Return Values

The following are the fields unique to this module:

| name | description | returned | type | sample |

| stdout_xml | output of the given OP command as JSON formatted string | success | string | <response status=success><result><system><hostname>fw2</hostname> </td> |
| stdout | output of the given OP command as JSON formatted string | success | string | {system: {app-release-date: 2017/05/01  15:09:12}} </td> |

#### Notes

- Checkmode is NOT supported.
- Panorama is NOT supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

