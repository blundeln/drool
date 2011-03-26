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

  function showLeftColumn($left, $right) {
    $noAccessColumns = getMaxColumns();
    if ($noAccessColumns == 3 && $left){
      return True;
    }
    return False;
  }
  
  function showRightColumn($left, $right) {
    $noAccessColumns = getMaxColumns();
    if (($noAccessColumns == 3 and $right) or ($noAccessColumns == 2 and ($left or $right))) {
      return True;
    }
    return False;
  }

  function adaptColumns($left, $right) {
    $columnData = array();
    $columnData["left"] = $left;
    $columnData["right"] = $right;
    
    /* Figure out which columns should show, based also on font size. */
    $showLeftCol = showLeftColumn($left, $right);
    $showRightCol = showRightColumn($left, $right);

    
    if ($left and !$showLeftCol and $showRightCol) {
      $columnData["right"] = $left . $right;
      $columnData["left"] = "";
    }
    
    if (!$showLeftCol and !$showRightCol) {
      $columnData["dropped_sidebar_content"] = $left . $right;
      $columnData["left"] = "";
      $columnData["right"] = "";
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
