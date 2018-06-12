from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ansible-pan',
    version='1.0.1',
    packages=['library'],
    # The project's main homepage.
    url='https://github.com/PaloAltoNetworks/ansible-pan',
    license='Apache V2.0',
    author='@ivanbojer',
    author_email='ijb@networkrift.com',
    description='Set ot Ansible modules for Palo Alto Networks device configuration',
    long_description=long_description,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'pan-python>=0.10.0',
        'pandevice>=0.6.0',
        'xmltodict',
    ],
)
