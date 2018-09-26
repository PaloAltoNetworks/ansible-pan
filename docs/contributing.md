# Developing Palo Alto Networks Ansible Modules

(draft)

## Should you develop a module?

Developing PANW Ansible modules is easy, but often it isn't necessary. Before you start writing a new module, ask:

#### Does a similar module already exist?

An existing module may cover the functionality you want. You might just need additional functionality in the existing
module. If you are not sure feel free to email PANW maintainers.

#### Does a Pull Request already exist?

An existing Pull Request may cover the functionality you want. If someone else has already started developing a similar 
module, you can review and test it.

* GitHub new module PRs <https://github.com/PaloAltoNetworks/ansible-pan/pulls>
* Already closed bun not yet released modules <https://github.com/PaloAltoNetworks/ansible-pan/blob/develop/docs/history.md>

If you find an existing PR that looks like it addresses your needs, please provide feedback on the PR. Community feedback 
speeds up the review and merge process.

#### Should you write multiple modules instead of one module?

The functionality you want may be too large for a single module. You might want to split it into separate modules or
enhance already existing module.

## Contributing to codebase

If your use case isn't covered by an existing module or an open PR then you're ready to start developing a new module.

In order to do this you need to (draft):
1. fork develop branch (**NOT MASTER**)
2. do your changes
    - update / change module
    - update [history.md](https://github.com/PaloAltoNetworks/ansible-pan/blob/develop/docs/history.md) with changes
    - make sure you run code through linter (TBD)
3. create pull request against **DEVELOP** branch
    - sometimes it is necessary to rebase your changes. If you need more info on how to this here is a good write-up
    that can be applied in our case <https://docs.ansible.com/ansible/2.5/dev_guide/developing_rebasing.html>
