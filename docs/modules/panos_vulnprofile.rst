.. _panos_vulnprofile:

panos_vulnprofile
``````````````````````````````

Create custom vulnerability profile 

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
    <td>rule_tuples</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>a list of dictionaries that contains each rule definition. A rule is made of:rule_name: requiredthreat_name: optional, deafult is 'any'vendor_id: optional, deafult is 'any'cve: optional, deafult is 'any'host_type: optional, deafult is 'client'severity: requiredaction: optional, deafult is 'default'capture: optional, deafult is 'disable'</td>
    </tr>
        </table>

Examples
--------

 ::

    
    panos_vulnprofile:
      ip_address: "10.0.0.43"
      password: "admin"
      vulnprofile_name: "SampleVRule"
      description: "some description"
      rule_tuples: [{'rule_name': 'simple-client-critical', 'threat_name': 'any', 'vendor_id': 'any', 'cve': '1.1.1.1', 'host_type': 'client', 'severity': 'critical', 'action': 'default', 'capture': 'disable'}, {'rule_name': 'simple-client-high', 'threat_name': 'any', 'cve': 'any', 'vendor_id': '1.1.1.1', 'host_type': 'client', 'severity': 'high', 'action': 'default', 'capture': 'disable'}]
      exception_ids: ["35931","35933"]
      commit: False
