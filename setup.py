#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

import pyenigma

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'pyenigma'
]

scripts = [
    'bin/enigma'
]

requires = []

with open('README.rst', 'r') as f:
    readme = f.read()
with open('CHANGELOG.rst', 'r') as f:
    changelog = f.read()

setup(
    name='pyEnigma',
    version=pyenigma.__version__,
    description='Python Enigma cypher machine simulator.',
    long_description=readme + '\n\n' + changelog,
    author='Christophe Goessen, Cédric Bonhomme',
    author_email='cedric@cedricbonhomme.org',
    url='https://github.com/cedricbonhomme/pyEnigma',
    packages=packages,
    package_dir={'pyenigma': 'pyenigma'},
    include_package_data=True,
    scripts=scripts,
    install_requires=requires,
    license='GPLv3',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ),
)
