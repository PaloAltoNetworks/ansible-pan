---
title: History and changelog
---

History
=======

V2.0.2
------

-   Released: In development
-   Status: In development

*New modules*

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
- panos_redistribution: Manages virtual router Redistribution Profiles

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
