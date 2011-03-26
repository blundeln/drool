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
# drupal (drupal.py)
# ------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: drupal.py 1144 2008-12-09 15:28:48Z blundeln $
#

import os
import re
import ftplib
import tempfile
import subprocess
import stat
import pwd

import drool
import drool.database
import drool.util
from nbdebug import *


EXCLUDED_SITES = ["all", "default"]
ALL_SITES = "ALL_SITES"


class SiteReference:
  """Represents a new or existing drupal site."""

  def __init__(self, name, drupalDir=None) :
    if drupalDir :
      self.name, self.drupalDir = name, drupalDir
    else :
      self.name, self.drupalDir = self._parseDrupalDir(name)

    debugOutput((self.name, self.drupalDir))

    # Raise an exception if the drupal installation folder is not valid.
    if not (os.path.exists(os.path.join(self.drupalDir, "sites")) and os.path.join(self.drupalDir, "index.php")) :
      raise Exception("%s is not a valid drupal installation" % self.drupalDir)

    # Check the user has permission to manipulate this site.
    if not drool.system.access(os.path.dirname(self.drupalDir), os.W_OK) :
      raise Exception("You do not have permission to manipulate the site %s" % self.name)
      
      
      
  def getDrupalVersion(self) :
    # TODO: Should parse drupal-5.7-patch -> 5.7
    parts = os.path.basename(self.drupalDir).lower().split("-")
    return parts[1]
  def getSitePath(self) :
    return os.path.join(self.drupalDir, "sites", self.name)
  def getDrupalDir(self) :
    return self.drupalDir
  def getSiteName(self) :
    return self.name
 
  def exists(self) :
    return os.path.exists(self.getSitePath())

  def _parseDrupalDir(self, name) :
    """Qualify the location of the site from:  'sitename', 'some/folder/sitename' '/abs/some/folder/sitename'."""
    
    # Use the default drupal dir.
    if "/" not in name :
      name = os.path.join(drool.core.getDefaultDrupalDir(), name)
    
    # Get the dir path and tail.
    drupalDir = os.path.dirname(name)
    name = os.path.basename(name)
    
    # Make this an absolute path.
    if not drupalDir.startswith("/") :
      drupalDir = os.path.join(drool.settings.drupalRoot, drupalDir)

    return name, drupalDir
  
  def __str__(self) :
    return self.name
  def __repr__(self) :
    return self.__str__()
  # Get database settings
  # --> #$db_url = 'mysql://user:pass@localhost/db_name';
  # TODO
  # getDatabasename from drupal settings file
  # get db username and pass from settings file.
  # get settings file.
  def getDatabaseName(self) :
    # TODO: If the site extsts, use settings 
    return self.name.replace(".","_").replace("-","_")
  def getDBCredentials(self) :
    # TODO: If the site extsts, use settings 
    # TODO: Try to parse settings from the settings file.
    return drool.settings.dbuser
  def getSettingsFile(self) :
    return os.path.join(self.getSitePath(), "settings.php")
    


# XXX: Deprecated.
#def getSiteDir(site) :
#  return os.path.join(drool.settings.drupalDir, "sites", site)


# Search for the specified module's directory.
def getModuleDir(moduleName, modulesPath) :
  
  moduleDir = None
  dirItems = os.listdir(modulesPath)
  for dirItem in dirItems :
    if dirItem.lower().startswith(moduleName.lower()) :
      moduleDir = os.path.join(modulesPath, dirItem)

  return moduleDir


def loadDrupalTables(site, dbuser) :

  debugOutput("site %s %s %s" % (site.name, site.getDrupalDir(), site.getDrupalVersion()))
  if site.getDrupalVersion().split(".")[0] not in ["4"] :
    return

  drupalDir = site.getDrupalDir()

  drupalMySql = os.path.join(drupalDir, "database/database.4.0.mysql")
  if not os.path.exists(drupalMySql) :
    drupalMySql = os.path.join(drupalDir, "database/database.mysql")
  if not os.path.exists(drupalMySql) :
    raise Exception("Can't find drupal database tables.")
    
  debugOutput("Loading tables.")
  drool.database.loadMysqlFile(drupalMySql, dbuser, site.getDatabaseName())



