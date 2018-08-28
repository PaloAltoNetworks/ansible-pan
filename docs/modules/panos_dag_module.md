# panos_dag

_(versionadded:: 2.3)_


## Synopsis

Create a dynamic address group object in the firewall used for policy rules


## Requirements (on host that executes module)

- pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice
- xmltodict can be obtained from PyPi https://pypi.python.org/pypi/xmltodict

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
| dag_match_filter  |
| yes |
|  |
| |  |
| dynamic filter user by the dynamic address group  |
</td></tr>
| dag_name  |
| yes |
|  |
| |  |
| name of the dynamic address group  |
</td></tr>
| description  |
| no |
|  |
| |  |
| The description of the object.  |
</td></tr>
| devicegroup  |
| no |
| None |
| |  |
| The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.  |
</td></tr>
| ip_address  |
| yes |
|  |
| |  |
| IP address (or hostname) of PAN-OS device  |
</td></tr>
| operation  |
| yes |
|  |
| |  |
| The operation to perform Supported values are <em>add</em>/<em>list</em>/<em>delete</em>.  |
</td></tr>
| password  |
| yes |
|  |
| |  |
| password for authentication  |
</td></tr>
| tag_name  |
| no |
|  |
| |  |
| Add administrative tags to the DAG  |
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

