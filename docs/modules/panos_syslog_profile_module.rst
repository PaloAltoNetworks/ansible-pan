:source: panos_syslog_profile.py

:orphan:

.. _panos_syslog_profile_module:


panos_syslog_profile -- Manage syslog server profiles
+++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- **NOTE: The modules in this role are deprecated in favour of the modules in the collection https://paloaltonetworks.github.io/pan-os-ansible**
- Manages syslog server profiles.



Requirements
------------
The below requirements are needed on the host that executes this module.

- pan-python
- pandevice >= 0.11.1


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
                    <b>auth</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom auth log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>config</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Custom config log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>data</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom data log format.</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"shared"</div>
                                    </td>
                                                                <td>
                                                                        <div>(Panorama only) The device group the operation should target.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>escape_character</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Escape character</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>escaped_characters</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Characters to be escaped.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>gtp</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom GTP log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>hip_match</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Custom HIP match log format.</div>
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
                    <b>iptag</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 9.0+</div>
                                                    <div>Custom Iptag log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the profile.</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"admin"</div>
                                    </td>
                                                                <td>
                                                                        <div>The username to use for authentication.  This is ignored if <em>api_key</em> is specified.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>sctp</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.1+</div>
                                                    <div>Custom SCTP log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>system</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Custom system log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>threat</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Custom threat log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>traffic</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Custom traffic log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>tunnel</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom tunnel log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>url</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom url log format.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>user_id</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom user-ID log format.</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"admin"</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"shared"</div>
                                    </td>
                                                                <td>
                                                                        <div>The vsys this object belongs to.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>wildfire</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>PAN-OS 8.0+</div>
                                                    <div>Custom wildfire log format.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - Panorama is supported.
   - Check mode is supported.
   - PAN-OS connectivity should be specified using *provider* or the classic PAN-OS connectivity params (*ip_address*, *username*, *password*, *api_key*, and *port*).  If both are present, then the classic params are ignored.



Examples
--------

.. code-block:: yaml+jinja

    
    # Create a profile
    - name: Create syslog profile
      panos_syslog_profile:
        provider: '{{ provider }}'
        name: 'my-profile'





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Garfield Lee Freeman (@shinmog)


