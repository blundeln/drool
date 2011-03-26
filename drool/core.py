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
# core (core.py)
# --------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: core.py 1141 2008-11-25 15:09:51Z blundeln $
#

import sys
import datetime, time
import pickle
import glob
import StringIO

import drool
import drool.apache
import drool.database
import drool.drupal
import drool.dns

from nbdebug import *

DEFAULT_STORAGE_QUOTA = 150 * 1024 * 1024
WARN_THRESHOLD = 0.8
PACK_NAME = "DROOLPACK"

DROOL_THEMES = ["drool3", "drool6_1", "drool4"]

class Setting :
  def __init__(self, description, userValue=None, systemValue=None) :
    self.description = description
    self.userValue = userValue
    self.systemValue = systemValue


def getStatusPath(site) :
  return os.path.join(site.getSitePath(), "status1")

# Create the site's status file.
# XXX: Thing I will get rid of this whole status thing.
def createStatusFile(site) :

  statusFilePath = getStatusPath(site)
  debugOutput("Creating status file '%s'." % statusFilePath)
  status = generateDefaultStatus()
  drool.system.writeToFile(statusFilePath, pickle.dumps(status))
  drool.system.runCommand("chmod o-r %s" % statusFilePath)

def generateDefaultStatus() :

  expireDate = datetime.datetime.now() + datetime.timedelta(365)

  status = {
    "storageQuota":Setting("Storage Quota (MB)", systemValue=DEFAULT_STORAGE_QUOTA),
    "siteExpirationDate":Setting("Site Expiration Date (DD/MM/YYYY)", systemValue=expireDate),
    "description":Setting("Site Description"),
  }

  return status

def setStatus(site, status) :
  drool.system.writeToFile(getStatusPath(site), pickle.dumps(status))

def getStatus(site) :

  statusFilePath = getStatusPath(site)

  try :
    status = pickle.loads(drool.system.readFromFile(statusFilePath))
  except :
    status = generateDefaultStatus()
    #raise Exception("Cannot load status from file %s" % statusFilePath)

  return status


def updateControlBar(site, customMessage=None) :
  
  # Create the monitoring images.
  status = drool.core.getStatus(site)
  storageUsage = [drool.drupal.getSiteDiskUsage(site), status["storageQuota"].systemValue]
  
  if drool.settings.manageApache :
    transferUsage = [drool.apache.getSiteTraffic(site), drool.apache.getTransferQuota(site)]
  else :
    transferUsage = [0, 0]
  
  siteDir = site.getSitePath()
  writeProgressImage(storageUsage[0], storageUsage[1], os.path.join(siteDir,"drool-disk.png"), text="%s/%s" % (drool.util.getHumanSize(storageUsage[0]), drool.util.getHumanSize(storageUsage[1])), warnThreshold=WARN_THRESHOLD)
  writeProgressImage(transferUsage[0], transferUsage[1], os.path.join(siteDir,"drool-transfer.png"), text="%s/%s" % (drool.util.getHumanSize(transferUsage[0]), drool.util.getHumanSize(transferUsage[1])), warnThreshold=WARN_THRESHOLD)
  
  # Update message.
  message = customMessage or ""
  #message += "Hosting expires on <b>%s</b><br/>" % (status["siteExpirationDate"].systemValue.strftime("%d/%m/%Y"))

  try : storageRatio = storageUsage[0]/float(storageUsage[1])
  except : storageRatio = 0
  try : transferRatio = transferUsage[0]/float(transferUsage[1])
  except : transferRatio = 0
  
  if storageRatio > 1 :
    message += "<b>Urgent</b>: this site is <b>exceeding</b> it's storage quota and data may be lost.<br/>"
  elif storageRatio > WARN_THRESHOLD :
    message += "Warning: this site is nearing or exceeding it's storage quota.<br/>"
    
  if transferRatio > 1 :
    message += "<b>Urgent</b>: this site is <b>exceeding</b> it's data transfer quota.<br/>"
  elif transferRatio > WARN_THRESHOLD :
    message += "Warning: this site is nearing or exceeding it's transfer quota<br/>"

  drool.system.writeToFile(os.path.join(siteDir, "message.txt"), message)
  

