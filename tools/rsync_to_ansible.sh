#!/bin/sh

####
# This script copies modules that are changed. Run it with caution as it
# will overwrite destination files

rsync ../library/__init__.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_admin.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_admpwd.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_commit.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_restart.py ../../ansible-modules-extras/network/panos/
