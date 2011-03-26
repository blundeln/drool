<?php
  /* Nick Blundell 2006 */
  /* Define variables and the dynamic style sets. */
  global $styleSets, $themeDir, $styleSetKeys, $switcher, $ieStyle;
  $ieStyle = FALSE;
  $styleSets = array(
    "graphical" => array (
      'graphical.css droolgen.css variables.css',
      'graphical.css droolgen.css variables.css',
    ),
    "textsize" => array (
      '',
      'text-medium.css',
      'text-large.css',
      'text-vlarge.css',
    ),
    "colourscheme" => array (
      '',
      'contrast.css black-on-white.css',
      'contrast.css yellow-on-blue.css',
    ),
  );

  // Some useful variables.
  $switcher = $base_path . $directory. "/switcher/switcher.php";
  $styleSetKeys = array_keys($styleSets);
  $themeDir = $base_path . $directory;
  
  /* Set the layout variable. */
  $simpleLayout = $_COOKIE["switchstyles-graphical"] % count($styleSets["graphical"]);
  
  
  function importSwitchStyles() {
    global $styleSets, $themeDir,$ieStyle;
    print "<style type='text/css' media='all'>";
            
      /* Dynamically load the style sheets. */ 
      $stylesDir = $themeDir. "/styles";
      foreach(array_keys($styleSets) as $styleSet) {
        $switchStyles = $styleSets[$styleSet][$_COOKIE["switchstyles-".$styleSet] % count($styleSets[$styleSet])];
        if (strpos($switchStyles, "graphical") !== FALSE) {
          $ieStyle = TRUE;
        }
        foreach(explode(" ", $switchStyles) as $style) {
          if ($style != "") {
            print "@import '".$stylesDir."/".$style."'; ";
          }
        }
      }
    print "</style>";
 
  }

  function displaySwitchButtons() {
    global $switcher, $styleSetKeys;
    ?>
    <div id="switchbuttons">
      <ul>
      <li><a class="a-graphical" title="Accessibility: cycle graphical layout" href="<?php print $switcher.'?switchcookie=switchstyles-'.$styleSetKeys[0]?>">&nbsp;</a></li>
      <li><a class="a-textsize" title="Accessibility: cycle text size" href="<?php print $switcher.'?switchcookie=switchstyles-'.$styleSetKeys[1]?>">&nbsp;</a></li>
      <li><a class="a-colourscheme" title="Accessibility: cycle colour scheme" href="<?php print $switcher.'?switchcookie=switchstyles-'.$styleSetKeys[2]?>">&nbsp;</a></li>
      <li><a class="a-reset" title="Accessibility: reset style" href="<?php print $switcher.'?switchcookie=reset'?>">&nbsp;</a></li>
      </ul>
    </div>
    <?php
  }
?>