def writeProgressImage(value, range, file, text=None, warnThreshold=0.8) :

  import PIL
  import Image, ImageDraw, ImageColor, ImageFont

  WIDTH = 100
  HEIGHT = 18

  def centerTextInBox(font, text, size) :
    center = [0,0]
    center[0] = size[0]/2.0 - font.getsize(text)[0]/2.0
    center[1] = size[1]/2.0 - font.getsize(text)[1]/2.0 + 1
    return center

  im = Image.new("RGBA",(WIDTH, HEIGHT))

  outline = ImageColor.getrgb("#000000")
  background = ImageColor.getrgb("#4697ff")
  bar = ImageColor.getrgb("#14ff00")
  barWarn = ImageColor.getrgb("#ff0f00")
  textColour = ImageColor.getrgb("#000000")

  try :
    percentage = float(value)/range
  except :
    percentage = 0.0

  if percentage > warnThreshold :
    barColour = barWarn
  else :
    barColour = bar
  barWidth = percentage * im.size[0]
  barWidth = min(barWidth, im.size[0])

  draw = ImageDraw.Draw(im)
  draw.rectangle([0,0, im.size[0]-1, im.size[1]-1], outline=outline, fill=background)
  draw.rectangle([0,0, barWidth-1, im.size[1]-1], outline=outline, fill=barColour)

  font = ImageFont.load_default()
  try :
    font = ImageFont.truetype("/var/tmp/Nimbus Sans L,",16)
  except :
    debugOutput("Cannot load Nimbus font")
    font = ImageFont.load_default()
  if text :
    draw.text(centerTextInBox(font, text, im.size), text, font=font, fill=textColour)

  if not drool.settings.options.testRun : 
    im.save(file)



#
# Interface methods
#

def createNewSite(siteName) :
  
  # Create a site object.
  try :
    newSite = drool.drupal.SiteReference(siteName)
  except :
    raise Exception("Ensure you are in the drupal installation folder\nwhere the new site is to be created.\nFor example: /home/websites/drupal-5.6")
 
  dbuser = newSite.getDBCredentials()
  drool.database.createDatabase(newSite.getDatabaseName(), drool.settings.dbroot, dbuser)
  drool.drupal.loadDrupalTables(newSite, dbuser)
  drool.drupal.createNewSiteDir(newSite, dbuser)
  drool.drupal.updateFilePermissions(newSite, allPermissions=True)
  
  if drool.settings.manageApache :
    drool.apache.createVirtualHost(newSite)

def deleteSite(siteName) :
 
  # Assume site drupal files might not be there.
  site = drool.drupal.getSite(siteName)
  
  #drool.system.displayHeader("Removing site '%s'." % site)

  debugOutput("Removing site '%s'." % (site))
  
  # Remove the database.
  try :
    drool.database.runSqlCommand("DROP DATABASE %s" % site.getDatabaseName(), drool.settings.dbroot[0], drool.settings.dbroot[1])
  except :
    pass
  
  # Remove the drupal site.
  drool.system.runCommand("rm -rf %s" % site.getSitePath())
  
  if drool.settings.manageApache :
    # Remove the virtual host.
    drool.apache.removeVirtualHost(site)


def cloneSite(sourceSite, destSiteName) :

  # Clone the site description.
  try :
    destSite = drool.drupal.SiteReference(destSiteName)
  except :
    # If local folder not drupal dir, use drupal dir of source site.
    destSite = drool.drupal.SiteReference(destSiteName, sourceSite.drupalDir)
      

  if not drool.drupal.isCompatible(destSite.getDrupalVersion(), sourceSite.getDrupalVersion()) :
    raise Exception("The drupal versions of sites to be cloned are incompatible.")

  drool.system.displayHeader("Creating clone site '%s' from '%s'." % (destSite, sourceSite))
 
  if not os.path.exists(sourceSite.getSitePath()) :
    raise Exception("Site '%s' does not exist to be cloned." % (sourceSite))
  if os.path.exists(destSite.getSitePath()) :
    raise Exception("Site '%s' exists already." % destSite)

  dumpFile = os.path.join("/tmp",sourceSite.getDatabaseName())
  debugOutput("dumpFile = %s" % dumpFile)
  drool.database.dumpDatabase(sourceSite, dumpFile)

  drool.system.message("Creating new database...")
  drool.database.createDatabase(destSite.getDatabaseName(), drool.settings.dbroot, destSite.getDBCredentials())
  drool.system.message("Cloning data...")
  drool.database.loadDatabase(destSite, dumpFile)
  
  # Copy site files.
  drool.system.runCommand("cp -aL %s %s" % (sourceSite.getSitePath(), destSite.getSitePath()))

  # Create a drupal settings file for the clone.
  drool.drupal.createSettingsFile(destSite)
 
  # Create the site's status file and scoreboard.
  drool.core.createStatusFile(destSite)
  
  if drool.settings.manageApache :
    drool.apache.resetScoreboard(destSite)
    drool.apache.createVirtualHost(destSite)

  # Update site permissions, so user can edit new theme.
  drool.drupal.updateFilePermissions(destSite, allPermissions=True)


  # Replace old site references in the database.
  drool.drupal.replaceSiteReferences(destSite, sourceSite.name)


