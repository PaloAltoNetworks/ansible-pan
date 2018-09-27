---
title: panos_zone
---
# panos_zone

_(versionadded:: 2.8)_


## Synopsis

Configure security zones on PAN-OS firewall or in Panorama template.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| enable_userid |  |  |  | Enable user identification. |
| exclude_acl |  |  |  | User identification ACL exclude list. |
| include_acl |  |  |  | User identification ACL include list. |
| interface |  |  |  | List of member interfaces. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| log_setting |  |  |  | Log forwarding setting. |
| mode |  | layer3 |  | The mode of the security zone. Must match the mode of the interface.Possible values *tap*/*virtual-wire*/*layer2*/*layer3*/*external* |
| password |  |  |  | Password credentials to use for auth. |
| state |  |  |  | The state of the zone.Possible values *present*/*absent*. |
| template |  |  |  | The Panorama template in which to create the zone. |
| username |  | admin |  | Username credentials to use for auth. |
| vsys |  | vsys1 |  | The firewall VSYS in which to create the zone. |
| zone | yes |  |  | Name of the security zone to configure. |
| zone_profile |  |  |  | Zone protection profile. |

## Examples

    # Create an L3 zone.
    - name: create DMZ zone on a firewall
      panos_zone:
        ip_address: {{ ip_address }}
        api_key: {{ api_key }}
        zone: 'dmz'
        mode: 'layer3'
        zone_profile: 'strict'
    
    # Add an interface to the zone.
    - name: add ethernet1/2 to zone dmz
      panos_interface:
        ip_address: '192.168.1.1'
        username: 'ansible'
        password: 'secret'
        zone: 'dmz'
        mode: 'layer3'
        interface: ['ethernet1/2']
        zone_profile: 'strict'
        
    # Delete the zone.
    - name: delete the DMZ zone
      panos_interface:
        ip_address: '192.168.1.1'
        username: 'ansible'
        password: 'secret'
        zone: 'dmz'
        state: 'absent'
        
    # Add a zone to a multi-VSYS Panorama template
    - name: add Cloud zone to template
      panos_interface:
        ip_address: {{ ip_address }}
        api_key: {{ api_key }}
        zone: 'datacenter'
        mode: 'layer3'
        enable_userid: true
        exclude_ip: '10.0.200.0/24'
        template: 'Datacenter Template'
        vsys: 'vsys4'
        




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