def downloadModule(moduleName, destination, drupalVersion) :
  debugOutput("Downloading module '%s'" % moduleName)

  host = drool.settings.drupalDownloadFTPHost
  path = drool.settings.drupalDownloadFTPPath

  # Find the appropriate module.
  drool.system.message("Getting module list from %s" % host)
  moduleList = getModuleList(host, path)
  drool.system.message("Getting specific module version")
  moduleFile = getModuleFilename(moduleName, moduleList, drupalVersion)

  if moduleFile :
    # Download the file.
    getFTPFile(host, path, moduleFile, destination)
    drool.system.message("Downloaded module file: %s" % moduleFile)
  else :  
    raise Exception("Unable to find module '%s' at '%s' - check at www.drupal.org." % (moduleName, host))
 
  currentDir = os.getcwd()
  os.chdir(destination)
 
  if drool.system.runCommand("tar -xzf %s" % (moduleFile)) != 0 :
    print("Error: Unable to uncompress module")

  # TODO: set ownership to admin user.

  drool.system.runCommand("rm %s" % moduleFile)
  os.chdir(currentDir)

    

def getSiteDiskUsage(site) :
   dbDir = os.path.join(drool.settings.dbpath, site.getDatabaseName())
   return drool.system.directorySize(site.getSitePath()) + drool.system.directorySize(dbDir)


def organiseSiteList(sites) :

  organisedSites = {}
  for site in sites :

    if site.lower().startswith("t-") :
      domain = "templates"
    elif site.lower().startswith("sb") :
      domain = "sandboxes"
    else :
      try :
        domain = ".".join(site.split(".")[1:])
      except :
        domain = site

    if domain not in organisedSites :
      organisedSites[domain] = [site]
    else :
      organisedSites[domain].append(site)
    debugOutput(domain)

  debugOutput(organisedSites)

  return organisedSites


def getDrupalDirs() :
  """Returns a list of all the drupal installations the user has access to under the drupal root folder."""

  drupalDirs = []
  for root, dirs, files in os.walk(drool.settings.drupalRoot):
    #debugOutput((root, dirs, files))
    basename = os.path.basename(root)

    # Note: do not need to walk into drupal dirs.


    if basename.lower().startswith("drupal-") and os.path.isdir(root) :
     
      # Prune dirs so we don't tranverse into drupal dirs - this wastes time.
      while dirs :
        del dirs[0]

      # Check the user has rw access to drupal folder parent folder.
      if not drool.system.access(os.path.dirname(root), os.W_OK) :
        continue
      
      drupalDirs.append(root)

  debugOutput(drupalDirs)

  return drupalDirs
  

def getSiteList() :
  
  debugOutput("Getting site list")

  drupalDirs = getDrupalDirs()
  debugOutput("drupalDirs: %s" % drupalDirs)

  sites = {}

  # This is for convenience.
  sites[ALL_SITES] = []

  # Process each drupal installation folder.
  for drupalDir in drupalDirs :
    #sitesDir = os.path.join(drool.settings.drupalRoot, drupalDir, "sites")
    sitesDir = os.path.join(drupalDir, "sites")
    localSites = []
    
    # Process each drupal site in the drupal installation folder.
    for siteName in os.listdir(sitesDir) :
      if siteName.lower() not in EXCLUDED_SITES :
        localSites.append(SiteReference(siteName, drupalDir))
    
    if localSites :
      sites[drupalDir] = localSites
      sites[ALL_SITES] += localSites

  debugOutput(sites)

  return sites

def completeName(namePrefix, list) :
  matches = []
  for item in list :
    if item and item.startswith(namePrefix) :
      matches.append(item)
  if matches and len(matches) == 1 :
    debugOutput("Found match: %s" % matches[0])
    return matches[0]
  else :
    return None

def getSite(siteName) :
  """Gets site if it exists, else throws exception."""
 
  # Search for the site by name if partial name is given.
  siteList = getSiteList()
  siteNames = [site.name for site in siteList[ALL_SITES]]
  debugOutput("Searching for %s in %s" % (siteName, siteNames))
  siteName = completeName(siteName, siteNames) or siteName
 
  debugOutput("All sites: %s" % siteList[ALL_SITES])

  try :
    return siteList[ALL_SITES][siteNames.index(siteName)]
  except :
    pass
    #raise Exception("Site %s does not exist." % siteName)

  # See if the site exists.
  try :
    site = SiteReference(siteName)
  except :
    site = None

  if site and site.exists() :
    return site
  
  raise Exception("Site %s does not exist - check you typed the name correctly." % siteName)

