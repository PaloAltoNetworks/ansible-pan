.. _examples:

========
Examples
========

Add security policy to Firewall or Panorama
===========================================

    Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
    The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
    the traffic is applied, the more specific rules must precede the more general ones.

.. include:: ../examples/fw_secrule_add.yml
    :literal:

Panorama
--------

.. include:: ../examples/pano_secrule_add.yml
    :literal:

Add NAT policy to Firewall or Panorama
======================================

    If you define Layer 3 interfaces on the firewall, you can configure a Network Address Translation (NAT) policy to
    specify whether source or destination IP addresses and ports are converted between public and private addresses and
    ports. For example, private source addresses can be translated to public addresses on traffic sent from an
    internal (trusted) zone to a public (untrusted) zone. NAT is also supported on virtual wire interfaces.

.. include:: ../examples/fw_natrule_add.yml
    :literal:

Panorama
--------

.. include:: ../examples/pano_natrule_add.yml
    :literal:

Add address service object
==========================

    Create address service object of different types [IP Range, FQDN, or IP Netmask].

.. include:: ../examples/fw_objects_add.yml
    :literal:

Panorama
--------

.. include:: ../examples/pano_objects_add.yml
    :literal:

Change firewall admin password
==============================

    PanOS module that allows changes to the user account passwords by doing
    API calls to the Firewall using pan-api as the protocol.

.. include:: ../examples/fw_admin.yml
    :literal:

Change firewall admin password using SSH
========================================

    Change admin password of PAN-OS device using SSH with SSH key. This is used in particular when NGFW is deployed in
    the cloud (such as AWS).

.. include:: ../examples/fw_adminpwd.yml
    :literal:

Generates self-signed certificate
=================================

    This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
    otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.

.. include:: ../examples/fw_cert_gen_ssh.yml
    :literal:

Check if FW is ready
====================

    Check if PAN-OS device is ready for being configured (no pending jobs). The check could be done
    once or multiple times until the device is ready.

.. include:: ../examples/fw_check.yml
    :literal:

Dynamic address group (DAG)
===========================

    Create a dynamic address group object in the firewall used for policy rules.

.. include:: ../examples/fw_dag.yml
    :literal:

Import configuration
====================

    Import file into PAN-OS device.

.. include:: ../examples/fw_import.yml
    :literal:

DHCP on DataPort
================

    Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.

.. include:: ../examples/fw_interface.yml
    :literal:

Load configuration
==================

- This is example playbook that imports and loads firewall configuration from a configuration file

::

    ---
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
