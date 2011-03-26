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
# system (system.py)
# ------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: system.py 1121 2008-11-04 11:29:32Z blundeln $
#

import os
import popen2
import pwd
import grp

import drool
from nbdebug import *


DEFAULT_NICE = 5



def oldBox(text) :
  border = "="*len(text)
  text = "\n%s\n%s\n%s" % (border, text, border)
  return text

def padString(text, width) :
  if len(text) < width :
    text += " " * (width-len(text))

  return text
    

def box(text, hChar=None, title=None) :
  hChar = hChar or "-"
  lines = text.split("\n")
  width = 0
  for line in lines :
    if len(line) > width :
      width = len(line)

  if title :
    if len(title) > width :
      width = len(title)
    lines[:0] = ["-" * width]
    lines[:0] = [title]

  text = "/%s\\\n" % (hChar*(width + 2))
  for line in lines :
    text += "| %s |\n" % padString(line, width)
  text += "\\%s/\n" % (hChar*(width + 2))

  #border = hChar*len(text)
  #text = "\n/%s\\\n|%s|\n\\%s/" % (border, text, border)
  return text

def displayBox(text, hChar=None, title=None) :
  message(box(text, hChar=hChar, title=title))

def displayHeader(headerString) :
  message(box(headerString, hChar="="))

def readFromFile(file) :
  debugOutput("Reading from file '%s'" % (file))
  if drool.settings.options.testRun :
    if not os.path.exists(file) :
      return ""
  
  return open(file, "r").read()


def writeToFile(file, string, mode="w") :

  sample = string[0:min(20,len(string))]
  if sample and len(sample) < len(string):
    sample += "..."
  #sample = ""
  debugOutput("Writing to file '%s': '%s'" % (file, sample))
  if not drool.settings.options.testRun :
    open(file,mode).write(string)

def autoSudo():

  if os.getuid() != 0 :
    command = "sudo"
    for arg in sys.argv :
      command += " %s" % arg
    os.system("%s" % command)
    sys.exit()

def checkRoot():

  if os.getuid() != 0 :
    self.abort("You must run this program with sudo or as the root user.")

def simpleForm(dicts) : 
  displayHeader("Please update the following fields, or hit <return> to leave a field unchanged")
  for dict in dicts :
    for settingName in dict :
      setting = dict[settingName]
      input = raw_input("%s [%s]: " % (setting.description, str(setting.systemValue) or ""))
      if input :
        setting.userValue = input

def directorySize(directory):

  command = "du %s --max-depth=0 --bytes" % directory
  du = os.popen(command,"r").readlines()

  try: size = int(du[0].split()[0])
  except : size = 0

  return size

def runCommand(command, exitOnFail = False, nice=DEFAULT_NICE) :
  result = 0

  if nice :
    command = "nice -n%s %s" % (nice, command)

  debugOutput(command)
  
  if drool.settings.options.testRun :
    pass
  else :
    if drool.settings.options.verbose :
      result = os.system(command)
    else :
      childProcess = popen2.Popen4(command)
      childProcess.fromchild.read()
      result = childProcess.wait()
 
  if exitOnFail and result != 0 :
    raise Exception("Command '%s' failed with exit code %s." % (command, result))

  return result

def getCommandOutput(command, nice=DEFAULT_NICE) :

  if nice :
    command = "nice -n%s %s" % (nice, command)
  
  debugOutput(command)
  try :
    return os.popen4(command)[1].read()
  except :
    return None

def mkdir(dir) :
  debugOutput("Making %s" % dir)
  if not drool.settings.options.testRun :
    os.mkdir(dir)

def abort(message) :
  displayBox("%s\n\n%s" % (message, "run: '%s --help' for help." % drool.SCRIPT_NAME), title="Abort")
  displayHeader(drool.DESCRIPTION)
  sys.exit(1)

def message(message, newline = True) :
  if not drool.settings.options.quiet :
    if newline :
      print message
    else :
      print message,

def yesQuestion(question) :
  
  if drool.settings.options.force :
    return True
    
  message(question)
  input = raw_input("Type 'yes' to contiue: ")
  return input.lower() == "yes"

def uncompress(file) :
  if runCommand("tar -xzpf %s" % (file)) != 0 :
    print("Error: Unable to uncompress file")

def compress(path) :
  dir = os.path.dirname(path)
  folder = os.path.basename(path)
  compressedFile = "%s.tar.gz" % folder
  if runCommand("tar -C %s -czpf %s %s" % (dir, compressedFile, folder)) != 0 :
    raise Exception("Error: Unable to compress file")
  return compressedFile


