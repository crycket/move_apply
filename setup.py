#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="move_apply", packages=find_packages('src'), install_requires=['fabric2', 'pytest'])