def installModule(moduleName, site) :
  
  debugOutput("Getting module")

  # Get the local modules
  localModulesPath = os.path.join(site.getSitePath(), "modules")
  
  # If there is not a global module, download a local one.
  drool.drupal.downloadModule(moduleName, localModulesPath, site.getDrupalVersion())
  moduleDir = drool.drupal.getModuleDir(moduleName, localModulesPath)
  if not moduleDir :
    raise Exception("Hmmm, I can't find the installed module '%s'." % moduleName)

  # If the module has a mysql file, install it.
  if os.path.isdir(moduleDir) :
    mysqlFiles = glob.glob(os.path.join(moduleDir, "*.mysql"))
    for mysqlFile in mysqlFiles :
      drool.system.message("Loading module database tables in '%s'." % mysqlFile)
      drool.database.loadMysqlFile(mysqlFile, site.getDBCredentials(), site.getDatabaseName())

  # Allow users to edit the new module files.
  drool.drupal.updateFilePermissions(site, allPermissions=True)
  
  debugOutput("Module '%s' has been installed to '%s'." % (moduleName, moduleDir))

  return moduleDir


def installTheme(themeName, site) :
  
  themesPath = os.path.join(site.getSitePath(), "themes")
  
  debugOutput("Installing theme '%s' to '%s'." % (themeName, themesPath))
  if themeName not in DROOL_THEMES :
    drool.drupal.downloadModule(themeName, themesPath, site.getDrupalVersion())
  else :
    # Copy the drool theme
    from pkg_resources import resource_filename
    droolThemesPath = resource_filename(__name__, os.path.join("resources","theme"))

    # Copy the theme
    if drool.settings.options.linkFiles :
      drool.system.runCommand("ln -s '%s' '%s'" % (os.path.join(droolThemesPath, themeName), themesPath))
    else :
      drool.system.runCommand("cp -a '%s' '%s'" % (os.path.join(droolThemesPath, themeName), themesPath))
      

  themeDir = drool.drupal.getModuleDir(themeName, themesPath)
  
  # Allow users to edit the theme files.
  drool.drupal.updateFilePermissions(site, allPermissions=True)
  
  return themeDir


def editStatus(site) :
  # XXX: Deprecated. 
  debugOutput(site)

  statusFilePath = getStatusPath(site)
  debugOutput(statusFilePath)
  
  status = getStatus(site)
  debugOutput(status)
  
  transferSetting = Setting("Monthly Transfer Limit (GB)", systemValue=drool.apache.getTransferQuota(site))
  additionalSettings = {"transfer":transferSetting}
  
  drool.system.simpleForm([status,additionalSettings])
 
  # Validate system values.
  if status["storageQuota"].userValue : status["storageQuota"].systemValue = int(status["storageQuota"].userValue) * 1024 * 1024
  if status["description"].userValue : status["description"].systemValue = status["description"].userValue
  if status["siteExpirationDate"].userValue :
    timeStruct = time.strptime(status["siteExpirationDate"].userValue,"%d/%m/%Y")
    status["siteExpirationDate"].systemValue = datetime.datetime(timeStruct[0], timeStruct[1], timeStruct[2])
  if additionalSettings["transfer"].userValue : additionalSettings["transfer"].systemValue = int(additionalSettings["transfer"].userValue) * 1024 * 1024 * 1024 

  setStatus(site, status)

  # Set the transfer limit.
  drool.apache.setTransferQuota(site, additionalSettings["transfer"].systemValue)
  # Update control bar.
  updateControlBar(site)


