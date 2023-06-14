.. Palo Alto Networks Ansible Galaxy Role documentation master file, created by
   sphinx-quickstart on Mon Apr 29 11:49:39 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Palo Alto Networks Ansible Galaxy Role Documentation
====================================================

**PLEASE NOTE: This role is deprecated, the modules are no longer being
updated. Please transition to using the modules in the collection
instead: https://paloaltonetworks.github.io/pan-os-ansible**

The Palo Alto Networks Ansible Galaxy role is a collection of modules that
automate configuration and operational tasks on Palo Alto Networks Next
Generation Firewalls (both physical and virtualized) and Panorama.  The
underlying protocol uses API calls that are wrapped within the Ansible
framework.

This is a **community supported project**. You can find the community
supported live page at https://live.paloaltonetworks.com/ansible.


Role / Collection Compatibility
-------------------------------

The Palo Alto Networks PAN-OS Ansible modules were previously distributed as an
Ansible Galaxy role (https://galaxy.ansible.com/paloaltonetworks/paloaltonetworks).
Since Ansible 2.9, RedHat has urged developers to migrate to `collections` to
organize and distribute their integrations.  The new collection can be found here:
https://galaxy.ansible.com/paloaltonetworks/panos

The 1.0 version of this collection is a straight port of the Ansible Galaxy
role v2.4.0.  If you are using Ansible 2.9 or later and you are using the
role, then you can safely use this instead with no change in functionality.  Just
specify the `collections` spec (as mentioned above in the Usage section), remove
`PaloAltoNetworks.paloaltonetworks` from the `roles` spec, and you're done!

Now that the collection is live, no new features will be added to the role.  All
active development will take place on the collection moving forwared.  Users are
encouraged to upgrade to Ansible 2.9 and start using the new collection to stay
up-to-date with features and bug fixes.


Installation - Collection (Recommended)
---------------------------------------

(For Ansible >= v2.9)

Install the collection using `ansible-galaxy`:

.. code-block:: bash

    ansible-galaxy collection install paloaltonetworks.panos

Then in your playbooks you can specify that you want to use the
`panos` collection like so:

.. code-block:: yaml

    collections:
        - paloaltonetworks.panos

* Ansible Galaxy: https://galaxy.ansible.com/PaloAltoNetworks/panos
* GitHub repo:  https://github.com/PaloAltoNetworks/pan-os-ansible


Installation - Role
-------------------

(For Ansible < v2.9)

Install the collection using `ansible-galaxy`:

.. code-block:: bash

    ansible-galaxy install PaloAltoNetworks.paloaltonetworks

To upgrade your existing role, add in the additional `-f` parameter to the
above command.

Then in your playbooks you can specify that you want to use the
`paloaltonetworks` role like so:

.. code-block:: yaml

    roles:
        - role: PaloAltoNetworks.paloaltonetworks

* Ansible Galaxy: https://galaxy.ansible.com/PaloAltoNetworks/paloaltonetworks
* GitHub repo: https://github.com/PaloAltoNetworks/ansible-pan


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
