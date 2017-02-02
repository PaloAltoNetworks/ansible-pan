#!/usr/bin/env python

#  Copyright 2016 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

DOCUMENTATION = '''
---
module: panos_dag
short_description: create a dynamic address group
description:
    - Create a dynamic address group object in the firewall used for policy rules
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer)"
version_added: "2.3"
requirements:
    - pan-python
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device
        required: true
        default: null
    password:
        description:
            - password for authentication
        required: true
        default: null
    username:
        description:
            - username for authentication
        required: false
        default: "admin"
    dag_name:
        description:
            - name of the dynamic address group
        required: true
        default: null
    dag_filter:
        description:
            - dynamic filter user by the dynamic address group
        required: true
        default: null
    commit:
        description:
            - commit if changed
        required: false
        default: true
'''

EXAMPLES = '''
- name: dag
  panos_dag:
    ip_address: "192.168.1.1"
    password: "admin"
    dag_name: "dag-1"
    dag_filter: "'aws-tag.aws:cloudformation:logical-id.ServerInstance' and 'instanceState.running'"
'''

RETURN='''
# Default return values
'''

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

from ansible.module_utils.basic import AnsibleModule

try:
    import pan.xapi
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

_ADDRGROUP_XPATH = "/config/devices/entry[@name='localhost.localdomain']" +\
                   "/vsys/entry[@name='vsys1']/address-group/entry[@name='%s']"


def addressgroup_exists(xapi, group_name):
    xapi.get(_ADDRGROUP_XPATH % group_name)
    e = xapi.element_root.find('.//entry')
    if e is None:
        return False
    return True


def add_dag(xapi, dag_name, dag_filter):
    if addressgroup_exists(xapi, dag_name):
        return False

    # setup the non encrypted part of the monitor
    exml = []

    exml.append('<dynamic>')
    exml.append('<filter>%s</filter>' % dag_filter)
    exml.append('</dynamic>')

    exml = ''.join(exml)
    xapi.set(xpath=_ADDRGROUP_XPATH % dag_name, element=exml)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True),
        username=dict(default='admin'),
        dag_name=dict(required=True),
        dag_filter=dict(required=True),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if not HAS_LIB:
        module.fail_json(msg='pan-python is required for this module')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']

    xapi = pan.xapi.PanXapi(
        hostname=ip_address,
        api_username=username,
        api_password=password
    )

    dag_name = module.params['dag_name']
    dag_filter = module.params['dag_filter']
    commit = module.params['commit']

    changed = add_dag(xapi, dag_name, dag_filter)

    if changed and commit:
        xapi.commit(cmd="<commit></commit>", sync=True, interval=1)

    module.exit_json(changed=changed, msg="okey dokey")

if __name__ == '__main__':
    main()
