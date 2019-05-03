.. Palo Alto Networks Ansible Galaxy Role documentation master file, created by
   sphinx-quickstart on Mon Apr 29 11:49:39 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Palo Alto Networks Ansible Galaxy Role Documentation
====================================================

The Palo Alto Networks Ansible Galaxy role is a collection of modules that
automate configuration and operational tasks on Palo Alto Networks Next
Generation Firewalls (both physical and virtualized) and Panorama.  The
underlying protocol uses API calls that are wrapped within the Ansible
framework.

This is a **community supported project**. You can find the community
supported live page at https://live.paloaltonetworks.com/ansible.


Installation
------------

The most recent release of the role is available on Ansible Galaxy:
https://galaxy.ansible.com/PaloAltoNetworks/paloaltonetworks. To
install this, you can use the `ansible-galaxy` command like so:

.. code-block:: bash

    ansible-galaxy install PaloAltoNetworks.paloaltonetworks

To upgrade your existing role, add in the additional `-f` parameter to the
above command.

Once the role is installed, update your playbooks to tell Ansible to use the
role you've installed:

.. code-block:: yaml

    roles:
        - role: PaloAltoNetworks.paloaltonetworks

The role is built from the Palo Alto Networks github repo:
https://github.com/PaloAltoNetworks/ansible-pan.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   modules/index
   history
   contributing
   authors
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
