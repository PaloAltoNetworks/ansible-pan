#!/usr/bin/env python

#  Copyright 2019 Palo Alto Networks, Inc
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
module: panos_loopback_interface
short_description: configure network loopback interfaces
description:
    - Configure loopback interfaces on PanOS


author: "Geraint Jones (@nexus_moneky_nz)"
version_added: "2.8"
requirements:
    - pan-python can be obtained from PyPi U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPi U(https://pypi.python.org/pypi/pandevice)
note:
    - Checkmode is not supported.
options:
    ip_address:
        description:
            - IP address (or hostname) of PAN-OS device being configured.
        required: true
    username:
        description:
            - Username credentials to use for auth.
        default: "admin"
    password:
        description:
            - Password credentials to use for auth.
    api_key:
        description:
            - API key that can be used instead of I(username)/I(password) credentials.
    state:
        description:
            - The state.  Can be either I(present)/I(absent).
    if_name:
        description:
            - Name of the interface to configure.
        required: true
    ip:
        description:
            - List of static IP addresses.
    ipv6_enabled:
        description:
            - Enable IPv6.
    management_profile:
        description:
            - Interface management profile name.
    mtu:
        description:
            - MTU for loopback interface.
    netflow_profile:
        description:
            - Netflow profile for loopback interface.
    comment:
        description:
            - Interface comment.
    zone_name:
        description:
            - Name of the zone for the interface. If the zone does not exist it is created but if the
            - zone exists and it is not of the correct mode the operation will fail.
        required: true
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
        default: "default"
    vsys_dg:
        description:
            - Name of the vsys (if firewall) or device group (if panorama) to put this object.
        default: "vsys1"
    commit:
        description:
            - Commit if changed
        default: true
'''

EXAMPLES = '''
# Delete loopback.1
- name: delete loopback.1
  panos_loopback_interface:
    ip_address: "192.168.1.1"
    username: "ansible"
    password: "secret"
    if_name: "loopback.1"
    state: absent

# Update/create loopback comment.
- name: update loopback.1 comment
  panos_loopback_interface:
    ip_address: "192.168.1.1"
    username: "ansible"
    password: "secret"
    if_name: "loopback.1"
    ip: ["10.1.1.1/32"]
    comment: "Loopback iterface"
    state: present
'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import get_exception


try:
    from pandevice import base
    from pandevice import panorama
    from pandevice import network
    from pandevice import device
    from pandevice import errors
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def set_zone(con, loopback, zone_name, zones):
    desired_zone = None

    # Remove the interface from the zone.
    for z in zones:
        if z.name == zone_name:
            desired_zone = z
        elif loopback.name in z.interface:
            z.interface.remove(loopback.name)
            z.update('interface')

    if desired_zone is not None:
        if desired_zone.interface is None:
            desired_zone.interface = []
        if loopback.name not in desired_zone.interface:
            desired_zone.interface.append(loopback.name)
            desired_zone.update('interface')
    elif zone_name is not None:
        z = network.Zone(zone_name, interface=[loopback.name, ])
        con.add(z)
        z.create()


def set_virtual_router(con, loopback, vr_name, routers):
    desired_vr = None

    for vr in routers:
        if vr.name == vr_name:
            desired_vr = vr
        elif loopback.name in vr.interface:
            vr.interface.remove(loopback.name)
            vr.update('interface')

    if desired_vr is not None:
        if desired_vr.interface is None:
            desired_vr.interface = []
        if loopback.name not in desired_vr.interface:
            desired_vr.interface.append(loopback.name)
            desired_vr.update('interface')
    elif vr_name is not None:
        raise ValueError('Virtual router {0} does not exist'.format(vr_name))


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        if_name=dict(required=True),
        ip=dict(type='list'),
        ipv6_enabled=dict(type='bool'),
        management_profile=dict(),
        mtu=dict(type='int'),
        adjust_tcp_mss=dict(type='bool'),
        netflow_profile=dict(),
        comment=dict(),
        ipv4_mss_adjust=dict(type='int'),
        ipv6_mss_adjust=dict(type='int'),
        zone_name=dict(required=True),
        vr_name=dict(default='default'),
        vsys_dg=dict(default='vsys1'),
        commit=dict(type='bool', default=True),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    # Get the firewall / panorama auth.
    auth = (
        module.params['ip_address'],
        module.params['username'],
        module.params['password'],
        module.params['api_key'],
    )

    # Get the object params.
    spec = {
        'name': module.params['if_name'],
        'ip': module.params['ip'],
        'ipv6_enabled': module.params['ipv6_enabled'],
        'management_profile': module.params['management_profile'],
        'mtu': module.params['mtu'],
        'adjust_tcp_mss': module.params['adjust_tcp_mss'],
        'netflow_profile': module.params['netflow_profile'],
        'comment': module.params['comment'],
        'ipv4_mss_adjust': module.params['ipv4_mss_adjust'],
        'ipv6_mss_adjust': module.params['ipv6_mss_adjust'],
    }

    # Get other info.
    state = module.params['state']
    zone_name = module.params['zone_name']
    vr_name = module.params['vr_name']
    vsys_dg = module.params['vsys_dg']
    commit = module.params['commit']

    # Open the connection to the PANOS device.
    con = base.PanDevice.create_from_device(*auth)

    # Set vsys if firewall, device group if panorama.
    parent = con
    if hasattr(con, 'refresh_devices'):
        # Panorama
        # Normally we want to set the device group here, but there are no
        # interfaces on Panorama.  So if we're given a Panorama device, then
        # error out.
        '''
        groups = panorama.DeviceGroup.refreshall(con, add=False)
        for parent in groups:
            if parent.name == vsys_dg:
                con.add(parent)
                break
        else:
            module.fail_json(msg="'{0}' device group is not present".format(vsys_dg))
        '''
        module.fail_json(msg="loopback interfaces don't exist on Panorama")
    else:
        con.vsys = vsys_dg

    # Retrieve the current config.
    try:
        interfaces = network.LoopbackInterface.refreshall(con, add=False, name_only=True)
        zones = network.Zone.refreshall(con)
        routers = network.VirtualRouter.refreshall(con)
        vsys_list = device.Vsys.refreshall(con)

    except errors.PanDeviceError:
        e = get_exception()
        module.fail_json(msg=e.message)

    # Build the object based on the user spec.
    loopback = network.LoopbackInterface(**spec)
    con.add(loopback)

    if state == 'present':
        if loopback.name in [x.name for x in interfaces]:
            i = network.LoopbackInterface(loopback.name)
            con.add(i)
            try:
                i.refresh()
            except PanDeviceError as e:
                module.fail_json(msg='Failed "present" refresh: {0}'.format(e))
            if not i.equal(loopback, compare_children=False):
                loopback.extend(i.children)
                try:
                    loopback.apply()
                    changed = True
                except PanDeviceError as e:
                    module.fail_json(msg='Failed "present" apply: {0}'.format(e))
        else:
            try:
                loopback.create()
                changed = True
            except PanDeviceError as e:
                module.fail_json(msg='Failed "present" create: {0}'.format(e))
        try:
            changed |= set_zone(con, loopback, zone_name, zones)
            changed |= set_virtual_router(con, loopback, vr_name, routers)
        except PanDeviceError as e:
            module.fail_json(msg='Failed zone/vr assignment: {0}'.format(e))
    elif state == 'absent':
        try:
            changed |= set_zone(con, loopback, None, zones)
            changed |= set_virtual_router(con, loopback, None, routers)
        except PanDeviceError as e:
            module.fail_json(msg='Failed "absent" zone/vr cleanup: {0}'.format(e))
            changed = True
        if loopback.name in [x.name for x in interfaces]:
            try:
                loopback.delete()
                changed = True
            except PanDeviceError as e:
                module.fail_json(msg='Failed "absent" delete: {0}'.format(e))
    else:
        module.fail_json(msg="Unsupported state '{0}'".format(state))

    # Commit if we were asked to do so.
    if commit:
        try:
            con.commit(sync=True)
        except errors.PanDeviceError:
            e = get_exception()
            module.fail_json(msg='Performed {0} but commit failed: {1}'.format(state, e.message))

    # Done!
    module.exit_json(changed=True, msg='Done')


if __name__ == '__main__':
    main()
