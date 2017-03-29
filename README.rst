==================================
Palo Alto Networks Ansible modules
==================================

The Palo Alto Networks Ansible modules project is a collection of Ansible modules to automate configuration and
operational tasks on Palo Alto Networks *Next Generation Firewalls*. The underlying protocol uses API calls that
are wrapped withing Ansible framework.

- Free software: Apache 2.0 License
- Documentation: http://panwansible.readthedocs.io/


Installation
------------

PANW PANOS Ansible modules are part of the default Ansible distribution which is available at:

    https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/panos

It is also available as free **Apache 2.0** licensed code from Palo Alto Networks Github repo at:

    https://github.com/PaloAltoNetworks/ansible-pan/

Or as package downloaded from pypi

    pip install ansible-pan

.. <comment> <> (ansible-galaxy install paloaltonetworks.panos) </comment>

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
    
