.. :changelog:
.. |biohazard| image:: images/biohazard.png

History
=======

V1.0.1
______

- Released: 2017-02-15
- Status: Release

All modules have been touched and refactored to adhere to Ansible module development practices. Documentatio
has been added as well as sample playbooks for each module.

*Refactored modules (now part of core Ansible)*

* panos_admin
* panos_admpwd
* panos_commit
* panos_restart
* panos_cert_gen_ssh
* panos_check
* panos_dag
* panos_service
* panos_mgtconfig
* panos_import
* panos_loadcfg
* panos_pg
* panos_lic
* panos_interface

*New modules*

* panos_address
* panos_security_policy

*Deprecated modules* |biohazard|

* panos_srule
* panos_content
* panos_swinstall
* panos_tunnelif
* panos_cstapphost
* panos_gpp_gateway
* panos_vulnprofile
* panos_swapif
* panos_vulnprofile


V1.0.0
______

- Released: 2016-11-27
- Status: Release

First release that adheres to the Ansible development practices, now part of the Ansible core development. The modules
have been completely refactored. Some retired and some new modules created.

V0.1.3
______

- Released: 2015-12-09
- Status: Alpha

Bug fixes and documentation updates

Alpha
_____

- Released: 2015-07-28
- Status: Alpha

First alpha and documentation
