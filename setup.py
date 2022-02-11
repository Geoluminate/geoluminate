#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, find_packages
from setuptools import setup
from core import __version__

REPO_URL = "https://github.com/SSJenny90/core"

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='core',
    packages=find_packages(),
    include_package_data=True,
    version=__version__,
    author='Sam Jennings',
    author_email='samuel.jennings@pm.me',
    license='MIT',
    description='Core functionality and patches for Django projects',
    url=REPO_URL,
    install_requires=[
        "Django>=3,<4",    
        ],
    keywords='scientific django',
    classifiers=[
        'Development Status :: 1 - Development',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)