#!/bin/sh

####
# This script copies modules that are changed. Run it with caution as it
# will overwrite destination files

# batch 1
rsync ../library/__init__.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_admin.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_admpwd.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_commit.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_restart.py ../../ansible-modules-extras/network/panos/

# batch 2
rsync ../library/panos_cert_gen_ssh.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_check.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_dag.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_lic.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_nat.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_mgtconfig.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_swapif.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_swinstall.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_loadcfg.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_content.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_import.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_dhcpif.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_pg.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_service.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_tunnelif.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_vulnprofile.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_cstapphost.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_gpp_gateway.py ../../ansible-modules-extras/network/panos/
