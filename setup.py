#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File
import imp

from distutils.core import setup

setup(name='sdist_maemo',
      version='0.0.1',
      license='GNU GPLv3',
      description='A distutil extension to build maemo source package.',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      url='http://www.khertan.net/sdist_maemo',
      requires=['python','setuptools'],
      packages= ['sdist_maemo',],
     )

