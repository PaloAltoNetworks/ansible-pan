.. _panos_dag:

panos_dag
``````````````````````````````

Create a dynamic address group 

.. raw:: html

    <table>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr>
    <td>username</td>
    <td>no</td>
    <td>admin</td>
    <td><ul></ul></td>
    <td>username for authentication</td>
    </tr>
        <tr>
    <td>dag_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the dynamic address group</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
    </tr>
        <tr>
    <td>password</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>password for authentication</td>
    </tr>
        <tr>
    <td>ip_address</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>IP address (or hostname) of PAN-OS device</td>
    </tr>
        <tr>
    <td>dag_filter</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>dynamic filter user by the dynamic address group</td>
    </tr>
        </table>

Examples
--------

 ::

    
    - name: dag
      panos_dag:
        ip_address: "192.168.1.1"
        password: "admin"
        dag_name: "dag-1"
        dag_filter: "'aws-tag.aws:cloudformation:logical-id.ServerInstance' and 'instanceState.running'"
