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

try:
    from pandevice import base
    from pandevice import firewall
    from pandevice import panorama
    from pandevice import policies

    from pandevice.errors import PanDeviceError

    HAS_PANOS_LIB = True
except ImportError:
    HAS_PANOS_LIB = False

from ansible.module_utils.basic import AnsibleModule

PANOS_COMMON_ARGUMENT_SPEC = {
    'ip_address': dict(type='str', required=True),
    'username': dict(type='str'),
    'password': dict(type='str', no_log=True),
    'api_key': dict(type='str', no_log=True)
}

PANOS_REQUIRED_ONE_OF_ARGS = [
    ['username', 'api_key']
]

PANOS_REQUIRED_TOGETHER_ARGS = [
    ['username', 'password']
]

PANOS_MUTUALLY_EXCLUSIVE_ARGS = [
    ['username', 'api_key']
]


class PanOSAnsibleModule(AnsibleModule):

    def __init__(
        self, argument_spec=None, required_one_of=None, required_together=None,
        required_if=None, mutually_exclusive=None, **kwargs
    ):

        # Append default values for argument specs and argument requirements before we pass them
        # to the superclass initializer.
        self.argument_spec = {}
        self.argument_spec.update(PANOS_COMMON_ARGUMENT_SPEC)
        if argument_spec:
            self.argument_spec.update(argument_spec)

        self.required_one_of = []
        self.required_one_of += PANOS_REQUIRED_ONE_OF_ARGS
        if required_one_of:
            self.required_one_of += required_one_of

        self.required_together = []
        self.required_together += PANOS_REQUIRED_TOGETHER_ARGS
        if required_together:
            self.required_together += required_together

        self.required_if = []
        if required_if:
            self.required_if += required_if

        self.mutually_exclusive = []
        self.mutually_exclusive += PANOS_MUTUALLY_EXCLUSIVE_ARGS
        if mutually_exclusive:
            self.mutually_exclusive += mutually_exclusive

        super(PanOSAnsibleModule, self).__init__(
            argument_spec=self.argument_spec, required_one_of=self.required_one_of,
            required_together=self.required_together, required_if=self.required_if,
            mutually_exclusive=self.mutually_exclusive, **kwargs
        )

        # Check to see if we were able to import required libraries.
        if not HAS_PANOS_LIB:
            self.fail_json(msg='pan-python and pandevice are required for this module.')

        self._device = None
        self._device_group = None

        self._rulebase = None
        self._rulebase_type = policies.SecurityRule

    @property
    def device(self):
        """
        Returns PanDevice object used by the module.
        """
        if self._device:
            return self._device
        else:
            try:
                self._device = base.PanDevice.create_from_device(
                    self.params['ip_address'], self.params['username'], self.params['password'],
                    api_key=self.params['api_key']
                )

            except PanDeviceError as e:
                self.fail_json(msg=e.message)

            return self._device

    @property
    def device_group(self):
        """
        Returns the current device group (if any) that we are working with.
        """
        return self._device_group

    @device_group.setter
    def device_group(self, dg_name):
        """
        Sets the device group to work with, and also validates that it exists.
        :param dg_name: Name of a Panorama device group.
        """
        if isinstance(self.device, panorama.Panorama):
            dgs = self.device.refresh_devices()

            for dg in dgs:
                if isinstance(dg, panorama.DeviceGroup):
                    if dg.name == dg_name:
                        self._device_group = dg

        if not self._device_group:
            self.fail_json(msg='Could not find {} device group.'.format(dg_name))

    @property
    def rulebase(self):
        """
        Returns the current rule base that we are working with.
        """
        if self._rulebase:
            return self._rulebase
        else:
            if isinstance(self.device, firewall.Firewall):
                self._rulebase = policies.Rulebase()
                self.device.add(self._rulebase)
            elif isinstance(self.device, panorama.Panorama):
                self._rulebase = policies.PreRulebase()
                if self.device_group:
                    self.device_group.add(self._rulebase)
                else:
                    self.device.add(self._rulebase)

            policies.SecurityRule.refreshall(self._rulebase)
            policies.NatRule.refreshall(self._rulebase)

            return self._rulebase

    @rulebase.setter
    def rulebase(self, panorama_rulebase=policies.PreRulebase):
        """
        Sets the current rule base that we are working with.  Used to switch between
        Panorama pre and post rules.
        :param panorama_rulebase: :class:`pandevice.policies.PreRulebase` or
                                  :class:`pandevice.policies.PostRulebase`
        """
        if isinstance(self.device, panorama.Panorama):
            self._rulebase = panorama_rulebase()
            self.device_group.add(self._rulebase)

            policies.SecurityRule.refreshall(self._rulebase)
            policies.NatRule.refreshall(self._rulebase)

    def create_or_update_object(self, obj_name, obj_type, new_obj):
        """
        Creates a new object, or updates an existing object.
        :param obj_name: Name of object to update, or create if it doesn't exist.
        :param obj_type: Type of object to create.
        :param new_obj: Object holding the desired attributes.  It will be created if it does
                        not exist, or attributes will be copied from this object to the existing
                        one.
        :returns: Boolean if an object was created or modified.
        """
        existing_obj = self.find_object(obj_name, obj_type)

        if not existing_obj:
            self._add_object(new_obj)
            new_obj.create()
            return True
        elif not existing_obj.equal(new_obj):
            for param in new_obj._params:
                setattr(existing_obj, param.name, getattr(new_obj, param.name))
            existing_obj.apply()
            return True

        return False

    def find_object(self, obj_name, obj_type):
        """
        Finds an object.
        :param obj_name: Name of object to find.
        :param obj_type: Type of object to find.
        :returns: Object, or None if the object is not found.
        """
        obj_type.refreshall(self.device)

        if isinstance(self.device, firewall.Firewall):
            return self.device.find(obj_name, obj_type)
        elif isinstance(self.device, panorama.Panorama):
            if self.device_group:
                self.device.add(self.device_group)
                obj_type.refreshall(self.device_group)
                return self.device_group.find(obj_name, obj_type)
            else:
                return self.device.find(obj_name, obj_type)

        return None

    def delete_object(self, obj_name, obj_type):
        """
        Deletes an object, if it exists.
        :param obj_name: Name of object to delete.
        :param obj_type: Type of object to delete.
        :returns: Boolean if an object was deleted.
        """
        existing_obj = self.find_object(obj_name, obj_type)

        if existing_obj:
            existing_obj.delete()
            return True

        return False

    def create_or_update_rule(
        self, rule_name, rule_type, new_rule, location=None, existing_rule_name=None
    ):
        """
        Creates a new rule, or updates an existing rule.
        :param rule_name: Name of rule to update, or create if it doesn't exist.
        :param rule_type: Type of rule to create.
        :param new_rule: Object holding the desired attributes.  It will be created if it does
                        not exist, or attributes will be copied from this object to the existing
                        one.
        :returns: Boolean if a rule was created or modified.
        """
        changed = False
        existing_obj = self.rulebase.find(rule_name, rule_type)

        if not existing_obj:
            self.rulebase.add(new_rule)
            new_rule.create()
            self.rulebase.apply()
            existing_obj = new_rule
            changed = True

        elif not existing_obj.equal(new_rule):
            for param in new_rule._params:
                setattr(existing_obj, param.name, getattr(new_rule, param.name))
            existing_obj.apply()
            self.rulebase.apply()
            changed = True

        if location:
            rule_current_loc = self._get_rule_index(self.rulebase, existing_obj.name)

            if location == 'top':
                if rule_current_loc != 0:
                    self.device.xapi.move(existing_obj.xpath(), 'top')
                    changed = True

            elif location == 'bottom':
                if rule_current_loc != (len(self.rulebase.children) - 1):
                    self.device.xapi.move(existing_obj.xpath(), 'bottom')
                    changed = True

            elif (location == 'before') or (location == 'after'):
                existing_rule_loc = self.get_rule_index(self.rulebase, existing_rule_name)

                if existing_rule_loc < 0:
                    self.fail_json(msg='Existing rule \'%s\' does not exist.' % existing_rule_name)

                if location == 'before':
                    if rule_current_loc != (existing_rule_loc - 1):
                        self.device.xapi.move(existing_obj.xpath(), 'before', existing_rule_name)
                        changed = True

                if location == 'after':
                    if rule_current_loc != (existing_rule_loc + 1):
                        self.device.xapi.move(existing_obj.xpath(), 'after', existing_rule_name)
                        changed = True

        return changed

    def delete_rule(self, rule_name, rule_type):
        """
        Deletes an rule, if it exists.
        :param rule_name: Name of rule to delete.
        :param rule_type: Type of rule to delete.
        :returns: Boolean if an rule was deleted.
        """
        existing_rule = self.rulebase.find(rule_name, rule_type)

        if existing_rule:
            existing_rule.delete()
            self.rulebase.apply()
            return True
        else:
            return False

    def find_rule(self, rule_name, rule_type):
        """
        Finds a rule in the current rulebase.
        :param rule_name: Name of rule to find.
        :param rule_type: Type of rule to find.
        :returns: Rule, or None if the rule is not found.
        """
        return self.rulebase.find(rule_name, rule_type)

    def disable_rule(self, rule_name, rule_type):
        """
        Disables a rule, if it exists.
        :param rule_name: Name of rule to delete.
        :param rule_type: Type of rule to delete.
        :returns: Boolean if an rule was deleted.
        """
        existing_rule = self.rulebase.find(rule_name, rule_type)

        if existing_rule:
            existing_rule.disabled = True
            existing_rule.apply()
            return True
        else:
            return False

    def _add_object(self, obj):
        if isinstance(self.device, firewall.Firewall):
            self.device.add(obj)
        elif isinstance(self.device, panorama.Panorama):
            if self.device_group:
                return self.device_group.add(obj)
            else:
                return self.device.add(obj)

    def _get_rule_index(self, rulebase, rule_name):
        if rulebase:
            for num, child in enumerate(rulebase.children):
                if rule_name == child.name:
                    return num
        return -1