def createSettingsFile(site) :

  defaultSiteDir = site.getSitePath().replace(site.name, "default")
  if site.getDrupalVersion().split(".")[0] in ["6","7"] :
    defaultSettingsFile = os.path.join(defaultSiteDir, "default.settings.php")
  else :
    defaultSettingsFile = os.path.join(defaultSiteDir, "settings.php")

  if not os.path.exists(defaultSettingsFile) :
    raise Exception("Unable to find default drupal settings file '%s'." % defaultSettingsFile)

  settings = drool.system.readFromFile(defaultSettingsFile)
  dbuser = site.getDBCredentials()
  settings = re.sub("db_url = 'mysql://[^']+", "db_url = 'mysql://%s:%s@localhost/%s" % (dbuser[0], dbuser[1], site.getDatabaseName()), settings) 
  
  # Write variables.
  drupalVars = {
    'file_directory_path' : os.path.join("sites",site.name,"files"),
  }
  
  drupalVarsString = ""
  for drupalVar in drupalVars :
    drupalVarsString += """"%s" => "%s",\n""" % (drupalVar, drupalVars[drupalVar])
  drupalVarsString = "$conf = array (\n%s);\n" % drupalVarsString
  
  settings += "\n" + drupalVarsString

  drool.system.writeToFile(site.getSettingsFile(), settings)


def createNewSiteDir(newSite, dbuser) :

  siteDir = newSite.getSitePath()
  
  if os.path.exists(siteDir) :
    raise Exception("'%s' exists: cannot create site folder." % siteDir)
  
  # Try to create a new folder for the site.
  try :
    drool.system.mkdir(siteDir)
  except :
    raise Exception("Unable to create '%s'." % siteDir)

  # Create the drupal settings file.
  createSettingsFile(newSite)

  filesPath = os.path.join(siteDir, "files")
  modulesPath = os.path.join(siteDir, "modules")
  themesPath = os.path.join(siteDir, "themes")

  # Create some special folders.
  drool.system.runCommand("mkdir %s" % filesPath)
  drool.system.runCommand("mkdir %s" % modulesPath)
  drool.system.runCommand("mkdir %s" % themesPath)

  # Create the site's status file.
  drool.core.createStatusFile(newSite)

  if drool.settings.manageApache :
    # Create scoreboard file.
    drool.apache.resetScoreboard(newSite)


def updateFilePermissions(site, allPermissions=False) :
  """
  Set the site's file permissions appropriately, so users can edit the files, and apache can write to its folders.
  If all == True, all permissions are updated; else, only special permissions are updated (e.g. www-data for files, etc.)
  """
  
  debugOutput(site.drupalDir)
  sitePath = site.getSitePath()
  debugOutput(sitePath)
  
  if allPermissions :
    debugOutput("Updating permissions")
    # To simplify this, we will set the folder permissions based on the drupal installation dir permissions.
    # get user, get group, get permissions.
    dirStat = os.stat(os.path.dirname(site.drupalDir))
    uid = dirStat.st_uid
    gid = dirStat.st_gid
    debugOutput((uid, gid))
    
    # Change the owner and user of the site folder.
    drool.system.changeOwner("%s:%s" % (uid,gid), sitePath)

    # Set permissions of site to those of drupal folder.
    mode = dirStat[stat.ST_MODE]
    debugOutput(mode)
    # Use least three sig figs of mode.
    modeStr = "%o" % mode
    if len(modeStr) > 3 :
      modeStr = modeStr[-3:]
    drool.system.changePermissions(modeStr, sitePath)
  
  # Set special case permissions for webserver.
  debugOutput("Updating special permissions")
  filesDir = os.path.join(sitePath, "files")
  scoreboardFile = os.path.join(sitePath, "scoreboard")
  for path in [filesDir, scoreboardFile] :
    drool.system.changeGroup(drool.settings.webGroup, path)
    drool.system.changePermissions("g+rwx", path)




