#!/usr/bin/python

# Copyright (c) 2016, Palo Alto Networks <techbizdev@paloaltonetworks.com>
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
module: panos_service
short_description: create a service object
description:
    - Create a service object. Service objects are fundamental representation of the applications given src/dst ports and protocol
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
    service_name:
        description:
            - name of the service
        required: true
    protocol:
        description:
            - protocol for the service, should be tcp or udp
        required: true
    port:
        description:
            - destination port
        required: true
    source_port:
        description:
            - source port
        required: false
        default: None
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
# Creates service for port 22
  - name: create SSH service
    panos_service:
      ip_address: "192.168.1.1"
      password: "admin"
      service_name: "service-tcp-22"
      protocol: "tcp"
      port: "22"
'''

RETURN='''
# Default return values
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    import pan.xapi
    from pan.xapi import PanXapiError
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_SERVICE_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
                 "/vsys/entry[@name='vsys1']" +\
                 "/service/entry[@name='%s']"


def service_exists(xapi, service_name):
    xapi.get(_SERVICE_XPATH % service_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_service(xapi, module, service_name, protocol, port, source_port):
    if service_exists(xapi, service_name):
        return False

    exml = ['<protocol>']
    exml.append('<%s>' % protocol)
    exml.append('<port>%s</port>' % port)
    if source_port:
        exml.append('<source-port>%s</source-port>' % source_port)
    exml.append('</%s>' % protocol)
    exml.append('</protocol>')

    exml = ''.join(exml)

    xapi.set(xpath=_SERVICE_XPATH % service_name, element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        service_name=dict(required=True),
        protocol=dict(required=True, choices=['tcp', 'udp']),
        port=dict(required=True),
        source_port=dict(),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    service_name = module.params['service_name']
    protocol = module.params['protocol']
    port = module.params['port']
    source_port = module.params['source_port']
    commit = module.params['commit']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    try:
        changed = add_service(xapi, module,
                              service_name,
                              protocol,
                              port,
                              source_port)
        if changed and commit:
            xapi.commit(cmd="<commit></commit>", sync=True, interval=1)
    except PanXapiError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    module.exit_json(changed=changed, msg="okey dokey")

if __name__ == '__main__':
    main()
