#
# Copyright (C) 2008 Nick Blundell.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# The GNU GPL is contained in /usr/doc/copyright/GPL on a Debian
# system and in the file COPYING in the Linux kernel source.
# 
# setup (setup.py)
# ----------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: setup.py 1123 2008-11-04 15:24:40Z blundeln $
#

import ez_setup 
ez_setup.use_setuptools()
from setuptools import setup, find_packages

MAIN_PACKAGE = "drool"
exec("import %s" % MAIN_PACKAGE)
VERSION = eval("%s.VERSION" % MAIN_PACKAGE)

# Initialise command extensions.
cmdclass = {}


# Try to add command extensions for distutil.
try :
  import disttools.bdist_deb
  cmdclass["bdist_deb"] = disttools.bdist_deb.bdist_deb
except :
  pass

setup(
  name = MAIN_PACKAGE,
  version = VERSION,
  author="Nick Blundell",
  packages = find_packages(),
  scripts=["scripts/drool"],
  data_files=[
    ('/etc',['drool/resources/config/drool.conf']),
    ('/etc/cron.d',['drool/resources/droolcron']),
  ],
  include_package_data = True,
  install_requires=["nbdebug","nbutil"],
  dependency_links=["http://www.nickblundell.org.uk/packages/"],
  cmdclass=cmdclass,
  description = """Drool (Drupal Tool) is a utility for managing lots of Drupal sites on a server.""",
  long_description = """Drool (Drupal Tool) is a utility for managing lots of Drupal sites on a server.""",
)
