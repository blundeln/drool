#
# Copyright (C) 2007 Nick Blundell.
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
# seleniumtest (seleniumtest.py)
# ------------------------------
#
# Description:
#
#
# Author       : Nick Blundell
# Organisation : www.nickblundell.org.uk
# Version Info : $Id$
#

import unittest, time, re, os
import random
import sys

from selenium import selenium
import nbutil.nbexpect
from nbdebug import *

HOST_STRING = sys.argv[1]
HOST = HOST_STRING.split(":")[0]
TIMEOUT = "600000"
EXPECT_TIMEOUT = 30

sel = None

TEST_SSH_ACCOUNT = "/home/blundeln/work/smartbox/ssh-test-account.txt"  

TEST_SITES = ["sb1.test.com", "sb2.test.com", "sb3.test.com"] 
APACHE_PAGE = "apache2-default"

DRUPAL_USER = "admin"
DRUPAL_EMAIL = "admin@admin.com"
DRUPAL_PASSWORD = "admin"
SERVER_PASSWORD = "server"

class TestBase(unittest.TestCase):
  
  def setUp(self):
    global sel
    if not sel :
      refreshSelenium()
    goFast()

  def assertPageNotBlank(self) :
    self.assertTrue(sel.get_html_source())

  def assertInBody(self, text) :
    self.assertTrue(text in sel.get_html_source())
  
  def assertNotInBody(self, text) :
    self.assertTrue(text not in sel.get_html_source())
  
  def assertInText(self, text) :
    self.assertTrue(text in sel.get_body_text())
  
  def assertNotInText(self, text) :
    self.assertTrue(text not in sel.get_body_text())

  def tearDown(self) :
    pause(3)

  def login(self, username, password) :
    openPage("/")
    sel.type("edit-name",username)
    sel.type("edit-pass",password)
    sel.click("edit-submit")
    wait()

  def logout(self) :
    openPage("/?q=logout")

  def addContent(self, type, title, body) :
    openPage("/?q=node/add/%s" % type)
    sel.type("edit-title",title)
    sel.type("edit-body",body)
    sel.click("edit-submit")
    wait()


class SiteCreationTests(TestBase) :

  def testNewSite(self) :
    self.assertTrue("has been created" in runServerCommand("drool new %s" % TEST_SITES[0])[0])
    switchHost(TEST_SITES[0])
    openPage("/install.php")
    openPage("/")
    self.assertInText("Welcome to your new Drupal website")

  def testSetupDrupal(self) :
    switchHost(TEST_SITES[0])
    openPage("/")
    sel.click("link=create the first account")
    wait()
    sel.type("edit-name", DRUPAL_USER)
    sel.type("edit-mail", DRUPAL_EMAIL)
    sel.submit("user-register")
    wait()
    sel.type("edit-pass-pass1", DRUPAL_PASSWORD)
    sel.type("edit-pass-pass2", DRUPAL_PASSWORD)
    sel.click("edit-submit")
    wait()
    openPage("/q=logout")


  
  def testCloneSite(self):
    self.assertTrue("has been created as a clone of" in runServerCommand("drool clone %s %s" % (TEST_SITES[1], TEST_SITES[0]))[0])
    switchHost(TEST_SITES[1])
    openPage("/")
    self.assertInText("Welcome to your new Drupal website")


class SiteManagementTests(TestBase) :
  
  def testDisableSite(self):
    switchHost(TEST_SITES[0])
    openPage("/")
    self.assertInText("Welcome to your new Drupal website")
    
    self.assertTrue("has been disabled" in runServerCommand("drool disable %s" % TEST_SITES[0])[0])
    openPage("/")
    self.assertInText(APACHE_PAGE)
    
    self.assertTrue("has been enabled" in runServerCommand("drool enable %s" % TEST_SITES[0])[0])
    openPage("/")
    self.assertInText("Welcome to your new Drupal website")
   
  def testListSites(self):
    siteList = runServerCommand("drool list")[0]
    self.assertTrue(TEST_SITES[0] in siteList)
    self.assertTrue(TEST_SITES[1] in siteList)

  def testChangeAdminPassword(self):
    runServerCommand("drool password %s cheese" % TEST_SITES[0])
    switchHost(TEST_SITES[0])
    self.login(DRUPAL_USER, "cheese")
    self.assertNotInText("unrecognized username or password")
    self.logout()

    # Now change the password back
    runServerCommand("drool password %s %s" % (TEST_SITES[0], DRUPAL_PASSWORD))

  def xxxtestInstallHooks(self):
    runServerCommand("drool install_hooks --force")
    self.login(DRUPAL_USER, DRUPAL_PASSWORD)
    self.assertInBody("controlbar")
    self.assertNotInBody("error")
    self.logout()

