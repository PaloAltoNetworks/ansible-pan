#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: panos_bgp
short_description: Configures Border Gateway Protocol (BGP)
description:
    - Use BGP to publish and consume routes from disparate networks.
author:
    - Joshua Colson (@freakinhippie)
    - Garfield Lee Freeman (@shinmog)
version_added: "2.9"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is supported.
    - Panorama is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.state
    - panos.full_template_support
options:
    commit:
        description:
            - Commit configuration if changed.
        default: true
    enable:
        description:
            - Enable BGP.
        default: true
    router_id:
        description:
            - Router ID in IP format (eg. 1.1.1.1)
        required: true
    reject_default_route:
        description:
            - Reject default route.
        default: true
    allow_redist_default_route:
        description:
            - Allow redistribute default route to BGP.
        default: false
    install_route:
        description:
            - Populate BGP learned route to global route table.
        default: false
    ecmp_multi_as:
        description:
            - Support multiple AS in ECMP.
        default: false
    enforce_first_as:
        description:
            - Enforce First AS for EBGP.
        default: true
    local_as:
        description:
            - Local Autonomous System (AS) number.
    as_format:
        description:
            - AS format I('2-byte')/I('4-byte').
        default: '2-byte'
    always_compare_med:
        description:
            - Always compare MEDs.
        default: false
    deterministic_med_comparison:
        description:
            - Deterministic MEDs comparison.
        default: true
    default_local_preference:
        description:
            - Default local preference.
        default: 100
    graceful_restart_enable:
        description:
            - Enable graceful restart.
        default: true
    gr_stale_route_time:
        description:
            - Time to remove stale routes after peer restart (in seconds).
    gr_local_restart_time:
        description:
            - Local restart time to advertise to peer (in seconds).
    gr_max_peer_restart_time:
        description:
            - Maximum of peer restart time accepted (in seconds).
    reflector_cluster_id:
        description:
            - Route reflector cluster ID.
    confederation_member_as:
        description:
            - Confederation requires member-AS number.
    aggregate_med:
        description:
            - Aggregate route only if they have same MED attributes.
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        default: "default"
'''

EXAMPLES = '''
- name: Configure and enable BGP
  panos_bgp:
    provider: '{{ provider }}'
    router_id: '1.1.1.1'
    local_as: '64512'
    commit: true
'''

RETURN = '''
# Default return values
'''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.errors import PanDeviceError
    from pandevice.network import Bgp
    from pandevice.network import BgpRoutingOptions
    from pandevice.network import VirtualRouter
except ImportError:
    pass


def setup_args():
    return dict(
        enable=dict(
            default=True, type='bool',
            help='Enable BGP'),
        router_id=dict(
            type='str',
            help='Router ID in IP format (eg. 1.1.1.1)'),
        reject_default_route=dict(
            type='bool', default=True,
            help='Reject default route'),
        allow_redist_default_route=dict(
            type='bool', default=False,
            help='Allow redistribute default route to BGP'),
        install_route=dict(
            type='bool', default=False,
            help='Populate BGP learned route to global route table'),
        ecmp_multi_as=dict(
            type='bool', default=False,
            help='Support multiple AS in ECMP'),
        enforce_first_as=dict(
            type='bool', default=True,
            help='Enforce First AS for EBGP'),
        local_as=dict(
            type='str',
            help='Local Autonomous System (AS) number'),
        as_format=dict(
            type='str', default='2-byte', choices=['2-byte', '4-byte'],
            help='AS format I("2-byte")/I("4-byte")'),
        always_compare_med=dict(
            type='bool', default=False,
            help='Always compare MEDs'),
        deterministic_med_comparison=dict(
            type='bool', default=True,
            help='Deterministic MEDs comparison'),
        default_local_preference=dict(
            type='int',
            help='Default local preference'),
        graceful_restart_enable=dict(
            type='bool', default=True,
            help='Enable graceful restart'),
        gr_stale_route_time=dict(
            type='int',
            help='Time to remove stale routes after peer restart (in seconds)'),
        gr_local_restart_time=dict(
            type='int',
            help='Local restart time to advertise to peer (in seconds)'),
        gr_max_peer_restart_time=dict(
            type='int',
            help='Maximum of peer restart time accepted (in seconds)'),
        reflector_cluster_id=dict(
            type='str',
            help='Route reflector cluster ID'),
        confederation_member_as=dict(
            type='str',
            help='Confederation requires member-AS number'),
        aggregate_med=dict(
            type='bool', default=True,
            help='Aggregate route only if they have same MED attributes'),
        vr_name=dict(
            default='default',
            help='Name of the virtual router; it must already exist'),
        commit=dict(
            type='bool', default=True,
            help='Commit configuration if changed'),
    )


def main():
    helper = get_connection(
        template=True,
        template_stack=True,
        with_state=True,
        with_classic_provider_spec=True,
        argument_spec=setup_args(),
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    parent = helper.get_pandevice_parent(module)

    # Other params.
    state = module.params['state']
    vr_name = module.params['vr_name']
    commit = module.params['commit']

    vr = VirtualRouter(vr_name)
    parent.add(vr)
    try:
        vr.refresh()
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))
    parent = vr

    # Generate the kwargs for network.Bgp.
    bgp_params = [
        'enable', 'router_id', 'reject_default_route', 'allow_redist_default_route',
        'install_route', 'ecmp_multi_as', 'enforce_first_as', 'local_as'
    ]
    bgp_spec = dict((k, module.params[k]) for k in bgp_params)

    # Generate the kwargs for network.BgpRoutingOptions.
    bgp_routing_options_params = [
        'as_format', 'always_compare_med', 'deterministic_med_comparison',
        'default_local_preference', 'graceful_restart_enable',
        'gr_stale_route_time', 'gr_local_restart_time', 'gr_max_peer_restart_time',
        'reflector_cluster_id', 'confederation_member_as', 'aggregate_med',
    ]
    bgp_routing_options_spec = dict((k, module.params[k]) for k in bgp_routing_options_params)

    bgp = Bgp(**bgp_spec)
    bgp_routing_options = BgpRoutingOptions(**bgp_routing_options_spec)
    bgp.add(bgp_routing_options)

    changed = False
    live_bgp = parent.find('', Bgp)
    if state == 'present':
        if live_bgp is None:
            changed = True
            parent.add(bgp)
            if not module.check_mode:
                try:
                    bgp.create()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed create: {0}'.format(e))
        else:
            live_options = None
            other_children = []
            options_children = []
            for x in live_bgp.children:
                if x.__class__ == BgpRoutingOptions:
                    live_options = x
                    options_children = x.children
                    x.removeall()
                else:
                    other_children.append(x)

            live_bgp.removeall()
            if live_options is not None:
                live_bgp.add(live_options)

            parent.add(bgp)
            if not live_bgp.equal(bgp):
                changed = True
                bgp.extend(other_children)
                bgp_routing_options.extend(options_children)
                if not module.check_mode:
                    try:
                        bgp.apply()
                    except PanDeviceError as e:
                        module.fail_json(msg='Failed apply: {0}'.format(e))
    else:
        if live_bgp is not None:
            changed = True
            if not module.check_mode:
                try:
                    live_bgp.delete()
                except PanDeviceError as e:
                    module.fail_json(msg='Failed delete: {0}'.format(e))

    if commit and changed:
        helper.commit(module)

    module.exit_json(msg='BGP configuration successful.', changed=changed)


if __name__ == '__main__':
    main()
