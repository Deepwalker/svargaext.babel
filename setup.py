#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import svargaext.babel

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'svargaext.babel',
    description = 'babel module for Svarga framework',
    long_description = read('README'),
    license = 'BSD',
    version = svargaext.babel.__version__,
    author = svargaext.babel.__author__,
    author_email = svargaext.babel.__email__,
    url = '',
    packages = find_packages(),
    namespace_packages = ['svargaext'],
    install_requires = ['svarga'],
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Svarga',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    platforms='any',
    )
