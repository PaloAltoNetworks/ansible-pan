#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type


HAS_PANDEVICE = True
try:
    from pandevice.base import PanDevice
    from pandevice.panorama import DeviceGroup, Template, TemplateStack
    from pandevice.policies import PreRulebase, PostRulebase, Rulebase
    from pandevice.device import Vsys
    from pandevice.errors import PanDeviceError
except ImportError:
    HAS_PANDEVICE = False


class ConnectionHelper(object):
    def __init__(self, panorama_error, firewall_error):
        """Performs connection initialization and determines params."""
        # Params for AnsibleModule.
        self.argument_spec = {}
        self.required_one_of = []

        # Params for pandevice tree construction.
        self.vsys = None
        self.device_group = None
        self.vsys_dg = None
        self.rulebase = None
        self.template = None
        self.template_stack = None
        self.vsys_importable = None
        self.panorama_error = panorama_error
        self.firewall_error = firewall_error

        # The PAN-OS device.
        self.device = None

    def get_pandevice_parent(self, module):
        """Builds the pandevice object tree, returning the parent object.

        If pandevice is not installed, then module.fail_json() will be
        invoked.

        Arguments:
            * module(AnsibleModule): the ansible module.

        Returns:
            * The parent pandevice object based on the spec given to
              get_connection().
        """
        # Sanity check.
        if not HAS_PANDEVICE:
            module.fail_json(msg='Missing required library "pandevice".')

        d, host_arg = None, None
        if module.params['provider'] and module.params['provider']['host']:
            d = module.params['provider']
            host_arg = 'host'
        elif module.params['ip_address'] is not None:
            d = module.params
            host_arg = 'ip_address'
        else:
            module.fail_json(msg='New or classic provider params are required.')

        # Create the connection object.
        try:
            self.device = PanDevice.create_from_device(
                d[host_arg], d['username'], d['password'], d['api_key'])
        except PanDeviceError as e:
            module.fail_json(msg='Failed connection: {0}'.format(e))

        parent = self.device
        not_found = '{0} "{1}" is not present.'
        if hasattr(self.device, 'refresh_devices'):
            # Panorama connection.
            # Error if Panorama is not supported.
            if self.panorama_error is not None:
                module.fail_json(msg=self.panorama_error)

            # Spec: template stack.
            if self.template_stack is not None:
                name = module.params[self.template_stack]
                stacks = TemplateStack.refreshall(parent)
                for ts in stacks:
                    if ts.name == name:
                        parent = ts
                        break
                else:
                    module.fail_json(msg=not_found.format(
                        'Template stack', name,
                    ))

            # Spec: template.
            if self.template is not None:
                name = module.params[self.template]
                templates = Template.refreshall(parent)
                for t in templates:
                    if t.name == name:
                        parent = t
                        break
                else:
                    module.fail_json(msg=not_found.format(
                        'Template', name,
                    ))

            # Spec: vsys importable.
            if self.vsys_importable is not None:
                name = module.params[self.vsys_importable]
                if name is not None:
                    vo = Vsys(name)
                    parent.add(vo)
                    parent = vo

            # Spec: vsys_dg or device_group.
            dg_name = self.vsys_dg or self.device_group
            if dg_name is not None:
                name = module.params[dg_name]
                if name not in (None, 'shared'):
                    groups = DeviceGroup.refreshall(parent)
                    for dg in groups:
                        if dg.name == name:
                            parent = dg
                            break
                    else:
                        module.fail_json(msg=not_found.format(
                            'Device group', name,
                        ))

            # Spec: rulebase.
            if self.rulebase is not None:
                if module.params[self.rulebase] in (None, 'pre-rulebase'):
                    rb = PreRulebase()
                    parent.add(rb)
                    parent = rb
                elif module.params[self.rulebase] == 'post-rulebase':
                    rb = PostRulebase()
                    parent.add(rb)
                    parent = rb
                else:
                    module.fail_json(msg=not_found.format(
                        'Rulebase', module.params[self.rulebase]))
        else:
            # Firewall connection.
            # Error if firewalls are not supported.
            if self.firewall_error is not None:
                module.fail_json(msg=self.firewall_error)

            # Spec: vsys or vsys_dg or vsys_importable.
            vsys_name = self.vsys_dg or self.vsys or self.vsys_importable
            if vsys_name is not None:
                self.con.vsys = module.params[vsys_name]

            # Spec: rulebase.
            if self.rulebase is not None:
                rb = Rulebase()
                parent.add(rb)
                parent = rb

        # Done.
        return parent


