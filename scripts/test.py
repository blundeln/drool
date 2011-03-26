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
# test (test.py)
# --------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id: test.py 402 2006-11-18 15:46:25Z blundeln $
#

import os

def test() :

  script = "drool"
  print("Running tests on  '%s'" % (script))

  testSite1 = "test1.illuminateweb.org.uk"
  testSite2 = "test2.illuminateweb.org.uk"
  testSite3 = "test3.illuminateweb.org.uk"
  templateSite = "drupal1.nickblundell.org.uk"
  
  print("Testing creation and cloning.")
  os.system("%s new %s" % (script, testSite1))
  os.system("%s clone %s %s" % (script, testSite2, testSite1))
  os.system("%s delete --force %s" % (script, testSite2))
  os.system("%s clone %s %s" % (script, testSite2, templateSite))
  
  print("Testing pack and unpack.")
  os.system("%s pack %s" % (script, testSite2))
  os.system("%s unpack %s %s" % (script, "DROOLPACK*%s.tar.gz" % testSite2 ,testSite3))
  
  print("Testing module and theme installation.")
  os.system("%s module %s %s" % (script, testSite2, "ecommerce"))
  os.system("%s theme %s %s" % (script, testSite2, "goofy"))
  
  print("Testing apache.")
  os.system("%s dis %s" % (script, testSite2))
  os.system("%s enable %s" % (script, testSite2))
  
  print("Testing database stuff.")
  os.system("%s dumpdb %s /tmp/dumptest" % (script, testSite2))
  os.system("%s loaddb --force %s /tmp/dumptest" % (script, testSite2))
  
  print("Testing misc.")
  os.system("%s monitor" % (script))
  os.system("%s list" % (script))
 
  """expects = [
    ["Site Expiration Date.*: ","31/05/2050"],
    ["Storage Quota.*: ", "50"],
    ["Site Description.*: ","Just a test"],
    ["Monthly Transfer Limit.*: ", "43"]
  ]
  pExpect.expect("%s status %s" % (script, testSite2), expects)
  """
  raw_input("Press enter to continue the test.")
    
  # TODO: Apply a skin
 
  drawSkin("/tmp/page.png",[800,800], "#000000","#14ff00")
  drawSkin("/tmp/block.png",[100,300], "#000000","#144488")
  drawSkin("/tmp/tab-a.png",[200,28], "#000000","#144422")
  drawSkin("/tmp/tab-n.png",[200,28], "#000000","#444444")

  os.system("%s skin %s %s" % (script, testSite2, "/tmp/page.png"))
  os.system("%s skin %s %s" % (script, testSite2, "/tmp/block.png"))
  os.system("%s skin %s %s" % (script, testSite2, "/tmp/tab-n.png"))
  os.system("%s skin %s %s" % (script, testSite2, "/tmp/tab-a.png"))

  raw_input("Press enter to continue the test.")

  os.system("%s unskin %s %s" % (script, testSite2, "page"))
  os.system("%s unskin %s %s" % (script, testSite2, "block"))
  os.system("%s unskin %s %s" % (script, testSite2, "tab-n"))
  os.system("%s unskin %s %s" % (script, testSite2, "tab-a"))
  
  raw_input("Press enter to finish the test.")
  
  os.system("%s delete --force %s" % (script, testSite1))
  os.system("%s delete --force %s" % (script, testSite2))
  os.system("%s delete --force %s" % (script, testSite3))
  os.system("%s list" % (script))


def drawSkin(imagePath, size, outlineColour, bgColour) :
  import PIL
  import Image, ImageDraw, ImageColor, ImageFont
  
  borderWidth = 2
  
  im = Image.new("RGBA",(size[0], size[1]))

  outline = ImageColor.getrgb(outlineColour)
  background = ImageColor.getrgb(bgColour)

  draw = ImageDraw.Draw(im)
  draw.rectangle([0,0, im.size[0]-1, im.size[1]-1], outline=outline, fill=background)

  im.save(imagePath)



test()
