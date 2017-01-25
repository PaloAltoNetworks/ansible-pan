.. _panos_security_policy:

panos_security_policy
``````````````````````````````

Synopsis
--------


Create a security policy


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
    <td style="vertical-align:middle">vulnprofile_name</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">None</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      name of the vulnerability profile<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">hip_profiles</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of HIP profiles<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">rule_name</td>
    <td style="vertical-align:middle">yes</td>
    <td style="vertical-align:middle"></td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      name of the security rule<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">log_start</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">false</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether to log at session start<br></td>
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
    <td style="vertical-align:middle">rule_type</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">universal</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      type of security rule (6.1+)<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">to_zone</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of destination zones<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">service</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">application-default</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of services<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">source</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of source addresses<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">destination</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of destination addresses<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">from_zone</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of source zones<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">application</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">any</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      list of applications<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">group_profile</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">None</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      security profile group<br></td>
    </tr>
        <tr style="text-align:center">
    <td style="vertical-align:middle">action</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">allow</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      action<br></td>
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
    <td style="vertical-align:middle">log_end</td>
    <td style="vertical-align:middle">no</td>
    <td style="vertical-align:middle">True</td>
        <td style="vertical-align:middle;text-align:left"><ul style="margin:0;"></ul></td>
        <td style="vertical-align:middle;text-align:left">
      whether to log at session end<br></td>
    </tr>
        </table><br>


.. important:: Requires pan-python


Examples
--------

 ::

    
    # permti ssh to 1.1.1.1
    - panos_security_policy:
        ip_address: "192.168.1.1"
        password: "admin"
        rule_name: "SSH permit"
        from_zone: ["public"]
        to_zone: ["private"]
        source: ["any"]
        source_user: ["any"]
        destination: ["1.1.1.1"]
        category: ["any"]
        application: ["ssh"]
        service: ["application-default"]
        hip_profiles: ["any"]
        action: "allow"
        commmit: False
    
    # deny all
    - panos_security_policy:
        ip_address: "192.168.1.1"
        password: "admin"
        rule_name: "DenyAll"
        username: "admin"
        log_start: true
        log_end: true
        action: "deny"
        rule_type: "interzone"
        commmit: False
