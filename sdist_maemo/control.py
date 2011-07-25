#
# sdist_maemo
#
# Script to add 'sdist_maemo' source package distribution command to
# 'distutils'. This command builds '.dsc, .changes, .tar.gz' packages suitable for installation
# on the Maemo platform by the Maemo autobuilder or the community obs.
#
# Author: khertan@khertan.net
# License: GPL 3.0
#
# (Based on standard Python-supplied 'command_template' file.)

'''Generate the control content'''

import os
import sys

class Control:
    def __init__(self,name,section,maintainer,email,arch,
                    depends,suggests,description,long_description,
                    conflicts,
                    replaces, optionnal = {}):

        self.control="""Source: %(name)s
Section: %(section)s
Priority: extra
Maintainer: %(maintainer)s <%(email)s>
Build-Depends: debhelper (>= 5)
Standards-Version: 3.7.2

Package: %(name)s
Architecture: %(arch)s""" % {'name':name,
                    'section':section,
                    'maintainer':maintainer,
                    'email':email,
                    'display_name':display_name,
                    'arch':arch,}

        if depends:
            self.control = self.control + '\nDepends: %s' % depends
        if suggests:
            self.control = self.control + '\nSuggests: %s' % suggests
        if conflicts:
            self.control = self.control + '\nConflicts: %s' % conflicts
        if replaces:
            self.control = self.control + '\nReplaces: %s' % replaces
        if description:
            self.control = self.control + '\nDescription: %s' % description

        for key, value in optionnal:
            if key and value:
                self.control = self.control + '\n%s: %s' % (key, value)

    def getContent(self):
        print self.control
        return self.control

