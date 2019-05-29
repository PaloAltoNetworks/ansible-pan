:source: panos_security_rule_facts.py

:orphan:

.. _panos_security_rule_facts_module:


panos_security_rule_facts -- Get information about a security rule
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about a single security rule or the names of all security rules.



Requirements
------------
The below requirements are needed on the host that executes this module.

- pan-python
- pandevice


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="2">
                    <b>all_details</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Get full-policy details when name is not set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>api_key</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <em>provider</em> to specify PAN-OS connectivity instead.</div>
                                                    <div><hr/></div>
                                                    <div>The API key to use instead of generating it using <em>username</em> / <em>password</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_group</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">shared</div>
                                    </td>
                                                                <td>
                                                                        <div>(Panorama only) The device group the operation should target.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <em>provider</em> to specify PAN-OS connectivity instead.</div>
                                                    <div><hr/></div>
                                                    <div>The IP address or hostname of the PAN-OS device being configured.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>password</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <em>provider</em> to specify PAN-OS connectivity instead.</div>
                                                    <div><hr/></div>
                                                    <div>The password to use for authentication.  This is ignored if <em>api_key</em> is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <em>provider</em> to specify PAN-OS connectivity instead.</div>
                                                    <div><hr/></div>
                                                    <div>The port number to connect to the PAN-OS device on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.8</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dict object containing connection details.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>api_key</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The API key to use instead of generating it using <em>username</em> / <em>password</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The IP address or hostname of the PAN-OS device being configured.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>password</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password to use for authentication.  This is ignored if <em>api_key</em> is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>port</b>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The port number to connect to the PAN-OS device on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>serial_number</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The serial number of a firewall to use for targeted commands. If <em>ip_address</em> is not a Panorama PAN-OS device, then this param is ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>username</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">admin</div>
                                    </td>
                                                                <td>
                                                                        <div>The username to use for authentication.  This is ignored if <em>api_key</em> is specified.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>rule_name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the security rule.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>rulebase</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>pre-rulebase</li>
                                                                                                                                                                                                <li>rulebase</li>
                                                                                                                                                                                                <li>post-rulebase</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The rulebase in which the rule is to exist.  If left unspecified, this defaults to <em>rulebase=pre-rulebase</em> for Panorama.  For NGFW, this is always set to be <em>rulebase=rulebase</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>username</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">admin</div>
                                    </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <em>provider</em> to specify PAN-OS connectivity instead.</div>
                                                    <div><hr/></div>
                                                    <div>The username to use for authentication.  This is ignored if <em>api_key</em> is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>vsys</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">vsys1</div>
                                    </td>
                                                                <td>
                                                                        <div>The vsys this object belongs to.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - Checkmode is not supported.
   - Panorama is supported.
   - PAN-OS connectivity should be specified using *provider* or the classic PAN-OS connectivity params (*ip_address*, *username*, *password*, *api_key*, and *port*).  If both are present, then the classic params are ignored.



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Get a list of all security rules
      panos_security_rule_facts:
        provider: '{{ provider }}'
      register: sec_rules

    - debug:
        msg: '{{ sec_rules.rules }}'

    - name: Get the definition for rule 'HTTP Multimedia'
      panos_security_rule_facts:
        provider: '{{ provider }}'
        rule_name: 'HTTP Multimedia'
      register: rule1

    - debug:
        msg: '{{ rule1.spec }}'




Return Values
-------------
Common return values are `documented here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <b>rules</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td>When <em>rule_name</em> is not specified</td>
                <td>
                                            <div>List of security rules present</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;rule1&#x27;, &#x27;rule2&#x27;, &#x27;rule3&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>rules_verbose</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <em>rule_name</em> is not specified and <em>all_details</em> is True.</td>
                <td>
                                            <div>List of security rules present with details</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>action</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>The rule action.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>antivirus</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined antivirus profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>application</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of applications, application groups, and/or application filters.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>category</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination URL categories.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>data_filtering</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined data_filtering profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>description</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Description of the security rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>destination_ip</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination addresses.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>destination_zone</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination zones.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>disable_server_response_inspection</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Disables packet inspection from the server to the client.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>disabled</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Disable this rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>file_blocking</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined file_blocking profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>group_profile</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Security profile group setting.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>hip_profiles</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>GlobalProtect host information profile list.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>icmp_unreachable</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Send &#x27;ICMP Unreachable&#x27;.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_end</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Whether to log at session end.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_setting</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Log forwarding profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_start</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Whether to log at session start.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>negate_destination</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Match on the reverse of the &#x27;destination_ip&#x27; attribute</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>negate_source</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Match on the reverse of the &#x27;source_ip&#x27; attribute</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rule_name</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the security rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rule_type</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Type of security rule (version 6.1 of PanOS and above).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>schedule</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Schedule in which this rule is active.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>service</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of services and/or service groups.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_ip</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source addresses.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_user</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source users.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_zone</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source zones.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>spyware</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined spyware profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>tag_name</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of tags associated with the rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>url_filtering</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined url_filtering profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vulnerability</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined vulnerability profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>wildfire_analysis</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined wildfire_analysis profile.</div>
                                        <br/>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>spec</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <em>rule_name</em> is specified</td>
                <td>
                                            <div>The security rule definition</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>action</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>The rule action.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>antivirus</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined antivirus profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>application</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of applications, application groups, and/or application filters.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>category</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination URL categories.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>data_filtering</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined data_filtering profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>description</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Description of the security rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>destination_ip</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination addresses.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>destination_zone</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of destination zones.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>disable_server_response_inspection</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Disables packet inspection from the server to the client.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>disabled</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Disable this rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>file_blocking</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined file_blocking profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>group_profile</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Security profile group setting.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>hip_profiles</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>GlobalProtect host information profile list.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>icmp_unreachable</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Send &#x27;ICMP Unreachable&#x27;.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_end</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Whether to log at session end.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_setting</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Log forwarding profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>log_start</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Whether to log at session start.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>negate_destination</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Match on the reverse of the &#x27;destination_ip&#x27; attribute</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>negate_source</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Match on the reverse of the &#x27;source_ip&#x27; attribute</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rule_name</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the security rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rule_type</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Type of security rule (version 6.1 of PanOS and above).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>schedule</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Schedule in which this rule is active.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>service</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of services and/or service groups.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_ip</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source addresses.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_user</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source users.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>source_zone</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of source zones.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>spyware</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined spyware profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>tag_name</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of tags associated with the rule.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>url_filtering</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined url_filtering profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vulnerability</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined vulnerability profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>wildfire_analysis</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the already defined wildfire_analysis profile.</div>
                                        <br/>
                                    </td>
            </tr>
                    
                                        </table>
    <br/><br/>


Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Garfield Lee Freeman (@shinmog)


