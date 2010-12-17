#!/usr/bin/python
# -*- coding: utf-8 -*-

import imp
import sys
reload(sys).setdefaultencoding("UTF-8")

#Remove pyc and pyo file
import glob,os
for fpath in glob.glob('*/*.py[c|o]'):
    os.remove(fpath)

from sdist_maemo import sdist_maemo as _sdist_maemo
from distutils.core import setup
from sdist_maemo import sdist_maemo
setup(name='python-sdist-maemo',
      version=sdist_maemo.__version__,
      
      license='GNU GPLv3',
      description='A distutil extension to build maemo source package.',
      long_description='A distutil extension to build maemo source package to be used by the MeeGo OBS or the Maemo Extras AutoBuilder',
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      maintainer=u'Benoît HERVIER',
      maintainer_email='khertan@khertan.net',
      url='http://www.khertan.net/sdist_maemo',
      requires=['python','setuptools'],
      packages= ['sdist_maemo',],
      cmdclass={'sdist_maemo': _sdist_maemo},      
      options = { 'sdist_maemo':{
      'buildversion':'1',
      'depends':'python2.5, python-setuptools',
      'XSBC_Bugtracker':'http://khertan.net/sdict_maemo:bugs',
      'XB_Maemo_Display_Name':'Python sdist_maemo',
      'XB_Maemo_Icon_26':'',
      'changelog':'* Fix path of file created',
      'copyright':'gpl'},},
      classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",]
      )

