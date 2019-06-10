#!/usr/bin/env python
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
module: panos_log_forwarding_profile_match_list_action
short_description: Manage log forwarding profile match list actions.
description:
    - Manages log forwarding profile match list actions.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.11.1
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.vsys_shared
    - panos.device_group
options:
    log_forwarding_profile:
        description:
            - Name of the log forwarding profile to add this action to.
        required: True
    log_forwarding_profile_match_list:
        description:
            - Name of the log forwarding profile match list to add this action to.
        required: True
    name:
        description:
            - Name of the profile.
        required: true
    action_type:
        description:
            - Action type.
        choices:
            - tagging
            - integration
        default: 'tagging'
    action:
        description:
            - The action.
        choices:
            - add-tag
            - remove-tag
            - Azure-Security-Center-Integration
    target:
        description:
            - The target.
        choices:
            - source-address
            - destination-address
    registration:
        description:
            - Registration.
        choices:
            - localhost
            - panorama
            - remote
    http_profile:
        description:
            - The HTTP profile when I(registration=remote).
    tags:
        description:
            - List of tags.
        type: list
    timeout:
        description:
            - Valid for PAN-OS 9.0+
            - Timeout in minutes
        type: int
'''

EXAMPLES = '''
# Create a log forwarding server match list action
- name: Create the action
  panos_log_forwarding_profile_match_list_action:
    provider: '{{ provider }}'
    log_forwarding_profile: 'my-profile'
    log_forwarding_profile_match_list: 'ml-1'
    name: 'my-action'
    action: 'add-tag'
    target: 'source-address'
    registration: 'localhost'
    tags: ['foo', 'bar']
    timeout: 2
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.objects import LogForwardingProfile
    from pandevice.objects import LogForwardingProfileMatchList
    from pandevice.objects import LogForwardingProfileMatchListAction
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            log_forwarding_profile=dict(required=True),
            log_forwarding_profile_match_list=dict(required=True),
            name=dict(required=True),
            action_type=dict(default='tagging', choices=['tagging', 'integration']),
            action=dict(choices=['add-tag', 'remove-tag', 'Azure-Security-Center-Integration']),
            target=dict(choices=['source-address', 'destination-address']),
            registration=dict(choices=['localhost', 'panorama', 'remote']),
            http_profile=dict(),
            tags=dict(type='list'),
            timeout=dict(type='int'),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    lfp = LogForwardingProfile(module.params['log_forwarding_profile'])
    parent.add(lfp)
    try:
        lfp.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    ml = lfp.find(module.params['log_forwarding_profile_match_list'], LogForwardingProfileMatchList)
    if ml is None:
        module.fail_json(msg='Log forwarding profile match list "{0}" does not exist'.format(
            module.params['log_forwarding_profile_match_list']))

    listing = ml.findall(LogForwardingProfileMatchListAction)

    spec = {
        'name': module.params['name'],
        'action_type': module.params['action_type'],
        'action': module.params['action'],
        'target': module.params['target'],
        'registration': module.params['registration'],
        'http_profile': module.params['http_profile'],
        'tags': module.params['tags'],
        'timeout': module.params['timeout'],
    }
    obj = LogForwardingProfileMatchListAction(**spec)
    ml.add(obj)

    changed = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
