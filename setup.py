#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import gzt

setup (
    name = "GZT",
    version = gzt.__version__,
    description="GZT is a simple news parser",
    long_description="""GZT is a news parser based on Flask and pywebview. It pulls the news from two different newspapers (for now) and refresh intervally.""",
    author="Şenol Alan",
    author_email="palynology@gmail.com",
    license='GNU',
    url="https://github.com/lonicera/gzt",
    entry_points = {
        'console_scripts': ['gzt=gzt.gzt:main'],
    },
    packages=['gzt'],
    include_package_data=True,
    zip_safe = True
)
