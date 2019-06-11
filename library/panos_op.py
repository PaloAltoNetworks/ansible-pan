#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2017 Palo Alto Networks, Inc
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_op
short_description: execute arbitrary OP commands on PANW devices (e.g. show interface all)
description:
    - This module will allow user to pass and execute any supported OP command on the PANW device.
author:
    - Ivan Bojer (@ivanbojer)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.5"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is NOT supported.
    - Panorama is supported.
extends_documentation_fragment:
    - panos.transitional_provider
options:
    cmd:
        description:
            - The OP command to be performed.
        required: true
    cmd_is_xml:
        description:
            - The cmd is already given in XML format, so don't convert it.
        default: false
        type: bool
'''

EXAMPLES = '''
- name: show list of all interfaces
  panos_op:
    provider: '{{ provider }}'
    cmd: 'show interfaces all'

- name: show system info
  panos_op:
    provider: '{{ provider }}'
    cmd: 'show system info'

- name: show system info as XML command
  panos_op:
    provider: '{{ provider }}'
    cmd: '<show><system><info/></system></show>'
    cmd_is_xml: true
'''

RETURN = '''
stdout:
    description: output of the given OP command as JSON formatted string
    returned: success
    type: string
    sample: "{system: {app-release-date: 2017/05/01  15:09:12}}"
stdout_xml:
    description: output of the given OP command as an XML formatted string
    returned: success
    type: string
    sample: "<response status=success><result><system><hostname>fw2</hostname>"
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    import xmltodict
    import json
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            cmd=dict(required=True),
            cmd_is_xml=dict(default=False, type='bool'),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    parent = helper.get_pandevice_parent(module)

    cmd = module.params['cmd']
    cmd_is_xml = module.params['cmd_is_xml']

    xml_output = ''
    try:
        xml_output = parent.op(cmd, xml=True, cmd_xml=(not cmd_is_xml))
    except PanDeviceError as e1:
        if cmd_is_xml:
            module.fail_json(msg='Failed to run XML command : {0} : {1}'.format(cmd, e1))
        tokens = cmd.split()
        tokens[-1] = '"{0}"'.format(tokens[-1])
        cmd2 = ' '.join(tokens)
        try:
            xml_output = parent.op(cmd2, xml=True)
        except PanDeviceError as e2:
            module.fail_json(msg='Failed to run command : {0} : {1}'.format(cmd2, e2))

    obj_dict = xmltodict.parse(xml_output)
    json_output = json.dumps(obj_dict)

    module.exit_json(changed=True, msg="Done",
                     stdout=json_output, stdout_xml=xml_output)


if __name__ == '__main__':
    main()