def get_connection(vsys=None, device_group=None,
                   vsys_dg=None, vsys_importable=None,
                   rulebase=None, template=None, template_stack=None,
                   classic_provider_spec=False,
                   panorama_error=None, firewall_error=None):
    """Returns a helper object that handles pandevice object tree init.

    All arguments to this function (except panorama_error, firewall_error,
    and classic_provider_spec) can be any of the following types:

        * None - do not include this in the spec
        * True - use the default param name
        * string - use this string for the param name

    Arguments:
        vsys: Firewall only - The vsys.
        device_group: Panorama only - The device group.
        vsys_dg: The param name if vsys and device_group are a shared param.
        vsys_importable: Either this or `vsys` should be specified.  For:
            - Interfaces
            - VLANs
            - Virtual Wires
            - Virtual Routers
        rulebase: This is a policy of some sort.
        template: Panorama - The template name.
        template_stack: Panorama - The template stack name.
        classic_provider_spec(bool): Include the ip_address, username,
            password, api_key params in the base spec, and make the
            "provider" param optional.
        panorama_error(str): The error message if the device is Panorama.
        firewall_error(str): The error message if the device is a firewall.

    Returns:
        ConnectionHelper
    """
    helper = ConnectionHelper(panorama_error, firewall_error)
    req = []
    spec = {
        'provider': {
            'required': True,
            'type': 'dict',
            'required_one_of': [['password', 'api_key'], ],
            'options': {
                'host': {'required': True},
                'username': {'default': 'admin'},
                'password': {'no_log': True},
                'api_key': {'no_log': True},
            },
        },
    }

    if classic_provider_spec:
        spec['provider']['required'] = False
        spec['provider']['options']['host']['required'] = False
        del(spec['provider']['required_one_of'])
        spec.update({
            'ip_address': {'required': False},
            'username': {'default': 'admin'},
            'password': {'no_log': True},
            'api_key': {'no_log': True},
        })
        req.extend([
            ['provider', 'ip_address'],
            ['provider', 'password', 'api_key'],
        ])

    if vsys_dg is not None:
        if isinstance(vsys_dg, bool):
            param = 'vsys_dg'
        else:
            param = vsys_dg
        spec[param] = {}
        helper.vsys_dg = param
    else:
        if vsys is not None:
            if isinstance(vsys, bool):
                param = 'vsys'
            else:
                param = vsys
            spec[param] = {'default': 'vsys1'}
            helper.vsys = param
        if device_group is not None:
            if isinstance(device_group, bool):
                param = 'device_group'
            else:
                param = device_group
            spec[param] = {'default': 'shared'}
            helper.device_group = param
        if vsys_importable is not None:
            if isinstance(vsys_importable, bool):
                param = 'vsys'
            else:
                param = vsys_importable
            spec[param] = {}
            helper.vsys_importable = param

    if rulebase is not None:
        if isinstance(rulebase, bool):
            param = 'rulebase'
        else:
            param = rulebase
        spec[param] = {
            'default': 'pre-rulebase',
            'choices': ['pre-rulebase', 'post-rulebase'],
        }
        helper.rulebase = param

    if template is not None:
        if isinstance(template, bool):
            param = 'template'
        else:
            param = template
        spec[param] = {}
        helper.template = param

    if template_stack is not None:
        if isinstance(template_stack, bool):
            param = 'template_stack'
        else:
            param = template_stack
        spec[param] = {}
        helper.template_stack = param

    # Done.
    helper.argument_spec = spec
    helper.required_one_of = req
    return helper
