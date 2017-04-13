.. _panos_nat_rule:


panos_nat_rule - create a policy NAT rule
+++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create a policy nat rule. Keep in mind that we can either end up configuring source NAT, destination NAT, or both. Instead of splitting it into two we will make a fair attempt to determine which one the user wants.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
  * pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice


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
            <tr>
    <td>api_key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div></td></tr>
            <tr>
    <td>destination_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>[u'any']</td>
        <td><ul></ul></td>
        <td><div>list of destination addresses</div></td></tr>
            <tr>
    <td>destination_zone<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>destination zone</div></td></tr>
            <tr>
    <td>dnat_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>dnat translated address</div></td></tr>
            <tr>
    <td>dnat_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>dnat translated port</div></td></tr>
            <tr>
    <td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>IP address (or hostname) of PAN-OS device being configured.</div></td></tr>
            <tr>
    <td>operation<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
            <tr>
    <td>rule_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>name of the SNAT rule</div></td></tr>
            <tr>
    <td>service<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td><ul></ul></td>
        <td><div>service</div></td></tr>
            <tr>
    <td>snat_bidirectional<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>false</td>
        <td><ul></ul></td>
        <td><div>bidirectional flag</div></td></tr>
            <tr>
    <td>snat_dynamic_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Source NAT translated address. Used with Dynamic-IP and Dynamic-IP-and-Port.</div></td></tr>
            <tr>
    <td>snat_interface<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>snat interface</div></td></tr>
            <tr>
    <td>snat_interface_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>snat interface address</div></td></tr>
            <tr>
    <td>snat_static_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Source NAT translated address. Used with Static-IP translation.</div></td></tr>
            <tr>
    <td>snat_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>type of source translation</div></td></tr>
            <tr>
    <td>source_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>[u'any']</td>
        <td><ul></ul></td>
        <td><div>list of source addresses</div></td></tr>
            <tr>
    <td>source_zone<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>list of source zones</div></td></tr>
            <tr>
    <td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td><ul></ul></td>
        <td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    # Create a source and destination nat rule
      - name: Create NAT SSH rule for 10.0.1.101
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          rule_name: "Web SSH"
          source_zone: ["external"]
          destination_zone: "external"
          source: ["any"]
          destination: ["10.0.0.100"]
          service: "service-tcp-221"
          snat_type: "dynamic-ip-and-port"
          snat_interface: "ethernet1/2"
          dnat_address: "10.0.1.101"
          dnat_port: "22"


Notes
-----

.. note:: Checkmode is not supported.
.. note:: Panorama is supported.

