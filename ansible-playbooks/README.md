# ansible-playbooks

This repo contains a variety of Ansible playbooks related to the deployment and configuration of Palo Alto Networks 
Next Generation Devices. Each playbook contains easy steps on how to use it in its header.

The structure of the folders is as following:

    root/
    |---custom/ (files shared between various playbooks)
    |
    |---aws/ (playbooks related to AWS deployments/configurations)
    |   |
    |   |---provision_fw_w_srule.yml
    |
    |---srules/ (various security rule examples)
    |   |
    |   |---playbook_set_srule.yml
    |   |---playbook_set_complex_rule.yml
    |
    |---one_click_multicloud/ (used in conjuction with terraform)
    |   |
    |   |---one_click_aws.yml
    |   |---one_click_azure.yml
    

##### More examples:
https://github.com/PaloAltoNetworks/ansible-pan/tree/master/examples
