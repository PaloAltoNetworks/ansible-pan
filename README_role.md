Role Name
=========

The Palo Alto Networks Ansible modules project is a collection of Ansible modules to automate configuration and
operational tasks on Palo Alto Networks *Next Generation Firewalls*. The underlying protocol uses API calls that
are wrapped within Ansible framework.

https://github.com/PaloAltoNetworks/ansible-pan/

Requirements
------------

- pip

Role Variables
--------------

N/A

Dependencies
------------

N/A

Example Playbook
----------------

Sample playbook that will inject security rule in the PANW Next Generation Firewall device.

    # FILENAME
    # playbook_set_complex_srule.yml
    #
    # DESCRIPTION
    # Example playbook that will connect to the firewall using credentials provided in the vars.yml and set few security rules.
    #
    # REQUIREMENTS
    # pip install ansible
    # ansible-galaxy install PaloAltoNetworks.paloaltonetworks
    #
    # STEPS
    # update vars.yml with your own credentials/settings
    #
    # Good practice: The var files are provided in cleartext. They should be edited and encrypred using:
    # ansible-vault encrypt firewall-secrets.yml
    #
    # EXECUTE
    # ansible-playbook playbook_set_complex_srule.yml
    ---
    - hosts: localhost
      connection: local
      
      roles:
        - role: PaloAltoNetworks.paloaltonetworks
    
      tasks:
        - name: include variables (free-form)
          include_vars: vars.yml
          no_log: 'yes'
    
        # permit ssh to 1.1.1.1
        - name: permit ssh to 1.1.1.1
          panos_security_rule:
            ip_address: "{{ mgmt_ip }}"
            password: "{{admin_password}}"
            rule_name: 'SSH permit'
            description: 'SSH rule test'
            source_zone: ['untrust']
            destination_zone: ['trust']
            source_ip: ['any']
            source_user: ['any']
            destination_ip: ['1.1.1.1']
            category: ['any']
            application: ['ssh']
            service: ['application-default']
            hip_profiles: ['any']
            action: 'allow'
            operation: 'add'
            commit: false
    
        # Allow HTTP multimedia only from CDNs
        - name: Allow HTTP multimedia only from CDNs
          panos_security_rule:
            ip_address: "{{ mgmt_ip }}"
            password: "{{admin_password}}"
            rule_name: 'HTTP Multimedia'
            description: 'Allow HTTP multimedia only to host at 1.1.1.1'
            source_zone: ['untrust']
            destination_zone: ['trust']
            source_ip: ['any']
            source_user: ['any']
            destination_ip: ['1.1.1.1']
            category: ['content-delivery-networks']
            application: ['http-video', 'http-audio']
            service: ['service-http', 'service-https']
            hip_profiles: ['any']
            action: 'allow'
            commit: false
    
        # more complex fictitious rule that uses profiles
        - name: More complex fictitious rule that uses profiles
          panos_security_rule:
            ip_address: "{{ mgmt_ip }}"
            password: "{{admin_password}}"
            rule_name: 'Allow HTTP w profile'
            log_start: false
            log_end: true
            action: 'allow'
            antivirus: 'default'
            vulnerability: 'default'
            spyware: 'default'
            url_filtering: 'default'
            wildfire_analysis: 'default'
            commit: false
    
        # deny all
        - name: Deny all rules used as a 'catch-all' at the end
          panos_security_rule:
            ip_address: "{{ mgmt_ip }}"
            password: "{{admin_password}}"
            rule_name: 'DenyAll'
            log_start: true
            log_end: true
            action: 'deny'
            rule_type: 'interzone'

License
-------

Apache 2.0

Author Information
------------------

Ivan Bojer, @ivanbojer
