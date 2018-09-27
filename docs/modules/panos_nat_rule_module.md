---
title: panos_nat_rule
---
# panos_nat_rule

_(versionadded:: 2.4)_


## Synopsis

Create a policy nat rule. Keep in mind that we can either end up configuring source NAT, destination NAT, or both. Instead of splitting it into two we will make a fair attempt to determine which one the user wants.


## Requirements (on host that executes module)

- pan-python can be obtained from PyPI https://pypi.python.org/pypi/pan-python
- pandevice can be obtained from PyPI https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| commit |  | True |  | Commit configuration if changed. |
| destination_ip |  | [u'any'] |  | list of destination addresses |
| destination_zone | yes |  |  | destination zone |
| devicegroup |  | shared |  | The device group to place the NAT rule into.Panorama only; ignored for firewalls. |
| dnat_address |  | None |  | dnat translated address |
| dnat_port |  | None |  | dnat translated port |
| existing_rule |  |  |  | If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| location |  |  |  | Position to place the created rule in the rule base.  Supported values are *top*/*bottom*/*before*/*after*. |
| nat_type |  | ipv4 |  | Type of NAT.Values are *ipv4*/*nat64*/*nptv6*. |
| operation |  |  |  | The action to be taken.  Supported values are *add*/*update*/*find*/*delete*/*disable*.This is used only if "state" is unspecified. |
| password | yes |  |  | Password credentials to use for auth unless *api_key* is set. |
| rule_name | yes |  |  | name of the SNAT rule |
| rulebase |  | pre-rulebase |  | The rulebase to put the NAT rule into.Values are *pre-rulebase*/*post-rulebase*.Panorama only; ignored for firewalls. |
| service |  | any |  | service |
| snat_address_type |  | translated-address |  | type of source translation. Supported values are *translated-address*/*interface-address*. |
| snat_bidirectional |  | false |  | bidirectional flag |
| snat_dynamic_address |  | None |  | Source NAT translated address. Used with Dynamic-IP and Dynamic-IP-and-Port. |
| snat_interface |  | None |  | snat interface |
| snat_interface_address |  | None |  | snat interface address |
| snat_static_address |  | None |  | Source NAT translated address. Used with Static-IP translation. |
| snat_type |  | None |  | type of source translation |
| source_ip |  | [u'any'] |  | list of source addresses |
| source_zone | yes |  |  | list of source zones |
| state |  | present |  | The state.  Can be either *present*/*absent*.If this is defined, then "operation" is ignored. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| vsys |  | vsys1 |  | The vsys to place the NAT rule into.Firewall only; ignored for Panorama. |

## Examples

    # Create a source and destination nat rule
      - name: Create NAT SSH rule for 10.0.1.101
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          rule_name: "Web SSH"
          source_zone: ["external"]
          destination_zone: "external"
          source: ["any"]
          destination: ["10.0.0.100"]
          service: "service-tcp-221"
          snat_type: "dynamic-ip-and-port"
          snat_interface: "ethernet1/2"
          dnat_address: "10.0.1.101"
          dnat_port: "22"
    
      - name: disable a specific security rule
        panos_nat_rule:
          ip_address: '{{ ip_address }}'
          username: '{{ username }}'
          password: '{{ password }}'
          operation: 'disable'
          rule_name: 'Prod-Legacy 1'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

