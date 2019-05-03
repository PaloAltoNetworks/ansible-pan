:source: panos_dag_tags.py

:orphan:

.. _panos_dag_tags_module:


panos_dag_tags -- Create tags for DAG's on PAN-OS devices
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

.. contents::
   :local:
   :depth: 1

DEPRECATED
----------
:Removed in Ansible: version: 2.9
:Why: Using new modern API calls in the panos_registered_ip
:Alternative: Use :ref:`panos_registered_ip <panos_registered_ip_module>` instead.



Synopsis
--------
- Create the ip address to tag associations. Tags will in turn be used to create DAG's



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
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>- Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama. If device group is not define we assume that we are contacting Firewall.</div>
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
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>IP address (or hostname) of PAN-OS device</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>ip_to_register</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>IP that will be registered with the given tag names.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>operation</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The action to be taken. Supported values are <em>add</em>/<em>update</em>/<em>find</em>/<em>delete</em>.</div>
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
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>password for authentication</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tag_names</b>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                                            </div>
                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The list of the tags that will be added or removed from the IP address.</div>
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


Notes
-----

.. note::
   - Checkmode is not supported.
   - Panorama is not supported.
   - use panos_registered_ip from now on



Examples
--------

.. code-block:: yaml+jinja

    
    - name: Create the tags to map IP addresses
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Tags to allow certain IP's to access various SaaS Applications"
        operation: 'add'
      tags: "adddagip"

    - name: List the IP address to tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        tag_names: "{{ tag_names }}"
        description: "List the IP address to tag mapping"
        operation: 'list'
      tags: "listdagip"

    - name: Unregister an IP address from a tag mapping
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Unregister IP address from tag mappings"
        operation: 'delete'
      tags: "deletedagip"





Status
------


- This module will be removed in version 2.9. *[deprecated]*
- For more information see `DEPRECATED`_.


Authors
~~~~~~~

- Vinay Venkataraghavan (@vinayvenkat)


