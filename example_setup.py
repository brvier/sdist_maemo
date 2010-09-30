#
# example_setup.py
#
# Example use of 'bdist_maemo' command.
#
#  Author: follower@rancidbacon.com
#
#    Date: 15 September 2006
#
# License: BSD
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


            