def pack(site) :
  
  debugOutput(site)

  # Create a folder to pack the data into.
  tempPackFolder = os.path.join("/tmp","%s-%s-%s" % (PACK_NAME, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), site.name))

  # Make some folders.
  drool.system.runCommand("mkdir -p %s/site" % tempPackFolder)
  
  # Record some version numbers.
  drool.system.runCommand("echo %s > %s" % (site.getDrupalVersion(), os.path.join(tempPackFolder, "DRUPAL_VERSION")))
  drool.system.runCommand("echo %s > %s" % (drool.VERSION, os.path.join(tempPackFolder, "DROOL_VERSION")))
  
  # Write the site's name.
  drool.system.writeToFile(os.path.join(tempPackFolder, "SITE_NAME"), str(site))

  # TODO: We really just want the site files in here: not the site folder.
  # Store the site's drupal files.
  drool.system.runCommand("cp -aL %s %s" % (site.getSitePath(), os.path.join(tempPackFolder, "site")))

  # Dump the database
  drool.database.dumpDatabase(site, os.path.join(tempPackFolder, "dbdump"))
  packFile = drool.system.compress(tempPackFolder)
  drool.system.runCommand("rm -r %s" % tempPackFolder)
  return packFile



def unpack(packFile, siteName=None) :
 
  debugOutput("%s -> %s" % (packFile, siteName))
  
  # Unpack the site.
  drool.system.uncompress(packFile)
  tempPackFolder = packFile.replace(".tar.gz","")
  
  # Get the name of the packed the site. 
  packedSiteName = drool.system.readFromFile(os.path.join(tempPackFolder, "SITE_NAME"))
  debugOutput("packedSiteName %s" % packedSiteName)
  
  # Get the drupal version of this site.
  drupalVersion = drool.system.readFromFile(os.path.join(tempPackFolder,"DRUPAL_VERSION")).rstrip("\n")
  debugOutput("packed drupal version: %s" % drupalVersion)
  
  # Get the name of the site to be created.
  siteName = siteName or packedSiteName
  if drool.settings.options.testRun :
    packedSiteName = packedSiteName or siteName
  
  # Create site objects to work with.
  newSite = drool.drupal.SiteReference(siteName)
  if newSite.exists() :
    drool.system.abort("Site %s exists already - first you must remove it if you want to replace it." % siteName)

  if not drool.drupal.isCompatible(newSite.getDrupalVersion(), drupalVersion) :
    drool.system.abort("The packed drupal site (%s) is not compatible with the destination site (%s)." % (drupalVersion, newSite.getDrupalVersion()))

  # Copy the site files.
  drool.system.runCommand("cp -aL %s %s" % (os.path.join(tempPackFolder, "site", "*"), newSite.getSitePath()))
 
  # Create the settings file for this site.
  drool.drupal.createSettingsFile(newSite)

  # Create the database and load dumped data.
  drool.database.createDatabase(newSite.getDatabaseName(), drool.settings.dbroot, newSite.getDBCredentials())
  dumpFile = os.path.join(tempPackFolder, "dbdump")
  drool.database.loadDatabase(newSite, dumpFile)

  # Replace old site references in the database.
  oldDomainName, oldSiteName = drool.database.getOriginalSiteDetails(dumpFile)
  drool.drupal.replaceSiteReferences(newSite, oldDomainName, oldSiteName)

  drool.drupal.updateFilePermissions(newSite, allPermissions=True)
  
  if drool.settings.manageApache :
    # Create the apache virtual host for this site.
    drool.apache.createVirtualHost(newSite)
  
  # Remove the unpacked folder.
  drool.system.runCommand("rm -r %s" % tempPackFolder)


