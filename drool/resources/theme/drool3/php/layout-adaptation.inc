<?php

  global $emSize;
  /* This cookie gets set by the jqem js script. */
  $emSize = $_COOKIE["emsize"];

  /* Nick Blundell 2007 */
  function getMaxColumns() {
    global $emSize;

    if (!$emSize) {
      return 3;
    }
    if ($emSize > 26 ) {
      return 1;
    } elseif ($emSize > 16) {
      return 2;
    } else {
      return 3;
    }
  }

  function showLeftColumn($sidebar_left, $sidebar_right) {
    $noAccessColumns = getMaxColumns();
    if ($noAccessColumns == 3 && $sidebar_left){
      return True;
    }
    return False;
  }
  
  function showRightColumn($sidebar_left, $sidebar_right) {
    $noAccessColumns = getMaxColumns();
    if (($noAccessColumns == 3 and $sidebar_right) or ($noAccessColumns == 2 and ($sidebar_left or $sidebar_right))) {
      return True;
    }
    return False;
  }

  function adaptColumns($sidebar_left, $sidebar_right) {
    $columnData = array();
    $columnData["sidebar_left"] = $sidebar_left;
    $columnData["sidebar_right"] = $sidebar_right;
    
    /* Figure out which columns should show, based also on font size. */
    $showLeftCol = showLeftColumn($sidebar_left, $sidebar_right);
    $showRightCol = showRightColumn($sidebar_left, $sidebar_right);

    
    if ($sidebar_left and !$showLeftCol and $showRightCol) {
      $columnData["sidebar_right"] = $sidebar_left . $sidebar_right;
      $columnData["sidebar_left"] = "";
    }
    
    if (!$showLeftCol and !$showRightCol) {
      $columnData["dropped_sidebar_content"] = $sidebar_left . $sidebar_right;
      $columnData["sidebar_left"] = "";
      $columnData["sidebar_right"] = "";
    }

    return $columnData;
  }

  function adaptStyle($default, $emThreshold, $adaptedStyle) {
    global $emSize;
    if ($emSize > $emThreshold) {
      return $adaptedStyle;
    } else {
      return $default;
    }
  }

?>
