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
module: panos_management_profile
short_description: Manage interface management profiles.
description:
    - This module will allow you to manage interface management profiles on PAN-OS.
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
    - xmltodict can be obtained from PyPI U(https://pypi.python.org/pypi/xmltodict)
notes:
    - Checkmode is NOT supported.
    - Panorama is supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device or Panorama management console being configured.
        required: true
    username:
        description:
            - Username credentials to use for authentication.
        default: "admin"
    password:
        description:
            - Password credentials to use for authentication.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - The state.  Can be either I(present)/I(absent).
        default: "present"
    panorama_template:
        description:
            - The template name (required if 'ip_address' is a Panorama); ignored if 'ip_address' is a firewall.
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
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    name: 'foo'
    ping: true
    ssh: true

- name: make sure mngt profile bar does not exist without doing a commit
  panos_management_profile:
    ip_address: '{{ ip_address }}'
    username: '{{ username }}'
    password: '{{ password }}'
    name: 'bar'
    state: 'absent'
    commit: false
'''

RETURN = '''
# Default return values.
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pandevice.base import PanDevice
    from pandevice.network import ManagementProfile
    from pandevice.panorama import Template
    from pandevice.errors import PanDeviceError
    # Needed for Template.refreshall().
    from pandevice import ha, device, objects

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        username=dict(default='admin'),
        password=dict(no_log=True),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        panorama_template=dict(),
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
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password', 'api_key')]
    state = module.params['state']
    panorama_template = module.params['panorama_template']
    obj = ManagementProfile(
        *[module.params[x] for x in (
            'name', 'ping', 'telnet', 'ssh', 'http', 'http_ocsp', 'https',
            'snmp', 'response_pages', 'userid_service',
            'userid_syslog_listener_ssl', 'userid_syslog_listener_udp',
            'permitted_ip')])
    commit = module.params['commit']

    # Create the device with the appropriate pandevice type
    dev = PanDevice.create_from_device(*auth)

    # Object tree initialization and parent selection.
    parent = dev
    if hasattr(dev, 'refresh_devices'):
        # This is Panorama.
        if not panorama_template:
            module.fail_json(msg="'panorama_template' is required for Panorama")
        ts = Template.refreshall(dev)
        for x in ts:
            if x.name == panorama_template:
                parent = x
                break
        else:
            module.fail_json(msg='template "{0}" not found'.format(panorama_template))

    # Check current status.
    try:
        cur_list = ManagementProfile.refreshall(parent)
    except PanDeviceError:
        e = get_exception()
        module.fail_json(msg='Failed refreshall: {0}'.format(e.message))
    parent.add(obj)

    # Determine what function to use based on the desired state.
    func = None
    changed = False
    if state == 'present':
        for x in cur_list:
            if x.name == obj.name:
                if not x.equal(obj, compare_children=False):
                    for child in x.children:
                        obj.add(child)
                    func = 'apply'
                break
        else:
            func = 'create'
    else:
        for x in cur_list:
            if x.name == obj.name:
                func = 'delete'
                break

    # Perform create / apply / delete, if needed.
    if func is not None:
        try:
            getattr(obj, func)()
        except PanDeviceError:
            e = get_exception()
            module.fail_json(msg='Failed {0}: {1}'.format(func, e.message))
        changed = True

        # Perform commit if requested.
        if commit:
            try:
                dev.commit()
            except PanDeviceError:
                e = get_exception()
                module.fail_json(msg='Failed commit: {0}'.format(e.message))

    # Done
    module.exit_json(changed=changed, msg="Done")


if __name__ == '__main__':
    main()
