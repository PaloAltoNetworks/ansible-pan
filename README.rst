About
-----

A collection of Ansible modules to automate configuration and operational tasks on Palo Alto Networks NGFWs

Overview of modules
-------------------

- panos_admin - add or modify admin user
- panos_admpwd - set admin password via SSH
- panos_cert_gen_ssh - create SSL certificate
- panos_check - check if device is ready
- panos_commit - commit candidate config
- panos_dag - create dynamic address groups
- panos_import - import files
- panos_interface - configure a DP interface in DHCP Client mode
- panos_lic - apply an authcode
- panos_loadcfg - load configuration file
- panos_mgtconfig - set management settings
- panos_nat_policy - create a nat rule
- panos_pg - create a security profile group
- panos_restart - restart a device
- panos_service - create a service
- panos_srule - create a security rule

Installation
--------------

PANWAnsible modules are part of the deafult Ansible distribution. If you'd like to download Apache 2 licensed code 
Clone the github repo at:
    https://github.com/PaloAltoNetworks/ansible-pan/

 [comment]: <> (ansible-galaxy install paloaltonetworks.panos)

Documentation
-------------

Each module is documented in docs/modules, you can also look at the documentation online at http://panwansible.readthedocs.io/en/develop/

#### Rebuild documentation
    
######Using Docker
    docker run -it -v <PATH_TO_REPO>/ansible-pan/docs/:/documents/ ivanbojer/spinx-with-rtd
    make html
    
######Using Spinx
    cd docs; make modules
    
Dependencies
------------

- panos_admpwd requires paramiko
- panos_search depends on ec2 module
- panos_import requires requests and requests_toolbelt modules
- all the other modules requires pan-python

Example Playbook
----------------

This is an example playbook for import and load a config on a list of hosts:

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
