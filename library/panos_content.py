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
module: panos_content
short_description: upgrade PAN-OS dynamic updates
description:
    - Upgrade PAN-OS device dynamic updates with the latest available version
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
    content_update:
        description:
            - whether content (Apps or Apps+Threats) should be updated
        required: false
        default: "false"
    anti_virus_update:
        description:
            - whether Anti-Virus signatures should be updated
        required: false
        default: "false"
    wildfire_update:
        description:
            - whether Wildfire signatures should be updated
        required: false
        default: "false"
    job_timeout:
        description:
            - timeout for download and install jobs in seconds
        required: false
        default: 240
'''

EXAMPLES = '''
# upgrade content to the lastest release
- name: upgrade content
  panos_content:
    ip_address: "192.168.1.1"
    password: "admin"
    content_update: yes

# upgrade anti-virus and wildfire signatures to the
# latest releases
- name: upgrade anti-virus
  panos_content:
    ip_address: "192.168.1.1"
    password: "admin"
    anti_virus_update: yes
    wildfire_update: yes
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
        print('result = {}'.format(xapi.xml_result()))
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
            return None

    raise JobException("Timeout in job %s" % jobnum)


def upgrade_something(xapi, module, something, job_timeout):
    # check something updates
    xapi.op(cmd="<request><%(something)s><upgrade>"
                "<check></check>"
                "</upgrade></%(something)s></request>" %
                dict(something=something))

    entries = xapi.element_root.findall('.//content-updates/entry')
    cus = []
    for e in entries:
        cus.append(
            (
                e.find('version').text,
                e.find('current').text,
                e.find('downloaded').text
            )
        )
    if len(cus) == 0:
        module.fail_json(msg="no content-updates after check")
    cus = sorted(cus, key=lambda x: x[0], reverse=True)

    latestcus = cus[0]
    if latestcus[1] == 'yes':
        # latest already current
        return False

    if not latestcus[2] == 'yes':
        # let's download it
        xapi.op(cmd="<request><%(something)s><upgrade>"
                    "<download><latest></latest></download>"
                    "</upgrade></%(something)s></request>" %
                    dict(something=something))
        job = xapi.element_root.find('.//job')
        if job is None:
            module.fail_json(msg="no job from download latest %s request" %
                             something)
        job = job.text
        check_job(xapi, job, job_timeout)

    xapi.op(cmd="<request><%(something)s><upgrade>"
                "<install><version>latest</version></install>"
                "</upgrade></%(something)s></request>" %
                dict(something=something))
    job = xapi.element_root.find('.//job')
    if job is None:
        module.fail_json(msg="no hob from install latest %s request" %
                         something)
    job = job.text
    jobresult = check_job(xapi, job, job_timeout)

    return True


def upgrade_content(xapi, module, job_timeout):
    return upgrade_something(xapi, module, 'content', job_timeout)


def upgrade_anti_virus(xapi, module, job_timeout):
    return upgrade_something(xapi, module, 'anti-virus', job_timeout)


def upgrade_wildfire(xapi, module, job_timeout):
    return upgrade_something(xapi, module, 'wildfire', job_timeout)


def main():
    argument_spec = dict(
        ip_address=dict(default=None),
        password=dict(default=None, no_log=True),
        username=dict(default='admin'),
        content_update=dict(type='bool', default=False),
        anti_virus_update=dict(type='bool', default=False),
        wildfire_update=dict(type='bool', default=False),
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

    job_timeout = module.params['job_timeout']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    changed = False

    content_update = module.params['content_update']
    if content_update:
        changed |= upgrade_content(xapi, module, job_timeout)
    anti_virus_update = module.params['anti_virus_update']
    if anti_virus_update:
        changed |= upgrade_anti_virus(xapi, module, job_timeout)
    wildfire_update = module.params['wildfire_update']
    if wildfire_update:
        changed |= upgrade_wildfire(xapi, module, job_timeout)

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa

main()
