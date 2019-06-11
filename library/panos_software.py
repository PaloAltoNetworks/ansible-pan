#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: panos_software
short_description: Install specific release of PAN-OS.
description:
    - Install specific release of PAN-OS.
author: "Michael Richardson (@mrichardson03)"
version_added: "2.6"
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
options:
    version:
        description:
            - Desired PAN-OS release for target device.
        required: true
    restart:
        description:
            - Restart device after installing desired version.  Use in conjunction with
              panos_check to determine when firewall is ready again.
        default: false
'''

EXAMPLES = '''
- name: Install PAN-OS 8.1.6 and restart
  panos_software:
    provider: '{{ provider }}'
    version: '8.1.6'
    restart: true
'''

RETURN = '''
version:
    description: After performing the software install, returns the version installed on the
        device.
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection

try:
    from pandevice import PanOSVersion
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        with_classic_provider_spec=True,
        argument_spec=dict(
            version=dict(type='str', required=True),
            restart=dict(type='bool', default=False)
        )
    )

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        supports_check_mode=True
    )

    # Verify libs are present, get parent object.
    device = helper.get_pandevice_parent(module)

    # Module params.
    version = module.params['version']
    restart = module.params['restart']

    changed = False

    try:
        device.software.check()

        if PanOSVersion(version) != PanOSVersion(device.version):

            if not module.check_mode:
                device.software.download_install(version, sync=True)

                if restart:
                    device.restart()

            changed = True

    except PanDeviceError as e:
        module.fail_json(msg=e.message)

    module.exit_json(changed=changed, version=version)


if __name__ == '__main__':
    main()
