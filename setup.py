#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtEditor Setup File
import imp

from sdist_maemo import sdist_maemo as _sdist_maemo
from distutils.core import setup

setup(name='python-sdist-maemo',
      version='0.0.1',
      
      license='GNU GPLv3',
      description='A distutil extension to build maemo source package.',
      long_description='A distutil extension to build maemo source package to be used by the MeeGo OBS or the Maemo Extras AutoBuilder',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      maintainer='Benoît HERVIER',
      maintainer_email='khertan@khertan.net',
      url='http://www.khertan.net/sdist_maemo',
      requires=['python','setuptools'],
      packages= ['sdist_maemo',],
      cmdclass={'sdist_maemo': _sdist_maemo},      
      options = { 'sdist_maemo':{
      'buildversion':'3',
      'depends':'python2.5, python-setuptools',
      'XSBC_Bugtracker':'http://khertan.net/sdict_maemo:bugs',
      'XB_Maemo_Display_Name':'Python sdist_maemo',
      }}
      
      )

