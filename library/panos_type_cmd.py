#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2019 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_type_cmd
short_description: Execute arbitrary TYPE commands on PAN-OS
description:
    - This module allows you to execute arbitrary TYPE commands on PAN-OS.
    - This module does not provide guards of any sort, so USE AT YOUR OWN RISK.
    - Refer to the PAN-OS and Panorama API guide for more info.
    - https://docs.paloaltonetworks.com/pan-os.html
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice
notes:
    - Panorama is supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - panos.transitional_provider
options:
    cmd:
        description:
            - The command to run.
        choices:
            - show
            - get
            - delete
            - set
            - edit
            - move
            - rename
            - clone
            - override
        default: 'set'
    xpath:
        description:
            - The XPATH.
            - All newlines are removed from the XPATH to allow for shorter lines.
        required: True
    element:
        description:
            - Used in I(cmd=set), I(cmd=edit), and I(cmd=override).
            - The element payload.
    where:
        description:
            - Used in I(cmd=move).
            - The movement keyword.
    dst:
        description:
            - Used in I(cmd=move).
            - The reference object.
    new_name:
        description:
            - Used in I(cmd=rename) and I(cmd=clone).
            - The new name.
    xpath_from:
        description:
            - Used in I(cmd=clone).
            - The from xpath.
    extra_qs:
        description:
            - A dict of extra params to pass in.
        type: complex
'''

EXAMPLES = '''
- name: Create an address object using set.
  panos_type_cmd:
    provider: '{{ provider }}'
    xpath: |
      /config/devices/entry[@name='localhost.localdomain']
      /vsys/entry[@name='vsys1']
      /address
    element: |
      <entry name="sales-block">
        <ip-netmask>192.168.55.0/24</ip-netmask>
        <description>Address CIDR for sales org</description>
      </entry>

- name: Then rename it.
  panos_type_cmd:
    provider: '{{ provider }}'
    cmd: 'rename'
    xpath: |
      /config/devices/entry[@name='localhost.localdomain']
      /vsys/entry[@name='vsys1']
      /address/entry[@name='sales-block']
    new_name: 'dmz-block'
'''

RETURN = '''
# Default return values
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            cmd=dict(default='set', choices=[
                'show', 'get', 'delete', 'set', 'edit',
                'move', 'rename', 'clone', 'override']),
            xpath=dict(required=True),
            element=dict(),
            where=dict(),
            dst=dict(),
            new_name=dict(),
            xpath_from=dict(),
            extra_qs=dict(),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    cmd = module.params['cmd']
    func = getattr(parent.xapi, cmd)

    kwargs = {
        'xpath': ''.join(module.params['xpath'].strip().split('\n')),
        'extra_qs': module.params['extra_qs'],
    }

    if cmd in ('set', 'edit', 'override'):
        kwargs['element'] = module.params['element'].strip()

    if cmd in ('move', ):
        kwargs['where'] = module.params['where']
        kwargs['dst'] = module.params['dst']

    if cmd in ('rename', 'clone'):
        kwargs['newname'] = module.params['new_name']

    if cmd in ('clone', ):
        kwargs['xpath_from'] = module.params['xpath_from']

    try:
        func(**kwargs)
    except PanDeviceError as e:
        module.fail_json(msg='{0}'.format(e))

    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
