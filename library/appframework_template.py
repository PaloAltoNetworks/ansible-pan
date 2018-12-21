from __future__ import print_function
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
module: appframeowrk_template
short_description: Loads an Application Framework-ready template on Panorama and NGFW
description:
    - Configures Panorama and NGFW and loads a Template, a Template Stack and a DevGroup
author:
    - Palo Alto Networks
    - Francesco Vigo (fvigo)
version_added: "0.0"
requirements:
    - pan-python
    - pan-device
options:
    panorama_ip_address:
        description:
            - IP address (or hostname) of Panorama
        required: true
    panorama_password:
        description:
            - password for authentication on Panorama
        required: true
    panorama_username:
        description:
            - username for authentication on Panorama
        required: false
        default: "admin"
    ngfw_ip_address:
        description:
            - IP address (or hostname) of NGFW
        required: true
    ngfw_password:
        description:
            - password for authentication on NGFW
        required: true
    ngfw_username:
        description:
            - username for authentication on NGFW
        required: false
        default: "admin"
    shared_file:
        description:
            - XML file containing the shared configuration
        required: false
        default: "./shared.xml"
    devgroup_file:
        description:
            - XML file containing the Device Group configuration
        required: false
        default: "./devgroup.xml"
    template_file:
        description:
            - XML file containing the Template configuration
        required: false
        default: "./template.xml"
    template_stack_file:
        description:
            - XML file containing the Template Stack configuration
        required: false
        default: "./template-stack.xml"
    devgroup_name:
        description:
            - Name in the Device Group in the configuration
        required: true
    template_name:
        description:
            - Name in the Template in the configuration
        required: true
    template_stack_name:
        description:
            - Name in the Template Stack in the configuration
        required: true
'''

EXAMPLES = '''
# configure Application Framework lab
- name: appframework lab
  appframework_template:
    panorama_ip_address: "192.168.1.1"
    panorama_username: "admin"
    panorama_password: "admin"
    ngfw_ip_address: "192.168.1.10"
    ngfw_username: "admin"
    ngfw_password: "admin"
    shared_file: "./shared.xml"
    devgroup_file: "./devgroup.xml"
    template_file: "./template.xml"
    template_stack_file: "./template-stack.xml"
    devgroup_name: "DevGroup1"
    template_name: "Template1"
    template_stack_name: "TS1"
