# Palo Alto Networks Ansible modules

A collection of Ansible modules that automate configuration and
operational tasks on Palo Alto Networks Next Generation Firewalls --
both physical and virtualized form factor. The underlying protocol uses
API calls that are wrapped within the Ansible framework.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://ansible-pan.readthedocs.io>
-   PANW community supported live page:
    <http://live.paloaltonetworks.com/ansible>

## Installation

The recommended way to install the modules is installing the Palo Alto
Networks Ansible Galaxy role:

```bash
$ ansible-galaxy install PaloAltoNetworks.paloaltonetworks
```

Older modules modules are part of the default Ansible distribution
which is available at:

> <https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/panos>

It is also available as free **Apache 2.0** licensed code from Palo Alto
Networks Github repo if you want to see what is coming in the next release:

> <https://github.com/PaloAltoNetworks/ansible-pan/>

## Sample playbooks

Sample playbooks can be found within this repo under:

    /examples
    (e.g. /examples/fw_dag.yml)

More comprehensive playbooks can be found under:

    /ansible-playbooks/

## Ansible galaxy role

The Palo Alto Networks Ansible modules project is a collection of Ansible modules to automate configuration and
operational tasks on Palo Alto Networks *Next Generation Firewalls*. The underlying protocol uses API calls that are wrapped within Ansible framework.

> <https://github.com/PaloAltoNetworks/ansible-pan/>

## Support

This template/solution is released under an as-is, best effort, support
policy. These scripts should be seen as community supported and Palo
Alto Networks will contribute our expertise as and when possible. We do
not provide technical support or help in using or troubleshooting the
components of the project through our normal support options such as
Palo Alto Networks support teams, or ASC (Authorized Support Centers)
partners and backline support options. The underlying product used (the
VM-Series firewall) by the scripts or templates are still supported, but
the support is only for the product functionality and not for help in
deploying or using the template or script itself.

Unless explicitly tagged, all projects or work posted in our GitHub
repository (at <https://github.com/PaloAltoNetworks>) or sites other
than our official Downloads page on <https://support.paloaltonetworks.com>
are provided under the besteffort policy.
