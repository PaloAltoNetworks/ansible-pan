---
title: panos_security_rule
---
# panos_security_rule

_(versionadded:: 2.4)_


## Synopsis

Security policies allow you to enforce rules and take action, and can be as general or specific as needed.
The policy rules are compared against the incoming traffic in sequence, and because the first rule that matches
the traffic is applied, the more specific rules must precede the more general ones.


## Requirements (on host that executes module)

- pandevice can be obtained from PyPi https://pypi.python.org/pypi/pandevice

## Options

| parameter | required | default | choices | comments |
| --- | --- | --- | --- | --- |
| action |  |  |  | Action to apply once rules matches. |
| antivirus |  | None |  | Name of the already defined antivirus profile. |
| api_key |  |  |  | API key that can be used instead of *username*/*password* credentials. |
| application |  | any |  | List of applications, application groups, and/or application filters. |
| category |  |  |  | List of destination URL categories. |
| commit |  |  |  | Commit configuration if changed. |
| data_filtering |  | None |  | Name of the already defined data_filtering profile. |
| description |  | None |  | Description of the security rule. |
| destination_ip |  | any |  | List of destination addresses. |
| destination_zone |  | any |  | List of destination zones. |
| devicegroup |  | None |  | Device groups are logical groups of firewalls in Panorama.If the device group is not defined actions will affect the Shared Panorama context. |
| disable_server_response_inspection |  |  |  | Disables packet inspection from the server to the client. Useful under heavy server load conditions. |
| disabled |  |  |  | Disable this rule. |
| existing_rule |  |  |  | If 'location' is set to 'before' or 'after', this option specifies an existing rule name.  The new rule will be created in the specified position relative to this rule.  If 'location' is set to 'before' or 'after', this option is required. |
| file_blocking |  | None |  | Name of the already defined file_blocking profile. |
| group_profile |  | None |  | - Security profile group that is already defined in the system. This property supersedes antivirus, vulnerability, spyware, url_filtering, file_blocking, data_filtering, and wildfire_analysis properties. |
| hip_profiles |  | any |  | - If you are using GlobalProtect with host information profile (HIP) enabled, you can also base the policy on information collected by GlobalProtect. For example, the user access level can be determined HIP that notifies the firewall about the user's local configuration. |
| icmp_unreachable |  |  |  | Send 'ICMP Unreachable'. Used with 'deny', 'drop', and 'reset' actions. |
| ip_address | yes |  |  | IP address (or hostname) of PAN-OS device being configured. |
| location |  | bottom |  | Position to place the created rule in the rule base.  Supported values are *top*/*bottom*/*before*/*after*. |
| log_end |  | True |  | Whether to log at session end. |
| log_setting |  |  |  | Log forwarding profile. |
| log_start |  |  |  | Whether to log at session start. |
| negate_destination |  |  |  | Match on the reverse of the 'destination_ip' attribute |
| negate_source |  |  |  | Match on the reverse of the 'source_ip' attribute |
| negate_target |  |  |  | Exclude this rule from the listed firewalls in Panorama. |
| operation |  | add |  | The action to be taken.  Supported values are *add*/*update*/*find*/*delete*.*Deprecated - use 'state' instead.* |
| password |  |  |  | Password credentials to use for auth unless *api_key* is set. |
| rule_name | yes |  |  | Name of the security rule. |
| rule_type |  | universal |  | Type of security rule (version 6.1 of PanOS and above). |
| rulebase |  | pre-rulebase |  | The Panorama rulebase in which the rule will be created. Only used with Panorama. |
| schedule |  |  |  | Schedule in which this rule is active. |
| service |  | application-default |  | List of services and/or service groups. |
| source_ip |  | any |  | List of source addresses. |
| source_user |  | any |  | Use users to enforce policy for individual users or a group of users. |
| source_zone |  | any |  | List of source zones. |
| spyware |  | None |  | Name of the already defined spyware profile. |
| state |  | present |  | The state of the rule.  Can be either *present*/*absent*. |
| tag_name |  | None |  | List of tags associated with the rule. |
| target |  |  |  | Apply this rule exclusively to the listed firewalls in Panorama. |
| url_filtering |  | None |  | Name of the already defined url_filtering profile. |
| username |  | admin |  | Username credentials to use for auth unless *api_key* is set. |
| vsys |  | vsys1 |  | The VSYS in which to create the rule. |
| vulnerability |  | None |  | Name of the already defined vulnerability profile. |
| wildfire_analysis |  | None |  | Name of the already defined wildfire_analysis profile. |

## Examples

    - name: add SSH inbound rule to Panorama device group
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_name: 'SSH permit'
        description: 'SSH rule test'
        tag_name: ['production']
        source_zone: ['public']
        source_ip: ['any']
        destination_zone: ['private']
        destination_ip: ['1.1.1.1']
        application: ['ssh']
        action: 'allow'
        devicegroup: 'Cloud Edge'
        rulebase: 'pre-rulebase'
    
    
    - name: add a rule to allow HTTP multimedia only to CDNs
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        rule_name: 'HTTP Multimedia'
        description: 'Allow HTTP multimedia only to host at 1.1.1.1'
        source_zone: ['private']
        destination_zone: ['public']
        category: ['content-delivery-networks']
        application: ['http-video', 'http-audio']
        service: ['service-http', 'service-https']
        action: 'allow'
    
    - name: add a more complex rule that uses security profiles
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_name: 'Allow HTTP'
        source_zone: ['public']
        destination_zone: ['private']
        log_start: false
        log_end: true
        action: 'allow'
        antivirus: 'strict'
        vulnerability: 'strict'
        spyware: 'strict'
        url_filtering: 'strict'
        wildfire_analysis: 'default'
    
    - name: disable a Panorama pre-rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        rule_name: 'Allow telnet'
        source_zone: ['public']
        destination_zone: ['private']
        source_ip: ['any']
        destination_ip: ['1.1.1.1']
        log_start: false
        log_end: true
        action: 'allow'
        devicegroup: 'Production edge'
        rulebase: 'pre-rulebase'
        disabled: true
    
    
    - name: delete a devicegroup security rule
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        api_key: '{{ api_key }}'
        operation: 'delete'
        rule_name: 'Allow telnet'
        devicegroup: 'DC Firewalls'
        rulebase: 'pre-rulebase'
        state: 'absent'
    
    - name: add a rule at a specific location in the rulebase
      panos_security_rule:
        ip_address: '{{ ip_address }}'
        username: '{{ username }}'
        password: '{{ password }}'
        operation: 'add'
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
        action: 'allow'
        location: 'before'
        existing_rule: 'Allow MySQL'

#### Notes

- Checkmode is not supported.
- Panorama is supported.



#### Status

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.

