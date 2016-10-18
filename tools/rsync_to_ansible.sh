#!/bin/sh

####
# This script copies modules that are changed

rsync ../library/__init__.py ../../ansible-modules-extras/network/panos/
rsync ../library/panos_admin.py ../../ansible-modules-extras/network/panos/
#rsync ../library/panos_admpwd ../../ansible-modules-extras/network/panos/
