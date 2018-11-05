#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#  Copyright 2018 Palo Alto Networks, Inc
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: panos_virtual_router
short_description: Configures a Virtual Router
description:
    - Manage PANOS Virtual Router
author: "Joshua Colson (@freakinhippie)"
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is NOT supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
        required: true
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Add or remove BGP configuration.
        choices: ['present', 'absent']
        default: 'present'
    commit:
        description:
            - Commit configuration if changed.
        default: true
    name (str):
        description:
            -  Name of virtual router (Default: "default")
    interface (list):
        description:
            -  List of interface names
    ad_static (int):
        description:
            -  Administrative distance for this protocol
    ad_static_ipv6 (int):
        description:
            -  Administrative distance for this protocol
    ad_ospf_int (int):
        description:
            -  Administrative distance for this protocol
    ad_ospf_ext (int):
        description:
            -  Administrative distance for this protocol
    ad_ospfv3_int (int):
        description:
            -  Administrative distance for this protocol
    ad_ospfv3_ext (int):
        description:
            -  Administrative distance for this protocol
    ad_ibgp (int):
        description:
            -  Administrative distance for this protocol
    ad_ebgp (int):
        description:
            -  Administrative distance for this protocol
    ad_rip (int):
        description:
            -  Administrative distance for this protocol
'''

EXAMPLES = '''
- name: Create Virtual Router
    panos_virtual_router:
      ip_address: '{{ ip_address }}'
      username: '{{ username }}'
      password: '{{ password }}'
      state: 'present'
      name: vr-1
      commit: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception

try:
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import base
    from pandevice import panorama
    from pandevice.errors import PanDeviceError
    from pandevice import network

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def setup_args():
    return dict(
        ip_address=dict(
            required=True,
            help='IP address (or hostname) of PAN-OS device being configured'),
        password=dict(
            no_log=True,
            help='Password credentials to use for auth unless I(api_key) is set'),
        username=dict(
            default='admin',
            help='Username credentials to use for auth unless I(api_key) is set'),
        api_key=dict(
            no_log=True,
            help='API key that can be used instead of I(username)/I(password) credentials'),
        state=dict(
            default='present', choices=['present', 'absent'],
            help='Add or remove virtual router'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        name=dict(
            type='str', default='default',
            help='Name of virtual router'),
        interface=dict(
            type='list',
            help='List of interface names'),
        ad_static=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_static_ipv6=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospf_int=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospf_ext=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospfv3_int=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ospfv3_ext=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ibgp=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_ebgp=dict(
            type='int',
            help='Administrative distance for this protocol'),
        ad_rip=dict(
            type='int',
            help='Administrative distance for this protocol'),
    )


def main():
    argument_spec = setup_args()

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get the firewall / panorama auth.
    auth = [module.params[x] for x in
            ('ip_address', 'username', 'password', 'api_key')]

    # exclude the default items from kwargs passed to the object
    exclude_list = ['ip_address', 'username', 'password', 'api_key', 'state', 'commit']

    # generate the kwargs for network.VirtualRouter
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    state = module.params['state']
    commit = module.params['commit']

    # create the new state object
    virtual_router = network.VirtualRouter(**obj_spec)

    changed = False
    try:
        # Create the device with the appropriate pandevice type
        device = base.PanDevice.create_from_device(*auth)
        network.VirtualRouter.refreshall(device)

        # search for the virtual router
        vr = device.find(name, network.VirtualRouter)

        # compare differences between the current state vs desired state
        if state == 'present':
            if vr is None or not virtual_router.equal(vr, compare_children=False):
                device.add(virtual_router)
                virtual_router.create()
                changed = True
        elif state == 'absent':
            if vr is not None:
                vr.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='Virtual router update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
