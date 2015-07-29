.. _panos_vulnprofile:

panos_vulnprofile
``````````````````````````````

Synopsis
--------

Create custom vulnerability profile


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">username</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      username for authentication<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">commit</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">True</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      commit if changed<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">password</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      password for authentication<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">ip_address</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      IP address (or hostname) of PAN-OS device<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">rule_tuples</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">None</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      a list of dictionaries that contains each rule definition. A rule is made of:<br>rule_name: required<br>threat_name: optional, deafult is 'any'<br>vendor_id: optional, deafult is 'any'<br>cve: optional, deafult is 'any'<br>host_type: optional, deafult is 'client'<br>severity: required<br>action: optional, deafult is 'default'<br>capture: optional, deafult is 'disable'<br></td>
    </tr>
        </table><br>


.. important:: Requires pan-python


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
