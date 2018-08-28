# panos_dag

_(versionadded:: 2.3)_


## Synopsis

Create a dynamic address group object in the firewall used for policy rules


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
<tr><td>dag_match_filter<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>dynamic filter user by the dynamic address group</div></td></tr>
<tr><td>dag_name<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>name of the dynamic address group</div></td></tr>
<tr><td>description<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>The description of the object.</div></td></tr>
<tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>None</td>
<td></td>
<td><div>The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.</div></td></tr>
<tr><td>ip_address<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>IP address (or hostname) of PAN-OS device</div></td></tr>
<tr><td>operation<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>The operation to perform Supported values are <em>add</em>/<em>list</em>/<em>delete</em>.</div></td></tr>
<tr><td>password<br/><div style="font-size: small;"></div></td>
<td>yes</td>
<td></td>
<td></td>
<td><div>password for authentication</div></td></tr>
<tr><td>tag_name<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td></td>
<td></td>
<td><div>Add administrative tags to the DAG</div></td></tr>
<tr><td>username<br/><div style="font-size: small;"></div></td>
<td>no</td>
<td>admin</td>
<td></td>
<td><div>username for authentication</div></td></tr>
</table>
</br>



## Examples

    - name: dag
        panos_dag:
            ip_address: "192.168.1.1"
            password: "admin"
            dag_name: "dag-1"
            dag_match_filter: "'aws-tag.aws:cloudformation:logical-id.ServerInstance' and 'instanceState.running'"
            description: 'Add / create dynamic address group to allow access to SaaS Applications'
            operation: 'add'




#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

