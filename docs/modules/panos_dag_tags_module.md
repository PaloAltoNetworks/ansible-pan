# panos_dag_tags

_(versionadded:: 2.5)_


## Synopsis

Create the ip address to tag associations. Tags will in turn be used to create DAG's


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key  |
| no |
|  |
| |  |
| API key that can be used instead of <em>username</em>/<em>password</em> credentials.  |
</td></tr>
| commit  |
| no |
| True |
| |  |
| commit if changed  |
</td></tr>
| description  |
| no |
|  |
| |  |
| The purpose / objective of the static Address Group  |
</td></tr>
| devicegroup  |
| no |
|  |
| |  |
| - Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
      |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS device  |
</td></tr>
| ip_to_register  |
| no |
|  |
| |  |
| IP that will be registered with the given tag names.  |
</td></tr>
| operation  |
| no |
|  |
| |  |
| The action to be taken. Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| password for authentication  |
</td></tr>
| tag_names  |
| no |
|  |
| |  |
| The list of the tags that will be added or removed from the IP address.  |
</td></tr>
| username  |
| no |
| admin |
| |  |
| username for authentication  |
</td></tr>
</table>
</br>



## Examples

    - name: Create the tags to map IP addresses
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Tags to allow certain IP's to access various SaaS Applications"
        operation: 'add'
      tags: "adddagip"
    
    - name: List the IP address to tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        tag_names: "{{ tag_names }}"
        description: "List the IP address to tag mapping"
        operation: 'list'
      tags: "listdagip"
    
    - name: Unregister an IP address from a tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Unregister IP address from tag mappings"
        operation: 'delete'
      tags: "deletedagip"

#### Notes

- Checkmode is not supported.
- Panorama is not supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

