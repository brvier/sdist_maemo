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
import md5hash

class Dsc(object):

    """
    """
    def __init__(self, StandardsVersion,BuildDepends,files, **kwargs):
      self.options = kwargs
      self.StandardsVersion = StandardsVersion
      self.BuildDepends=BuildDepends
      self.files=files

    def _getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k,v in self.options.iteritems()]


        if self.BuildDepends:
            content.append("Build-Depends: %s" % self.BuildDepends)
        if self.StandardsVersion:
            content.append("Standards-Version: %s" % self.StandardsVersion)

        content.append('Files:')

        for onefile in self.files:
            md5=md5hash.md5sum(onefile)
            size=os.stat(onefile).st_size.__str__()
            content.append(' '+md5 + ' ' + size +' '+os.path.basename(onefile))

        return "\n".join(content)+"\n\n"

    content = property(_getContent, doc="")