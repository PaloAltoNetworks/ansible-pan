#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_http_profile
short_description: Manage http server profiles.
description:
    - Manages http server profiles.
author: "Garfield Lee Freeman (@shinmog)"
version_added: "2.8"
requirements:
    - pan-python
    - pandevice >= 0.11.1
    - PAN-OS >= 8.0
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - panos.transitional_provider
    - panos.vsys_shared
    - panos.device_group
options:
    name:
        description:
            - Name of the profile.
        required: true
    tag_registration:
        description:
            - The server should have user-ID agent running in order for tag
              registration to work.
        type: bool
    config_name:
        description:
            - Name for custom config format.
    config_uri_format:
        description:
            - URI format for custom config format.
    config_payload:
        description:
            - Payload for custom config format.
    system_name:
        description:
            - Name for custom config format.
    system_uri_format:
        description:
            - URI format for custom config format.
    system_payload:
        description:
            - Payload for custom config format.
    threat_name:
        description:
            - Name for custom config format.
    threat_uri_format:
        description:
            - URI format for custom config format.
    threat_payload:
        description:
            - Payload for custom config format.
    traffic_name:
        description:
            - Name for custom config format.
    traffic_uri_format:
        description:
            - URI format for custom config format.
    traffic_payload:
        description:
            - Payload for custom config format.
    hip_match_name:
        description:
            - Name for custom config format.
    hip_match_uri_format:
        description:
            - URI format for custom config format.
    hip_match_payload:
        description:
            - Payload for custom config format.
    url_name:
        description:
            - Name for custom config format.
    url_uri_format:
        description:
            - URI format for custom config format.
    url_payload:
        description:
            - Payload for custom config format.
    data_name:
        description:
            - Name for custom config format.
    data_uri_format:
        description:
            - URI format for custom config format.
    data_payload:
        description:
            - Payload for custom config format.
    wildfire_name:
        description:
            - Name for custom config format.
    wildfire_uri_format:
        description:
            - URI format for custom config format.
    wildfire_payload:
        description:
            - Payload for custom config format.
    tunnel_name:
        description:
            - Name for custom config format.
    tunnel_uri_format:
        description:
            - URI format for custom config format.
    tunnel_payload:
        description:
            - Payload for custom config format.
    user_id_name:
        description:
            - Name for custom config format.
    user_id_uri_format:
        description:
            - URI format for custom config format.
    user_id_payload:
        description:
            - Payload for custom config format.
    gtp_name:
        description:
            - Name for custom config format.
    gtp_uri_format:
        description:
            - URI format for custom config format.
    gtp_payload:
        description:
            - Payload for custom config format.
    auth_name:
        description:
            - Name for custom config format.
    auth_uri_format:
        description:
            - URI format for custom config format.
    auth_payload:
        description:
            - Payload for custom config format.
    sctp_name:
        description:
            - PAN-OS 8.1+.
            - Name for custom config format.
    sctp_uri_format:
        description:
            - PAN-OS 8.1+.
            - URI format for custom config format.
    sctp_payload:
        description:
            - PAN-OS 8.1+.
            - Payload for custom config format.
    iptag_name:
        description:
            - PAN-OS 9.0+.
            - Name for custom config format.
    iptag_uri_format:
        description:
            - PAN-OS 9.0+.
            - URI format for custom config format.
    iptag_payload:
        description:
            - PAN-OS 9.0+.
            - Payload for custom config format.
'''

EXAMPLES = '''
# Create a profile
- name: Create http profile
  panos_http_profile:
    provider: '{{ provider }}'
    name: 'my-profile'
    tag_registration: true
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.panos.panos import get_connection


try:
    from pandevice.device import HttpServerProfile
    from pandevice.errors import PanDeviceError
except ImportError:
    pass


