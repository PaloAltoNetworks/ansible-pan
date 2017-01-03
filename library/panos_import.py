#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage PaloAltoNetworks Firewall
# (c) 2016, techbizdev <techbizdev@paloaltonetworks.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: panos_import
short_description: import file on PAN-OS devices
description:
    - Import file on PAN-OS device
author: 
    - Palo Alto Networks 
    - Luigi Mori (jtschichold)
version_added: "0.0"
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

import sys
import os.path
import xml.etree
import tempfile
import shutil
import os

try:
    import pan.xapi
except ImportError:
    print "failed=True msg='pan-python required for this module'"
    sys.exit(1)

try:
    import requests
except ImportError:
    print "failed=True msg='requests required for this module'"
    sys.exit(1)

try:
    import requests_toolbelt
except ImportError:
    print "failed=True msg='requests_toolbelt required for this module'"
    sys.exit(1)


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
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        category=dict(default='software'),
        file=dict(default=None),
        url=dict(default=None)
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

    file_ = module.params['file']
    url = module.params['url']
    if file_ is None and url is None:
        module.fail_json(msg="file or url is required")
    if file_ is not None and url is not None:
        module.fail_json(msg="only one of file or url can be specified")
    category = module.params['category']

    if url is not None:
        file_ = download_file(url)

    changed, filename = import_file(xapi, module, ip_address, file_, category)

    if url is not None:
        delete_file(file_)

    module.exit_json(changed=changed, filename=filename, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
