Release History
===============

V2.2.2
------

- *Released*: 2019-06-18

Bug fixes:

* Fixed module handling when targeting Panorama template stacks

V2.2.1
------

- *Released*: 2019-06-12

Bug fixes:

* Fixed `panos_l3_subinterface` DHCP handling to match `panos_interface`

V2.2.0
------

- *Released*: 2019-06-11

New modules:

* `panos_zone_facts`
* `panos_ipsec_ipv4_proxyid`
* `panos_virtual_router_facts`
* `panos_l3_subinterface`
* `panos_l2_subinterface`
* `panos_log_forwarding_profile`
* `panos_log_forwarding_profile_match_list`
* `panos_log_forwarding_profile_match_list_action`
* `panos_email_profile`
* `panos_email_server`
* `panos_snmp_profile`
* `panos_snmp_v2c_server`
* `panos_snmp_v3_server`
* `panos_syslog_profile`
* `panos_syslog_server`
* `panos_http_profile`
* `panos_http_profile_header`
* `panos_http_profile_param`
* `panos_http_server`
* `panos_type_cmd`

Enhancements:

* `panos_security_rule_facts` can now return full policy info.

Bug fixes:

* Added module encoding to all modules.
* Various documentation fixes.

V2.1.2
------

- *Released*: 2019-05-24

Enhancements:

* `panos_registered_ip_facts` can now filter on IP addresses (in addition to tags)
* All modules: Panorama commits can now still push to a device group even if a Panorama
  commit is unnecessary
* `panos_nat_rule`: Changed the default location to unspecified instead of bottom

Bug fixes:

* `panos_bgp`: Added the "state" param to this module
* `panos_facts`: Corrected virtual router output name to use underscores

V2.1.1
------

- *Released*: 2019-05-08
- *Status*: Released

- Minor bug fix with `panos_op`
- Documentation tweaks

V2.1.0
------

- *Released*: 2019-04-26
- *Status*: Released

New modules:

* `panos_security_rule_facts`
* `panos_vlan`
* `panos_vlan_interface`

The following shorthand applies to this version's updates:

- `provider` - Any module below that lists a change of `provider` means that
  it supports a new provider dict for PAN-OS authentication credentials in
  addition to the old `ip_address` / `username` / `password` / `api_key`.  Additionally
  these modules now support Panorama to firewall connections, performed by specifying
  Panorama IP address, username, and password, then specifying a firewall's serial
  number using the `serial_number` param in the `provider` dict.
- `removed operation` - This module has had the old `operation` param removed in favor
  of `state`.  Please update your playbooks to use `state` instead.
- `template support` - This module now supports Panorama templates.
- `full template support` - This module now supports both Panorama templates and
  template stacks.
- `vsys support` - This module now includes support for specifying the firewall vsys.
- `checkmode` - This module now supports Ansible's check mode.

Given the above shorthand, the following modules have been updated as follows:

- `panos_address_group`: provider; checkmode
- `panos_address_object`: provider; checkmode
- `panos_administrator`: provider; full template support; checkmode; Now supports
  supplying the password hash directly
- `panos_api_key`: provider
- `panos_bgp`: provider; full template support; checkmode
- `panos_bgp_aggregate`: provider; full template support; checkmode
- `panos_bgp_auth`: provider; full template support; checkmode; `replace` is
  deprecated as this is now the default behavior for `state=apply`
- `panos_bgp_conditional_advertisement`: provider; full template support;
  checkmode; `advertise_filter` and `non_exist_filter` have been deprecated,
  add filters using `panos_bgp_policy_filter` instead
- `panos_bgp_dampening`: provider; full template support; checkmode
- `panos_bgp_peer`: provider; full template support; checkmode
- `panos_bgp_peer_group`: provider; full template support; checkmode
- `panos_bgp_policy_filter`: provider; full template support; checkmode;
  "state=return-object" has been deprecated, just use states of absent/present
  like other modules as normal; `address_prefix` can now be a dict with
  "name"/"exact" keys or a string
