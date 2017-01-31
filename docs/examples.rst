.. _examples:

========
Snippets
========

Address service object
=============================

    Create address service object of different types [IP Range, FQDN, or IP Netmask].

.. include:: ../samples/panos_address.yml
    :literal:

Set admin password
==================

    PanOS module that allows changes to the user account passwords by doing
      API calls to the Firewall using pan-api as the protocol.

.. include:: ../samples/panos_admin.yml
    :literal:

Change admin password (SSH)
===========================

.. include:: ../samples/panos_adminpwd.yml
    :literal:

Generates self-signed certificate
=================================

    This module generates a self-signed certificate that can be used by GlobalProtect client, SSL connector, or
    otherwise. Root certificate must be preset on the system first. This module depends on paramiko for ssh.

.. include:: ../samples/panos_cert_gen_ssh.yml
    :literal:

Check if FW is ready
====================

    Check if PAN-OS device is ready for being configured (no pending jobs). The check could be done
    once or multiple times until the device is ready.

.. include:: ../samples/panos_check.yml
    :literal:

Dynamic address group (DAG)
===========================

    Create a dynamic address group object in the firewall used for policy rules.

.. include:: ../samples/panos_dag.yml
    :literal:

Import configuration
====================

    Import file into PAN-OS device.

.. include:: ../samples/panos_import.yml
    :literal:

DHCP on DataPort
================

    Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.

.. include:: ../samples/panos_interface.yml
    :literal:

Apply authcode to device
========================

    Apply an authcode to a device. The authcode should have been previously registered on the
    Palo Alto Networks support portal. The device should have Internet access.

.. include:: ../samples/panos_lic.yml
    :literal:

Load configuration
==================

- This is example playbook that imports and loads firewall configuration to a list of firewalls:

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
