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
# database (database.py)
# ----------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: database.py 1158 2009-06-09 07:40:00Z blundeln $
#

import MySQLdb
import re
import gzip
import os

import drool
import drool.system
from nbdebug import *

DB_NAME = "DB_NAME"


def dumpDatabase(site, dumpFile) :
  
  if dumpFile.endswith(".gz") :
    rawDumpFile = os.path.splitext(dumpFile)[0]
  else :
    rawDumpFile = dumpFile

  debugOutput("dumpFile %s rawDumpFile %s" % (dumpFile, rawDumpFile))

  # Stamp the first line of the dump file with the name of the site.
  # As Matthew pointed out, mysql likes a space after '--' nowadays
  droolStamp = "-- DROOL %s\n" % str(site)
  drool.system.writeToFile(rawDumpFile, droolStamp)
  if drool.system.runCommand("mysqldump -u %s -p%s --databases --no-create-db %s | sed s/%s/%s/ >> %s" % (drool.settings.dbroot[0], drool.settings.dbroot[1], site.getDatabaseName(), site.getDatabaseName(), DB_NAME, rawDumpFile)) != 0 :
    raise Exception("Unable to extract data from the database of '%s'." % site)

  # Compress the dump file.
  if dumpFile.endswith(".gz") :
    debugOutput("Compressing %s" % dumpFile)
    # Compress the dump file
    drool.system.runCommand("gzip -c '%s' > '%s'" % (rawDumpFile, dumpFile))

    # Remove the raw file.
    drool.system.runCommand("rm '%s'" % (rawDumpFile))

def shell(site) :
  """Run the database shell for this site."""
  dbuser = site.getDBCredentials()
  command = "mysql -u %s -p%s %s" % (dbuser[0], dbuser[1], site.getDatabaseName())
  os.system(command)

def stop() :
  drool.system.runCommand("/etc/init.d/mysql stop")
  
def start() :
  drool.system.runCommand("/etc/init.d/mysql start")

def fixTables(path, site=None) :
  """Fix mysql tables under the path."""
  if site :
    path = os.path.join(path, site.getDatabaseName())
  stop()
  command = "find '%s' -name *.MYI -print0 | xargs -0 --max-args=1 myisamchk -r" % path
  os.system(command)
  start()

def getOriginalSiteDetails(dumpFile) :
  """Tries to get details of the site's original drupal path and domain name from the database dump."""

  # Parse the first line of the dump file.
  if dumpFile.endswith(".gz") :
    firstLine = gzip.open(dumpFile,"r").readline()
  else :  
    firstLine = open(dumpFile,"r").readline()
  if not "DROOL" in firstLine :
    raise Exception("This database was not dumped by drool.")
 
  args = firstLine.replace("-- DROOL","").replace("--DROOL","").split()

  domain = args[0]
  try :
    siteName = args[1]
  except :
    siteName = None

  return (domain, siteName)


def loadDatabase(site, dumpFile, replacements=None) :

  rawDumpFile = dumpFile.replace(".gz","")
  
  # Un compress the dump file.
  if dumpFile.endswith(".gz") :
    debugOutput("Uncompressing %s" % dumpFile)
    # Unompress the dump file
    drool.system.runCommand("gunzip -c '%s' > '%s'" % (dumpFile, rawDumpFile))

  if not replacements :
    replacements = []

  replacements.append((DB_NAME, site.getDatabaseName()))

  # Clean things from the database dump.
  if drool.settings.options.cleanDB :
    replacements.append(("DEFAULT CHARSET=utf8", ""))
    replacements.append(("DEFAULT CHARSET=latin1", ""))
    replacements.append(("character set utf8 collate utf8_bin", ""))
    replacements.append(("character set latin1", ""))
    replacements.append(("collate utf8_bin", ""))

  if replacements :
    modifiedDumpFile = rawDumpFile + ".mod"
    drool.system.replaceFileTerms(rawDumpFile, modifiedDumpFile, replacements) 
    rawDumpFile = modifiedDumpFile
  
  drool.system.runCommand("mysql %s -u %s -p%s < %s" % (site.getDatabaseName(), drool.settings.dbroot[0], drool.settings.dbroot[1], rawDumpFile), exitOnFail=True)
  
  # Clear all cache_* tables
  dbuser = site.getDBCredentials()
  for cacheTable in ["cache","cache_filter","cache_menu","cache_page", "cache_block", "cache_content", "cache_form", "cache_views", "sessions", "watchdog"] :
    try : 
      runSqlCommand("delete from %s;" % cacheTable ,dbuser[0],dbuser[1], site.getDatabaseName())
    except :
      pass


def runSqlCommand(command, user, password, database=None) :
  result = None
  debugOutput(command)
  if not drool.settings.options.testRun :
    if database :
      db = MySQLdb.connect(host="localhost", user=user, passwd=password, db=database)
    else:
      db = MySQLdb.connect(host="localhost", user=user, passwd=password)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(command)
    result = cursor.fetchall()
  
  return result

#XXX: Hmmmm.  Have I replaced this?
def loadMysqlFile(mysqlFile, dbuser, database) :
  command = "mysql -u %s -p%s %s < %s" % (dbuser[0], dbuser[1], database, mysqlFile)
  if drool.system.runCommand(command) != 0 :
    raise Exception("Unable to run mysql command '%s'." % command)
    
def grantDatabaseAccess(databaseName, dbroot, dbuser) :
  grantCommand = "GRANT ALL PRIVILEGES ON %s.* TO %s@localhost IDENTIFIED by '%s'" % (databaseName, dbuser[0], dbuser[1]) 
  runSqlCommand(grantCommand, dbroot[0], dbroot[1]) 
  runSqlCommand("FLUSH PRIVILEGES", dbroot[0], dbroot[1])
        

def createDatabase(databaseName, dbroot, dbuser) :
 
  debugOutput("Creating database: %s" % databaseName)
  command = "mysqladmin -u%s -p%s create %s" % (dbroot[0], dbroot[1], databaseName)
  try :
    drool.system.runCommand(command)
  except :
    raise Exception("Unable to create database '%s' - it may already exist." % databaseName)
  
  # Set database rights.
  grantDatabaseAccess(databaseName, dbroot, dbuser)

