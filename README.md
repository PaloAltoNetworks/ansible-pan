# Palo Alto Networks Ansible modules

[![Build Status](https://travis-ci.org/PaloAltoNetworks/ansible-pan.svg?branch=develop)](https://travis-ci.org/PaloAltoNetworks/ansible-pan)

A collection of Ansible modules that automate configuration and
operational tasks on Palo Alto Networks Next Generation Firewalls --
both physical and virtualized form factor. The underlying protocol uses
API calls that are wrapped within the Ansible framework.

-   Free software: Apache 2.0 License
-   Documentation:
    <https://paloaltonetworks.github.io/ansible-pan/>
-   PANW community supported live page:
    <http://live.paloaltonetworks.com/ansible>

## Installation

PANW PANOS Ansible modules are part of the default Ansible distribution
which is available at:

> <https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/panos>

It is also available as free **Apache 2.0** licensed code from Palo Alto
Networks Github repo. This repo usually contains the newest feature and
bug fixes and it is synchronised with official RedHat Ansible repo upon
every new Ansible release.

> <https://github.com/PaloAltoNetworks/ansible-pan/>

Or as ansible role installed from ansible-galaxy

    ansible-galaxy install PaloAltoNetworks.paloaltonetworks

## Sample playbooks

Sample playbooks can be found within this repo under:

    /examples
    (e.g. /examples/fw_dag.yml)

More comprehensive playbooks can be found under:

    /ansible-playbooks/

## Documentation

Each module is documented in docs/modules, you can also look at the
documentation online at
<https://paloaltonetworks.github.io/ansible-pan/> under *modules* section

## Developing modules / contributing to codebase

Please see:
> <http://paloaltonetworks.github.io/ansible-pan/contributing.html>

## Ansible galaxy role

The Palo Alto Networks Ansible modules project is a collection of Ansible modules to automate configuration and
operational tasks on Palo Alto Networks *Next Generation Firewalls*. The underlying protocol uses API calls that are wrapped within Ansible framework.

> <https://github.com/PaloAltoNetworks/ansible-pan/>