def getModuleList(host=None, path=None) :

  host = host or drool.settings.drupalDownloadFTPHost
  path = path or drool.settings.drupalDownloadFTPPath
  
  ftp = ftplib.FTP(host)
  ftp.login()
  ftp.cwd(path)
  listing = ftp.nlst()
  ftp.quit()
  listing.sort()
  list = []
  for filename in listing :
    if filename.lower().endswith("tar.gz") :
      list += [filename]
  return list


def getModuleFilename(moduleName, moduleList, drupalVersion, dev=False) :

  # TODO: Un-hardcode these.
  # Now just check that the module has been published on the drupal modules or themes page.
  import urllib
  drool.system.message("Looking at drupal website for published modules")
  #modulesPage = urllib.urlopen("http://drupal.org/project/Modules/name").read()
  modulesPage = urllib.urlopen("http://drupal.org/project/%s" % moduleName).read()
  modulesPage += urllib.urlopen("http://drupal.org/project/Themes").read()

  candidates = []
  for filename in moduleList :

    # Include dev releases?
    if "-dev" in filename.lower() and not dev :
      continue

    #if filename.lower().startswith(moduleName.lower()+"-") and filename in modulesPage:
    if filename.lower().startswith(moduleName.lower()+"-"):
      candidates += [filename]

  candidates.reverse()
 
  debugOutput("candidates: %s" % str(candidates))

  versionMask = drupalVersion.split("."); versionMask[-1] = "x"; versionMask = ".".join(versionMask)

  for candidate in candidates :
    if "-%s" % versionMask in candidate :
      return candidate

  return None

def getEnabledModules(site) :
  """Returns the enabled modules of a site."""
  results = runSqlCommand(site, "SELECT * FROM system WHERE type = 'module' AND status = 1 ORDER BY filename ASC")
  modulesList = [mod["name"] for mod in results]
  return modulesList
  

def resetRootPassword(site, newPassword) :
  siteDatabase = site.getDatabaseName()
  dbuser = site.getDBCredentials()
  #result = drool.database.runSqlCommand("select * from %s.users" % siteDatabase, dbuser[0], dbuser[1])
  result = drool.database.runSqlCommand("UPDATE `users` SET `pass` = MD5('%s') WHERE `uid` =1 LIMIT 1" % newPassword, dbuser[0], dbuser[1], siteDatabase)
  user = drool.database.runSqlCommand("select * from users WHERE `uid` = 1", dbuser[0], dbuser[1], siteDatabase)
  debugOutput("result = %s" % str(result))
  return user[0]["name"]
  
def runSqlCommand(site, command) :
  siteDatabase = site.getDatabaseName()
  dbuser = site.getDBCredentials()
  result = drool.database.runSqlCommand(command, dbuser[0], dbuser[1], siteDatabase)
  #debugOutput("result = %s" % str(result))
  return result

def phpUnserialise(value) :
  if not value :
    return None
    
  if value.startswith("s:") :
    return value[value.find("\"")+1:value.rfind("\"")]
  else :
    return value

def getNoNodes(site) :
  try :
    results = runSqlCommand(site, "select * from node;")
  except :
    return 0
  return len(results)

def getDrupalVariable(site, variable) :
  try :
    results = runSqlCommand(site, "select * from variable;")
  except :
    return None
  #debugOutput("variables : %s" % str(results))
  for item in results :
    if item["name"] == variable :
      return phpUnserialise(item["value"])
  return None

def getMainEmailAddress(site) :
  return getDrupalVariable(site, "site_mail")

def getUserDetails(site) :

  users = {}
  try :
    items = runSqlCommand(site, "select * from users;")
  except :
    return {}
  for item in items :
    if not item["name"] :
      continue
    users[item["name"]] = item
  return items

def getFTPFile(host, path, filename, destination) :
  debugOutput("%s %s %s %s" % (host, path, filename, destination))
  ftp = ftplib.FTP(host)
  ftp.login()
  ftp.cwd(path)
  ftp.retrbinary('RETR %s' % filename, open(os.path.join(destination, filename), 'wb').write)
  ftp.quit()

def getDrupalDir(drupalVersion) :
  drupalDir = os.path.join(drool.settings.drupalRoot, "drupal-%s" % drupalVersion)
  return drupalDir


