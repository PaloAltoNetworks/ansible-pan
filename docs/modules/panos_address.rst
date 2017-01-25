.. _panos_address:

panos_address
``````````````````````````````

Synopsis
--------


Create address service object of different types [IP Range, FQDN, or IP Netmask].


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
        <td style="vertical-align:middle">ip_address</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">IP address (or hostname) of PAN-OS device<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">username</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">admin</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">username for authentication<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">IP address with or without mask, range, or fqdn<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">address_name</td>
        <td style="vertical-align:middle">yes</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">name of the addressr<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">type</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">ip-netmask</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">ip-netmask, fqdn, ip-range<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">description</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">description of address object<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">tag</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">tag of address object<br></td>
    </tr>
    <tr style="text-align:center">
        <td style="vertical-align:middle">commit</td>
        <td style="vertical-align:middle">no</td>
        <td style="vertical-align:middle">true</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">commit if changed<br></td>
    </tr>
    </table><br>


.. important:: Requires pan-python


Examples
--------

 ::

    
    # Creates service for port 22
    # Doesn't commit the candidate config
      - name: create IP-Netmask Object
        panos_address:
          ip_address: "192.168.1.1"
          password: 'admin'
          address_name: 'google_dns'
          address: '8.8.8.8/32'
          description: 'Google DNS'
          tag: 'Outbound'
          commit: False

    # Creates ip-range for whitelist
    # Doesn't commit the candidate config
      - name: create IP-Range Object
        panos_address:
          ip_address: "192.168.1.1"
          password: 'admin'
          type: 'ip-range'
          address_name: 'apple-range'
          address: '17.0.0.0-17.255.255.255'
          commit: False

    # Creates FQDN
    # Doesn't commit the candidate config
      - name: create FQDN Object
        panos_address:
          ip_address: "192.168.1.1"
          password: 'admin'
          type: 'fqdn'
          address_name: 'google.com'
          address: 'www.google.com'