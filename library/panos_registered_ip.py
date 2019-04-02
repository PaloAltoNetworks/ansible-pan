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
module: panos_registered_ip
short_description: Register IP addresses for use with dynamic address groups on PAN-OS devices.
description:
    - Registers tags for IP addresses that can be used to build dynamic address groups.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.7"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Check mode is supported.
    - Panorama is not supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.vsys
options:
    ips:
        description:
            - List of IP addresses to register/unregister.
        required: true
    tags:
        description:
            - List of tags that the IP address will be registered to.
        required: true
'''

EXAMPLES = '''
- name: Add 'First_Tag' tag to 1.1.1.1
  panos_registered_ip:
    provider: '{{ provider }}'
    ips: ['1.1.1.1']
    tags: ['First_Tag']
    state: 'present'

- name: Add 'First_Tag' tag to 1.1.1.2
  panos_registered_ip:
    provider: '{{ provider }}'
    ips: ['1.1.1.2']
    tags: ['First_Tag']
    state: 'present'

- name: Add 'Second_Tag' tag to 1.1.1.1
  panos_registered_ip:
    provider: '{{ provider }}'
    ips: ['1.1.1.1']
    tags: ['Second_Tag']
    state: 'present'

- name: Remove 'Second_Tag' from 1.1.1.1
  panos_registered_ip:
    provider: '{{ provider }}'
    ips: ['1.1.1.1']
    tags: ['Second_Tag']
    state: 'absent'

- name: Remove 'First_Tag' from 1.1.1.2 (will unregister entirely)
  panos_registered_ip:
    provider: '{{ provider }}'
    ips: ['1.1.1.2']
    tags: ['First_Tag']
    state: 'absent'
'''

RETURN = '''
results:
    description: After performing action, returns tags for given IPs.  IP addresses as keys,
        tags as values.
    returned: always
    type: dict
    sample: { '1.1.1.1': ['First_Tag', 'Second_Tag'] }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection

try:
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys=True,
        with_classic_provider_spec=True,
        with_state=True,
        panorama_error='Panorama is not supported for this module.',
        argument_spec=dict(
            ips=dict(type='list', required=True),
            tags=dict(type='list', required=True),
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True
    )

    # Verify libs are present, get parent object.
    device = helper.get_pandevice_parent(module)

    ips = module.params['ips']
    tags = module.params['tags']
    state = module.params['state']

    changed = False

    try:
        registered_ips = device.userid.get_registered_ip(tags=tags)

        if state == 'present':
            # Check to see if IPs actually need to be registered.
            to_add = set(ips) - set(registered_ips.keys())
            if to_add:
                if not module.check_mode:
                    device.userid.register(ips, tags=tags)
                changed = True

        elif state == 'absent':
            # Check to see if IPs actually need to be unregistered.
            to_remove = set(ips) & set(registered_ips.keys())
            if to_remove:
                if not module.check_mode:
                    device.userid.unregister(to_remove, tags=tags)
                changed = True

        results = device.userid.get_registered_ip(ips)

    except PanDeviceError as e:
        module.fail_json(msg='Failed register/unregister: {0}'.format(e))

    module.exit_json(changed=changed, results=results)


if __name__ == '__main__':
    main()
