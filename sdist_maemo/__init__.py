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

'''distutils.command.sdist_maemo

Implements the Distutils 'sdist_maemo' command.
'''

from distutils.core import Command
from distutils.file_util import copy_file
from rules import Rules
from changelog import Changelog
from control import Control
from datetime import datetime

import os

class sdist_maemo(Command):
    # Brief (40-50 characters) description of the command
    description = "Maemo source package"

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [('name=', None,
                     "Package name"),
                    ('buildversion=', None,
                     "Package buildversion"),
                    ('section=', None,
                     "Section (Only 'user/*' will display in AI usually)"),
                    ('priority=', None,
                     "Priority"),
                    ('architecture=', None,
                     "Architecture"),
                    ('depends=', None,
                     "Other Debian package dependencies (comma separated)"),
                    ('changelog=', None,
                     "ChangeLog"), 
                    ('XSBC-Bugtracker=', None,
                     "URI of the bug tracker"),
                    ('XB-Maemo-Upgrade-Description=', None,
                     "Upgrade description"),
                    ('XB-Maemo-Display-Name=', None,
                     "Display name"),
                    ('XB-Maemo-Icon-26=', None,
                     "Maemo package icon"),
                    ('postinst=', None,
                     "Post install script"),
                    ('postre=', None,
                     "Post remove script"),
                    ('prere=', None,
                     "Pre remove script"),
                    ('preinst=', None,
                     "Pre install script"),
                    ('XB-Maemo-Upgrade-Description=', None,
                     "Upgrade description"),
                    ('Suggests=', None,
                     "Suggests dependancies"),
                   ]

    def initialize_options (self):
        self.dist_dir = None
        self.section = None
        self.priority = None
        self.architecture = None
        self.depends = None
        self.suggests = None
        self.buildversion = None
        self.changelog = None
        self.XB_Maemo_Icon_26 = None
        self.XB_Maemo_Display_Name = None
        self.XSBC_Bugtracker = None
        self.XB_Maemo_Upgrade_Description = None
        self.postinst = None
        self.preinst = None
        self.prere = None
        self.postre = None
        
    def finalize_options (self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

        if self.section is None:
            self.section = "user/other"

        if self.priority is None:
            self.priority = "optional"

        if self.architecture is None:
            self.architecture = "all"

        self.maintainer = "%s <%s>" % \
                          (self.distribution.get_maintainer(),
                           self.distribution.get_maintainer_email())


        if self.depends is None:
            self.depends = "python2.5,"

        if self.suggests is None:
            self.suggests = ''

        if self.changelog is None:
            self.changelog = ""
            
        self.name = self.distribution.get_name()
        self.description = self.distribution.get_description()
        self.long_description = self.distribution.get_long_description()
        self.version = self.distribution.get_version()

        if self.buildversion is None:
            self.buildversion = "1"
            
        if self.XB_Maemo_Icon_26 is None:
            self.XB_Maemo_Icon_26 = ''
            
        if self.XB_Maemo_Display_Name is None:
            self.XB_Maemo_Display_Name = self.distribution.get_name()
            
        if self.XSBC_Bugtracker is None:
            self.XSBC_Bugtracker = ''
        
        if self.XB_Maemo_Upgrade_Description is None:
            self.XB_Maemo_Upgrade_Description = ''
           
    def mkscript( name , dest ):
        if name and name.strip()!="":
            if (os.path.isfile(name)):# or (os.path.isfile(os.path.join(CURRENT,name))):    # it's a file
                content = file(name).read()
            else:   # it's a script
                content = name
            print dest
            open(dest,"w").write(content)
              
    def run (self):
        """
        """

        #Create folders and copy sources files
        DEBIAN_DIR = os.path.join(self.dist_dir,'debian')
        DATA_DIR = os.path.join(self.dist_dir,self.name)
        
        try:
            os.makedirs(DEBIAN_DIR)
        except: # TODO: Check exception is exists
            pass
            
        try:
            os.makedirs(os.path.join(DATA_DIR,'usr','bin'))
        except StandardError,e: # TODO: Check exception is exists
            print e
            
        for script in self.distribution.scripts:
            copy_file(script, os.path.join(DATA_DIR,'usr','bin'))

        for theDir, theFiles in self.distribution.data_files:
            fulldirpath = os.path.join(DATA_DIR,'usr', theDir)
            try:
                os.makedirs(fulldirpath)
            except: # TODO: Check exception is exists
                pass

            for currFile in theFiles:
                copy_file(currFile, fulldirpath)

        #Create the debian rules
        rules = Rules(self.name,DATA_DIR)
        dirs = rules.dirs
        open(os.path.join(DEBIAN_DIR,"rules"),"w").write(rules.getContent())
        os.chmod(os.path.join(DEBIAN_DIR,"rules"),0755)

        #Create the debian compat
        open(os.path.join(DEBIAN_DIR,"compat"),"w").write("5\n")
          
        #Create the debian dirs
        open(os.path.join(DEBIAN_DIR,"dirs"),"w").write("\n".join(dirs))
                 
        #Create the debian changelog
        d=datetime.now()
        self.buildDate=d.strftime("%a, %d %b %Y %H:%M:%S +0000")
        clog = Changelog(self.name,self.version,self.buildversion,self.changelog,self.distribution.get_maintainer(),self.distribution.get_maintainer_email(),self.buildDate)
        open(os.path.join(DEBIAN_DIR,"changelog"),"w").write(clog.getContent())
          
        #Create the pre/post inst/rm Script
        if self.preinst is not None:
            mkscript(self.preinst ,os.path.join(DEBIAN_DIR,"preinst"))
        if self.postinst is not None:
            mkscript(self.postinst,os.path.join(DEBIAN_DIR,"postinst"))
        if self.prere is not None:
            mkscript(self.prere  ,os.path.join(DEBIAN_DIR,"prerm"))
        if self.postre is not None:
            mkscript(self.postre ,os.path.join(DEBIAN_DIR,"postrm"))

        #Create the control file
        control = Control(self.name,
                    self.section,
                    self.distribution.get_maintainer(),
                    self.distribution.get_maintainer_email(),
                    self.XB_Maemo_Display_Name,
                    self.architecture,
                    self.depends,
                    self.suggests,
                    self.description,
                    self.long_description,
                    self.XB_Maemo_Upgrade_Description,
                    self.XSBC_Bugtracker,
                    self.XB_Maemo_Icon_26,
                    )
        open(os.path.join(DEBIAN_DIR,"control"),"w").write(control.getContent())

         
         

        