- `panos_bgp_policy_rule`: provider; full template support; checkmode;
  `address_prefix` can now be a dict with "name"/"exact" keys or a string
- `panos_bgp_redistribute`: provider; full template support; checkmode
- `panos_check`: provider; fixed #183; fixed #311
- `panos_commit`: provider; added `include_template` param; `devicegroup` is
  deprecated, use `device_group` instead
- `panos_facts`: provider; fixed bug when running against VM NGFW; `host` has
  been removed, use `provider` instead
- `panos_ike_crypto_profile`: provider; full template support; checkmode
- `panos_ike_gateway`: provider; full template support; checkmode; many params
  have been aliased to new param names to better match the `pandevice` naming
- `panos_interface`: provider; template support; checkmode; removed operation;
  fixed #193; fixed #266; fixed #267; `vsys_dg` is deprecated, use `vsys` instead
- `panos_ipsec_profile`: provider; full template support; checkmode
- `panos_ipsec_tunnel`: provider; full template support; checkmode; many new
  params added to support missing functionality added in, please refer to the
  module documentation for the complete list of params now supported
- `panos_lic`: provider; added new output `licenses`
- `panos_loopback_interface`: provider; template support; checkmode; `vsys_dg` is
  deprecated; use `vsys` instead
- `panos_management_profile`: provider; full template support; checkmode;
  `panorama_template` is deprecated, use `template` instead
- `panos_match_rule`: provider; `vsys_id` is deprecated, use `vsys`; fixed #248;
  output `stdout_lines` is deprecated, use `rule` instead (note: this has a
  different format, so please update your playbooks)
- `panos_mgtconfig`: provider; checkmode; `devicegroup` is removed as this param
  was not doing anything; added `verify_update_server`
- `panos_nat_rule`: provider; removed operation; checkmode; `devicegroup` is
  deprecated, use `device_group`; `tag_name` (string type) is deprecated, use
  `tag` (list type); added `enable` and `disable` types for the `state` param
- `panos_object_facts`: provider; added support for name regexes and a new
  `objects` output
- `panos_op`: provider
- `panos_pg`: provider; added Panorama support; added `state`
- `panos_redistribution`: provider; full template support; checkmode
- `panos_registered_ip`: provider; vsys support; checkmode
- `panos_registered_ip_facts`: provider; vsys support
- `panos_restart`: provider
- `panos_security_rule`: provider; removed operation; checkmode; `devicegroup`
  is deprecated, use `device_group` instead
- `panos_service_group`: provider; checkmode
- `panos_service_object`: provider; checkmode
- `panos_software`: provider; checkmode
- `panos_static_route`: provider; full template support; added nexthop type
  of "next-vr"
- `panos_tag_object`: provider; checkmode
- `panos_tunnel`: provider; template support; checkmode; `vsys_dg` is deprecated,
  use `vsys` instead
- `panos_userid`: provider; removed operation; `state` added as a param
- `panos_virtual_router`: provider; full template support; checkmode
- `panos_zone`: provider; full template support; checkmode

Generic updates across all modules mentioned above:
- The minimum version of `pandevice` to run all "provider" modules is 0.9.1
- Cleaned up module documentation

The following modules have been deprecated:

- `panos_admin`
- `panos_dag`
- `panos_query_rules`
- `panos_sag`

The following modules have not been modified:

- `panos_admpwd`
- `panos_cert_gen_ssh`
- `panos_dag_tags`
- `panos_import`
- `panos_loadcfg`
- `panos_object`

V2.0.4
-----

-   Released: 2019-03-11
-   Status: Released (minor)

- Fixes the DHCP param handling of panos\_interface

V2.0.3
------

-   Released: 2019-03-04
-   Status: Released

*New modules*

