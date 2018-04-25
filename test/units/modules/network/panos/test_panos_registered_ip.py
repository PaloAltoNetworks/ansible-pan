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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from library import panos_registered_ip
    from module_utils.network.panos import PanOSAnsibleModule
except ImportError:
    from ansible.modules.network.panos import panos_registered_ip
    from ansible.module_utils.network.panos import PanOSAnsibleModule

from ansible.compat.tests.mock import patch

from units.modules.utils import set_module_args
from .panos_module import TestPanOSModule


class TestPanOSRegisteredIpModule(TestPanOSModule):

    module = panos_registered_ip

    def test_panos_registered_ip_no_registered_ip(self):
        set_module_args({
            'ip_address': '1.1.1.1', 'username': 'admin', 'password': 'admin', 'tag': 'Foo'
        })
        result = self.execute_module(failed=True)
        assert result['msg'] == 'missing required arguments: registered_ip'

    def test_panos_registered_ip_no_tag(self):
        set_module_args({
            'ip_address': '1.1.1.1', 'username': 'admin', 'password': 'admin',
            'registered_ip': '2.2.2.2'
        })
        result = self.execute_module(failed=True)
        assert result['msg'] == 'missing required arguments: tag'

    def test_panos_registered_ip_test_register(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'registered_ip': '2.2.2.2',
            'tag': 'Foo'
        })

        with patch.object(PanOSAnsibleModule, 'device') as mock_device:
            mock_device.userid.get_registered_ip.side_effect = [{}, {'2.2.2.2': ['Foo']}]
            result = self.execute_module(changed=True)
            mock_device.userid.register.assert_called_once()

        assert result['results'] == {'2.2.2.2': ['Foo']}

    def test_panos_registered_ip_test_register_idempotent(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'registered_ip': '2.2.2.2',
            'tag': 'Foo'
        })

        with patch.object(PanOSAnsibleModule, 'device') as mock_device:
            mock_device.userid.get_registered_ip.return_value = {'2.2.2.2': ['Foo']}
            result = self.execute_module(changed=False)
            mock_device.userid.register.assert_not_called()

        assert result['results'] == {'2.2.2.2': ['Foo']}

    def test_panos_registered_ip_test_unregister(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'registered_ip': '2.2.2.2',
            'tag': 'Foo',
            'state': 'absent'
        })

        with patch.object(PanOSAnsibleModule, 'device') as mock_device:
            mock_device.userid.get_registered_ip.side_effect = [{'2.2.2.2': ['Foo']}, {}]
            result = self.execute_module(changed=True)
            mock_device.userid.unregister.assert_called_once()

        assert result['results'] == {}

    def test_panos_registered_ip_test_unregister_idempotent(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'registered_ip': '2.2.2.2',
            'tag': 'Foo',
            'state': 'absent'
        })

        with patch.object(PanOSAnsibleModule, 'device') as mock_device:
            mock_device.userid.get_registered_ip.side_effect = [{}, {}]
            result = self.execute_module(changed=False)
            mock_device.userid.unregister.assert_not_called()

        assert result['results'] == {}