def skinSite(site, themeName, skinRegion, skinImage, skinSelector, skinPseudoClass, xChop, yChop, chopThreshold) :
 
  xChop = xChop and int(xChop) or xChop
  yChop = yChop and int(yChop) or yChop
 
  debugOutput("%s %s %s %s %s %s %s" % (site, skinRegion, skinImage, skinSelector, skinPseudoClass, xChop, yChop))
  
  try : from nbutil import chopper
  except : raise Exception("You must have chopper installed to apply a skin.")

  themePath = os.path.join(site.getSitePath(),"themes",themeName)
  
  if not os.path.exists(themePath) :
    raise Exception("The theme cannot be found at '%s'." % themePath)

  skinImagePath = drool.theme.getSkinImagePath(themePath)
 
  skinRegions = drool.theme.getSkinRegions(themePath)
  
  if len(skinRegions) == 0 :
    raise Exception("The theme %s has no skin regions defined and so cannot be skinned." % themeName)

  skinPath = drool.theme.detectSkinPath(themePath)
  if not skinPath :
    raise Exception("The theme %s does not have a 'skin' directory." % themeName)

  debugOutput("skinPath %s" % skinPath)

  # Return a list of skin regions is none was specified.
  if not skinRegion :
    return skinRegions

  if skinRegion not in skinRegions :
    raise Exception("The theme %s does not have a skin region called '%s'." % (themeName, skinRegion))

  # Skinning the logo is easy.
  if skinRegion.lower() == "logo" and skinImage :
    if drool.system.runCommand("cp %s %s" % (skinImage, os.path.join(themePath,"logo.png"))) == 0 :
      drool.system.displayHeader("Skin successfuly applied.")
    else :
      raise Exception("The skin could not be applied.")
    return

  # If there is an image chop it and copy it.  
  if skinImage :
    
    # Copy skin image.
    skinDestImage = os.path.join(skinImagePath, os.path.basename(skinImage))
    if drool.system.runCommand("cp %s %s" % (skinImage, skinDestImage)) != 0 :
      raise Exception("The skin could not be applied.")
    
    # Chop the skin.
    if chopThreshold :
      skinColour = chopper.chopBox(skinDestImage,vChop=xChop,hChop=yChop, threshold=chopThreshold, debug=True)
    else :
      skinColour = chopper.chopBox(skinDestImage,vChop=xChop,hChop=yChop, debug=True)
  else :
    skinDestImage = None
    skinColour = None

  
  # Now add css for the skin.
  drool.theme.addSkinCSS(themePath, skinRegion, skinDestImage, skinSelector, skinPseudoClass, skinColour = skinColour)

def unskinSite(site, themeName, skinRegion, skinSelector, skinPseudoClass) :
  
  debugOutput("%s, %s" % (site, skinRegion))

  themePath = os.path.join(site.getSitePath(),"themes",themeName)
  
  if not os.path.exists(themePath) :
    raise Exception("You must have the 'drool' Drupal theme installed to apply skins.")
 
  if skinRegion.lower() == "logo" :
    drool.system.runCommand("rm %s" % (os.path.join(themePath,"logo.png")))
  else :
    drool.theme.removeSkinCSS(themePath, skinRegion, skinSelector, skinPseudoClass)
  

# XXX: Gonna get rid of this.
def installHooks(drupalVersion=None, removeHooks=False) :
  raise Exception("Deprecated")
  drupalVersion = drupalVersion or drool.settings.defaultDrupalVersion
  drupalDir = drool.drupal.getDrupalDir(drupalVersion)
 
  debugOutput("Installing drool hooks into drupal %s." % drupalVersion)
  
  from pkg_resources import resource_filename
  controlBarDir = resource_filename(__name__, os.path.join("resources","controlbar"))
  droolPath = os.path.join(drupalDir,"drool")

  # Add control bar hook to phptemplate
  templateHookFile = resource_filename(__name__, os.path.join("resources","phptemplatehook.php"))
  phptemplateFile = os.path.join(drupalDir, "themes","engines","phptemplate","phptemplate.engine")
  phptemplate = drool.system.readFromFile(phptemplateFile)
  
  tag, tagReplacement = drool.system.readFromFile(templateHookFile).split("\n>>>\n")

  if removeHooks :
    if tagReplacement not in phptemplate :
      raise Exception("Unable to remove hooks from %s" % phptemplateFile)
  else :   
    if tag not in phptemplate :
      raise Exception("Unable to tag %s" % phptemplateFile)

    # Copy control bar code to drupal source dir.
    drool.system.runCommand("mkdir -p %s" % droolPath)
    drool.system.runCommand("cp -rLf %s %s" % (controlBarDir, droolPath))
  
  debugOutput(phptemplate)
  debugOutput(phptemplate)
  phptemplate = phptemplate.replace(removeHooks and tagReplacement or tag, removeHooks and tag or tagReplacement)
  debugOutput(phptemplate)
  drool.system.writeToFile(phptemplateFile,phptemplate)

