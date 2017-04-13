#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for journal
'''
import os
_USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
_HOME = os.path.expanduser("~"+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, ".config")

from setuptools import setup

# from distutils.core import setup

setup(name="journal",
      version="1.1",
      description="",
      long_description="""Simple module to handle time-dependent data from csv
      files.
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be",
      packages=["journal"],
      license="Free for non-commercial use",
      )

