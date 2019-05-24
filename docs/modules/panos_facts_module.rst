:source: panos_facts.py

:orphan:

.. _panos_facts_module:


panos_facts -- Collects facts from Palo Alto Networks device
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Collects fact information from Palo Alto Networks firewall running PanOS.



Requirements
------------
The below requirements are needed on the host that executes this module.

- pan-python


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
                    <b>gather_subset</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">[&#39;!config&#39;]</div>
                                    </td>
                                                                <td>
                                                                        <div>Scopes what information is gathered from the device. Possible values for this argument include all, system, session, interfaces, ha, routing, vr, vsys and config. You can specify a list of values to include a larger subset. Values can also be used with an initial ! to specify that a specific subset should not be collected. Certain subsets might be supported by Panorama.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>host</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div><b>Removed</b></div>
                                                    <div>Use <em>provider</em> instead.</div>
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
                        </table>
    <br/>


Notes
-----

.. note::
   - Tested on PanOS 8.0.5
   - Checkmode is not supported.
   - Panorama is not supported.
   - PAN-OS connectivity should be specified using *provider* or the classic PAN-OS connectivity params (*ip_address*, *username*, *password*, *api_key*, and *port*).  If both are present, then the classic params are ignored.



Examples
--------

.. code-block:: yaml+jinja

    
    # Gather facts
    - name: Get facts
      panos_facts:
        provider: '{{ provider }}'
        gather_subset: ['config']




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
                    <b>ansible_net_config</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>config</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Device confiration in XML format.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_full_commit_required</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies whether full commit is required to apply changes.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_ha_enabled</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td>When <code>ha</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies whether HA is enabled or not.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_ha_localmode</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>ha</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies the HA mode on local node.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Active-Passive</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_ha_localstate</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>ha</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies the HA state on local node.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">active</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_hostname</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Hostname of the local node.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_interfaces</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <code>interface</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Network interface information.</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>comment</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Interface description/comment.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>ip</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of interface IP addresses in CIDR format.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">192.0.2.1/24</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>ipv6</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of interface IPv6 addresses in CIDR format.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2001:db8::0000:1/64</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>name</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Interface name.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">ae1.23</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>tag</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>VLAN tag for the subinterface.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">23</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ansible_net_kbps</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td>When <code>session</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Current kb/s throughput.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_model</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Device model of the local node.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_multivsys</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies whether multivsys mode is enabled on local node.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_pps</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td>When <code>session</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Current packets/s throughput.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_routing_table</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <code>routing</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Routing Table information.</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>age</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Age of the route entry in the routing table.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>destination</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>IP prefix of the destination.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>flags</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Flags for the route entry in the routing table.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>interface</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Egress interface the router will use to reach the next hop.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>metric</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Metric for the route.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>nexthop</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Address of the device at the next hop toward the destination network.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>route_table</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Unicast or multicast route table.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>virtual_router</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Virtual router the route belongs to.</div>
                                        <br/>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ansible_net_serial</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Serial number of the local node.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_session_max</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td>When <code>session</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Maximum number of sessions on local node.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_session_usage</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td>When <code>session</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Current number of active sessions on local node</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_uncommitted_changes</b>
                    <div style="font-size: small; color: purple">boolean</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Specifies if commit is required to apply changes.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_uptime</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Uptime of the local node.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">469 days, 19:30:16</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_version</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td>When <code>system</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>PanOS version of the local node.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>ansible_net_virtual_routers</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <code>vr</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Virtual Router information.</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vr_asn</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>BGP autonomous system number.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">65001</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vr_iflist</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List interfaces in the VR.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ae2.12&#x27;, &#x27;ae2.14&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vr_name</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Name of the virtual router.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vr_routerid</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>BGP router ID.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">192.0.2.1</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>ansible_net_virtual_systems</b>
                    <div style="font-size: small; color: purple">complex</div>
                                    </td>
                <td>When <code>vsys</code> is specified in <code>gather_subset</code>.</td>
                <td>
                                            <div>Virtual System information.</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_currentsessions</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Number of active sessions on VSYS.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_description</b>
                    <div style="font-size: small; color: purple">string</div>
                                    </td>
                <td></td>
                <td>
                                            <div>VSYS description/name.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_id</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>VSYS ID.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_iflist</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of interfaces attached to the VSYS.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_name</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>VSYS name.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">vsys1</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_vrlist</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of virtual routers attached to the VSYS.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_vsys_maxsessions</b>
                    <div style="font-size: small; color: purple">integer</div>
                                    </td>
                <td></td>
                <td>
                                            <div>Number of configured maximum sessions on VSYS. 0 for unlimited.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>vsys_zonelist</b>
                    <div style="font-size: small; color: purple">list</div>
                                    </td>
                <td></td>
                <td>
                                            <div>List of security zones attached to the VSYS.</div>
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

- Tomi Raittinen (@traittinen)


