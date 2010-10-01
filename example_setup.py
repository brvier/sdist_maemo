#
# example_setup.py
#
# Example use of 'sdist_maemo' command.
#
#  Author: khertan@khertan.net
#
#    Date: 1 October 2010
#
# License: GPLv3
#

from sdist_maemo import sdist_maemo as _sdist_maemo
from distutils.core import setup

setup(name="example",
      scripts=['example'],
      version='0.0.1',
      maintainer="Khertan",
      maintainer_email="khertan@khertan.net",
      description="An example.",
      long_description=\
         "An example packed with sdist_maemo--the pure Python packager!",
      data_files = [('share/applications/hildon', ['example.desktop'])],
      cmdclass={'sdist_maemo': _sdist_maemo})


            

