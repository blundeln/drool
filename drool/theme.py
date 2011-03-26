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
# theme (theme.py)
# ----------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: theme.py 869 2007-12-07 15:49:30Z blundeln $
#

import os
import re

import drool
import drool.system
import drool.drupal
from nbdebug import *


SKIN_REGIONS = ["page","content","block","block-","logo","tab"]
THEME_NAME = "flexi-theme"
SKIN_SUFFIXES = ["ts","rs","bs","ls","tl","tr","br","bl"]

SKIN_TEMPLATE = """SKIN_PREFIXdiv.SKIN_REGIONskin1SKIN_MODE { background: BG_COLOUR SKIN_IMAGE_1 repeat-x top; }
SKIN_PREFIXdiv.SKIN_REGIONskin2SKIN_MODE { background: transparent SKIN_IMAGE_2 repeat-y right; }
SKIN_PREFIXdiv.SKIN_REGIONskin3SKIN_MODE { background: transparent SKIN_IMAGE_3 repeat-x bottom; }
SKIN_PREFIXdiv.SKIN_REGIONskin4SKIN_MODE { background: transparent SKIN_IMAGE_4 repeat-y left; }
SKIN_PREFIXdiv.SKIN_REGIONskin5SKIN_MODE { background: transparent SKIN_IMAGE_5 no-repeat top left; }
SKIN_PREFIXdiv.SKIN_REGIONskin6SKIN_MODE { background: transparent SKIN_IMAGE_6 no-repeat top right; }
SKIN_PREFIXdiv.SKIN_REGIONskin7SKIN_MODE { background: transparent SKIN_IMAGE_7 no-repeat bottom right; }
SKIN_PREFIXdiv.SKIN_REGIONskin8SKIN_MODE { background: transparent SKIN_IMAGE_8 no-repeat bottom left; }
"""

def addSkinCSS(themePath, skinRegion, skinImage, skinSelector, skinPseudoClass, skinColour) :
  
  removeSkinCSS(themePath, skinRegion, skinSelector, skinPseudoClass)
  
  genCSSPath = detectSkinPath(themePath)
  skinCSS = SKIN_TEMPLATE
  
  for i in range(0,8) :
    if skinImage :
      skinSuffix = SKIN_SUFFIXES[i]
      skinFile = os.path.join("..", "images", os.path.basename(skinImage).replace(".png","-%s.png" % skinSuffix))
      skinFile = os.path.basename(skinImage).replace(".png","-%s.png" % skinSuffix)
      skinCSS = skinCSS.replace("SKIN_IMAGE_%s" % str(i+1), "url(%s)" % skinFile)
    else :
      skinCSS = skinCSS.replace("SKIN_IMAGE_%s" % str(i+1), "none")
      
 
  skinCSS = skinCSS.replace("SKIN_REGION", skinRegion)
  skinCSS = skinCSS.replace("BG_COLOUR", skinImage and getCSSColour(skinColour) or "transparent")
  skinCSS = skinCSS.replace("SKIN_PREFIX", skinSelector and "%s " % skinSelector or "")
  skinCSS = skinCSS.replace("SKIN_MODE", skinPseudoClass and "%s " % skinPseudoClass or "")
  
  debugOutput(skinCSS)
 
  # Add the css to the theme.
  try :
    genCSS = drool.system.readFromFile(genCSSPath)
  except :
    genCSS = ""
  genCSS += skinCSS
  drool.system.writeToFile(genCSSPath, genCSS)

def detectSkinPath(themePath) :
  if os.path.exists(os.path.join(themePath, "skin")) :
    return os.path.join(themePath, "skin","skin.css")
  elif os.path.exists(os.path.join(themePath, "styles")) :
    return os.path.join(themePath, "styles","skin.css")
  else :
    return None

def getSkinImagePath(themePath) :
  return os.path.dirname(detectSkinPath(themePath))

def removeSkinCSS(themePath, skinRegion, skinSelector, skinPseudoClass) :
  
  genCSSPath = detectSkinPath(themePath)
  try :
    genCSS = drool.system.readFromFile(genCSSPath)
  except :
    genCSS = ""
  
  if skinRegion.lower() == "all" :
    genCSS = ""
  else :
    regEx = re.compile("^%sdiv\.%sskin.%s\s+{.+?}\n" % (skinSelector and "%s " % skinSelector or "", skinRegion, skinPseudoClass or ""), re.MULTILINE)
    genCSS = regEx.sub("", genCSS)
  
  debugOutput(genCSS)
  
  drool.system.writeToFile(genCSSPath, genCSS)


# TODO: Will need to get image names form the css file.
def removeSkinFiles(siteName, skinName) :

  debugOutput("Unskinning '%s'" % skinName)
  themePath = os.path.join(drool.drupal.getSiteDir(siteName),"themes",THEME_NAME)
 
  if not os.path.exists(themePath) :
    drool.system.abort("You must have the %s theme installed to use skins." % THEME_NAME)
  
  skinImagePath = getSkinImagePath(themePath)
  
  skinName = skinName.lower()
  if not skinName.startswith("block-") and skinName not in SKIN_REGIONS :
    drool.system.abort("'%s' is not the name of a skin." % skinName)

  if skinName == "logo" :
    drool.system.runCommand("rm %s" % (os.path.join(themePath, skinName + ".png")))
  
  else :
    drool.system.runCommand("rm %s" % (os.path.join(skinImagePath, skinName + "*.png")))

def getCSSColour(colour) :
  
  debugOutput("colour = %s" % str(colour))
  cssColour = "#"
  for i in range(0, 3) :
    cssColour += "%.2x" % colour[i]
    debugOutput("cssColour = %s" % cssColour)
  return cssColour

def getSkinRegions(themePath) :
  
  skinRegions = ["logo"]
  
  for themeFile in os.listdir(themePath) :
    if not themeFile.endswith(".php") :
      continue
    for match in re.finditer("startSkin\([\"\'](?P<skinName>.*?)[\"\'].*?\)", drool.system.readFromFile(os.path.join(themePath, themeFile))) :
      if match.groupdict()["skinName"] not in skinRegions :
        skinRegions.append(match.groupdict()["skinName"])

  return skinRegions