def main():
    helper = get_connection(
        vsys_shared=True,
        device_group=True,
        with_state=True,
        with_classic_provider_spec=True,
        min_pandevice_version=(0, 11, 1),
        min_panos_version=(8, 0, 0),
        argument_spec=dict(
            name=dict(required=True),
            tag_registration=dict(type='bool'),
            config_name=dict(),
            config_uri_format=dict(),
            config_payload=dict(),
            system_name=dict(),
            system_uri_format=dict(),
            system_payload=dict(),
            threat_name=dict(),
            threat_uri_format=dict(),
            threat_payload=dict(),
            traffic_name=dict(),
            traffic_uri_format=dict(),
            traffic_payload=dict(),
            hip_match_name=dict(),
            hip_match_uri_format=dict(),
            hip_match_payload=dict(),
            url_name=dict(),
            url_uri_format=dict(),
            url_payload=dict(),
            data_name=dict(),
            data_uri_format=dict(),
            data_payload=dict(),
            wildfire_name=dict(),
            wildfire_uri_format=dict(),
            wildfire_payload=dict(),
            tunnel_name=dict(),
            tunnel_uri_format=dict(),
            tunnel_payload=dict(),
            user_id_name=dict(),
            user_id_uri_format=dict(),
            user_id_payload=dict(),
            gtp_name=dict(),
            gtp_uri_format=dict(),
            gtp_payload=dict(),
            auth_name=dict(),
            auth_uri_format=dict(),
            auth_payload=dict(),
            sctp_name=dict(),
            sctp_uri_format=dict(),
            sctp_payload=dict(),
            iptag_name=dict(),
            iptag_uri_format=dict(),
            iptag_payload=dict(),
        ),
    )
    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        supports_check_mode=True,
        required_one_of=helper.required_one_of,
    )

    # Verify imports, build pandevice object tree.
    parent = helper.get_pandevice_parent(module)

    try:
        listing = HttpServerProfile.refreshall(parent)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    spec = {
        'name': module.params['name'],
        'tag_registration': module.params['tag_registration'],
        'config_name': module.params['config_name'],
        'config_uri_format': module.params['config_uri_format'],
        'config_payload': module.params['config_payload'],
        'system_name': module.params['system_name'],
        'system_uri_format': module.params['system_uri_format'],
        'system_payload': module.params['system_payload'],
        'threat_name': module.params['threat_name'],
        'threat_uri_format': module.params['threat_uri_format'],
        'threat_payload': module.params['threat_payload'],
        'traffic_name': module.params['traffic_name'],
        'traffic_uri_format': module.params['traffic_uri_format'],
        'traffic_payload': module.params['traffic_payload'],
        'hip_match_name': module.params['hip_match_name'],
        'hip_match_uri_format': module.params['hip_match_uri_format'],
        'hip_match_payload': module.params['hip_match_payload'],
        'url_name': module.params['url_name'],
        'url_uri_format': module.params['url_uri_format'],
        'url_payload': module.params['url_payload'],
        'data_name': module.params['data_name'],
        'data_uri_format': module.params['data_uri_format'],
        'data_payload': module.params['data_payload'],
        'wildfire_name': module.params['wildfire_name'],
        'wildfire_uri_format': module.params['wildfire_uri_format'],
        'wildfire_payload': module.params['wildfire_payload'],
        'tunnel_name': module.params['tunnel_name'],
        'tunnel_uri_format': module.params['tunnel_uri_format'],
        'tunnel_payload': module.params['tunnel_payload'],
        'user_id_name': module.params['user_id_name'],
        'user_id_uri_format': module.params['user_id_uri_format'],
        'user_id_payload': module.params['user_id_payload'],
        'gtp_name': module.params['gtp_name'],
        'gtp_uri_format': module.params['gtp_uri_format'],
        'gtp_payload': module.params['gtp_payload'],
        'auth_name': module.params['auth_name'],
        'auth_uri_format': module.params['auth_uri_format'],
        'auth_payload': module.params['auth_payload'],
        'sctp_name': module.params['sctp_name'],
        'sctp_uri_format': module.params['sctp_uri_format'],
        'sctp_payload': module.params['sctp_payload'],
        'iptag_name': module.params['iptag_name'],
        'iptag_uri_format': module.params['iptag_uri_format'],
        'iptag_payload': module.params['iptag_payload'],
    }
    obj = HttpServerProfile(**spec)
    parent.add(obj)

    changed = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, msg='Done')


if __name__ == '__main__':
    main()
