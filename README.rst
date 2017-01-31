=========================
Palo Alto Ansible modules
=========================

About
-----

A collection of Ansible modules to automate configuration and operational tasks on Palo Alto Networks NGFWs


Installation
------------

PANW Ansible modules are part of the default Ansible distribution. If you'd like to download Apache 2 licensed code
you can clone the github repo at:

    https://github.com/PaloAltoNetworks/ansible-pan/

.. <comment> <> (ansible-galaxy install paloaltonetworks.panos) </comment>

Documentation
-------------

Each module is documented in docs/modules, you can also look at the documentation online at http://panwansible.readthedocs.io/en/develop/
under *modules* section

How to Rebuild documentation?
    
Using Docker::

    $ docker run -it -v <PATH_TO_REPO>/ansible-pan/docs/:/documents/ ivanbojer/spinx-with-rtd
    $ make html

Using Spinx::

    $ cd docs
    $ make html
    
Example Playbook
----------------

This is an example playbook for import and load a config on a list of hosts:

::

    ---
    - name: import config
      hosts: gp-portals
      connection: local
      gather_facts: False
      vars:
        cfg_file: gp-portal-empty.xml
    
      tasks:
      - name: wait for SSH (timeout 10min)
        wait_for: port=22 host="{{inventory_hostname}}" search_regex=SSH timeout=600
      - name: checking if device ready
        panos_check: 
          ip_address: "{{inventory_hostname}}" 
          password: "{{password}}"
        register: result
        until: not result|failed
        retries: 10
        delay: 10
      - name: import configuration
        panos_import:
          ip_address: "{{inventory_hostname}}" 
          password: "{{password}}"
          file: "{{cfg_file}}"
          category: "configuration"
        register: result
      - name: load configuration
        panos_loadcfg:
          ip_address: "{{inventory_hostname}}" 
          password: "{{password}}"
          file: "{{result.filename}}"
          commit: False       
      - name: set admin password
        panos_admin:
          ip_address: "{{inventory_hostname}}"
          password: "{{password}}"
          admin_username: admin
          admin_password: "{{password}}"
          commit: False
      - name: commit
        panos_commit:
          ip_address: "{{inventory_hostname}}"
          password: "{{password}}"
          sync: False
      - name: waiting for commit
        panos_check: 
          ip_address: "{{inventory_hostname}}" 
          password: "{{password}}"
        register: result
        until: not result|failed
        retries: 10
        delay: 10
