# -*- coding: utf-8 -*-
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
from distutils.dir_util import copy_tree, remove_tree, mkpath
from rules import Rules
from changelog import Changelog
from control import Control
from datetime import datetime
from licence import Licence
from changes import Changes
from dsc import Dsc
import time
import os

def copy_directory(source, target):
    print 'copy dir %s -> %s' % (source, target)
    if not os.path.exists(target):
        os.makedirs(target)
    for afile in os.listdir(source):
        src_file = os.path.join(source,afile)
        if not os.path.isdir(src_file):
            copy_file(src_file, os.path.join(target,afile))


class sdist_maemo(Command):

    SECTIONS="user/desktop, user/development, user/education, user/games, user/graphics, user/multimedia, user/navigation, user/network, user/office, user/science, user/system, user/utilities, accessories, communication, games, multimedia, office, other, programming, support, themes, tools".split(", ")
    ARCHS="all any armel i386 ia64 alpha amd64 armeb arm hppa m32r m68k mips mipsel powerpc ppc64 s390 s390x sh3 sh3eb sh4 sh4eb sparc darwin-i386 darwin-ia64 darwin-alpha darwin-amd64 darwin-armeb darwin-arm darwin-hppa darwin-m32r darwin-m68k darwin-mips darwin-mipsel darwin-powerpc darwin-ppc64 darwin-s390 darwin-s390x darwin-sh3 darwin-sh3eb darwin-sh4 darwin-sh4eb darwin-sparc freebsd-i386 freebsd-ia64 freebsd-alpha freebsd-amd64 freebsd-armeb freebsd-arm freebsd-hppa freebsd-m32r freebsd-m68k freebsd-mips freebsd-mipsel freebsd-powerpc freebsd-ppc64 freebsd-s390 freebsd-s390x freebsd-sh3 freebsd-sh3eb freebsd-sh4 freebsd-sh4eb freebsd-sparc kfreebsd-i386 kfreebsd-ia64 kfreebsd-alpha kfreebsd-amd64 kfreebsd-armeb kfreebsd-arm kfreebsd-hppa kfreebsd-m32r kfreebsd-m68k kfreebsd-mips kfreebsd-mipsel kfreebsd-powerpc kfreebsd-ppc64 kfreebsd-s390 kfreebsd-s390x kfreebsd-sh3 kfreebsd-sh3eb kfreebsd-sh4 kfreebsd-sh4eb kfreebsd-sparc knetbsd-i386 knetbsd-ia64 knetbsd-alpha knetbsd-amd64 knetbsd-armeb knetbsd-arm knetbsd-hppa knetbsd-m32r knetbsd-m68k knetbsd-mips knetbsd-mipsel knetbsd-powerpc knetbsd-ppc64 knetbsd-s390 knetbsd-s390x knetbsd-sh3 knetbsd-sh3eb knetbsd-sh4 knetbsd-sh4eb knetbsd-sparc netbsd-i386 netbsd-ia64 netbsd-alpha netbsd-amd64 netbsd-armeb netbsd-arm netbsd-hppa netbsd-m32r netbsd-m68k netbsd-mips netbsd-mipsel netbsd-powerpc netbsd-ppc64 netbsd-s390 netbsd-s390x netbsd-sh3 netbsd-sh3eb netbsd-sh4 netbsd-sh4eb netbsd-sparc openbsd-i386 openbsd-ia64 openbsd-alpha openbsd-amd64 openbsd-armeb openbsd-arm openbsd-hppa openbsd-m32r openbsd-m68k openbsd-mips openbsd-mipsel openbsd-powerpc openbsd-ppc64 openbsd-s390 openbsd-s390x openbsd-sh3 openbsd-sh3eb openbsd-sh4 openbsd-sh4eb openbsd-sparc hurd-i386 hurd-ia64 hurd-alpha hurd-amd64 hurd-armeb hurd-arm hurd-hppa hurd-m32r hurd-m68k hurd-mips hurd-mipsel hurd-powerpc hurd-ppc64 hurd-s390 hurd-s390x hurd-sh3 hurd-sh3eb hurd-sh4 hurd-sh4eb hurd-sparc".split(" ")
    LICENSES=["gpl","lgpl","bsd","artistic","shareware"]

    __version__ = '0.1.2'

    # Brief (40-50 characters) description of the command
    description = "Maemo source package"

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [('name=', None,
                     "Python Package name"),
                     ('debian-package=', None,
                     "Debian Package name"),
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
                    ('Maemo-Bugtracker=', None,
                     "URI of the bug tracker"),
                    ('Maemo-Display-Name=', None,
                     "Display name"),
                    ('Maemo-Upgrade-Description=', None,
                     "Upgrade description"),
                    ('Maemo-Icon-26=', None,
                     "Maemo package icon"),
                    ('Maemo-Flags=', None,
                     "Maemo specifics flags"),
                    ('MeeGo-Desktop-Entry-Filename=', None,
                     "MeeGo specifics entry filename or filepath"),
                    ('postinst=', None,
                     "Post install script"),
                    ('postre=', None,
                     "Post remove script"),
                    ('prere=', None,
                     "Pre remove script"),
                    ('preinst=', None,
                     "Pre install script"),
                    ('Suggests=', None,
                     "Suggests dependancies"),
                    ('Replaces=', None,
                     "Replaces package"),
                    ('Conflicts=', None,
                     "Conflicts package"),
                    ('copyright=', None,
                     "Licence copyright"),
                    ('install-purelib=', None,
                     "Override the module install path to allow packaging from alternative platforms"),
                    ('dist-dir=', 'd',
                     "directory to put the source distribution archive(s) in [default: dist]"),
                   ]

    def initialize_options (self):
        self.dist_dir = None
        self.install_purelib = None
        self.debian_package = None
        self.build_dir = None
        self.section = None
        self.priority = None
        self.copyright = None
        self.architecture = None
        self.depends = None
        self.suggests = None
        self.buildversion = None
        self.changelog = None
        self.Maemo_Icon_26 = None
        self.Maemo_Display_Name = None
        self.Maemo_Bugtracker = None
        self.Maemo_Upgrade_Description = None
        self.Maemo_Flags = None
        self.MeeGo_Desktop_Entry_Filename = None
        self.postinst = None
        self.preinst = None
        self.prere = None
        self.postre = None
        self.repository = None
        self.urgency = None
        self.conflicts = None
        self.replaces = None

    def finalize_options (self):
        self.set_undefined_options('sdist', ('dist_dir', 'dist_dir'))

        if self.build_dir is None:
            self.build_dir = "build"

        if self.section is None:
            self.section = "user/other"

        if self.section not in self.SECTIONS:
            print "WARNING section '%s' is unknown (%s)" % (self.section,str(self.SECTIONS))

        if self.architecture not in self.ARCHS:
            print "WARNING arch '%s' is unknown (%s)"% (self.architecture,str(self.ARCHS))

        if self.copyright not in self.LICENSES:
            print "WARNING License '%s' is unknown (%s)" % (self.copyright,str(self.LICENSES))

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

        if self.conflicts is None:
            self.conflicts = ''

        if self.replaces is None:
            self.replaces = ''

        if self.copyright is None:
            self.copyright = 'gpl'

        if self.changelog is None:
            self.changelog = ""

        #clean changelog (add 2 spaces before each next lines)
        self.changelog=self.changelog.replace("\r","").strip()
        self.changelog = "\n  ".join(self.changelog.split("\n"))

        self.name = self.distribution.get_name()

        if self.debian_package is None:
            self.debian_package = self.name

        self.description = self.distribution.get_description()
        self.long_description = self.distribution.get_long_description()

        #clean description (add a space before each next lines)
        self.description=self.description.replace("\r","").strip()
        self.description = "\n ".join(self.description.split("\n"))

        #clean long_description (add a space before each next lines)
        self.long_description=self.long_description.replace("\r","").strip()
        self.long_description = "\n ".join(self.long_description.split("\n"))

        self.version = self.distribution.get_version()

        if self.repository is None:
            self.repository = 'Extras'

        if self.urgency is None:
            self.urgency = 'low'

        if self.buildversion is None:
            self.buildversion = "1"

        if self.Maemo_Icon_26 is None:
            self.Maemo_Icon_26 = ''

        if self.Maemo_Display_Name is None:
            self.Maemo_Display_Name = self.distribution.get_name()

        if self.Maemo_Bugtracker is None:
            self.Maemo_Bugtracker = ''

        if self.Maemo_Upgrade_Description is None:
            self.Maemo_Upgrade_Description = ''

        if self.MeeGo_Desktop_Entry_Filename is None:
            self.Maemo_Upgrade_Description = ''

        if self.Maemo_Flags is None:
            self.Maemo_Flags = 'visible'

        #clean long_description (add a space before each next lines)
        self.Maemo_Upgrade_Description=self.Maemo_Upgrade_Description.replace("\r","").strip()
        self.Maemo_Upgrade_Description = "\n ".join(self.Maemo_Upgrade_Description.split("\n"))

    def mkscript(self, name , dest):
        if name and name.strip() != "":
            if os.path.isfile(name):# or (os.path.isfile(os.path.join(CURRENT,name))):    # it's a file
                content = file(name).read()
            else:   # it's a script
                content = name
            print dest
            open(dest,"w").write(content)

    def getIconContent(self,icon):
        try:
          import base64
          iconb64 = "\n ".join(base64.encodestring(open(icon).read()).split("\n")[0:-1])
          return "\n %s" % ( iconb64 )
        except:
          return ''

    def run (self):
        """
        """

        #Create folders and copy sources files
        DEBIAN_DIR = os.path.join(self.build_dir,'debian')
        DATA_DIR = os.path.join(self.build_dir,self.debian_package)

        mkpath(DEBIAN_DIR)
        mkpath(self.dist_dir)
        #mkpath(os.path.join(DATA_DIR,'usr','bin'))

        self.bdist_dir = DATA_DIR
        install = self.reinitialize_command('install', reinit_subcommands=1)
        install.root = self.bdist_dir
        if self.install_purelib is not None:
            install.install_purelib = self.install_purelib
        install.skip_build = 0
        install.warn_dir = 1

        self.run_command('install')

        #Create the debian rules
        rules = Rules(self.debian_package,DATA_DIR)
        dirs = rules.dirs
        open(os.path.join(DEBIAN_DIR,"rules"),"w").write(unicode(rules.getContent()).encode('utf-8'))
        os.chmod(os.path.join(DEBIAN_DIR,"rules"),0755)

        #Create the debian compat
        open(os.path.join(DEBIAN_DIR,"compat"),"w").write("5\n")

        #Create the debian dirs
        open(os.path.join(DEBIAN_DIR,"dirs"),"w").write("\n".join(dirs))

        #Create the debian changelog
        d=datetime.now()
        self.buildDate=d.strftime("%a, %d %b %Y %H:%M:%S +0000")
        clog = Changelog(self.debian_package,self.version,self.buildversion,self.changelog,self.distribution.get_maintainer(),self.distribution.get_maintainer_email(),self.buildDate)
        open(os.path.join(DEBIAN_DIR,"changelog"),"w").write(unicode(clog.getContent()).encode('utf-8'))

        #Create the pre/post inst/rm Script
        if self.preinst is not None:
            self.mkscript(self.preinst ,os.path.join(DEBIAN_DIR,"preinst"))
        if self.postinst is not None:
            self.mkscript(self.postinst,os.path.join(DEBIAN_DIR,"postinst"))
        if self.prere is not None:
            self.mkscript(self.prere  ,os.path.join(DEBIAN_DIR,"prerm"))
        if self.postre is not None:
            self.mkscript(self.postre ,os.path.join(DEBIAN_DIR,"postrm"))

        #Create the control file
        control = Control(self.debian_package,
                    self.section,
                    self.distribution.get_maintainer(),
                    self.distribution.get_maintainer_email(),
                    self.architecture,
                    self.depends,
                    self.suggests,
                    self.description,
                    self.long_description,
                    self.conflicts,
                    self.replaces,

                    optionnal = {
                        'XB-Maemo-Display-Name':self.Maemo_Display_Name,
                        'XB-Maemo-Upgrade-Description':self.Maemo_Upgrade_Description,
                        'XSBC-Bugtracker':self.Maemo_Bugtracker,
                        'XB-Maemo-Icon-26':self.getIconContent(self.Maemo_Icon_26),
                        'XB-Maemo-Flags':self.Maemo_Flags,
                        'XB-Meego-Desktop-Entry-Filename':self.MeeGo_Desktop_Entry_Filename
                        }
                    )
        open(os.path.join(DEBIAN_DIR,"control"),"w").write(unicode(control.getContent()).encode('utf-8'))

        #Create the debian licence file
        licence = Licence(self.copyright,
                          self.distribution.get_maintainer(),
                          self.distribution.get_maintainer_email(),
                          self.buildDate,
                          str(datetime.now().year))
        open(os.path.join(DEBIAN_DIR,"copyright"),"w").write(unicode(licence.getContent()).encode('utf-8'))

        #Delete tar if already exist as it will made add to the same tar
        tarpath = os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion+'.tar.gz')
        if os.path.exists(tarpath):
            os.remove(tarpath)

        #Now create the tar.gz
        import tarfile
        def reset(tarinfo):
            tarinfo.uid = tarinfo.gid = 0
            tarinfo.uname = tarinfo.gname = "root"
            return tarinfo
        tar = tarfile.open(tarpath, 'w:gz')
        #tar.add(self.dist_dir,'.')
        tar.add(self.build_dir,'.')
        tar.close()

        #Clean the build dir
        remove_tree(DEBIAN_DIR)
        remove_tree(DATA_DIR)

        #Create the Dsc file
        import locale
        try:
            old_locale,iso=locale.getlocale(locale.LC_TIME)
            locale.setlocale(locale.LC_TIME,'en_US')
        except:
            pass
        dsccontent = Dsc("%s-%s"%(self.version,self.buildversion),
                     self.depends,
                     (os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion+'.tar.gz'),),
                     Format='1.0',
                     Source=self.debian_package,
                     Version="%s-%s"%(self.version,self.buildversion),
                     Maintainer="%s <%s>"%(self.distribution.get_maintainer(),self.distribution.get_maintainer_email()),
                     Architecture="%s"%self.architecture,
                    )
        f = open(os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion+'.dsc'),"wb")
        f.write(unicode(dsccontent._getContent()).encode('utf-8'))
        f.close()

        #Changes file
        changescontent = Changes(
                        "%s <%s>"%(self.distribution.get_maintainer(),self.distribution.get_maintainer_email()),
                        "%s"%self.description,
                        "%s"%self.changelog,
                        (
                                 "%s.tar.gz"%os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion),
                                 "%s.dsc"%os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion),
                          ),
                          "%s"%self.section,
                          "%s"%self.repository,
                          Format='1.7',
                          Date=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
                          Source="%s"%self.debian_package,
                          Architecture="%s"%self.architecture,
                          Version="%s-%s"%(self.version,self.buildversion),
                          Distribution="%s"%self.repository,
                          Urgency="%s"%self.urgency,
                          Maintainer="%s <%s>"%(self.distribution.get_maintainer(),self.distribution.get_maintainer_email())
                          )

        f = open(os.path.join(self.dist_dir,self.debian_package+'_'+self.version+'-'+self.buildversion+'.changes'),"wb")
        f.write(unicode(changescontent.getContent()).encode('utf-8'))
        f.close()
        try:
            locale.setlocale(locale.LC_TIME,old_locale)
        except:
            pass

