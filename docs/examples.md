---
title: Examples
---

# Examples

### Note: You can see a complete examples [here](https://github.com/PaloAltoNetworks/ansible-pan/tree/master/examples)

## Add security policy to Firewall or Panorama

> Security policies allow you to enforce rules and take action, and can
> be as general or specific as needed. The policy rules are compared
> against the incoming traffic in sequence, and because the first rule
> that matches the traffic is applied, the more specific rules must
> precede the more general ones.

##### Firewall

      - name: Add test rule 1 to the firewall
        panos_security_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'add'
          rule_name: 'Ansible test 1'
          description: 'An Ansible test rule'
          source_zone: ['internal']
          destination_zone: ['external']
          source_ip: ['1.2.3.4']
          source_user: ['any']
          destination_ip: ['any']
          category: ['any']
          application: ['any']
          service: ['service-http']
          hip_profiles: ['any']
          action: 'allow'
          commit: 'False'

##### Panorama
    
      - name: Add test pre-rule to Panorama
        panos_security_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'add'
          rule_name: 'Ansible test 1'
          description: 'An Ansible test pre-rule'
          source_zone: ['internal']
          destination_zone: ['external']
          source_ip: ['1.2.3.4']
          source_user: ['any']
          destination_ip: ['any']
          category: ['any']
          application: ['any']
          service: ['service-http']
          hip_profiles: ['any']
          action: 'allow'
          devicegroup: 'DeviceGroupA'
          commit: 'False'

## Add NAT policy to Firewall or Panorama

> If you define Layer 3 interfaces on the firewall, you can configure a
> Network Address Translation (NAT) policy to specify whether source or
> destination IP addresses and ports are converted between public and
> private addresses and ports. For example, private source addresses can
> be translated to public addresses on traffic sent from an internal
> (trusted) zone to a public (untrusted) zone. NAT is also supported on
> virtual wire interfaces.
    
##### Firewall

      - name: Add the necessary service object to the firewall first
        panos_object:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          serviceobject: 'service-tcp-221'
          protocol: 'tcp'
          destination_port: '221'
          description: 'SSH on port 221'
          operation: 'add'
    
      - name: Create dynamic NAT rule on the firewall
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          rule_name: 'Web SSH inbound'
          source_zone: ['external']
          destination_zone: 'external'
          source_ip: ['any']
          destination_ip: ['10.0.0.100']
          service: 'service-tcp-221'
          snat_type: 'dynamic-ip-and-port'
          snat_interface: ['ethernet1/2']
          dnat_address: '10.0.1.101'
          dnat_port: '22'
          operation: 'add'
      
##### Panorama

      - name: Add the necessary service object to Panorama first
        panos_object:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          serviceobject: 'service-tcp-221'
          protocol: 'tcp'
          destination_port: '221'
          description: 'SSH on port 221'
          devicegroup: 'shared_services_11022'
          operation: 'add'
    
      - name: Create dynamic NAT rule on Panorama
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          rule_name: 'Web SSH inbound'
          source_zone: ['external']
          destination_zone: 'external'
          source_ip: ['any']
          destination_ip: ['10.0.0.100']
          service: 'service-tcp-221'
          snat_type: 'dynamic-ip-and-port'
          snat_interface: ['ethernet1/2']
          dnat_address: '10.0.1.101'
          dnat_port: '22'
          devicegroup: 'shared_services_11022'
          operation: 'add'

## Add address service object

> Create address service object of different types \[IP Range, FQDN, or
> IP Netmask\].

##### Firewall

      - name: Add an address object to the firewall
        panos_object:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          addressobject: 'test-address'
          address: '192.168.100.89/24'
          address_type: 'ip-netmask'
          description: 'This is a test address object'
          operation: 'add'

##### Panorama
    
      - name: Add an address object to Panorama
        panos_object:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          addressobject: 'test-address'
          address: '192.168.100.89/24'
          address_type: 'ip-netmask'
          description: 'This is a test address object'
          devicegroup: 'shared_services_11022'
          operation: 'add'

