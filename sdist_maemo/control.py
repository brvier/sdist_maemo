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
    def __init__(self,name,section,maintainer,email,display_name,arch,
                    depends,suggests,description,long_description,
                    upgrade_description,
                    bugtracker,
                    icon,
                    conflicts,
                    replaces):       

        self.control="""Source: %(name)s
Section: %(section)s
Priority: extra
Maintainer: %(maintainer)s <%(email)s>
Build-Depends: debhelper (>= 5)
Standards-Version: 3.7.2

Package: %(name)s
XB-Maemo-Display-Name: %(display_name)s
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
        if upgrade_description:
            self.control = self.control + '\nXB-Maemo-Upgrade-Description: %s' % upgrade_description
        if bugtracker:
            self.control = self.control + '\nXSBC-Bugtracker: %s' % bugtracker
        iconb64 = self.getIconContent(icon)
        if iconb64:
            self.control = self.control + '\nXB-Maemo-Icon-26: %s' % iconb64

    def getContent(self):
        print self.control
        return self.control

    def getIconContent(self,icon):
        try:
          import base64
          iconb64 = "\n ".join(base64.encodestring(open(icon).read()).split("\n")[0:-1])
          return "\n %s" % ( iconb64 )
        except:
          return ''            
    
