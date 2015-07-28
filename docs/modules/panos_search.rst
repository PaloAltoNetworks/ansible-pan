.. _panos_search:

panos_search
``````````````````````````````

Search and return AMI ID of PA-VM-AWS instance in a specific region. 
All the standard EC2 module paramaters are supported. 

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
    <td>release</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>release of PAN-OS</td>
    </tr>
        <tr>
    <td>first</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>whether return only the first AMI found</td>
    </tr>
        </table>

Examples
--------

 ::

    
    - name: retrieve PA-VM-AWS AMI ID
      panos_search:
        region: "eu-west-1"
        release: "6.1.0"
      register: pavmawsamiid
