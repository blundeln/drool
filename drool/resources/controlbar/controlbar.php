<?php
// Nick Blundell 2007

$siteDir = $base_path . "sites/" . $_SERVER[SERVER_NAME]; 
global $user;
$renderedControlPanel = "";

/* Add something to the footer of all sites. */
$variables["footer_message"] .= "";

if ($user->uid > 0) {

  $messageFile = $_SERVER["DOCUMENT_ROOT"] . $siteDir . "/message.txt";
  if (file_exists($messageFile)) {
    $message = fgets(fopen($messageFile,"r"));
  }

  $diskImage = "/". $siteDir . "/" . "drool-disk.png";
  $transferImage = "/". $siteDir . "/" . "drool-transfer.png";
  $controlbarPath = $base_path . "/drool/controlbar";
  $cssFile = $controlbarPath . "/controlbar.css";
  
  /* Update this with your (i.e. the website hosts) own logo and link. */
  $controlbarLogo = $controlbarPath . "/logo.png";
  $controlbarLink = "http://www.yourhostswebsite.org.uk";

  $renderedControlPanel = <<<ENDSTRING
<style type="text/css" media="all">@import "$cssFile";</style>

<h1 class="access-hidden">Website Control Bar</h1>

<div id="controlbar" class="clear-block">
  <div class="left" class="clear-block">
    <div>
    <ul class="cbicons">
    <li><a href='/?q=admin' title='Control Panel'><img alt="Control panel" src='$controlbarPath/controlbar.png'/></a></li>
    <li><a href='/?q=logout' title='Logout.'><img alt="Control panel" src='$controlbarPath/logout.png' /></a></li>
    </ul>
    </div>

    <div class="clear-block">
      <ul class="cbstatus">
      <li>Site disk usage <img title="Server disk usage." src="$diskImage"/></li>
      <li>Site monthly web traffic <img title="Server monthly transfer." src="$transferImage"/></li>
      </ul>
    </div>
  </div>
  
  <div class="middle">
    $message
  </div>
  
  <div class="right">
    <a href="$controlbarLink" title="Hosting logo"><img src="$controlbarLogo"/></a>
  </div>
</div>
ENDSTRING;

} else {
  $renderedControlPanel = "";
}

?>