## Change firewall admin password

> PanOS module that allows changes to the user account passwords by
> doing API calls to the Firewall using pan-api as the protocol.
    
      - name: Set admin password
        panos_admin:
          ip_address: '{{ ip_address }}'
          password: '{{ password }}'
          admin_username: admin
          admin_password: "paloalto"
          commit: False

## Change firewall admin password using SSH

> Change admin password of PAN-OS device using SSH with SSH key. This is
> used in particular when NGFW is deployed in the cloud (such as AWS).
    
      - name: Change user password using ssh protocol
        panos_admpwd:
          ip_address: '{{ ip_address }}'
          password: '{{ password }}'
          newpassword: '{{ new_password }}'
          key_filename: '{{ key_filename }}'

## Generates self-signed certificate

> This module generates a self-signed certificate that can be used by
> GlobalProtect client, SSL connector, or otherwise. Root certificate
> must be preset on the system first. This module depends on paramiko
> for ssh.
    
      - name: generate self signed certificate
        panos_cert_gen_ssh:
          ip_address: "{{ ip_address }}"
          username: "{{ username }}"
          password: "{{ password }}"
          cert_cn: "{{ cn }}"
          cert_friendly_name: "{{ friendly_name }}"
          signed_by: "{{ signed_by }}"

## Check if FW is ready

> Check if PAN-OS device is ready for being configured (no pending
> jobs). The check could be done once or multiple times until the device
> is ready.
    
      - name: Wait for FW reboot
        panos_check:
          ip_address: "{{ ip_address }}"
          username: "{{ username }}"
          password: "{{ password }}"
        register: result
        until: not result|failed
        retries: 50
        delay: 5

## Dynamic address group (DAG)

> Create a dynamic address group object in the firewall used for policy
> rules.

    - name: Create the tags to map IP addresses
      panos_dag_tags:
        ip_address: "{{ ip_address }}"
        password: "{{ password }}"
        ip_to_register: "{{ ip_to_register }}"
        tag_names: "{{ tag_names }}"
        description: "Tags to allow certain IP's to access various SaaS Applications"
        operation: 'add'
      tags: "add-dagip"

## Import configuration

> Import file into PAN-OS device.

    - name: import configuration file into PAN-OS
      panos_import:
          ip_address: "{{ ip_address }}"
          username: "{{ username }}"
          password: "{{ password }}"
          file: "{{ config_file }}"
          category: "configuration"
      
## DHCP on DataPort

> Configure data-port (DP) network interface for DHCP. By default DP
> interfaces are static.

    - name: enable DHCP client on ethernet1/1 in zone external
      panos_interface:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          if_name: "ethernet1/1"
          zone_name: "external"
          create_default_route: "yes"
          operation: "update"
          commit: False

## Load configuration

-   This is example playbook that imports and loads firewall
    configuration from a configuration file

```
    - name: import config
      hosts: my-firewall
      connection: local
      gather_facts: False

      vars:
        cfg_file: candidate-template-empty.xml

      tasks:
      - name: Grab the credentials from ansible-vault
        include_vars: 'firewall-secrets.yml'
        no_log: 'yes'

      - name: wait for SSH (timeout 10min)
        wait_for: port=22 host='{{ ip_address }}' search_regex=SSH timeout=600

      - name: checking if device ready
        panos_check:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
        register: result
        until: not result|failed
        retries: 10
        delay: 10

      - name: import configuration
        panos_import:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          file: '{{cfg_file}}'
          category: 'configuration'
        register: result

      - name: load configuration
        panos_loadcfg:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          file: '{{result.filename}}'
          commit: False

      - name: set admin password
        panos_admin:
          ip_address: '{{ ip_address }}'
          password: '{{ password }}'
          admin_username: admin
          admin_password: '{{password}}'
          commit: False

      - name: commit
        panos_commit:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          sync: False
      - name: waiting for commit
        panos_check:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
        register: result
        until: not result|failed
        retries: 10
        delay: 10
```
