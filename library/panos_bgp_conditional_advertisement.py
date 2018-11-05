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
module: panos_bgp_conditional_advertisement
short_description: Configures a BGP Authentication Profile
description:
    - Use BGP to publish and consume routes from disparate networks.
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
            required: True
    username:
        description:
            - Username credentials to use for auth unless I(api_key) is set.
            default: admin
    password:
        description:
            - Password credentials to use for auth unless I(api_key) is set.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - Add or remove BGP Conditional Advertisement Policy.
                - present
                - absent
            default: present
    commit:
        description:
            - Commit configuration if changed.
            default: True
    vr_name:
        description:
            - Name of the virtual router; it must already exist; see panos_virtual_router.
            default: default
    advertisement_filter:
        description:
            - Advertisement filter object returned by panos_bgp_policy_filter; only needed on creation.
    non_exist_filter:
        description:
            - Non-Exist filter object returned by panos_bgp_policy_filter; only needed on creation.
    enable:
        description:
            - Enable this policy.
    name:
        description:
            - Name of Conditional Advertisement policy.
            required: True
    used_by:
        description:
            - List of Peer Groups using this policy.
'''

EXAMPLES = '''
    - name: Create BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: cond-rule-01
        enable: true
        non_exist_filter: '{{ non_exist.panos_obj }}'
        advertise_filter: '{{ advertise.panos_obj }}'

    - name: Update BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        vr_name: default
        name: cond-rule-01
        enable: false

    - name: Remove BGP Conditional Advertisement Rule
      panos_bgp_conditional_advertisement:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        state: absent
        vr_name: default
        name: cond-rule-01
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
            help='Add or remove BGP Conditional Advertisement Policy'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),

        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist; see panos_virtual_router'),
        non_exist_filter=dict(
            type='str',
            help='Non-Exist filter object returned by panos_bgp_policy_filter; only needed on creation'),
        advertise_filter=dict(
            type='str',
            help='Advertise filter object returned by panos_bgp_policy_filter; only needed on creation'),

        name=dict(
            type='str', required=True,
            help='Name of Conditional Advertisement policy'),
        enable=dict(
            type='bool',
            help='Enable this policy'),
        used_by=dict(
            type='list',
            help='List of Peer Groups using this policy'),
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
    # exclude these items from the kwargs passed to the object
    exclude_list += ['vr_name', 'non_exist_filter', 'advertise_filter']

    # generate the kwargs for the object
    obj_spec = dict((k, module.params[k]) for k in argument_spec.keys() if k not in exclude_list)

    name = module.params['name']
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']
    ne_filter = module.params['non_exist_filter']
    ad_filter = module.params['advertise_filter']

    # create the new state object
    new_obj = network.BgpPolicyConditionalAdvertisement(**obj_spec)

    changed = False
    try:
        # Create the device with the appropriate pandevice type
        device = base.PanDevice.create_from_device(*auth)
        network.VirtualRouter.refreshall(device)

        # grab the virtual router
        vr = device.find(vr_name, network.VirtualRouter)
        if vr is None:
            raise ValueError('Virtual router {0} does not exist'.format(vr_name))

        # fetch the current settings
        bgp = vr.find('', network.Bgp) or network.Bgp()
        cur_obj = vr.find(name, network.BgpPolicyConditionalAdvertisement, recursive=True)

        if state == 'present':
            if cur_obj is None or not new_obj.equal(cur_obj, compare_children=False):
                if cur_obj is None and (ne_filter is None or ad_filter is None):
                    raise ValueError(
                        'Creating a new Conditional Advertisement policy requires: ' +
                        'non_exist_filter and advertise_filter')
                elif cur_obj is None:
                    import pickle
                    from base64 import b64decode
                    # deserialize BgpPolicyNonExistFilter object
                    ne_filter_obj = pickle.loads(b64decode(ne_filter))
                    # deserialize BgpPolicyAdvertisementFilter object
                    ad_filter_obj = pickle.loads(b64decode(ad_filter))
                    # add them both to the new policy
                    new_obj.add(ne_filter_obj)
                    new_obj.add(ad_filter_obj)
                bgp.add(new_obj)
                # use create() here instead of apply because the children are required
                new_obj.create()
                changed = True
        elif state == 'absent':
            if cur_obj is not None:
                cur_obj.delete()
                changed = True
        else:
            module.fail_json(msg='[%s] state is not implemented yet' % state)
    except (PanDeviceError, KeyError):
        exc = get_exception()
        module.fail_json(msg=exc.message)

    if commit and changed:
        device.commit(sync=True, exception=True)

    if changed:
        module.exit_json(msg='BGP conditional advertisement policy update successful.', changed=changed)
    else:
        module.exit_json(msg='no changes required.', changed=changed)


if __name__ == '__main__':
    main()
