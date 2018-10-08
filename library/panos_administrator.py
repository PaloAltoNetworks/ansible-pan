#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2016 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: panos_administrator
short_description: Manage PAN-OS administrator user accounts.
description:
    - Manages PAN-OS administrator user accounts.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - The state.  Can be either I(present)/I(absent).
        default: "present"
    admin_username:
        description:
            - Admin name.
        required: false
        default: "admin"
    authentication_profile:
        description:
            - The authentication profile.
    web_client_cert_only:
        description:
            - Use only client certificate authenciation (Web)
    superuser:
        description:
            - Admin type - superuser
    superuser_read_only:
        description:
            - Admin type - superuser, read only
    panorama_admin:
        description:
            - This is for Panorama only.
            - Make the user a Panorama admin only
    device_admin:
        description:
            - Admin type - device admin
    device_admin_read_only:
        description:
            - Admin type - device admin, read only
    vsys:
        description:
            - This is for multi-vsys physical firewalls only.
            - The list of vsys this admin should manage.
    vsys_read_only:
        description:
            - This is for multi-vsys physical firewalls only.
            - The list of vsys this read only admin should manage.
    ssh_public_key:
        description:
            - Use public key authentication (ssh)
    role_profile:
        description:
            - The role based profile.
    admin_password:
        description:
            - New plain text password for the I(admin_username) user.
            - If this is not specified, then the password is left as-is.
    password_profile:
        description:
            - The password profile for this user.
    commit:
        description:
            - Commit configuration if changed.
        default: true
'''

EXAMPLES = '''
# Configure user "foo"
# Doesn't commit the candidate config
  - name: configure foo administrator
    panos_administrator:
      ip_address: "192.168.1.1"
      password: "admin"
      admin_username: 'foo'
      admin_password: 'secret'
      superuser: true
      commit: false
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "done"
'''
from ansible.module_utils.basic import AnsibleModule

try:
    from pandevice.base import PanDevice
    from pandevice.device import Administrator
    from pandevice.errors import PanDeviceError
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
        admin_username=dict(default='admin'),
        authentication_profile=dict(),
        web_client_cert_only=dict(type='bool'),
        superuser=dict(type='bool'),
        superuser_read_only=dict(type='bool'),
        panorama_admin=dict(type='bool'),
        device_admin=dict(type='bool'),
        device_admin_read_only=dict(type='bool'),
        vsys=dict(type='list'),
        vsys_read_only=dict(type='list'),
        ssh_public_key=dict(),
        role_profile=dict(),
        admin_password=dict(no_log=True),
        password_profile=dict(no_log=False),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])

    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get PAN-OS auth info.
    auth = [module.params[x] for x in
            ['ip_address', 'username', 'password', 'api_key']]

    # Open the connection to the PAN-OS device.
    con = PanDevice.create_from_device(*auth)

    # Get administrator object spec.
    spec_params = [
        'authentication_profile', 'web_client_cert_only', 'superuser',
        'superuser_read_only', 'panorama_admin', 'device_admin',
        'device_admin_read_only', 'vsys', 'vsys_read_only',
        'ssh_public_key', 'role_profile', 'password_profile',
    ]
    params = dict((k, module.params[k]) for k in spec_params)
    params['name'] = module.params['admin_username']
    password = module.params['admin_password']

    # Get other params.
    state = module.params['state']
    commit = module.params['commit']

    # Get the current administrators.
    admins = Administrator.refreshall(con, add=False)
    obj = Administrator(**params)
    con.add(obj)

    # Set "password_hash" by requesting a password hash.
    if password is not None:
        try:
            obj.password_hash = con.request_password_hash(password)
        except PanDeviceError as e:
            module.fail_json(msg='Failed to get phash: {0}'.format(e))

    # Perform the requested action.
    changed = False
    if state == 'present':
        for x in admins:
            if obj.name == x.name:
                # If user did not specify a password, keep the current one.
                if obj.password_hash is None and x.password_hash:
                    obj.password_hash = x.password_hash
                # Don't use .equal() here because we don't want pandevice to
                # try and do smart things with the password_hash field.
                if obj.element_str() != x.element_str():
                    try:
                        obj.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
                    else:
                        changed = True
                break
        else:
            try:
                obj.create()
            except PanDeviceError as e:
                module.fail_json(msg='Failed create: {0}'.format(e))
            else:
                changed = True
    elif state == 'absent':
        if obj.name in [x.name for x in admins]:
            try:
                obj.delete()
            except PanDeviceError as e:
                module.fail_json(msg='Failed delete: {0}'.format(e))
            else:
                changed = True

    # Commit if appropriate.
    if changed and commit:
        try:
            con.commit(sync=True)
        except PanDeviceError as e:
            module.fail_json(msg='Failed commit: {0}'.format(e))

    # Done.
    module.exit_json(changed=changed, msg='done')


if __name__ == '__main__':
    main()
