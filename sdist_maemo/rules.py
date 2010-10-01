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

import os
import sys

'''Generate the rule content'''

from os.path import curdir, sep, pardir, join, abspath, commonprefix

def relpath(path, start=curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")
    start_list = abspath(start).split(sep)
    path_list = abspath(path).split(sep)
    # Work out how much of the filepath is shared by start and path.
    i = len(commonprefix([start_list, path_list]))
    rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return join(*rel_list)
    
class Rules:
    def __init__(self,name,origin):
        self.rules=[]
        self.dirs=[]
        self.origin_dir = origin
        self.package_name = name
        
        self.header(self.rules)
        
        self.rules.append('\tmkdir -p "$(CURDIR)/debian/%s"' % self.package_name)
        for root, dirs, fs in os.walk(self.origin_dir):
            fpath = relpath(root,self.origin_dir)
            
            for f in fs:                        
                # make a line RULES to be sure the destination folder is created
                # and one for copying the file
                #print root,dirs,f                
                #print fpath
                self.rules.append('\tmkdir -p "$(CURDIR)/debian/%s/%s"' % (self.package_name,fpath))
                self.rules.append('\tcp -a "%s" "$(CURDIR)/%s"' % (os.path.join(self.package_name,fpath,f),os.path.join('debian',self.package_name,fpath,f)))
        
            # append a dir
            self.dirs.append(fpath)
            
        self.footer(self.rules)

    def getContent(self):
        return '\n'.join(self.rules)
            
    def header(self,rules):
        rules.append('''#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

CFLAGS = -Wall -g

ifneq (,$(findstring noopt,$(DEB_BUILD_OPTIONS)))
	CFLAGS += -O0
else
	CFLAGS += -O2
endif

configure: configure-stamp

configure-stamp:
	dh_testdir
	touch configure-stamp

build: build-stamp

build-stamp: configure-stamp
	dh_testdir
	touch build-stamp

clean:
	dh_testdir
	dh_testroot
	rm -f build-stamp configure-stamp
	dh_clean

install: build
	dh_testdir
	dh_testroot
	dh_clean -k
	dh_installdirs

	# ======================================================''')
    
    def footer(self,rules):
        rules.append('''\t# ======================================================

# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
	dh_installchangelogs debian/changelog
	dh_installdocs
	dh_installexamples
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install configure''')