'''

import ssl
import sys
import time
import json
import os

try:
    import pan.xapi
    from pandevice import panorama
    from pandevice import firewall
    from pandevice import device
except ImportError:
    print("failed=True msg='pan-python and pan-device required for this module'")
    sys.exit(1)

def editPanoramaEntry(pn, xpath, file, module):
    if 'hostname' not in pn or 'username' not in pn or 'password' not in pn:
        module.fail_json(msg='Panorama credentials not specified!')
  
    #print('Reading configuration file: {}'. format(file))
    try:
        f = open(file,'r')
        d = f.read()
        f.close()
    except Exception as msg:
        module.fail_json(msg='Error while reading file: {}'.format(msg))

    #print('Configuration file read, connecting to Panorama...')

    try:
        xapi = pan.xapi.PanXapi(hostname=pn['hostname'], api_username=pn['username'], api_password=pn['password'])
    except pan.xapi.PanXapiError as msg:
        module.fail_json(msg='pan.xapi.PanXapi: {}'.format(msg))
    except Exception as e:
        module.fail_json(msg='Exception: {}'.format(e))

    #print('Connected to Panorama, editing configuration in path: {}'.format(xpath))

    try:
        xapi.edit(xpath=xpath, element=d)
    except pan.xapi.PanXapiError as msg:
        module.fail_json(msg='pan.xapi.PanXapi (edit): {}'.format(msg))

    #print('Configuration successfully edited!')
    return True

def setPanoramaEntry(pn, xpath, value, module):
    if 'hostname' not in pn or 'username' not in pn or 'password' not in pn:
        module.fail_json(msg='Panorama credentials not specified!')

    #print('Connecting to Panorama')

    try:
        xapi = pan.xapi.PanXapi(hostname=pn['hostname'], api_username=pn['username'], api_password=pn['password'])
    except pan.xapi.PanXapiError as msg:
        module.fail_json(msg='pan.xapi.PanXapi: {}'.format(msg))
    except Exception as e:
        module.fail_json(msg='Exception: {}'.format(e))

    #print('Connected to Panorama, setting configuration in path: {}'.format(xpath))

    try:
        xapi.set(xpath=xpath, element=value)
    except pan.xapi.PanXapiError as msg:
        module.fail_json(msg='pan.xapi.PanXapi (set): {}'.format(msg))

    #print('Configuration successfully set!')
    return True

def configurePanorama(pn, fwSerial, sharedFile, devGroupName, devGroupFile, templateName, templateFile, templateStackName, templateStackFile, module):
    if 'hostname' not in pn or 'username' not in pn or 'password' not in pn:
        raise RuntimeError('Panorama credentials not specified!')

    #print('Editing shared configuration')
    if not editPanoramaEntry(pn, "/config/shared", sharedFile, module):
        raise RuntimeError('Error editing shared resource')

    #print('Editing Device Group: {}'.format(devGroupName))
    if not editPanoramaEntry(pn, "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{}']".format(devGroupName), devGroupFile, module):
        raise RuntimeError('Error editing Device Group')

    #print('Editing Template: {}'.format(templateName))
    if not editPanoramaEntry(pn, "/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='{}']".format(templateName), templateFile, module):
        raise RuntimeError('Error editing Template')

    #print('Editing Template Stack: {}'.format(templateStackName))
    if not editPanoramaEntry(pn, "/config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{}']".format(templateStackName), templateStackFile, module):
        raise RuntimeError('Error editing Template Stack')

    #print('Adding device {} to Panorama managed devices'.format(fwSerial))
    xpath = "/config/mgt-config/devices"
    element = '<entry name=\"{}\"><vsys><entry name=\"vsys1\"/></vsys></entry>'.format(fwSerial)
    if not setPanoramaEntry(pn, xpath, element, module):
        raise RuntimeError('Error adding device to Panorama managed devices')

    #print('Adding device {} to Panorama Device Group: {}'.format(fwSerial, devGroupName))
    xpath = "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{}']/devices".format(devGroupName)
    element = '<entry name=\"{}\"><vsys><entry name=\"vsys1\"/></vsys></entry>'.format(fwSerial)
    if not setPanoramaEntry(pn, xpath, element, module):
        raise RuntimeError('Error adding device to Panorama Device Group')

    #print('Adding device {} to Panorama Template Stack: {}'.format(fwSerial, templateStackName))
    xpath = "/config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{}']/devices".format(templateStackName)
    element = '<entry name=\"{}\"/>'.format(fwSerial)
    if not setPanoramaEntry(pn, xpath, element, module):
        raise RuntimeError('Error adding device to Panorama Template Stack')
    #print('Panorama Configuration complete!')
    return True

def getDeviceSerial(fw, module):
    if 'hostname' not in fw or 'username' not in fw or 'password' not in fw:
        module.fail_json(msg='Device credentials not specified!')

    device = firewall.Firewall(fw['hostname'], fw['username'], fw['password'])
    devInfo = device.refresh_system_info()
    devSerial = devInfo.serial
    #print('Device Serial = {}'.format(devSerial))
    return devSerial


def panoramaCommitAll(pn, devicegroup, module):
    try: 
        pano = panorama.Panorama(pn['hostname'], pn['username'], pn['password'])
        #print("Committing on Panorama")
        pano.commit(sync=True)
        #print("Committed on Panorama")
        #print("Committing All on Panorama")
        pano.commit_all(sync=True, sync_all=True, devicegroup=devicegroup)
        #print("Committed All on Panorama")
    except Exception as e:
        module.fail_json(msg='Fail on commit: {}'.format(e))
    return True

def main():
    argument_spec = dict(
        panorama_ip_address=dict(default=None),
        panorama_password=dict(default=None, no_log=True),
        panorama_username=dict(default='admin'),
        ngfw_ip_address=dict(default=None),
        ngfw_password=dict(default=None, no_log=True),
        ngfw_username=dict(default='admin'),
        shared_file=dict(default='./shared.xml'),
        devgroup_file=dict(default='./devgroup.xml'),
        template_file=dict(default='./template.xml'),
        template_stack_file=dict(default='./template_stack.xml'),
        devgroup_name=dict(default=None),
        template_name=dict(default=None),
        template_stack_name=dict(default=None)
    )
    module = AnsibleModule(argument_spec=argument_spec)

    panorama_ip_address = module.params["panorama_ip_address"]
    if not panorama_ip_address:
        module.fail_json(msg="Panorama ip_address should be specified")
    panorama_password = module.params["panorama_password"]
    if not panorama_password:
        module.fail_json(msg="Panorama password is required")
    panorama_username = module.params['panorama_username']

    ngfw_ip_address = module.params["ngfw_ip_address"]
    if not ngfw_ip_address:
        module.fail_json(msg="NGFW ip_address should be specified")
    ngfw_password = module.params["ngfw_password"]
    if not ngfw_password:
        module.fail_json(msg="NGFW password is required")
    ngfw_username = module.params['ngfw_username']


    shared_file = module.params['shared_file']
    devgroup_file = module.params['devgroup_file']
    template_file = module.params['template_file']
    template_stack_file = module.params['template_stack_file']

    devgroup_name = module.params['devgroup_name']
    if not devgroup_name:
        module.fail_json(msg="Device Group name must be specified")
    
    template_name = module.params['template_name']
    if not template_name:
        module.fail_json(msg="Template name must be specified")

    template_stack_name = module.params['template_stack_name']
    if not template_stack_name:
        module.fail_json(msg="Template Stack name must be specified")
    
    changed = False

    pn = {
        'hostname' : panorama_ip_address,
        'username' : panorama_username,
        'password' : panorama_password
    }
    fw = {
        'hostname' : ngfw_ip_address,
        'username' : ngfw_username,
        'password' : ngfw_password
    }

    try:
        fwSerial = getDeviceSerial(fw, module)
        changed |= configurePanorama(pn, fwSerial, shared_file, devgroup_name, devgroup_file, template_name, template_file, template_stack_name, template_stack_file, module)
        changed |= panoramaCommitAll(pn, devgroup_name, module)
    except Exception as e:
        module.fail_json(msg='Got exception: {}'.format(e))

    module.exit_json(changed=changed, msg="okey dokey")

from ansible.module_utils.basic import *  # noqa


if __name__ == "__main__":
    main()
