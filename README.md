About
-----

A collection of Ansible modules to automate configuration and operational tasks on Palo Alto Networks NGFWs

Overview of modules
-------------------

- panos_admpwd - set admin password via SSH
- panos_awsmonitor - create AWS VM monitor
- panos_check - check if device is ready
- panos_content - upgrade dynamic updates
- panos_cstapphost - create a custom application for a website
- panos_dag - create dynamic address groups
- panos_dhcpif - configure a DP interface in DHCP Client mode
- panos_lic - apply an authcode
- panos_mgtconfig - set management settings
- panos_pg - create a security profile group
- panos_restart - restart a device
- panos_search - search AWS Matketplace for PA-VM-AWS images
- panos_snat - create a source nat rule
- panos_srule - create a security rule
- panos_sshkey - manage public SSH keys

Installation
--------------

We are working to add the modules to the Ansible Galaxy, in the meantime just clone this repo and add the library folder to the Ansible library paths using the ANSIBLE_LIBRARY environment variable or an ansible.cfg file.

Documentation
-------------

Each module is documented using Ansible best practices, the documentation is in the module source code.

Dependencies
------------

- panos_admpwd requires paramiko
- panos_search depends on ec2 module
- all the other modules requires pan-python

Example Playbooks
-----------------

### standalone-example.yml

This playbook creates an instance of VM-Series for AWS in the AWS EC2 cloud.

	export AWS_ACCESS_KEY_ID=<AWS ACCESS KEY>
	export AWS_SECRET_ACCESS_KEY=<AWS SECRET ACCESS KEY>
	export AWS_REGION=eu-west-1

	ansible-playbook -vvvv ansible-pan/standalone-example.yml --extra-vars 'key_name=ansible-test key_filename=/tmp/ansible-test.pem auth_code=IBADCODE admin_password=BADPASSWORD'

### cloudformation-example.yml

This playbook creates a protected server infrastructure in the AWS cloud using Cloudformation:

- a VPC
- 2 subnets (Public and Private)
- a server instance on the Private subnet
- a PA-VM-AWS instance to protect the server

How to launch it:

	export AWS_ACCESS_KEY_ID=<AWS ACCESS KEY>
	export AWS_SECRET_ACCESS_KEY=<AWS SECRET ACCESS KEY>
	export AWS_REGION=eu-west-1

	ansible-playbook -vvvv ansible-pan/cloudformation-example.yml --extra-vars 'key_name=ansible-test key_filename=/tmp/ansible-test.pem auth_code=IBADCODE admin_password=BADPASSWORD'

License
-------

ISC

Author Information
------------------

Palo Alto Networks

