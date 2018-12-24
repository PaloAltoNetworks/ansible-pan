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
module: panos_mgtconfig
short_description: Module used to configure some of the device management.
description:
    - Configure management settings of device. Not all configuration options are configurable at this time.
author: "Luigi Mori (@jtschichold), Ivan Bojer (@ivanbojer), Patrik Malinen (@pmalinen), Francesco Vigo (@fvigo)"
version_added: "2.4"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Checkmode is not supported.
    - Panorama is supported
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
    dns_server_primary:
        description:
            - IP address of primary DNS server.
    dns_server_secondary:
        description:
            - IP address of secondary DNS server.
    panorama_primary:
        description:
            - IP address (or hostname) of primary Panorama server.
    panorama_secondary:
        description:
            - IP address (or hostname) of secondary Panorama server.
    ntp_server_primary:
        description:
            - IP address (or hostname) of primary NTP server.
    ntp_server_secondary:
        description:
            - IP address (or hostname) of secondary NTP server.
    timezone:
        description:
            - Device timezone.
    login_banner:
        description:
            - Login banner text.
    update_server:
        description:
            - IP or hostname of the update server.
    hostname:
        description:
            - The hostname of the device.
    domain:
        description:
            - The domain of the device
    devicegroup:
        description:
            - Device groups are used for the Panorama interaction with Firewall(s). The group must exists on Panorama.
    commit:
        description:
            - Commit configuration if changed.
        default: true

'''

EXAMPLES = '''
- name: set dns and panorama
  panos_mgtconfig:
    ip_address: "192.168.1.1"
    password: "admin"
    dns_server_primary: "1.1.1.1"
    dns_server_secondary: "1.1.1.2"
    panorama_primary: "1.1.1.3"
    panorama_secondary: "1.1.1.4"
    ntp_server_primary: "1.1.1.5"
    ntp_server_secondary: "1.1.1.6"
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
    from pan.xapi import PanXapiError
    import pandevice
    from pandevice import base
    from pandevice import panorama
    from pandevice.device import SystemSettings
    HAS_LIB = True
except ImportError:
    HAS_LIB = False


def get_devicegroup(device, devicegroup):
    dg_list = device.refresh_devices()
    for group in dg_list:
        if isinstance(group, pandevice.panorama.DeviceGroup):
            if group.name == devicegroup:
                return group
    return False


def set_ntp_server(system_settings, new_ntp_server, primary=True):
    ntp = None
    classType = None
    if primary:
        from pandevice.device import NTPServerPrimary
        classType = NTPServerPrimary
        ntp = NTPServerPrimary(address=new_ntp_server)
    else:
        from pandevice.device import NTPServerSecondary
        classType = NTPServerSecondary
        ntp = NTPServerSecondary(address=new_ntp_server)

    # find the duplicate
    nodes = system_settings.findall(classType)
    for n in nodes:
        a = getattr(n, 'address')
        if a and a == new_ntp_server:
            return False

    # continue with the change
    system_settings.removeall(classType)
    system_settings.add(ntp)

    return True


def main():
    argument_spec = dict(
        ip_address=dict(required=True),
        password=dict(required=True, no_log=True),
        username=dict(default='admin'),
        api_key=dict(no_log=True),
        dns_server_primary=dict(),
        dns_server_secondary=dict(),
        panorama_primary=dict(),
        panorama_secondary=dict(),
        ntp_server_primary=dict(),
        ntp_server_secondary=dict(),
        timezone=dict(),
        login_banner=dict(),
        update_server=dict(),
        hostname=dict(),
        domain=dict(),
        devicegroup=dict(),
        commit=dict(type='bool', default=True)
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False,
                           required_one_of=[['api_key', 'password']])
    if not HAS_LIB:
        module.fail_json(msg='Missing required libraries.')

    ip_address = module.params["ip_address"]
    password = module.params["password"]
    username = module.params['username']
    dns_server_primary = module.params['dns_server_primary']
    dns_server_secondary = module.params['dns_server_secondary']
    ntp_server_primary = module.params['ntp_server_primary']
    ntp_server_secondary = module.params['ntp_server_secondary']
    panorama_primary = module.params['panorama_primary']
    panorama_secondary = module.params['panorama_secondary']
    commit = module.params['commit']
    api_key = module.params['api_key']
    timezone = module.params['timezone']
    login_banner = module.params['login_banner']
    update_server = module.params['update_server']
    hostname = module.params['hostname']
    domain = module.params['domain']
    devicegroup = module.params['devicegroup']

    # Create the device with the appropriate pandevice type
    device = base.PanDevice.create_from_device(ip_address, username, password, api_key=api_key)

    # If Panorama, validate the devicegroup
    dev_group = None
    if devicegroup and isinstance(device, panorama.Panorama):
        dev_group = get_devicegroup(device, devicegroup)
        if dev_group:
            device.add(dev_group)
        else:
            module.fail_json(msg='\'%s\' device group not found in Panorama. Is the name correct?' % devicegroup)

    changed = False
    try:
        ss = SystemSettings.refreshall(device)[0]

        print('changed = {}'.format(changed))
        if dns_server_primary is not None and ss.dns_primary != dns_server_primary:
            ss.dns_primary = dns_server_primary
            changed = True
        print('changed = {}'.format(changed))
        if dns_server_secondary is not None and ss.dns_secondary != dns_server_secondary:
            ss.dns_secondary = dns_server_secondary
            changed = True
        print('changed = {}'.format(changed))
        if panorama_primary is not None and ss.panorama != panorama_primary:
            ss.panorama = panorama_primary
            changed = True
        print('changed = {}'.format(changed))
        if panorama_secondary is not None and ss.panorama2 != panorama_secondary:
            ss.panorama2 = panorama_secondary
            changed = True
        print('changed = {}'.format(changed))
        if ntp_server_primary is not None:
            changed |= set_ntp_server(ss, ntp_server_primary, primary=True)
        print('changed = {}'.format(changed))
        if ntp_server_secondary is not None:
            changed |= set_ntp_server(ss, ntp_server_secondary, primary=False)
        print('changed = {}'.format(changed))
        if login_banner and ss.login_banner != login_banner:
            ss.login_banner = login_banner
            changed = True
        if timezone and ss.timezone != timezone:
            ss.timezone = timezone
            changed = True
        if update_server and ss.update_server != update_server:
            ss.update_server = update_server
            changed = True
        if hostname and ss.hostname != hostname:
            ss.hostname = hostname
            changed = True
        if domain and ss.domain != domain:
            ss.domain = domain
            changed = True

        print('changed = {}'.format(changed))
        if changed:
            ss.apply()
        if commit:
            device.commit(sync=True)
    except PanXapiError:
        exc = get_exception()
        module.fail_json(msg=exc.message)

    module.exit_json(changed=changed, msg="okey dokey")


if __name__ == '__main__':
    main()
