#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for journal
'''
import journal

from distutils.core import setup

setup(name="journal",
      version=journal.__version__,
      description="",
      long_description="""
      Simple module to ...
      """,
      author="Julien Spronck",
      author_email="frenticb@hotmail.com",
      url="http://frenticb.com/",
      packages=["journal"],
      license="Free for non-commercial use",
     )

