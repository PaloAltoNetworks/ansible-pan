:source: panos_sag.py

:orphan:

.. _panos_sag_module:


panos_sag -- Create a static address group
++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in Ansible: version: 2.12
:Why: This module's functionality is a subset of :ref:`panos_address_group <panos_address_group_module>`.
:Alternative: Use :ref:`panos_address_group <panos_address_group_module>` instead.



Synopsis
--------
- Create a static address group object in the firewall used for policy rules.



Requirements
------------
The below requirements are needed on the host that executes this module.

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice
- xmltodict can be obtained from PyPI https://pypi.python.org/pypi/xmltodict


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>api_key</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>API key that can be used instead of <em>username</em>/<em>password</em> credentials.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>commit</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                                                                <b>Default:</b><br/><div style="color: blue">yes</div>
                                    </td>
                                                                <td>
                                                                        <div>commit if changed</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>description</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The purpose / objective of the static Address Group</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>devicegroup</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>- The name of the Panorama device group. The group must exist on Panorama. If device group is not defined it is assumed that we are contacting a firewall.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>ip_address</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>IP address (or hostname) of PAN-OS device</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>operation</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The operation to perform Supported values are <em>add</em>/<em>list</em>/<em>delete</em>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>password for authentication</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>sag_name</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>name of the dynamic address group</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>static_match_filter</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>                    </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Static filter used by the address group</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tags</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>Tags to be associated with the address group</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>username</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">admin</div>
                                    </td>
                                                                <td>
                                                                        <div>username for authentication</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

    
    - name: sag
      panos_sag:
        ip_address: "192.168.1.1"
        password: "admin"
        sag_name: "sag-1"
        static_value: ['test-addresses', ]
        description: "A description for the static address group"
        tags: ["tags to be associated with the group", ]





Status
------


- This module will be removed in version 2.12. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Vinay Venkataraghavan @vinayvenkat


