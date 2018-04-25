.. _panos_security_rule:


panos_security_rule
+++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Security policies allow you to enforce rules and take action, and can be as general or specific as needed. The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches the traffic is applied, the more specific rules must precede the more general ones.


Requirements (on host that executes module)
-------------------------------------------

  * pan-python can be obtained from PyPi https://pypi.python.org/pypi/pan-python
  * pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice
  * xmltodict can be obtained from PyPi https://pypi.python.org/pypi/xmltodict


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
                <tr><td>action<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>allow</td>
        <td></td>
        <td><div>Action to apply once rules maches.</div>        </td></tr>
                <tr><td>antivirus<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined antivirus profile.</div>        </td></tr>
                <tr><td>api_key<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div>        </td></tr>
                <tr><td>application<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>List of applications.</div>        </td></tr>
                <tr><td>commit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td></td>
        <td><div>Commit configuration if changed.</div>        </td></tr>
                <tr><td>data_filtering<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined data_filtering profile.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Description for the security rule.</div>        </td></tr>
                <tr><td>destination_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>List of destination addresses.</div>        </td></tr>
                <tr><td>destination_zone<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>List of destination zones.</div>        </td></tr>
                <tr><td>devicegroup<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>- Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.
    </div>        </td></tr>
                <tr><td>file_blocking<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined file_blocking profile.</div>        </td></tr>
                <tr><td>group_profile<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>- Security profile group that is already defined in the system. This property supersedes antivirus, vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties.
    </div>        </td></tr>
                <tr><td>hip_profiles<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>- If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy on information collected by GlobalProtect. For example, the user access level can be determined HIP that notifies the firewall about the user's local configuration.
    </div>        </td></tr>
                <tr><td>ip_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>IP address (or hostname) of PAN-OS device being configured.</div>        </td></tr>
                <tr><td>log_end<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td></td>
        <td><div>Whether to log at session end.</div>        </td></tr>
                <tr><td>log_start<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Whether to log at session start.</div>        </td></tr>
                <tr><td>operation<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>add</td>
        <td></td>
        <td><div>The action to be taken.  Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>/<em>disable</em>.</div>        </td></tr>
                <tr><td>panorama_post_rule<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>If the security rule is applied against panorama, set this to True in order to inject it into post rule.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Password credentials to use for auth unless <em>api_key</em> is set.</div>        </td></tr>
                <tr><td>position<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Forces a position of the rule. Use '0' for top. Don't specify one if appending the rule to the end.</div>        </td></tr>
                <tr><td>rule_name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the security rule.</div>        </td></tr>
                <tr><td>rule_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>universal</td>
        <td></td>
        <td><div>Type of security rule (version 6.1 of PanOS and above).</div>        </td></tr>
                <tr><td>service<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>application-default</td>
        <td></td>
        <td><div>List of services.</div>        </td></tr>
                <tr><td>source_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>List of source addresses.</div>        </td></tr>
                <tr><td>source_user<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>Use users to enforce policy for individual users or a group of users.</div>        </td></tr>
                <tr><td>source_zone<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>any</td>
        <td></td>
        <td><div>List of source zones.</div>        </td></tr>
                <tr><td>spyware<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined spyware profile.</div>        </td></tr>
                <tr><td>tag_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Administrative tags that can be added to the rule. Note, tags must be already defined.</div>        </td></tr>
                <tr><td>url_filtering<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined url_filtering profile.</div>        </td></tr>
                <tr><td>username<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>admin</td>
        <td></td>
        <td><div>Username credentials to use for auth unless <em>api_key</em> is set.</div>        </td></tr>
                <tr><td>vulnerability<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined vulnerability profile.</div>        </td></tr>
                <tr><td>wildfire_analysis<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Name of the already defined wildfire_analysis profile.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: add an SSH inbound rule to devicegroup
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        rule_name: 'SSH permit'
        description: 'SSH rule test'
        tag_name: ['ProjectX']
        source_zone: ['public']
        destination_zone: ['private']
        source: ['any']
        source_user: ['any']
        destination: ['1.1.1.1']
        category: ['any']
        application: ['ssh']
        service: ['application-default']
        hip_profiles: ['any']
        action: 'allow'
        devicegroup: 'Cloud Edge'
    
    - name: add a rule to allow HTTP multimedia only from CDNs
      panos_security_rule:
        ip_address: '10.5.172.91'
        username: 'admin'
        password: 'paloalto'
        operation: 'add'
        rule_name: 'HTTP Multimedia'
        description: 'Allow HTTP multimedia only to host at 1.1.1.1'
        source_zone: ['public']
        destination_zone: ['private']
        source: ['any']
        source_user: ['any']
        destination: ['1.1.1.1']
        category: ['content-delivery-networks']
        application: ['http-video', 'http-audio']
        service: ['service-http', 'service-https']
        hip_profiles: ['any']
        action: 'allow'
    
    - name: add a more complex rule that uses security profiles
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
        rule_name: 'Allow HTTP w profile'
        log_start: false
        log_end: true
        action: 'allow'
        antivirus: 'default'
        vulnerability: 'default'
        spyware: 'default'
        url_filtering: 'default'
        wildfire_analysis: 'default'
    
    - name: delete a devicegroup security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'delete'
        rule_name: 'Allow telnet'
        devicegroup: 'DC Firewalls'
    
    - name: find a specific security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        password: '{{ password }}'
        operation: 'find'
        rule_name: 'Allow RDP to DCs'
      register: result
    - debug: msg='{{result.stdout_lines}}'
    
    - name: Add test rule 4 to the firewall in position 1!!
        panos_security_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'add'
          position: '1'
          rule_name: 'Ansible test 4'
          description: 'Another Ansible test rule'
          source_zone: ['internal']
          source_ip: ['192.168.100.101']
          source_user: ['any']
          hip_profiles: ['any']
          destination_zone: ['external']
          destination_ip: ['any']
          category: ['any']
          application: ['any']
          service: ['service-https']
          action: 'allow'
          commit: 'False'
    
    - name: disable a specific security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'disable'
        rule_name: 'Prod-Legacy 1'


Notes
-----

.. note::
    - Checkmode is not supported.
    - Panorama is supported.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

