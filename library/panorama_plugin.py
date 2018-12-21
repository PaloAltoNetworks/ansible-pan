#!/usr/bin/env python

# Copyright (c) 2018, Palo Alto Networks <techbizdev@paloaltonetworks.com>
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
module: panorama_plugin
short_description: Install Panorama Plugin
description:
    - Install Panorama Plugin
author:
    - Palo Alto Networks
    - Luigi Mori (jtschichold), Francesco Vigo (fvigo)
version_added: "0.0"
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of Panorama device
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
    plugin:
        description:
            - Plugin to be installed, including version (i.e. cloud_services-1.2.0 )
        required: true
    job_timeout:
        description:
            - timeout for download and install jobs in seconds
        required: false
        default: 120
'''

EXAMPLES = '''
# Install cloud services plugin 1.2.0
- name: install cloud plugin
  panorama_plugin:
    ip_address: "192.168.1.1"
    password: "admin"
    plugin: cloud_services-1.2.0

'''

import sys
import time

try:
    import pan.xapi
except ImportError:
    print("failed=True msg='pan-python required for this module'")
    sys.exit(1)

class JobException(Exception):
    pass


def check_job(xapi, jobnum, timeout=240):
    now = time.time()
    while time.time() < now+timeout:
        xapi.op(cmd='<show><jobs><id>%s</id></jobs></show>' % jobnum)
        #print('result = {}'.format(xapi.xml_result()))
        status = xapi.element_root.find('.//status')
        if status is None:
            raise JobException("Invalid job %s: no status information %s" %
                               (jobnum, xapi.xml_document))
        if status.text == 'FIN':
            result = xapi.element_root.find('.//job/result')
            if result is None:
                raise JobException("Invalid FIN job %s: no result %s" %
                                   (jobnum, xapi.xml_document))
            if result.text != 'OK':
                details = xapi.element_root.find('.//job/details/line')
                #print('details is: {}'.format(details.text))
                if details is None or details.text is None or details.text != 'Image exists already':
                   raise JobException("Job %s failed: %s" %
                                       (jobnum, xapi.xml_document))
            return None

    raise JobException("Timeout in job %s" % jobnum)


def download_install_plugin(xapi, module, plugin, job_timeout):
    # check if the plugin is already installed
    xapi.op(cmd="<show><plugins><installed></installed></plugins></show>")
    #print("Installed plugins: {}".format(xapi.xml_document))

    entries = xapi.element_root.findall('.//list/entry')
    for e in entries:
        ver = e.find('version').text
        #print('Found version: {}'.format(ver))
        if ver == plugin:
                # plugin already installed!
                return False

    # check updates
    xapi.op(cmd="<request><plugins>"
                "<check></check>"
                "</plugins></request>")

    result = xapi.element_root.find('.//result')
    #print('Result check is: {}'.format(result.text))
    if result is None or result.text is None or result.text != "List of plugin packages has been updated":
        module.fail_json(msg="Unable to check for plugins: %s".format(xapi.xml_document))

    xapi.op(cmd="<request><plugins>"
                "<download><file>%(plugin)s</file></download>"
                "</plugins></request>" %
                dict(plugin=plugin))
    job = xapi.element_root.find('.//job')
    if job is None:
        module.fail_json(msg="no job from download latest %s request" %
                         something)
    job = job.text
    check_job(xapi, job, job_timeout)

    xapi.op(cmd="<request><plugins>"
                "<install>%(plugin)s</install>"
                "</plugins></request>" %
                dict(plugin=plugin))

    result = xapi.element_root.find('.//result')
    #print('Result is: {}'.format(result.text))
    if result is None or result.text is None or "has been installed successfully" not in result.text:
        module.fail_json(msg="Unable to install plugin: %s".format(xapi.xml_document))

    return True

def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        plugin=dict(default=None),
        job_timeout=dict(type='int', default=240)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    ip_address = module.params["ip_address"]
    if not ip_address:
        module.fail_json(msg="ip_address should be specified")
    password = module.params["password"]
    if not password:
        module.fail_json(msg="password is required")
    username = module.params['username']
    plugin = module.params["plugin"]
    if not plugin:
        module.fail_json(msg="plugin is required")

    job_timeout = module.params['job_timeout']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    changed = False

    changed |= download_install_plugin(xapi, module, plugin, job_timeout)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
