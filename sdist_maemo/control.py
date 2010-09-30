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
    def __init__(self,name,section,author,email,display_name,arch,
                    depends,suggests,description,long_description,
                    upgrade_description,
                    bugtracker,
                    icon,):       

        self.getIconContent(icon)
        self.control="""Source: %(name)s
Section: %(section)s
Priority: extra
Maintainer: %(author)s <%(email)s>
Build-Depends: debhelper (>= 5)
Standards-Version: 3.7.2

Package: %(name)s
XB-Maemo-Display-Name: %(display_name)s
Architecture: %(arch)s
Depends: %(depends)s
Suggests: %(suggests)s
Description: %(description)s
Long-Description: %(long_description)s
XB-Maemo-Upgrade-Description: %(upgrade_description)s
XSBC-Bugtracker: %(bugtracker)s
XB-Maemo-Icon26: %(iconb64)s""" % {'name':name,
                    'section':section,
                    'author':author,
                    'email':email,
                    'display_name':display_name,
                    'arch':arch,
                    'depends':depends,
                    'suggests':suggests,
                    'description':description,
                    'long_description':long_description,
                    'upgrade_description':upgrade_description,
                    'bugtracker':bugtracker,
                    'iconb64':self.iconb64}

    def getContent(self):
        return self.control

    def getIconContent(self,icon):
        try:
          import base64
          iconb64 = "\n ".join(base64.encodestring(open(icon).read()).split("\n")[0:-1])
          self.iconb64 = "\n %s" % ( iconb64 )
        except:
          self.iconb64 = ''            
    