#!/usr/bin/env python

#  Copyright 2018 Palo Alto Networks, Inc
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
module: panos_object_facts
short_description: Retrieve facts about objects on PAN-OS devices.
description:
    - Retrieves tag information objects on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is not supported.
extends_documentation_fragment:
    - panos.transitional_provider
options:
    name:
        description:
            - Name of object to retrieve.
        required: true
    object_type:
        description:
            - Type of object to retrieve.
        choices: ['address', 'address-group', 'service', 'service-group', 'tag']
        default: 'address'
'''

EXAMPLES = '''
- name: Retrieve address group object 'Prod'
  panos_object_facts:
    provider: '{{ provider }}'
    name: 'Prod'
    object_type: 'address-group'
  register: result

- name: Retrieve service group object 'Prod-Services'
  panos_object_facts:
    provider: '{{ provider }}'
    name: 'Prod-Services'
    object_type: 'service-group'
  register: result
'''

RETURN = '''
results:
    description: Dict containing object attributes.  Empty if object is not found.
    returned: always
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice import objects
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


COLOR_NAMES = [
    'red', 'green', 'blue', 'yellow', 'copper', 'orange', 'purple', 'gray', 'light green',
    'cyan', 'light gray', 'blue gray', 'lime', 'black', 'gold', 'brown'
]


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            object_type=dict(
                type='str', default='address',
                choices=['address', 'address-group', 'service', 'service-group', 'tag'],
            ),
        ),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=False,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    object_type = module.params['object_type']
    name = module.params['name']

    results = {}

    try:
        obj = None
        obj_type = None

        if object_type == 'address':
            obj_type = objects.AddressObject
        elif object_type == 'address-group':
            obj_type = objects.AddressGroup
        elif object_type == 'service':
            obj_type = objects.ServiceObject
        elif object_type == 'service-group':
            obj_type = objects.ServiceGroup
        elif object_type == 'tag':
            obj_type = objects.Tag

        obj_type.refreshall(parent)
        obj = parent.find(name, obj_type)

        if obj:
            results = obj.about()

            # If the object type was a tag, convert the color id back into the name.
            if object_type == 'tag':
                color_index = int(results['entry']['color'][5:]) - 1
                results['entry']['color'] = COLOR_NAMES[color_index]

        module.exit_json(changed=False, results=results)

    except PanDeviceError as e:
        module.fail_json(msg=e.message)


if __name__ == '__main__':
    main()