def normaliseDrupalDir(path):
  path = os.path.abspath(path)
  if "drupal-" not in path.lower() :
    raise Exception("'%s' is not a Drupal installaton path" % path)

  # Prune down to the actual drupal folder.
  while (path and not os.path.basename(path).lower().startswith("drupal-")) :
    path = os.path.dirname(path)

  # Should not get here.
  if not path :
    raise Exception("'%s' is not a Drupal installaton path" % path)

  return path

def isCompatible(v1, v2) :
  return v1.split(".")[0] == v2.split(".")[0]

def replaceSiteReferences(site, oldDomainName, oldSiteName=None) :
  """Drupal stores references to the site name in a serialised form, so this
     functions tries to replace those references."""

  oldSiteName = oldSiteName or oldDomainName

  if oldSiteName == site.name and oldDomainName == site.name:
    debugOutput("Nothing to replace")
    return

  replacements = {}
  # Replace references to the drupal site folder.
  replacements["sites/%s" % oldSiteName] = "sites/%s" % site.name

  # Replace references to the domain name.
  replacements[oldDomainName] = site.name
  
  phpArgs = ["%s->%s" % (oldTerm, replacements[oldTerm]) for oldTerm in replacements]

  debugOutput("phpArgs: %s" % phpArgs)

  from pkg_resources import resource_filename
  phpFile = resource_filename(__name__, os.path.join("resources","php_snippets","updateSerialised.php"))
  runPhpCode(site, drool.system.readFromFile(phpFile), *phpArgs)


def runPhpCode(site, code, *args) :
  # TODO: Check drupal version of site.
  return runPhpCodeD5(site, code, *args)

def runPhpCodeD5(site, code, *args) :

  # Strip php tags from code.
  code = code.strip()
  code = drool.util.lreplace(code, "<?php","")
  code = drool.util.rreplace(code, "?>","")

  debugOutput("args: %s" % str(args))

  #debugOutput("Running drupal php code: %s" % code)

  phpCode = D5_DRUPAL_SCRIPT.replace("SITE_ADDRESS", site.name).replace("PHP_CODE", code)
  #phpCode = PHP_SCRIPT.replace("SITE_ADDRESS", site.name).replace("PHP_CODE", code)
  #debugOutput(phpCode)

  codeFile = open("/tmp/drutest.php","w")
  codeFile.write(phpCode)
  codeFile.flush()
  codeFile.close()
  #command = "php %s" % codeFile.name
  command = "cd '%s' && php %s" % (site.getDrupalDir(), codeFile.name)

  # Add the args
  if args :
    debugOutput(args[0])
    for arg in args :
      command += " \"%s\"" % arg


  debugOutput("command: %s" % command)
  os.system(command)

  return

  origPath = os.getcwd()

  os.chdir(site.getDrupalDir())

  #codeFile = tempfile.NamedTemporaryFile()
  codeFile = open("/tmp/drutest.php","w")
  codeFile.write(phpCode)
  codeFile.flush()

  command = "php %s" % codeFile.name
  
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  errCode = process.wait()
  err = process.stderr.read()
  output = process.stdout.read().strip()
 
  os.chdir(origPath)
  
  if errCode != 0 :
    raise Exception("%s returned error code %s: output %s : err%s" % (command, errCode, output, err))

  debugOutput(">>>%s<<<" % output)
  codeFile.close()
  return output


PHP_SCRIPT = """
<?php
PHP_CODE
?>
"""
D5_DRUPAL_SCRIPT = """
<?php
require_once('./includes/bootstrap.inc');

$drupal_base_url = parse_url("http://SITE_ADDRESS");
$_SERVER['HTTP_HOST'] = $drupal_base_url['host'];
$_SERVER['PHP_SELF'] = $drupal_base_url['path'].'/index.php';
$_SERVER['REQUEST_URI'] = $_SERVER['SCRIPT_NAME'] = $_SERVER['PHP_SELF'];
$_SERVER['REMOTE_ADDR'] = NULL;
$_SERVER['REQUEST_METHOD'] = NULL;

$conf_path = conf_path();
drupal_bootstrap(DRUPAL_BOOTSTRAP_FULL);

// Login as site root user
global $user;
$user = user_load(array('uid' => 1));
PHP_CODE
?>
"""
