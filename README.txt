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
# README (README.txt)
# -------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id$
#

Drool is a command-line tool to make the management of many Drupal sites on a web-server as easy as possible.  It does this
by automating mundane tasks, such as creating databases, downloading modules, etc.

For general help, run:
  $drool --help

For help on a specific command, run:
  $drool help <command>

Area Permissions

To give multiple users control over regions within the drupal root folder, drool looks to see if the user/(sudo user) has read/write permissions
to the parent folder of drupal folders (termed 'areas').
