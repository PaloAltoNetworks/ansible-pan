==================================
Palo Alto Networks Ansible modules
==================================

The Palo Alto Networks Ansible modules project is a collection of Ansible modules to automate configuration and
operational tasks on Palo Alto Networks *Next Generation Firewalls*. The underlying protocol uses API calls that
are wrapped within the Ansible framework.

- Free software: Apache 2.0 License
- Documentation: http://panwansible.readthedocs.io/
- PANW community supported live page: http://live.paloaltonetworks.com/ansible


Installation
------------

PANW PANOS Ansible modules are part of the default Ansible distribution which is available at:

    https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/panos

It is also available as free **Apache 2.0** licensed code from Palo Alto Networks Github repo. This repo usually contains
the newest feature and bug fixes and it is synchronised with official RedHat Ansible repo upon every new Ansible release.

    https://github.com/PaloAltoNetworks/ansible-pan/

Or as ansible role installed from ansible-galaxy

    ansible-galaxy install PaloAltoNetworks.paloaltonetworks

.. <comment> <> (ansible-galaxy install paloaltonetworks.paloaltonetworks) </comment>


Sample playbooks
----------------

Sample playbooks can be found within this repo under::

    /examples
    (e.g. /samples/fw_dag.yml)
    
More comprehensive playbooks can be found here:

    https://github.com/PaloAltoNetworks/ansible-playbooks


Documentation
-------------

Each module is documented in docs/modules, you can also look at the documentation online at http://panwansible.readthedocs.io/
under *modules* section

**How to build doc's locally?**
    
Using Docker::

    $ docker run -it -v <PATH_TO_REPO>/ansible-pan/:/documents/ ivanbojer/spinx-with-rtd
    $ cd docs
    $ make html

Using Spinx::

    $ cd docs
    $ make html
    
