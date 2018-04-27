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

from units.modules.utils import set_module_args
from . import panos_common_module
from .panos_module import TestPanOSModule


class TestPanOSCommonModule(TestPanOSModule):

    module = panos_common_module

    def test_panos_common_no_args(self):
        set_module_args({})
        result = self.execute_module(failed=True)
        assert result['msg'] == 'missing required arguments: ip_address'

    def test_panos_common_no_username_or_api_key(self):
        set_module_args({'ip_address': '1.1.1.1'})
        result = self.execute_module(failed=True)
        assert result['msg'] == 'one of the following is required: username, api_key'

    def test_panos_common_username_no_password(self):
        set_module_args({'ip_address': '1.1.1.1', 'username': 'admin'})
        result = self.execute_module(failed=True)
        assert result['msg'] == 'parameters are required together: username, password'

    def test_panos_common_username_and_api_key(self):
        set_module_args({'ip_address': '1.1.1.1', 'username': 'admin', 'api_key': 'foo'})
        result = self.execute_module(failed=True)
        assert result['msg'] == 'parameters are mutually exclusive: username, api_key'

    def test_panos_common_username_and_password(self):
        set_module_args({'ip_address': '1.1.1.1', 'username': 'admin', 'password': 'admin'})
        self.execute_module(changed=False)

    def test_panos_common_api_key(self):
        set_module_args({'ip_address': '1.1.1.1', 'api_key': 'foo'})
        self.execute_module(changed=False)
