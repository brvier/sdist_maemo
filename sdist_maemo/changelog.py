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

'''Generate the changelog content'''

class Changelog:
    def __init__(self,name,version,buildversion,changelog,author,email,buildDate):
        print [s for s in changelog.replace('\n','*').split('*') if s]
        changelog = '\n  *'+'\n  *'.join([s for s in changelog.replace('\n','*').split('*') if ((s!='*') and (s!=''))])
        self.clog="""%(name)s (%(version)s-%(buildversion)s) stable; urgency=low
%(changelog)s

 -- %(author)s <%(email)s>  %(buildDate)s
""" % {'name':name,
       'version':version,
       'buildversion':buildversion,
       'changelog':changelog,
       'author':author,
       'email':email,
       'buildDate':buildDate}
        
    def getContent(self):
        return self.clog
        