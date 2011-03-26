<?php
  /* Nick Blundell 2007 */
  /* Define variables and the dynamic style sets. */
  global $styleSets, $themeDir, $styleSetKeys, $switcher, $noAccessColumns, $imagesDir;
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
  if ($textSizeLevel > 2 ) {
    $noAccessColumns = 1;
  } elseif ($textSizeLevel > 0) {
    $noAccessColumns = 2;
  } else {
    $noAccessColumns = 3;
  }


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

  function showLeftColumn($sidebar_left, $sidebar_right) {
    global $noAccessColumns;
    if ($noAccessColumns == 3 && $sidebar_left){
      return True;
    }
    return False;
  }
  
  function showRightColumn($sidebar_left, $sidebar_right) {
    global $noAccessColumns;
    if (($noAccessColumns == 3 and $sidebar_right) or ($noAccessColumns == 2 and ($sidebar_left or $sidebar_right))) {
      return True;
    }
    return False;
  }
?>

