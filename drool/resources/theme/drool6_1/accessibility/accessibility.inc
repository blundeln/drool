<?php
  /* Nick Blundell 2007 */
  /* Define variables and the dynamic style sets. */
  global $styleSets, $themeDir, $styleSetKeys, $switcher, $imagesDir, $emSize;
  $styleSets = array(
    "textsize" => array (
      '',
      'text-medium.css',
      'text-large.css',
      'text-vlarge.css',
      'text-vvlarge.css',
    ),
    "colourscheme" => array (
      '',
      'contrast.css black-on-white.css',
      'contrast.css yellow-on-blue.css',
      'contrast.css dyslexia.css',
    ),
  );

  // Some useful variables.
  $switcher = $base_path . $directory. "/accessibility/switcher.php";
  $imagesDir = $base_path . $directory. "/accessibility/images";
  $styleSetKeys = array_keys($styleSets);
  $themeDir = $base_path . $directory;
  
  /* Alter layout based on text size. */
  $textSizeLevel = $_COOKIE["switchstyles-textsize"] % count($styleSets["textsize"]);

 

  function getSwitchStyles() {
    global $styleSets, $themeDir;
    $styles = "<style type='text/css' media='all'>";
            
      /* Dynamically load the style sheets. */ 
      $stylesDir = $themeDir. "/accessibility/styles";
      foreach(array_keys($styleSets) as $styleSet) {
        $switchStyles = $styleSets[$styleSet][$_COOKIE["switchstyles-".$styleSet] % count($styleSets[$styleSet])];
        foreach(explode(" ", $switchStyles) as $style) {
          if ($style != "") {
            $styles .= "@import '".$stylesDir."/".$style."'; ";
          }
        }
      }
    $styles .= "</style>";
    
    return $styles;
  }

  function getSwitchButtons() {
    global $switcher, $styleSetKeys, $imagesDir;
    $switchButtons = <<<END_STRING2
      <ul>
      <li><a class="a-textsize" title="Accessibility: cycle text size" href="$switcher?switchcookie=switchstyles-$styleSetKeys[0]"><span class="access-hidden">Cycle text size</span><img src="$imagesDir/switch-textsize-off.png" class="rollover"/></a></li>
      <li><a class="a-colourscheme" title="Accessibility: cycle colour scheme" href="$switcher?switchcookie=switchstyles-$styleSetKeys[1]"><span class="access-hidden">Cycle colour scheme</span><img src="$imagesDir/switch-colourscheme-off.png" class="rollover"/></a></li>
      <li><a class="a-reset" title="Accessibility: reset style" href="$switcher?switchcookie=reset"><span class="access-hidden">Reset style</span><img src="$imagesDir/switch-reset-off.png" class="rollover"/></a></li>
      </ul>
END_STRING2;
    return $switchButtons;
  }

  function displayAccessKeys($logged_in) {
    ?>
      <div class="access-hidden">
        <h1>Accessibilty: Site Navigation</h1>
        <ul>
          <li><a href="/" accesskey="1">Go to home page</a></li>
          <li><a href="#main-content" accesskey="2">Skip to main content</a></li>
          <li><a href="/sitemap" accesskey="3">Go to site map</a></li>
          <li><a href="/?q=search/node" accesskey="4">Go to search page</a></li>
          <?php if ($logged_in) : ?>
            <li><a href="/?q=logout" accesskey="5">Logout</a></li>
            <li><a href="/?q=node/add" accesskey="6">Go to Create Content page</a></li>
            <li><a href="/?q=admin/content/node" accesskey="7">Go to View Content List page</a></li>
            <li><a href="/?q=admin" accesskey="8">Go to main Control Panel page</a></li>
          <?php else: ?>
            <li><a href="/?q=user/login" accesskey="5">Login</a></li>
          <?php endif; ?>
        </ul>
      </div>
    <?
  }

?>

