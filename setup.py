#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import gzt

setup (
    name = "Gzt",
    version = gzt.__version__,
    description="Gzt is a simple news parser",
    long_description="""Gzt is a news parser based on Flask and pywebview. It pulls the news from two different newspapers (for now) and refresh intervally.""",
    author="Şenol Alan",
    author_email="palynology@gmail.com",
    license='GNU',
    url="https://github.com/lonicera/gzt",
    entry_points = {
        'console_scripts': ['gzt=gzt.gzt_m:main'],
    },
    packages=['gzt'],
    include_package_data=True,
    zip_safe = True
)
