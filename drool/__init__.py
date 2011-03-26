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
# __init__ (__init__.py)
# ----------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: __init__.py 1096 2008-10-09 15:26:14Z blundeln $
#

VERSION_PARTS = ("2","0","a1")

VERSION = ".".join(VERSION_PARTS)
SCRIPT_NAME = "drool"
DESCRIPTION = "%s %s (Drupal Tool) by Nick Blundell (www.nickblundell.org.uk) 2008" % (SCRIPT_NAME, VERSION)

class Settings :
  def __init__(self) :
    self.__dict__["settings"] = {}
  def __setattr__(self, name, value) : self.__dict__["settings"][name] = value
  def __getattr__(self, name, default=None) : return name in self.settings and self.settings[name] or default

settings = Settings()
