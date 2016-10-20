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
module: panos_commit
short_description: commit firewall's candidate configuration
description:
    - PanOS module that will commit firewall's candidate configuration on
    the device. The new configuration will become active immediately.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
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
    interval:
        description:
            - interval for checking commit job
        required: false
        default: 0.5
    timeout:
        description:
            - timeout for commit job
        required: false
        default: None
    sync:
        description:
            - if commit should be synchronous
        required: false
        default: true
'''

EXAMPLES = '''
# Commit candidate config on 192.168.1.1 in sync mode
- panos_commit:
    ip_address: "192.168.1.1"
    username: "admin"
    password: "admin"
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
    sample: "okey dokey"
'''


from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def main():
    argument_spec = dict(
        ip_address=dict(),
        password=dict(no_log=True),
        username=dict(default='admin'),
        interval=dict(default=0.5),
        timeout=dict(),
        sync=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    if not HAS_LIB:
        module.fail_json(msg='pan-python required for this module')

    ip_address = module.params["ip_address"]
    if not ip_address:
        module.fail_json(msg="ip_address should be specified")
    password = module.params["password"]
    if not password:
        module.fail_json(msg="password is required")
    username = module.params['username']

    interval = module.params['interval']
    timeout = module.params['timeout']
    sync = module.params['sync']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    xapi.commit(
        cmd="<commit></commit>",
        sync=sync,
        interval=interval,
        timeout=timeout
    )

    module.exit_json(changed=True, msg="okey dokey")

if __name__ == '__main__':
    main()