def replaceFileTerms(inPath, outPath, replacements) :
  debugOutput("Reading %s, writing %s, terms %s" % (inPath, outPath, replacements))
  inFile = open(inPath,"r")
  outFile = open(outPath, "w")
  i = 0
  for line in inFile :
    newLine = line
    for term, replacement in replacements :
      if term in newLine:
        newLine = newLine.replace(term, replacement)
    outFile.write(newLine)
    i+=1

  debugOutput("wrote %s lines." % i)


def appExists(appName) :
  output = getCommandOutput("whereis '%s'" % appName)
  if "/" in output :
    return True

  return False

def changeOwner(newOwner, target, recursive=True) :
  runCommand("chown %s '%s' '%s'" % (recursive and "-R" or "", newOwner, target))

def changeGroup(newGroup, target, recursive=True) :
  runCommand("chgrp %s '%s' '%s'" % (recursive and "-R" or "", newGroup, target))

def changePermissions(newPermissions, target, recursive=True) :
  runCommand("chmod %s '%s' '%s'" % (recursive and "-R" or "", newPermissions, target))


def emailFile(sender, to, subject, filePath) :
  os.system("""cat '%s' | uuencode '%s' | mail -s "%s" %s""" % (filePath, os.path.basename(filePath), subject, to))

def sendEmail(sender, to, subject, message, attachments=None) :
  debugOutput("Sendin email to '%s' from '%s': %s" % (to, sender, subject))

  # Import smtplib for the actual sending function
  import smtplib
  #from email.mime.text import MIMEText

  #msg = email.mime.text.MIMEText(message)
  #msg['Subject'] = subject
  #msg['From'] = sender
  #msg['To'] = to
  #cat drool-report.csv | uuencode drool-report.csv | mail -s "drool: site" to
  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  s = smtplib.SMTP()
  s.connect()
  s.sendmail(sender, [to], message)
  s.close()

def getUsername() :
  """Gets the user of sudo if available."""
  try :
    return os.environ["SUDO_USER"]
  except :
    return os.getlogin()


def getUsersGroups(uid) :
  """Gets a list of group ids for the user."""
  
  username = pwd.getpwuid(uid).pw_name
  
  output = getCommandOutput("groups %s" % username)
  debugOutput(output)
  if not output:
    return []

  groupNames = output.split()
  gids = [grp.getgrnam(groupName).gr_gid for groupName in groupNames]
  return gids
  

# Use a cache to speed up access function
accessCache={}

# TODO: Implement this cache with a decorator.

def access(path, mode, username=None) :
  debugOutput(path)
  global hasAccess

  # XXX: I don't really like this access code, but it's the best I can do at the moment.

  # If no username was specified, assume the real sudo user.
  username = username or getUsername()
 
  key = "%s-%s-%s" % (path, mode, username)

  if key in accessCache :
    return accessCache[key]

  hasAccess = False

  # If the user is in the master group, return True.
  output = getCommandOutput("groups %s" % username)
  if output :
    if drool.settings.masterGroup in output.split() :
      hasAccess = True

  if not hasAccess :
    code = """import os; print os.access("%s", %s)""" % (path, mode)
    output = getCommandOutput("""echo '%s' | sudo -u %s python""" % (code, username))
    #debugOutput(output)
    if "True" in output :
      hasAccess = True

  accessCache[key] = hasAccess
  return hasAccess
  


def access_old(path, mode, uid=None, username=None) :
  """
  Checks another user's access to a file.  Note that, when drool is run with sudo, real and effective
  uid and gid are roots, hence this code.
  """

  # If no username was specified, assume the real sudo user.
  username = username or getUsername()

  if uid :
    pass
  elif username :
    uid = pwd.getpwnam(username).pw_uid
  else :
    raise Exception("No user specified")

  gid = uid

  debugOutput("Checking access of %s on %s" % (uid, path))

  # Exit code to signal a users access.
  ACCESS_TRUE = 25
 
  hasAccess = False

  # Fork
  cid = os.fork()
  if cid == 0 :
    # Switch to a less privileged user to test their permission.
    
    # Set process groups to the user's groups.
    groups = getUsersGroups(uid)
    os.setgroups(groups)
    
    os.setgid(gid)
    os.setuid(uid)
    os.setegid(gid)
    os.seteuid(uid)
     
    debugOutput((os.getuid(), os.getgid(), os.getgroups()))

    # Exit this process with an exit code that the parent can interpret for access.
    if os.access(path, mode) :
      sys.exit(ACCESS_TRUE)
    else :
      sys.exit()
  else :
    # Wait for the child and check its exit status.
    status = os.waitpid(cid, 0)
    exitCode = status[1] >> 8
    hasAccess = exitCode == ACCESS_TRUE

  debugOutput("hasAccess: %s" % hasAccess)

  return hasAccess