class PluginInstallations(TestBase) :
  
  def testModuleInstall(self) :
    self.assertTrue("Module 'event' has been installed" in runServerCommand("drool module %s event" % TEST_SITES[0], timeout=None)[0])
    switchHost(TEST_SITES[0])
    self.login(DRUPAL_USER, DRUPAL_PASSWORD)
    openPage("/?q=admin/build/modules")
    self.assertInText("Calendaring API")
    self.logout()
  
  def testThemeInstall(self) :
    self.assertTrue("Installed theme" in runServerCommand("drool theme %s aquasoft" % TEST_SITES[0], timeout=None)[0])
    switchHost(TEST_SITES[0])
    self.login(DRUPAL_USER, DRUPAL_PASSWORD)
    openPage("/?q=admin/build/themes")
    self.assertInText("aquasoft")
    self.logout()


class BackupTests(TestBase) :

  def testCronSetup(self) :
    output = runServerCommand("cat /etc/cron.d/droolcron")[0]
    self.assertTrue("/usr/bin/drool event hourly" in output)
    self.assertTrue("/usr/bin/drool event daily" in output)

  def testDatabaseDump(self) :
    
    # Add some unique content to the first site
    switchHost(TEST_SITES[0])
    self.login(DRUPAL_USER, DRUPAL_PASSWORD)
    self.addContent("story","Monkey","A monkey has been put in jail for...")
    self.logout()
    
    # Dump the database
    self.assertTrue("Successfully dumped database" in runServerCommand("drool dumpdb %s dbdump" % TEST_SITES[0], timeout=None)[0])

    # Load it into another site
    self.assertTrue("Successfully loaded database" in runServerCommand("drool --force loaddb %s dbdump %s" % (TEST_SITES[1], TEST_SITES[0]), timeout=None)[0])

    runServerCommand("rm dbdump")

    # Check drupal to see what happened.
    switchHost(TEST_SITES[1])
    openPage("/")
    self.assertInText("A monkey has been put in jail")

  
  def testPackUnpack(self) :
    
    switchHost(TEST_SITES[0])
    
    # Pack the site
    output = runServerCommand("drool pack %s" % TEST_SITES[0], timeout=None)[0]
    self.assertTrue("Successfully packed site" in output)
    packFile = output[output.find("DROOLPACK"):output.find("tar.gz")] + "tar.gz"
    
    # Unpack the site
    debugOutput("packFile %s" % packFile)
    self.assertTrue("Successfully unpacked site" in runServerCommand("drool unpack %s %s" % (packFile, TEST_SITES[2]), timeout=None)[0])
    
    # Remove pack file.
    runServerCommand("rm -fr DROOLPACK*")
    
    # Check drupal to see what happened.
    switchHost(TEST_SITES[2])
    openPage("/")
    self.assertInText("A monkey has been put in jail")

    
