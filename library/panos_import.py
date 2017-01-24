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
module: panos_import
short_description: import file on PAN-OS devices
description:
    - Import file on PAN-OS device
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - pan-python
    - requests
    - requests_toolbelt
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
    category:
        description:
            - category of file
        required: false
        default: software
    file:
        description:
            - file to import
        required: false
        default: None
    url:
        description:
            - url to file to import
        required: false
        default: None
'''

EXAMPLES = '''
# import software image PanOS_vm-6.1.1 on 192.168.1.1
- name: import software image into PAN-OS
  panos_import:
    ip_address: 192.168.1.1
    username: admin
    password: admin
    file: /tmp/PanOS_vm-6.1.1
    category: software
'''

RETURN='''
# Default return values
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

import os.path
import xml.etree
import tempfile
import shutil
import os

try:
    import pan.xapi
    import requests
    import requests_toolbelt
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def import_file(xapi, module, ip_address, file_, category):
    xapi.keygen()

    params = {
        'type': 'import',
        'category': category,
        'key': xapi.api_key
    }

    filename = os.path.basename(file_)

    mef = requests_toolbelt.MultipartEncoder(
        fields={
            'file': (filename, open(file_, 'rb'), 'application/octet-stream')
        }
    )

    r = requests.post(
        'https://'+ip_address+'/api/',
        verify=False,
        params=params,
        headers={'Content-Type': mef.content_type},
        data=mef
    )

    # if something goes wrong just raise an exception
    r.raise_for_status()

    resp = xml.etree.ElementTree.fromstring(r.content)

    if resp.attrib['status'] == 'error':
        module.fail_json(msg=r.content)

    return True, filename


def download_file(url):
    r = requests.get(url, stream=True)
    fo = tempfile.NamedTemporaryFile(prefix='ai', delete=False)
    shutil.copyfileobj(r.raw, fo)
    fo.close()

    return fo.name


def delete_file(path):
    os.remove(path)


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        category=dict(default='software'),
        file=dict(),
        url=dict()
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, required_one_of=[['file', 'url']])
    if not HAS_LIB:
        module.fail_json(msg='pan-python, requests, and requests_toolbelt are required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    file_ = module.params['file']
    url = module.params['url']

    category = module.params['category']

    # we can get file from URL or local storage
    if url is not None:
        file_ = download_file(url)

    try:
        changed, filename = import_file(xapi, module, ip_address, file_, category)
    except Exception:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    # cleanup and delete file if local
    if url is not None:
        delete_file(file_)

    module.exit_json(changed=changed, filename=filename, msg="okey dokey")

if __name__ == '__main__':
    main()