- panos\_api\_key: retrieve api\_key for username/password combination
- panos\_bgp: Manages basic BGP configuration settings
- panos\_bgp\_aggregate: Manages BGP Aggregation Policy Rules
- panos\_bgp\_auth: Manages BGP Authentication Profiles
- panos\_bgp\_conditional\_advertisement: Manages BGP Conditional Advertisement Policy Rules
- panos\_bgp\_dampening: Manages BGP Dampening Profiles
- panos\_bgp\_peer: Manages BGP Peers
- panos\_bgp\_peer\_group: Manages BGP Peer Groups
- panos\_bgp\_policy\_filter: Manages BGP Policy Filters, children of Aggregate and Conditional Advertisement
- panos\_bgp\_policy\_rule: Manage BGP Import/Export Rules
- panos\_bgp\_redistribute: Manages BGP Redistribution Rules
- panos\_loopback\_interface: manage loopback interfaces
- panos\_redistribution: Manages virtual router Redistribution Profiles

*Refactored modules*

- panos\_ike\_gateway: fixed misspelling of passive_mode and added additional module arguments to support more advanced configurations


V2.0.1
------

-   Released: 2018-10-08
-   Status: Released (minor)

This is minor release to address issue 
https://github.com/PaloAltoNetworks/ansible-pan/issues/163

V2.0.0
------

-   Released: 2018-09-27
-   Status: Released

*New modules*

- panos\_administrator: Manages Panorama / NGFW administrators
- panos\_registered\_ip: Use this instead of panos\_dag\_tags
- panos\_registered\_ip\_facts: Use this instead of panos\_dag\_tags
- panos\_address\_object: Use this instead of panos\_object
- panos\_address\_group: Use this instead of panos\_object
- panos\_service\_object: Use this instead of panos\_object
- panos\_service\_group: Use this instead of panos\_object
- panos\_tag\_object: Use this instead of panos\_object
- panos\_object\_facts: Get facts about objects

*Removed modules*

*Refactored modules*

**Now supporting state / idempotency**
- panos\_interface
- panos\_nat\_rule
- panos\_security\_rule

*Miscellanies / Fixes*

- merged Ansible role repo together with this one
- https://github.com/PaloAltoNetworks/ansible-pan/issues/44
- adding beta support for connections lib
- https://github.com/PaloAltoNetworks/ansible-pan/issues/150

V1.0.8
------

-   Released: 2018-09-13
-   Status: Released

*New modules*

-   panos\_management\_profile: Manages interface management profiles
-   panos\_ike\_crypto\_profile: Use the IKE Crypto Profiles page to specify protocols and algorithms for 
identification, authentication, and encryption (IKEv1 or IKEv2, Phase 1).
-   panos\_ipsec\_profile: Configures IPSec Crypto profile on the firewall with subset of settings.
-   panos\_ike\_gateway: Configures IKE gateway on the firewall with subset of settings.
-   panos\_ipsec\_tunnel: Configure data-port (DP) network interface for DHCP. By default DP interfaces are static.

*Removed modules*

*Refactored modules*

*Miscellanies*

-   *panos\_security\_rule* - New [log\_setting]{.title-ref} param added
    to specify the log forwarding profile to be used
-   re-wrote documentation 

V1.0.7
------

-   Released: 2018-05-03
-   Status: Released

*New modules*

-   panos\_userid: added ability to (un)register userid with ip address
-   panos\_software: Upgrade and downgrade PAN-OS on firewalls and
    Panorama.
-   panos\_userid: added ability to (un)register userid with ip address
-   panos\_static\_route: ability to manipulate static routing tables

*Removed modules*

N/A

*Refactored modules*

-   

    panos\_interface: Added full support for static configuration of ethernet interfaces

    :   -   <https://github.com/PaloAltoNetworks/ansible-pan/pull/61>

-   

    Add functionality to list static address groups

    :   -   <https://github.com/PaloAltoNetworks/ansible-pan/pull/64>

-   

    Pass api\_key to pandevice

    :   -   <https://github.com/PaloAltoNetworks/ansible-pan/pull/63>

-   

    panos\_security\_rule: Security Policy position/order

    :   -   <https://github.com/PaloAltoNetworks/ansible-pan/issues/14>

-   

    panos\_security\_rule: unable to add security policies in Post rule

    :   -   <https://github.com/PaloAltoNetworks/ansible-pan/issues/38>

