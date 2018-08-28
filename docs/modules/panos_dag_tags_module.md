# panos_dag_tags

_(versionadded:: 2.5)_


## Synopsis

Create the ip address to tag associations. Tags will in turn be used to create DAG's


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
<td><div>commit if changed</div></td></tr>
<tr><td>description<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The purpose / objective of the static Address Group</div></td></tr>
<tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>- Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
    </div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
<tr><td>ip_to_register<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>IP that will be registered with the given tag names.</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The action to be taken. Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>password for authentication</div></td></tr>
<tr><td>tag_names<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The list of the tags that will be added or removed from the IP address.</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>username for authentication</div></td></tr>
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

