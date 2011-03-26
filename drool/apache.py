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
# apache (apache.py)
# ------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: apache.py 1121 2008-11-04 11:29:32Z blundeln $
#

import os
import re
import struct

import drool
import drool.system
from nbdebug import *


DEFAULT_TRANSFER = 5 * 1024 * 1024 * 1024

def resetScoreboard(site) :
  scoreboardPath = os.path.join(site.getSitePath(), "scoreboard")
  drool.system.writeToFile(scoreboardPath, "")

def getTransferQuota(site) :
  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  vHostInfo = drool.system.readFromFile(vHostFilePath)
  match = re.search("CBandLimit (?P<transfer>[^(Ki)]+)Ki", vHostInfo)
  if match : 
    return int(match.groupdict()["transfer"]) * 1024
  else :
    return None
  
def setTransferQuota(site, transferQuota) :
  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  vHostInfo = drool.system.readFromFile(vHostFilePath)
  transferQuota /= 1024
  vHostInfo = re.sub("CBandLimit [^(Ki)]+Ki", "CBandLimit %sKi" % int(transferQuota), vHostInfo)
  drool.system.writeToFile(vHostFilePath, vHostInfo)
  reload()

def restart() :
  if drool.system.runCommand("/etc/init.d/apache2 restart") != 0 :
    drool.system.abort("Unable to restart Apache")

def reload() :
  if drool.system.runCommand("/etc/init.d/apache2 reload") != 0 :
    drool.system.abort("Unable to reload Apache")

def getSiteEnabled(site) :
    return os.path.exists(os.path.join("/etc/apache2/sites-enabled",site.name))

def setSiteEnabled(site, enabled) :

  if enabled :
    if drool.system.runCommand("a2ensite %s" % site.name) != 0 :
      raise Exception("Unable to enable Apache site '%s'" % site)
  else :
    if drool.system.runCommand("a2dissite %s" % site.name) != 0 :
      raise Exception("Unable to disable Apache site '%s'" % site)

  reload()

def addAlias(site, alias) :
  ALIAS_TEMPLATE = """
<VirtualHost *:80>
  ServerAdmin admin@domain
  ServerName ALIAS
  Redirect / http://SITE/
</VirtualHost>
  """
  
  aliasClause = ALIAS_TEMPLATE.replace("ALIAS", alias).replace("SITE", site.name).strip()
  
  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  if not os.path.exists(vHostFilePath) :
    drool.system.abort("Error: virtual host file '%s' does not exist to add an alias." % vHostFilePath)

  vHostInfo = drool.system.readFromFile(vHostFilePath)
  if aliasClause not in vHostInfo :
    vHostInfo += "\n\n%s\n" % aliasClause
  else :
    drool.system.abort("Error: That alias already exists in '%s'." % vHostFilePath)

  drool.system.writeToFile(vHostFilePath, vHostInfo)

  debugOutput(vHostInfo)

  # Reload apache.
  reload()

def getSiteTraffic(site) :
  
  scoreboardPath = os.path.join(site.getSitePath(), "scoreboard")
  if not os.path.exists(scoreboardPath) :
    return None
  scoreboard = open(scoreboardPath,"rb").read()
  format = "QQLliiiii"
  try :
    return struct.unpack(format, scoreboard)[0]
  except :
    return None


def makeVHostString(site, transferLimit) :

  siteName = site.name
  drupalDir = site.getDrupalDir()

  transferLimit /= 1024
  template = """
<VirtualHost *:80>
ServerAdmin ADMIN_EMAIL
ServerName SITE_NAME

CustomLog /var/log/apache2/access.log combined
DocumentRoot DRUPAL_DIR

<IfModule mod_cband>
  CBandPeriod 4W
  CBandPeriodSlice 1W
  CBandLimit TRANSFER_LIMITKi
  CBandExceededSpeed 56 5 15
  CBandScoreboard SCORE_BOARD
</IfModule>

<Directory DRUPAL_DIR/>
  Options +FollowSymLinks
  AllowOverride All
  order allow,deny
  allow from all
</Directory>
</VirtualHost>
"""

  scoreboardPath = os.path.join(site.getSitePath(), "scoreboard")

  vhostString = template
  vhostString = vhostString.replace("ADMIN_EMAIL","admin@domain")
  vhostString = vhostString.replace("SITE_NAME",siteName)
  vhostString = vhostString.replace("DRUPAL_DIR",drupalDir)
  vhostString = vhostString.replace("TRANSFER_LIMIT",str(transferLimit))
  vhostString = vhostString.replace("SCORE_BOARD",scoreboardPath)

  return vhostString

def getVHost(site) :
  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  return drool.system.readFromFile(vHostFilePath)

def setVHost(site, vHostInfo) :
  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  drool.system.writeToFile(vHostFilePath, vHostInfo)
  reload()

  

def createVirtualHost(site, transferLimit=DEFAULT_TRANSFER) :

  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  if os.path.exists(vHostFilePath) :
    drool.system.abort("Error: virtual host file '%s' exists already." % vHostFilePath)
    
  setVirtualHost(site, transferLimit)

def setVirtualHost(site, transferLimit=DEFAULT_TRANSFER) :

  vHostFilePath = os.path.join("/etc/apache2/sites-available", site.name)
  vHostString = makeVHostString(site, transferLimit)
  debugOutput(vHostString)
    
  debugOutput("Creating apache vhost file '%s'." % vHostFilePath)
  drool.system.writeToFile(vHostFilePath, vHostString)
  #if not drool.settings.options.testRun :
  #  sitefile = open(vHostFilePath, "w")
  #  sitefile.write(vHostString)
  #  sitefile.close()

  # Enable the site.
  setSiteEnabled(site, True)

def removeVirtualHost(site) :
  try :
    setSiteEnabled(site, False)
  except :
    pass
  drool.system.runCommand("rm -rf /etc/apache2/sites-available/%s" % site.name)
