#
# Copyright (C) 2009 Nick Blundell.
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
# dns (dns.py)
# ------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id$
#

import socket, re

import drool.system

from nbdebug import *

def dnsLookup(hostname) :
  debugOutput("Doing dns lookup on %s" % hostname)
  output = drool.system.getCommandOutput("dig '%s'" % hostname)
  if not output :
    return None
  debugOutput(output)
  #debugOutput(output)
  
  # Get our hostname and IP address.
  hostname = socket.gethostname()
  ip = socket.gethostbyname(hostname)
  
  # Look to see if CNAME or A recrods point to this server.
  configuredRecords = []
  if re.search("CNAME\s+%s" % (hostname), output) :
    configuredRecords.append("CNAME")
  elif re.search("A\s+%s" % (ip), output) :
    configuredRecords.append("A")

  return configuredRecords