class SkinningTests(TestBase) :

  REGIONS = ["logo", "header", "accessibility", "content", "footer", "page", "link", "block", "blocktitle"]

  def testDroolThemeInstall(self) :
    switchHost(TEST_SITES[0])
    output = runServerCommand("drool theme %s drool3" % TEST_SITES[0], timeout=None)[0]
    self.assertTrue("Installed theme 'drool3'" in output)
   
    # Activate the drool3 theme.
    self.login(DRUPAL_USER, DRUPAL_PASSWORD)
    openPage("/?q=/admin/build/themes")
    sel.check("name=theme_default value=drool3")
    sel.click("edit-submit")
    self.logout()

    # Check the page renders with theme (i.e. correct filer permissions)
    openPage("/")
    self.assertPageNotBlank()


  def testSkinRegions(self) :
    for region in self.REGIONS :
      self._applySkin(TEST_SITES[0], region)

  def testUnskinRegions(self) :
    for region in self.REGIONS :
      self._unskin(TEST_SITES[0], region)
  
  def testSpecificSkins(self) :
    self._applySkin(TEST_SITES[0], "blocktitle", skinSelector="#block-user-0")
    self._unskin(TEST_SITES[0], "blocktitle", skinSelector="#block-user-0")
    self._applySkin(TEST_SITES[0], "blocktitle", skinSelector="#block-user-0", skinPseudoClass=":hover")
    pause(3)
    self._applySkin(TEST_SITES[0], "blocktitle")
    # Transparent skin
    self._applySkin(TEST_SITES[0], "blocktitle", skinSelector="#block-user-0", skinImage="")

    # Unskin all
    self._unskin(TEST_SITES[0], "all")

  def _applySkin(self, site, region, skinImage="--test-skin", skinSelector=None, skinPseudoClass=None) :
    output = runServerCommand("drool skin %s drool3 %s %s %s %s" % (site, region, skinImage, skinSelector and "--skinSelector='%s'" % (skinSelector) or "", skinPseudoClass and "--skinPseudoClass='%s'" % (skinPseudoClass) or ""), timeout=None)[0]
    self.assertTrue("Successfully skinned region" in output)
    openPage("/")
    pause(1)
  
  def _unskin(self, site, region, skinSelector=None, skinPseudoClass=None) :
    output = runServerCommand("drool unskin %s drool3 %s --test-skin %s %s" % (site, region, skinSelector and "--skinSelector='%s'" % (skinSelector) or "", skinPseudoClass and "--skinPseudoClass='%s'" % (skinPseudoClass) or ""), timeout=None)[0]
    self.assertTrue("Successfully unskinned region" in output)
    openPage("/")

class ClosureTests(TestBase) :

  def testDeleteSites(self) :
    for site in [TEST_SITES[0], TEST_SITES[1], TEST_SITES[2]] :
      self.assertTrue("has been deleted" in runServerCommand("drool --force delete %s" % site)[0])
      switchHost(site)
      openPage("/")
      self.assertInText(APACHE_PAGE)
      

#
# Helper classes and methods.
#


def wait() : sel.wait_for_page_to_load(TIMEOUT)
def goSlow(speed=2000) : sel.set_speed(speed)
def goFast() : sel.set_speed(0)
def pause(secs=10) : time.sleep(secs)

def refreshSelenium() :
  global sel
  if sel :
    sel.stop()
    sel = None
  sel = selenium("localhost", 4444, "*firefox", getWebRoot())
  sel.start()


def getWebRoot() :
  try :
     port = ":%s" % HOST_STRING.split(":")[1]
  except :
    port = ""
  return "http://%s%s" % (HOST, port)

def openPage(page) :
  sel.open("%s%s" % (getWebRoot(), page))
  wait()

def switchHost(newHost) :
  global HOST
  oldHost = HOST

  if newHost != oldHost :
    HOST = newHost
    refreshSelenium()


  return oldHost

def runCommand(command, input=None) :
  debugOutput(command)
  
  # Retry if connection failes - remember: we are constantly restarting samba server.
  while True :
    output = os.popen4(command)[1].read()
    if "Connection to smartbox failed" in output :
      debugOutput("Connection failed so retrying!")
    else :
      break
    time.sleep(1)
  
  debugOutput("OUTPUT: %s" % output)
  return output

def runSSHCommand(username, host, command, password=None, timeout=EXPECT_TIMEOUT) :
  sshCommand = """ssh %s@%s "%s" """ % (username, host, command)
  debugOutput("running ssh command: %s" % sshCommand)
  if password :
    output = nbutil.nbexpect.runExpect(sshCommand, events={"password": "%s\n" % password,"yes/no":"yes\n"}, timeout=timeout)
  else :
    output = nbutil.nbexpect.expect(sshCommand, [[".*", None]], timeout=timeout)
  debugOutput("output: %s" % str(output))
  return output

def runServerCommand(command, timeout=EXPECT_TIMEOUT) :
  return runSSHCommand("root",HOST, command, password=SERVER_PASSWORD, timeout=timeout)

def getTestSSHAccount() :
  return open(TEST_SSH_ACCOUNT,"r").read().replace("\n","").split(",") 

if __name__ == "__main__" :
  debugOutput("Testing")
  debugOutput(getTestSSHAccount())


def doTests() :

  debugOutput("Testing")
  output = runServerCommand("drool list")
  debugOutput(output)

if __name__ == "__main__" :
  doTests()
