:source: panos_bgp_conditional_advertisement.py

:orphan:

.. _panos_bgp_conditional_advertisement_module:


panos_bgp_conditional_advertisement -- Configures a BGP conditional advertisement
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- **NOTE: The modules in this role are deprecated in favour of the modules in the collection https://paloaltonetworks.github.io/pan-os-ansible**
- Use BGP to publish and consume routes from disparate networks.
- In the PAN-OS GUI, this resource cannot be created without also creating at least one non-exist filter and one advertise filter. The API behaves a little differently; you can create the conditional advertisement itself, but the API will start throwing errors if you try to update it and there is not at least one non-exist filter and one advertise filter.
- In order for a conditional advertisement to be valid, you must specify at least one non-exist and one advertise filter.
- When modifying a BGP conditional advertisement, any filters attached are left as-is, unless *advertise_filter* or *non_exist_filter* are specified.



Requirements
------------
The below requirements are needed on the host that executes this module.

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice


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
                    <b>advertise_filter</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <span class='module'>panos_bgp_policy_filter</span> to define filters after creation.</div>
                                                    <div><hr/></div>
                                                    <div>Advertisement filter object returned by <span class='module'>panos_bgp_policy_filter</span>.</div>
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
                    <b>commit</b>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                    <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Commit configuration if changed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable</b>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enable this policy.</div>
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
                    <b>name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of Conditional Advertisement policy.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>non_exist_filter</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Deprecated</b></div>
                                                    <div>Use <span class='module'>panos_bgp_policy_filter</span> to define filters after creation.</div>
                                                    <div><hr/></div>
                                                    <div>Non-Exist filter object returned by <span class='module'>panos_bgp_policy_filter</span>.</div>
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
                    <b>state</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The state.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>template</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>(Panorama only) The template this operation should target. Mutually exclusive with <em>template_stack</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>template_stack</b>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>(Panorama only) The template stack this operation should target. Mutually exclusive with <em>template</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>used_by</b>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of Peer Groups using this policy.</div>
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
                    <b>vr_name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">"default"</div>
                                    </td>
                                                                <td>
                                                                        <div>Name of the virtual router; it must already exist and have BGP configured.</div>
                                                    <div>See <span class='module'>panos_virtual_router</span>.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
   - Checkmode is supported.
   - Panorama is supported.
   - PAN-OS connectivity should be specified using *provider* or the classic PAN-OS connectivity params (*ip_address*, *username*, *password*, *api_key*, and *port*).  If both are present, then the classic params are ignored.
   - If the PAN-OS to be configured is Panorama, either *template* or *template_stack* must be specified.



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        provider: '{{ provider }}'
        name: 'cond-rule-01'
        enable: true
        non_exist_filter: '{{ non_exist.panos_obj }}'
        advertise_filter: '{{ advertise.panos_obj }}'





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Joshua Colson (@freakinhippie)
- Garfield Lee Freeman (@shinmog)