*Miscellanies* -
<https://github.com/PaloAltoNetworks/ansible-pan/pull/78> -
<https://github.com/PaloAltoNetworks/ansible-pan/issues/22>

V1.0.6
------

-   Released: 2018-2-6
-   Status: Released

*New modules*

N/A

*Removed modules*

N/A

*Miscellanies*

-   

    Synchronized repository with RedHat Ansible official repo. Added missing modules:

    :   -   panos\_op.py
        -   panos\_dag\_tags.py
        -   panos\_query\_rules.py
        -   panos\_match\_rule.py

*Closed issues*

> -   <https://github.com/PaloAltoNetworks/ansible-pan/issues/52>
> -   <https://github.com/PaloAltoNetworks/ansible-pan/issues/46>

V1.0.5
------

-   Released: 2017-12-20
-   Status: Released

*New modules*

-   panos\_op: OP commands module that allows execution of the arbitrary
    op commands on the PANOS devices

*Refactored modules*

N/A

*Removed modules*

N/A

*Miscellanies*

N/A

*Closed issues*

\#36 <https://github.com/PaloAltoNetworks/ansible-pan/issues/36>

V1.0.4
------

-   Released: 2017-08-31
-   Status: Released

*New modules*

-   panos\_sag: Added the ability to add / delete static address groups.
-   

    panos\_dag\_tags: A new module to create registered IP to tag associations

    :   Implemented the ability to create / delete / list IP to tag
        associations

-   panos\_security\_rule
-   panos\_nat\_rule

*Refactored modules*

-   panos\_restart refactored to use PanDevice internally; supports
    Panorama
-   panos\_mgtconfig refactored to use PanDevice internally; added
    support for NTP servers config
-   

    panos\_dag: Converted the module to use pandevice

    :   Also added the ability to perform create / delete / list

*Removed modules*

-   panos\_nat\_policy (Use panos\_nat\_rule)
-   panos\_nat\_security\_policy (use panos\_security\_rule)
-   panos\_service (use panos\_object)

*Miscellanies*

-   removed deprecated\_libraries folder
-   consolidated all samples from samples/ into examples/
-   synchronized repo with core Ansible distribution

V1.0.3
------

Minor release with documentation updates and few BUG fixes.

V1.0.2
------

-   Released: 2017-04-13

Another major refactor in order to streamline the code.

-   Refactored modules
-   panos\_address \--\> panos\_object
-   panos\_match\_rule
-   panos\_nat\_policy \--\> panos\_nat\_rule
-   panos\_query\_rules
-   panos\_security\_policy \--\> panos\_security\_rule
-   panos\_service \--\> panos\_object

V1.0.1
------

-   Released: 2017-02-15
-   Status: Release

All modules have been touched and refactored to adhere to Ansible module
development practices. Documentatio has been added as well as sample
playbooks for each module.

*Refactored modules (now part of core Ansible)*

-   panos\_admin
-   panos\_admpwd
-   panos\_commit
-   panos\_restart
-   panos\_cert\_gen\_ssh
-   panos\_check
-   panos\_dag
-   panos\_service
-   panos\_mgtconfig
-   panos\_import
-   panos\_loadcfg
-   panos\_pg
-   panos\_lic
-   panos\_interface

*New modules*

-   panos\_address
-   panos\_security\_policy

*Deprecated modules*

-   panos\_srule
-   panos\_content
-   panos\_swinstall
-   panos\_tunnelif
-   panos\_cstapphost
-   panos\_gpp\_gateway
-   panos\_vulnprofile
-   panos\_swapif
-   panos\_vulnprofile

V1.0.0
------

-   Released: 2016-11-27
-   Status: Release

First release that adheres to the Ansible development practices, now
part of the Ansible core development. The modules have been completely
refactored. Some retired and some new modules created.

V0.1.3
------

-   Released: 2015-12-09
-   Status: Alpha

Bug fixes and documentation updates

Alpha
-----

-   Released: 2015-07-28
-   Status: Alpha

First alpha and documentation
