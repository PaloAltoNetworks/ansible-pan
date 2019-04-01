#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_ike_crypto_profile
short_description: Configures IKE Crypto profile on the firewall with subset of settings
description:
    - Use the IKE Crypto Profiles page to specify protocols and algorithms for identification, authentication, and
    - encryption (IKEv1 or IKEv2, Phase 1).
author: "Ivan Bojer (@ivanbojer)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.full_template_support
options:
    name:
        description:
            - Name for the profile.
        required: true
    dh_group:
        description:
            - Specify the priority for Diffie-Hellman (DH) groups.
        default: group2
        choices: ['group1', 'group2', 'group5', 'group14', 'group19', 'group20']
        aliases: dhgroup
    authentication:
        description:
            - Authentication hashes used for IKE phase 1 proposal.
        choices: ['md5', 'sha1', 'sha256', 'sha384', 'sha512']
        default: sha1
    encryption:
        description:
            - Encryption algorithms used for IKE phase 1 proposal.
        choices: ['des', '3des', 'aes-128-cbc', 'aes-192-cbc', 'aes-256-cbc']
        default: ['aes-256-cbc', '3des']
    lifetime_seconds:
        description:
            - IKE phase 1 key lifetime in seconds.
        aliases: lifetime_sec
    lifetime_minutes:
        description:
            - IKE phase 1 key lifetime in minutes.
    lifetime_hours:
        description:
            - IKE phase 1 key lifetime in hours.  If no key lifetime is
              specified, default to 8 hours.
    lifetime_days:
        description:
            - IKE phase 1 key lifetime in days.
    commit:
        description:
            - Commit configuration if changed.
        default: true
'''

EXAMPLES = '''
- name: Add IKE crypto config to the firewall
    panos_ike_crypto_profile:
      provider: '{{ provider }}'
      state: 'present'
      name: 'vpn-0cc61dd8c06f95cfd-0'
      dh_group: ['group2']
      authentication: ['sha1']
      encryption: ['aes-128-cbc']
      lifetime_seconds: '28800'
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection

try:
    from pandevice.network import IkeCryptoProfile
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(required=True),
            dh_group=dict(
                type='list',
                default=['group2'],
                choices=[
                    'group1', 'group2', 'group5', 'group14', 'group19', 'group20'
                ],
                aliases=['dhgroup']
            ),
            authentication=dict(
                type='list',
                choices=[
                    'md5', 'sha1', 'sha256', 'sha384', 'sha512'
                ],
                default=['sha1']
            ),
            encryption=dict(
                type='list',
                choices=[
                    'des', '3des', 'aes-128-cbc', 'aes-192-cbc', 'aes-256-cbc'
                ],
                default=['aes-256-cbc', '3des']
            ),
            lifetime_seconds=dict(type='int', aliases=['lifetime_sec']),
            lifetime_minutes=dict(type='int'),
            lifetime_hours=dict(type='int'),
            lifetime_days=dict(type='int'),
            commit=dict(type='bool', default=True)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
        mutually_exclusive=[
            [
                'lifetime_seconds',
                'lifetime_minutes',
                'lifetime_hours',
                'lifetime_days'
            ]
        ]
    )

    # Verify libs are present, get parent object.
    parent = helper.get_pandevice_parent(module)

    # Object params.
    spec = {
        'name': module.params['name'],
        'dh_group': module.params['dh_group'],
        'authentication': module.params['authentication'],
        'encryption': module.params['encryption'],
        'lifetime_seconds': module.params['lifetime_seconds'],
        'lifetime_minutes': module.params['lifetime_minutes'],
        'lifetime_hours': module.params['lifetime_hours'],
        'lifetime_days': module.params['lifetime_days']
    }

    # Other info.
    commit = module.params['commit']

    # Reflect GUI behavior.  Default is 8 hour key lifetime if nothing else is
    # specified.
    if not any([
        spec['lifetime_seconds'], spec['lifetime_minutes'], spec['lifetime_hours'], spec['lifetime_days']
    ]):
        spec['lifetime_hours'] = 8

    # Retrieve current info.
    try:
        listing = IkeCryptoProfile.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = IkeCryptoProfile(**spec)
    parent.add(obj)

    # Apply the state.
    changed = helper.apply_state(obj, listing, module)

    # Commit.
    if commit and changed:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
