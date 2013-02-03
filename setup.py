#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

import pyenigma

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'pyenigma'
]

requires = []

setup(
    name='pyEnigma',
    version=pyenigma.__version__,
    description='Python Enigma cypher machine simulator.',
    long_description=open('README.md').read(),
    author='Christophe Goessen, Cédric Bonhomme',
    author_email='kimble.mandel@gmail.com',
    url='https://bitbucket.org/azmaeve/pyenigma',
    packages=packages,
    #package_data={'': ['LICENSE', 'NOTICE'], 'pyenigma': ['*.pem']},
    package_dir={'pyenigma': 'pyenigma'},
    include_package_data=True,
    install_requires=requires,
    license=open('COPYING').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)