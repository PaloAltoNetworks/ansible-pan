from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys


HEADER = '''.. _module_reference:

****************
Module Reference
****************

.. toctree::
   :maxdepth: 1

'''


def usage():
    x = [
        'Usage: python mkmodref.py',
        '',
        'This script creates the modules reference in the modules directory.',
    ]
    print('\n'.join(x))

def main():
    if len(sys.argv) != 1:
        usage()
        return

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
    files = [x.split('.')[0] for x in os.listdir(path)]

    with open(os.path.join(path, 'index.rst'), 'w') as fd:
        fd.write(HEADER)
        for x in sorted(os.listdir(path)):
            if not x.startswith('panos_') or not x.endswith('.rst'):
                continue
            link = x.split('.')[0]
            fd.write('   {0}\n'.format(link))


if __name__ == '__main__':
    main()
