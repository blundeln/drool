#
# Copyright (C) 2006 Nick Blundell.
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
# util (util.py)
# --------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: util.py 1120 2008-11-03 15:52:34Z blundeln $
#

import os, sys

import drool
import drool.system
from nbdebug import *

def lreplace(string, search, replace) :
  """Replace start of string."""
  if string.startswith(search) :
    string = replace + string[len(search):]
  return string

def rreplace(string, search, replace) :
  """Replace end of string."""
  if string.endswith(search) :
    string = string[0:-len(search)] + replace
  return string

def proportionString(size1, size2) :
  displayString = "%s/%s" % (size1 and getHumanSize(size1) or "-", size2 and getHumanSize(size2) or "-")
  if size1 and size2 : 
    displayString += "(%.1f%%)" % (100 * float(size1)/size2)
  return displayString 

def getNearestItemMatch(abrev, items) :

  nearestItem = None

  for item in items :
    if item.lower().startswith(abrev.lower()) :
      if nearestItem :
        return None
      else :
        nearestItem = item
    
  return nearestItem

def getHumanSize(size) :

  if not size :
    return "-"
  
  abbrevs = [
    (1<<50L, 'PB'),
    (1<<40L, 'TB'), 
    (1<<30L, 'GB'), 
    (1<<20L, 'MB'), 
    (1<<10L, 'KB'),
    (1, '')
  ]

  for factor, suffix in abbrevs:
    if size > factor:
      break
  return `int(size/factor)` + suffix

def configGet(config, section, option, default=None) :
  try :
    return config.get(section,option)
  except :
    return default


class Pexpect :

  def install(self) :
    debugOutput("Installing pexpect")
    drool.system.runCommand("wget http://kent.dl.sourceforge.net/sourceforge/pexpect/pexpect-2.1.tar.gz")
    drool.system.runCommand("tar -xzf pexpect-2.1.tar.gz")
    drool.system.runCommand("cd pexpect-2.1 && python setup.py install && cd ..")

  def expect(self, command, qas) :
    debugOutput("%s: %s" % (command, qas))
    try :
      import pexpect
    except :
      debugOutput("No pexpect!")
      return
 
    if options.testRun :
      return
 
    process = pexpect.spawn(command)
    process.logfile = sys.stdout
    for qa in qas :
      try :
        process.expect(qa[0],timeout=5)
      except :
        debugOutput(str(process))
        os.exit(1)
      if qa[1] :
        process.sendline(qa[1])
    process.expect(pexpect.EOF)

