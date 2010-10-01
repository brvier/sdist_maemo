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

'''Generate the licence content'''

class Licence:
    def __init__(self,licence,author,email,buildDate,buildDateYear):       
        
        self.licence="""This package was packaged with sdist_maemo by %(author)s <%(email)s> on
%(buildDate)s.

Upstream Author: %(author)s <%(email)s>

Copyright: %(buildDateYear)s by %(author)s

License:

%(txtLicense)s

The Debian packaging is (C) %(buildDateYear)s, %(author)s <%(email)s> and
is licensed under the GPL, see above.


# Please also look if there are files or directories which have a
# different copyright/license attached and list them here.
"""% {'author':author,
                    'email':email,
                    'txtLicense':self.getTxtLicence(licence),
                    'buildDate':buildDate,
                    'buildDateYear':buildDateYear,}

    def getTxtLicence(self,licence):
        copy={}
        copy["gpl"]="""
  This package is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This package is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this package; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU General
Public License can be found in `/usr/share/common-licenses/GPL'.
"""
        copy["lgpl"]="""
  This package is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This package is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this package; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU Lesser General
Public License can be found in `/usr/share/common-licenses/LGPL'.
"""
        copy["bsd"]="""
  Redistribution and use in source and binary forms, with or without
  modification, are permitted under the terms of the BSD License.

  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
  SUCH DAMAGE.

On Debian systems, the complete text of the BSD License can be
found in `/usr/share/common-licenses/BSD'.
"""
        copy["shareware"]="""
This product is copyrighted shareware, not public-domain software.
You may use the unregistered version at no charge for an evaluation period.
To continue to use the software beyond evaluation period, you must register it.

THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""
        copy["artistic"]="""
  This program is free software; you can redistribute it and/or modify it
  under the terms of the "Artistic License" which comes with Debian.

  THIS PACKAGE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
  WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
  OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.

On Debian systems, the complete text of the Artistic License
can be found in `/usr/share/common-licenses/Artistic'.
"""        
        
        if licence in copy:
            return copy[licence]
        else:
            return licence
            
    def getContent(self):
        return self.licence
        