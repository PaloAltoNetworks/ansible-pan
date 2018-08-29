# panos_sag

_(versionadded:: 2.4)_


## Synopsis

Create a static address group object in the firewall used for policy rules.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice
- xmltodict can be obtained from PyPi https://pypi.python.org/pypi/xmltodict

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |

NOT suboptions
|api_key|no||
API key that can be used instead of <em>username</em>/<em>password</em> credentials.
 |
NOT suboptions
|commit|no||
commit if changed
 |
NOT suboptions
|description|no||
The purpose / objective of the static Address Group
 |
NOT suboptions
|devicegroup|no||
- The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.
    
 |
NOT suboptions
|ip_address|yes||
IP address (or hostname) of PAN-OS device
 |
NOT suboptions
|operation|yes||
The operation to perform Supported values are <em>add</em>/<em>list</em>/<em>delete</em>.
 |
NOT suboptions
|password|yes||
password for authentication
 |
NOT suboptions
|sag_name|yes||
name of the dynamic address group
 |
NOT suboptions
|static_match_filter|yes||
Static filter used by the address group
 |
NOT suboptions
|tags|no||
Tags to be associated with the address group
 |
NOT suboptions
|username|no||
username for authentication
 |

## Examples

    - name: sag
      panos_sag:
        ip_address: "192.168.1.1"
        password: "admin"
        sag_name: "sag-1"
        static_value: ['test-addresses', ]
        description: "A description for the static address group"
        tags: ["tags to be associated with the group", ]




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

