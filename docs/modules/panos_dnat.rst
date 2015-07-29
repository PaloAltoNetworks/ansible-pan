.. _panos_dnat:

panos_dnat
``````````````````````````````

Synopsis
--------


Create a destination nat rule


.. important:: Superseded, use panos_nat module


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
    <td style="vertical-align:middle">translated_address</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">None</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      translated address<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">to_zone</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      destination zone<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">service</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      service<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">rule_name</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      name of the SNAT rule<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">destination</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      destination address<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">from_zone</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      source zone<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">source</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      source address<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">translated_port</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">None</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      translated port<br></td>
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
        </table><br>


.. important:: Requires pan-python


Examples
--------

 ::

    
    # Create a destination nat rule dnat-ssh on 192.168.1.1
      - name: create destination nat rule for server
        panos_dnat:
          ip_address: "192.168.1.1"
          password: "admin"
          rule_name: "dnat-ssh"
          from_zone: "external"
          to_zone: "external"
          source: "any"
          destination: "{{PAVMAWSPublicIP}}"
          service: "service-tcp-22"
          translated_address: "{{ServerIP}}"

.. raw:: html

    <h4>Notes</h4>
        <p>Superseded, use panos_nat module</p>
    