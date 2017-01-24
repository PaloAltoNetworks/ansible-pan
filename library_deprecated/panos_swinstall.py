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
module: panos_swinstall
short_description: install PAN-OS software image
description:
    - Install PAN-OS software image.
    - The image should have been already imported on the device
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
    version:
        description:
            - version to install
        required: false
        default: None
    file:
        description:
            - file to install
        required: false
        default: None
    job_timeout:
        description:
            - timeout for download and install jobs in seconds
        required: false
        default: 240
'''

EXAMPLES = '''
# install PanOS_vm-6.1.1 image
- name: install software
  panos_swinstall:
    ip_address: 192.168.1.1
    username: admin
    password: admin
    file: PanOS_vm-6.1.1
'''

RETURN = '''
status:
    description: success status
    returned: success
    type: string
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

from ansible.module_utils.basic import *
import time

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


class JobException(Exception):
    pass


def check_job(xapi, jobnum, timeout=240):
    now = time.time()
    while time.time() < now+timeout:
        xapi.op(cmd='<show><jobs><id>%s</id></jobs></show>' % jobnum)
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
                raise JobException("Job %s failed: %s" %
                                   (jobnum, xapi.xml_document))
            nextjob = xapi.element_root.find('.//nextjob')
            if nextjob is not None:
                return nextjob.text

            return None

    raise JobException("Timeout in job %s" % jobnum)


def install_software(xapi, module, version, file_, job_timeout):
    # check something updates
    if version is not None:
        cmd = '<request><system><software>' +\
              '<install><version>%s</version></install>' +\
              '</software></system></request>' % version
        something = version
    else:
        cmd = '<request><system><software>' +\
              '<install><file>%s</file></install>' +\
              '</software></system></request>' % file_
        something = file_

    xapi.op(cmd=cmd)
    job = xapi.element_root.find('.//job')
    if job is None:
        module.fail_json(msg="no job from install software image %s" %
                         something)
    job = job.text
    check_job(xapi, job, timeout=job_timeout)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        version=dict(default=None),
        file=dict(default=None),
        job_timeout=dict(type='int', default=240)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

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

    job_timeout = module.params['job_timeout']
    file_ = module.params['file']
    version = module.params['version']
    if version is None and file_ is None:
        module.fail_json(msg="one of version or file should be specified")

    changed = install_software(xapi, module, version, file_, job_timeout)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
