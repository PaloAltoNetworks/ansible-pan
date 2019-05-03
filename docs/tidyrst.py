from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys


def usage():
    x = [
        'Usage: tidyrst.py <filename>',
        '',
        'This script tweaks a .rst file output by Ansible\'s plugin_formatter.py',
        'such that it is suitable to be published on readthedocs.',
    ]
    print('\n'.join(x))

def main():
    if len(sys.argv) != 2 or sys.argv[1] in ('-h', '--help', '?'):
        usage()
        return

    with open(sys.argv[1], 'r') as fd:
        lines = fd.readlines()

    with open(sys.argv[1], 'w') as fd:
        for line in lines:
            if '<modules_support>' in line:
                fd.write('- This module is `maintained by the Ansible Community <https://docs.ansible.com/ansible/latest/user_guide/modules_support.html#modules-support>`_.\n')
            elif '<common_return_values>' in line:
                fd.write('Common return values are `documented here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:\n')
            elif '.. hint::' in line or 'edit this document' in line:
                continue
            else:
                fd.write(line)


if __name__ == '__main__':
    main()
