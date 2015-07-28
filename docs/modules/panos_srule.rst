.. _panos_srule:

panos_srule
``````````````````````````````

Create a security rule 

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
    <td>vulnprofile_name</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the vulnerability profile</td>
    </tr>
        <tr>
    <td>hip_profiles</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of HIP profiles</td>
    </tr>
        <tr>
    <td>rule_name</td>
    <td>yes</td>
    <td></td>
    <td><ul></ul></td>
    <td>name of the security rule</td>
    </tr>
        <tr>
    <td>log_start</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>whether to log at session start</td>
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
    <td>rule_type</td>
    <td>no</td>
    <td>universal</td>
    <td><ul></ul></td>
    <td>type of security rule (6.1+)</td>
    </tr>
        <tr>
    <td>to_zone</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of destination zones</td>
    </tr>
        <tr>
    <td>service</td>
    <td>no</td>
    <td>application-default</td>
    <td><ul></ul></td>
    <td>list of services</td>
    </tr>
        <tr>
    <td>source</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of source addresses</td>
    </tr>
        <tr>
    <td>destination</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of destination addresses</td>
    </tr>
        <tr>
    <td>from_zone</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of source zones</td>
    </tr>
        <tr>
    <td>application</td>
    <td>no</td>
    <td>any</td>
    <td><ul></ul></td>
    <td>list of applications</td>
    </tr>
        <tr>
    <td>group_profile</td>
    <td>no</td>
    <td></td>
    <td><ul></ul></td>
    <td>security profile group</td>
    </tr>
        <tr>
    <td>action</td>
    <td>no</td>
    <td>allow</td>
    <td><ul></ul></td>
    <td>action</td>
    </tr>
        <tr>
    <td>commit</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>commit if changed</td>
    </tr>
        <tr>
    <td>log_end</td>
    <td>no</td>
    <td>True</td>
    <td><ul></ul></td>
    <td>whether to log at session end</td>
    </tr>
        </table>

Examples
--------

 ::

    
    # permti ssh to 1.1.1.1
    - panos_srule:
        ip_address: "192.168.1.1"
        password: "admin"
        rule_name: "server permit"
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
    
    # deny all
    - panos_srule:
        ip_address: "192.168.1.1"
        password: "admin"
        username: "admin"
        log_start: true
        log_end: true
        action: "deny"
        rule_type: "interzone"
