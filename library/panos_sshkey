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
module: panos_sshkey
short_description: manage public SSH keys of admins
description:
    - Manage SSH keys of admins
author: 
    - Palo Alto Networks 
    - Luigi Mori (jtschichold)
version_added: "0.0"
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
            - username of the admin to operate on
        required: true
    public_key:
        description:
            - SSH public key to set
        required: false
        default: None
    state:
        description:
            - if C(present) module checks for presence of SSH key
              if C(absent) module deletes SSH key if present
        required: true
        choices: [ present, absent ]
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# delete SSH key of foo if present
- panos_sshkey:
    ip_address: "192.168.1.1"
    password: "admin"
    admin_username: "foo"
    state: "absent"
'''

import sys
import base64

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

_ADMINPROFILE_XPATH = "/config/mgt-config/users/entry[@name='%s']"
_PKEY_XPATH = _ADMINPROFILE_XPATH+"/public-key"


def get_publickey(xapi, user):
    xapi.get(xpath=_PKEY_XPATH % user)
    pkey = xapi.element_root.find('.//public-key')
    if pkey is None:
        return None
    return base64.b64decode(pkey.text)


def delete_publickey(xapi, user):
    xapi.delete(xpath=_PKEY_XPATH % user)


def set_publickey(xapi, user, cpkey, pkey):
    b64pkey = base64.b64encode(pkey)
    e = "<public-key>%s</public-key>" % b64pkey
    if cpkey is None:
        xapi.set(xpath=_ADMINPROFILE_XPATH % user, element=e)
    else:
        xapi.edit(xpath=_PKEY_XPATH % user, element=e)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        admin_username=dict(default=None, required=True),
        public_key=dict(default=None),
        state=dict(choices=['present', 'absent'], required=True,
                   default=None),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec)

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

    panos_user = module.params['admin_username']
    public_key = module.params['public_key']
    state = module.params['state']
    commit = module.params['commit']

    changed = False

    pkey = get_publickey(xapi, panos_user)

    if state == 'absent':
        if pkey is not None:
            delete_publickey(xapi, panos_user)
            changed = True
    else:
        # state 'present'
        if pkey is None and public_key is None:
            module.fail_json(msg="state 'present' but no public_key to set")

        if pkey != public_key and public_key is not None:
            set_publickey(xapi, panos_user, pkey, public_key)
            changed = True

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
