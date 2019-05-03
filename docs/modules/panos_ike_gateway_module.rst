:source: panos_ike_gateway.py

:orphan:

.. _panos_ike_gateway_module:


panos_ike_gateway -- Configures IKE gateway on the firewall with subset of settings
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Use this to manage or define a gateway, including the configuration information necessary to perform Internet Key Exchange (IKE) protocol negotiation with a peer gateway. This is the Phase 1 portion of the IKE/IPSec VPN setup.



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
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">yes</div>
                                    </td>
                                                                <td>
                                                                        <div>Commit configuration if changed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dead_peer_detection_interval</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">99</div>
                                    </td>
                                                                <td>
                                                                        <div>Time in seconds to check for a dead peer.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>dead_peer_detection_retry</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">10</div>
                                    </td>
                                                                <td>
                                                                        <div>Retry attempts before peer is marked dead.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable_dead_peer_detection</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">no</div>
                                    </td>
                                                                <td>
                                                                        <div>True to enable Dead Peer Detection on the gateway.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: d, e, a, d, _, p, e, e, r, _, d, e, t, e, c, t, i, o, n</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable_fragmentation</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">no</div>
                                    </td>
                                                                <td>
                                                                        <div>True to enable IKE fragmentation</div>
                                                    <div>Incompatible with pre-shared keys, or &#x27;aggressive&#x27; exchange mode</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: f, r, a, g, m, e, n, t, a, t, i, o, n</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable_liveness_check</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">yes</div>
                                    </td>
                                                                <td>
                                                                        <div>Enable sending empty information liveness check message.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable_nat_traversal</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">no</div>
                                    </td>
                                                                <td>
                                                                        <div>True to NAT Traversal mode</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: n, a, t, _, t, r, a, v, e, r, s, a, l</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enable_passive_mode</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">yes</div>
                                    </td>
                                                                <td>
                                                                        <div>True to have the firewall only respond to IKE connections and never initiate them.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: p, a, s, s, i, v, e, _, m, o, d, e</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ikev1_crypto_profile</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">default</div>
                                    </td>
                                                                <td>
                                                                        <div>Crypto profile for IKEv1.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: c, r, y, p, t, o, _, p, r, o, f, i, l, e, _, n, a, m, e</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ikev1_exchange_mode</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>auto</li>
                                                                                                                                                                                                <li>main</li>
                                                                                                                                                                                                <li>aggressive</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The IKE exchange mode to use</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ikev2_crypto_profile</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">default</div>
                                    </td>
                                                                <td>
                                                                        <div>Crypto profile for IKEv2.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: c, r, y, p, t, o, _, p, r, o, f, i, l, e, _, n, a, m, e</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>interface</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">ethernet1/1</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify the outgoing firewall interface to the VPN tunnel.</div>
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
                    <b>liveness_check_interval</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">5</div>
                                    </td>
                                                                <td>
                                                                        <div>Delay interval before sending probing packets (in seconds).</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: l, i, v, e, n, e, s, s, _, c, h, e, c, k</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>local_id_type</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>ipaddr</li>
                                                                                                                                                                                                <li>fwdn</li>
                                                                                                                                                                                                <li>ufqdn</li>
                                                                                                                                                                                                <li>keyid</li>
                                                                                                                                                                                                <li>dn</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify the type of local ID.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>local_id_value</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The value for the local_id.  (See also local_id_type, above.)</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>local_ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Bind IKE gateway to the specified interface IP address</div>
                                                    <div>It should include the mask, such as &#x27;192.168.1.1/24&#x27;</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>local_ip_address_type</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>ip</li>
                                                                                                                                                                                                <li>floating-ip</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The address type of the bound interface IP address</div>
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
                                                                        <div>Name for the profile.</div>
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
                    <b>peer_id_check</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>exact</li>
                                                                                                                                                                                                <li>wildcard</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Type of checking to do on peer_id.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>peer_id_type</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>ipaddr</li>
                                                                                                                                                                                                <li>fwdn</li>
                                                                                                                                                                                                <li>ufqdn</li>
                                                                                                                                                                                                <li>keyid</li>
                                                                                                                                                                                                <li>dn</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify the type of peer ID.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>peer_id_value</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The value for the peer_id.  (See also peer_id_type, above.)</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>peer_ip_value</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">127.0.0.1</div>
                                    </td>
                                                                <td>
                                                                        <div>IPv4 address of the peer gateway.</div>
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
                    <b>pre_shared_key</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">CHANGEME</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify pre-shared key.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: p, s, k</div>
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
                    <b>version</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">ike2</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify the priority for Diffie-Hellman (DH) groups.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: p, r, o, t, o, c, o, l, _, v, e, r, s, i, o, n</div>
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
   - If the PAN-OS to be configured is Panorama, either *template* or *template_stack* must be specified.



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Add IKE gateway config to the firewall
      panos_ike_gateway:
        provider: '{{ provider }}'
        state: 'present'
        name: 'IKEGW-Ansible'
        version: 'ikev2'
        interface: 'ethernet1/1'
        enable_passive_mode: True
        enable_liveness_check: True
        liveness_check_interval: '5'
        peer_ip_value: '1.2.3.4'
        pre_shared_key: 'CHANGEME'
        ikev2_crypto_profile: 'IKE-Ansible'
        commit: False





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.





Authors
~~~~~~~

- Ivan Bojer (@ivanbojer)


