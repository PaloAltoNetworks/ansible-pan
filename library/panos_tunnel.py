#!/usr/bin/env python

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

DOCUMENTATION = '''
---
module: panos_tunnel
short_description: configure tunnel interfaces
description:
    - Configure tunnel interfaces on PanOS
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Geraint Jones (@nexus_moneky_nz)"
author: "Joshua Colson (@freakinhippie)"
version_added: "2.9"
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
            - Create or remove static route.
        choices: ['present', 'absent']
        default: 'present'
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
            - Interface management profile name; it must already exist.
    mtu:
        description:
            - MTU for tunnel interface.
    netflow_profile:
        description:
            - Netflow profile for tunnel interface.
    comment:
        description:
            - Interface comment.
    zone_name:
        description:
            - Name of the zone for the interface. If the zone does not exist it is created but
            - if the zone exists and it is not of the correct mode the operation will fail.
    vr_name:
        description:
            - Name of the virtual router; it must already exist.
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
# Create tunnel.1
- name: create tunnel.1
  panos_tunnel:
    ip_address: "192.168.1.1"
    username: "ansible"
    password: "secret"
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]

# Update tunnel comment.
- name: update tunnel.1 comment
  panos_tunnel:
    ip_address: "192.168.1.1"
    username: "ansible"
    password: "secret"
    if_name: "tunnel.1"
    ip: ["10.1.1.1/32"]
    comment: "tunnel interface"
    operation: update

'''

RETURN = '''
# Default return values
'''

ANSIBLE_METADATA = {'metadata_version': '1.0',
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


def set_zone(con, iface, zone_name, zones):
    desired_zone = None

    # Remove the interface from the zone.
    for z in zones:
        if z.name == zone_name:
            desired_zone = z
        elif iface.name in z.interface:
            z.interface.remove(iface.name)
            z.update('interface')

    if desired_zone is not None:
        if desired_zone.interface is None:
            desired_zone.interface = []
        if iface.name not in desired_zone.interface:
            desired_zone.interface.append(iface.name)
            desired_zone.update('interface')
    elif zone_name is not None:
        z = network.Zone(zone_name, interface=[iface.name, ])
        con.add(z)
        z.create()


def set_virtual_router(con, eth, vr_name, routers):
    changed = False
    desired_vr = None

    for vr in routers:
        if vr.name == vr_name:
            desired_vr = vr
        elif vr.interface is not None and eth.name in vr.interface:
            vr.interface.remove(eth.name)
            vr.update('interface')
            changed = True

    if desired_vr is not None:
        if desired_vr.interface is None:
            desired_vr.interface = []
        if eth.name not in desired_vr.interface:
            desired_vr.interface.append(eth.name)
            desired_vr.update('interface')
            changed = True
    elif vr_name is not None:
        raise ValueError('Virtual router {0} does not exist in set {1}'.format(vr_name, routers))

    return changed


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        state=dict(default='present', choices=['present', 'absent']),
        if_name=dict(required=True),
        ip=dict(type='list'),
        ipv6_enabled=dict(),
        management_profile=dict(),
        mtu=dict(),
        netflow_profile=dict(),
        comment=dict(),
        zone_name=dict(default=None),
        vr_name=dict(default=None),
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
        'netflow_profile': module.params['netflow_profile'],
        'comment': module.params['comment'],
    }

    # Get other info.
    # operation = module.params['operation']
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
        module.fail_json(msg="tunnel interfaces don't exist on Panorama")

    # Retrieve the current config.
    try:
        interfaces = network.TunnelInterface.refreshall(con, add=False, name_only=True)
        zones = network.Zone.refreshall(con)
        routers = network.VirtualRouter.refreshall(con)
        vsys_list = device.Vsys.refreshall(con)

    except errors.PanDeviceError:
        e = get_exception()
        module.fail_json(msg=e.message)

    # Build the object based on the user spec.
    iface = network.TunnelInterface(**spec)
    con.add(iface)

    if state == 'present':
        if iface.name not in [x.name for x in interfaces]:
            # Create the interface.
            try:
                iface.create()
                set_zone(con, iface, zone_name, zones)
                set_virtual_router(con, iface, vr_name, routers)
            except (errors.PanDeviceError, ValueError):
                e = get_exception()
                module.fail_json(msg=e.message)
        else:
            # Update the interface.
            try:
                con.organize_into_vsys()
            except errors.PanDeviceError:
                e = get_exception()
                module.fail_json(msg=e.message)
            if iface.vsys != vsys_dg:
                try:
                    iface.delete_import()
                except errors.PanDeviceError:
                    e = get_exception()
                    module.fail_json(msg=e.message)

            # Move the tunnel object to the correct vsys.
            for vsys in vsys_list:
                if vsys.name == vsys_dg:
                    vsys.add(iface)
                    break
            else:
                module.fail_json(msg='Vsys {0} does not exist'.format(vsys))

            # Update the interface.
            try:
                iface.apply()
                set_zone(con, iface, zone_name, zones)
                set_virtual_router(con, iface, vr_name, routers)

            except (errors.PanDeviceError, ValueError):
                e = get_exception()
                module.fail_json(msg=e.message)
    elif state == 'absent':
        if iface.name in [x.name for x in interfaces]:
            try:
                con.organize_into_vsys()
                set_zone(con, iface, None, zones)
                set_virtual_router(con, iface, None, routers)
                iface.delete()
            except (errors.PanDeviceError, ValueError):
                e = get_exception()
                module.fail_json(msg=e.message)

    if commit:
        try:
            con.commit(sync=True)
        except errors.PanDeviceError:
            e = get_exception()
            module.fail_json(msg='Performed {0} but commit failed: {1}'.format(state, e.message))

    # Done!
    module.exit_json(changed=True, msg='okey dokey')


if __name__ == '__main__':
    main()
