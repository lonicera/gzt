#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import gzt


setup(
    name='Gzt',
    version='1.0',
    long_description=__doc__,
    packages=['gzt'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    entry_points = {
            'console_scripts': ['gzt=gzt.main'],
        },
)
