#!/usr/bin/env python

# Copyright (c) 2014, Palo Alto Networks <techbizdev@paloaltonetworks.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

DOCUMENTATION = '''
---
module: panos_admin
short_description: add or modify PAN-OS admins
description:
    - Add or modify PAN-OS admins
author: 
    - Palo Alto Networks 
    - Luigi Mori (jtschichold)
version_added: "2.2"
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
    password:
        description:
            - password for authentication
        required: true
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    admin_username:
        description:
            - username for admin user
        required: false
        default: "admin"
    admin_password:
        description:
            - password for admin user
        required: true
    role:
        description:
            - role for admin user
        required: false
        default: null
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# Set the password of user admin to "badpassword"
# Doesn't commit the candidate config
  - name: set admin password
    panos_admin:
      ip_address: "192.168.1.1"
      password: "admin"
      admin_username: admin
      admin_password: "badpassword"
      commit: False
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "okey dokey"
'''

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_ADMIN_XPATH = "/config/mgt-config/users/entry[@name='%s']"


def admin_exists(xapi, admin_username):
    xapi.get(_ADMIN_XPATH % admin_username)
    e = xapi.element_root.find('.//entry')
    return e


def admin_set(xapi, module, admin_username, admin_password, role):
    if admin_password is not None:
        xapi.op(cmd='request password-hash password "%s"' % admin_password,
                cmd_xml=True)
        r = xapi.element_root
        phash = r.find('.//phash').text
    if role is not None:
        rbval = "yes"
        if role != "superuser" and role != 'superreader':
            rbval = ""

    ea = admin_exists(xapi, admin_username)
    if ea is not None:
        # user exists
        changed = False

        if role is not None:
            rb = ea.find('.//role-based')
            if rb is not None:
                if rb[0].tag != role:
                    changed = True
                    xpath = _ADMIN_XPATH % admin_username
                    xpath += '/permissions/role-based/%s' % rb[0].tag
                    xapi.delete(xpath=xpath)

                    xpath = _ADMIN_XPATH % admin_username
                    xpath += '/permissions/role-based'
                    xapi.set(xpath=xpath,
                             element='<%s>%s</%s>' % (role, rbval, role))

        if admin_password is not None:
            xapi.edit(xpath=_ADMIN_XPATH % admin_username+'/phash',
                      element='<phash>%s</phash>' % phash)
            changed = True

        return changed

    # setup the non encrypted part of the monitor
    exml = []

    exml.append('<phash>%s</phash>' % phash)
    exml.append('<permissions><role-based><%s>%s</%s>'
                '</role-based></permissions>' % (role, rbval, role))

    exml = ''.join(exml)
    # module.fail_json(msg=exml)

    xapi.set(xpath=_ADMIN_XPATH % admin_username, element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        admin_username=dict(default='admin'),
        admin_password=dict(default=None, no_log=True),
        role=dict(default=None),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    if not HAS_LIB:
        module.fail_json(msg='pan-python required for this module')

    ip_address = module.params["ip_address"]
    if not ip_address:
        module.fail_json(msg="ip_address should be specified")
    password = module.params["password"]
    if not password:
        module.fail_json(msg="password is required")
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    admin_username = module.params['admin_username']
    if admin_username is None:
        module.fail_json(msg="admin_username is required")
    admin_password = module.params['admin_password']
    role = module.params['role']
    commit = module.params['commit']

    changed = admin_set(xapi, module, admin_username, admin_password, role)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import * # flake8: noqa

if __name__ == '__main__':
    main()
