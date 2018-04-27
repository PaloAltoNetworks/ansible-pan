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
    from library import panos_object
    from module_utils.network.panos import PanOSAnsibleModule
except ImportError:
    from ansible.modules.network.panos import panos_object
    from ansible.module_utils.network.panos import PanOSAnsibleModule

from ansible.compat.tests.mock import patch

from units.modules.utils import set_module_args
from .panos_module import TestPanOSModule


class TestPanOSObjectModule(TestPanOSModule):

    module = panos_object

    def test_panos_object_address_no_name(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'object_type': 'address'
        })
        result = self.execute_module(failed=True)
        assert result['msg'] == 'missing required arguments: name'

    def test_panos_object_address_no_address_value(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'object_type': 'address',
            'name': 'Foo'
        })
        result = self.execute_module(failed=True)
        assert result['msg'] == (
            "'object_type' is 'address', 'state' is 'present' but the following are missing: "
            "address_value"
        )

    def test_panos_object_address_create(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'object_type': 'address',
            'name': 'Foo',
            'address_value': '2.2.2.2'
        })

        with patch.object(PanOSAnsibleModule, 'create_or_update_object') as mock_create:
            mock_create.return_value = True
            self.execute_module(changed=True)
            mock_create.assert_called_once()

    def test_panos_object_address_delete(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'object_type': 'address',
            'name': 'Foo',
            'address_value': '2.2.2.2',
            'state': 'absent'
        })

        with patch.object(PanOSAnsibleModule, 'delete_object') as mock_delete:
            mock_delete.return_value = True
            self.execute_module(changed=True)
            mock_delete.assert_called_once()

    def test_panos_object_address_group_no_static_value(self):
        set_module_args({
            'ip_address': '1.1.1.1',
            'username': 'admin',
            'password': 'admin',
            'object_type': 'address-group',
            'address_group_type': 'static',
            'name': 'Foo',
            'state': 'present'
        })
        result = self.execute_module(failed=True)
        assert result['msg'] == (
            "'address_group_type' is 'static', 'object_type' is 'address-group', 'state' is "
            "'present' but the following are missing: static_value"
        )
