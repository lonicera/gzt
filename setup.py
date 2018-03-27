#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import gzt


setup(
    name='Gzt',
    version='1.0',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    entry_points = {
            'console_scripts': ['gzt=gzt.main'],
        },
    install_requires=['Flask', 'pywebview', 'bs4', 'urllib3'],
    packages=find_packages(),
)
