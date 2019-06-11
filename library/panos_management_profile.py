#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: panos_management_profile
short_description: Manage interface management profiles.
description:
    - This module will allow you to manage interface management profiles on PAN-OS.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.full_template_support
    - panos.state
options:
    panorama_template:
        description:
            - B(Deprecated)
            - Use I(template) instead.
            - HORIZONTALLINE
            - (Panorama only) The template name.
    name:
        description:
            - The management profile name.
        required: true
    ping:
        description:
            - Enable ping
        type: bool
    telnet:
        description:
            - Enable telnet
        type: bool
    ssh:
        description:
            - Enable ssh
        type: bool
    http:
        description:
            - Enable http
        type: bool
    http_ocsp:
        description:
            - Enable http-ocsp
        type: bool
    https:
        description:
            - Enable https
        type: bool
    snmp:
        description:
            - Enable snmp
        type: bool
    response_pages:
        description:
            - Enable response pages
        type: bool
    userid_service:
        description:
            - Enable userid service
        type: bool
    userid_syslog_listener_ssl:
        description:
            - Enable userid syslog listener ssl
        type: bool
    userid_syslog_listener_udp:
        description:
            - Enable userid syslog listener udp
        type: bool
    permitted_ip:
        description:
            - The list of permitted IP addresses
        type: list
    commit:
        description:
            - Perform a commit if a change is made.
        type: bool
        default: true
'''

EXAMPLES = '''
- name: ensure mngt profile foo exists and allows ping and ssh and commit
  panos_management_profile:
    provider: '{{ provider }}'
    name: 'foo'
    ping: true
    ssh: true

- name: make sure mngt profile bar does not exist without doing a commit
  panos_management_profile:
    provider: '{{ provider }}'
    name: 'bar'
    state: 'absent'
    commit: false
'''

RETURN = '''
# Default return values.
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.network import ManagementProfile
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_classic_provider_spec=True,
        with_state=True,
        min_pandevice_version=(0, 8, 0),
        argument_spec=dict(
            name=dict(required=True),
            ping=dict(type='bool'),
            telnet=dict(type='bool'),
            ssh=dict(type='bool'),
            http=dict(type='bool'),
            http_ocsp=dict(type='bool'),
            https=dict(type='bool'),
            snmp=dict(type='bool'),
            response_pages=dict(type='bool'),
            userid_service=dict(type='bool'),
            userid_syslog_listener_ssl=dict(type='bool'),
            userid_syslog_listener_udp=dict(type='bool'),
            permitted_ip=dict(type='list'),
            commit=dict(type='bool', default=True),

            # TODO(gfreeman) - Removed in the next role release.
            panorama_template=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # TODO(gfreeman) - Removed when "panorama_template" is removed.
    if module.params['panorama_template'] is not None:
        module.deprecate('Param "panorama_template" is deprecated; use "template"', '2.12')
        if module.params['template'] is not None:
            msg = [
                'Both "template" and "panorama_template" have been given',
                'Specify one or the other, not both.',
            ]
            module.fail_json(msg='. '.join(msg))
        module.params['template'] = module.params['panorama_template']

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    # Build the object based on the spec.
    obj = ManagementProfile(
        *[module.params[x] for x in (
            'name', 'ping', 'telnet', 'ssh', 'http', 'http_ocsp', 'https',
            'snmp', 'response_pages', 'userid_service',
            'userid_syslog_listener_ssl', 'userid_syslog_listener_udp',
            'permitted_ip')])
    parent.add(obj)

    # Retrieve current config.
    try:
        profiles = ManagementProfile.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    # Perform requested action.
    changed = helper.apply_state(obj, profiles, module)
    if changed and module.params['commit']:
        helper.commit(module)

    # Done.
    module.exit_json(changed=changed, msg="Done")


if __name__ == '__main__':
    main()