def getSiteDetails(site) :
  data = {}

  #raise Exception(drool.drupal.getEnabledModules(site))

  # Gather some data on the site
  #data["domain"] = site.name
  data["site email"] = drool.drupal.getMainEmailAddress(site)
  data["site name"] = drool.drupal.getDrupalVariable(site, "site_name")
  
  userDetails = drool.drupal.getUserDetails(site)
  data["no users"] = len(userDetails)
  data["drupal version"] = "drupal " + site.getDrupalVersion()
  data["no nodes"] = drool.drupal.getNoNodes(site)

  # TODO: enabled/disabled, user names.

  # Find earliest user.
  earliestCreated = None
  recentLogin = None
  #debugOutput(userDetails)
  for user in userDetails :
    #if user["uid"] in [0,1] :
    #  continue
    if not earliestCreated :
      earliestCreated = user["created"]
    elif user["created"] < earliestCreated :
      earliestCreated = user["created"]
  data["earliest user"] = earliestCreated and datetime.datetime.fromtimestamp(earliestCreated).strftime("%d/%m/%Y") or None

  for user in userDetails :
    if not recentLogin :
      recentLogin = user["login"]
    else :
      if user["login"] > recentLogin :
        recentLogin = user["login"]
  data["last login"] = recentLogin and datetime.datetime.fromtimestamp(recentLogin).strftime("%d/%m/%Y") or None

  # Get dns status for this site.
  dnsStatus = drool.dns.dnsLookup(site.getSiteName())
  if dnsStatus :
    data["DNS Status"] = "\n".join(dnsStatus)
  else :
    data["DNS Status"] = "Not configured"

  data["Site Path"] = site.getDrupalDir()

  data["Database"] = site.getDatabaseName()
  
  if drool.settings.manageApache :
    data["Status"] = drool.apache.getSiteEnabled(site) and "Enabled" or "Disabled"

  return data

def generateReport(specificSite=None) :
  """Generate a report about sites."""
  siteDetails = {}
  debugOutput("Generating report for site %s" % specificSite)

  # Get a list of sites to build the report on
  siteList = specificSite and [specificSite] or drool.drupal.getSiteList()[drool.drupal.ALL_SITES]

  for site in siteList :
    siteDetails[site] = getSiteDetails(site)
  
  return siteDetails


def updatePermissions(site = None, allPermissions=False) :
  """Upudates the file permissions of a site."""
  debugOutput("Updating permissions for %s" % site)
  if site :
    drool.drupal.updateFilePermissions(site, allPermissions=allPermissions)
    return

  # Get a list of all sites and update their permissions.
  siteList = drool.drupal.getSiteList()
  sites = siteList[drool.drupal.ALL_SITES]

  for site in sites :
    drool.drupal.updateFilePermissions(site, allPermissions=allPermissions)
    drool.system.message(".", newline=False)
  
  # Newline
  drool.system.message("")


def move(site, destDrupalPath) :
  debugOutput("Moving site %s to %s" % (site, destDrupalPath))

  # Normalise destDrupalPath
  nDestDrupalPath = drool.drupal.normaliseDrupalDir(destDrupalPath)
  debugOutput(nDestDrupalPath)

  # Try to create a reference to the target site.
  destSite = drool.drupal.SiteReference(site.name, nDestDrupalPath)

  # Test the major versions.
  if not drool.drupal.isCompatible(destSite.getDrupalVersion(), site.getDrupalVersion()) :
    raise Exception("The drupal versions of the site and destination drupal installation are incompatible.")

  if destSite.exists() :
    raise Exception("%s exists already" % destSite)

  # Move the files
  drool.system.runCommand("mv '%s' '%s'" % (site.getSitePath(), destSite.getSitePath()))

  if drool.settings.manageApache :
    # Update vhost file.
    vHostConfig = drool.apache.getVHost(site)
    vHostConfig = vHostConfig.replace(site.getDrupalDir(), destSite.getDrupalDir())
    debugOutput(vHostConfig)
    drool.apache.setVHost(site, vHostConfig)

def displayDetails(site) :

  details = {}
  details = getSiteDetails(site)

  detailsString = ""
  for key, content in details.iteritems() :
    detailsString += "%s: %s\n" % (key.capitalize(), content)

  drool.system.displayBox(str(detailsString), title="Details of %s" % site.name)

def getDefaultDrupalDir() :
  # Base this on the current path.
  # XXX: This should not really have symbollic links in: they should be reolved to the true path.
  return os.path.realpath(os.getcwd())
