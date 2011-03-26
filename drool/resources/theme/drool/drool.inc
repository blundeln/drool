<?php
  /* Nick Blundell 2007 */
  function startSkin($skinName, $classes="", $display=True, $skinID="", $clear=True) {
    $skinName .= "skin";
    for ($i=0;$i<9;$i++) {
      if ($i==0) {
        $classes = "$skinName $classes";
        $id = ($skinID != "") ? "id='$skinID' " : "";
      } else {
        $classes = "$skinName$i";
        $id = "";
      }
     
      if ($i == 0) {
        $classes .= " skin";
      }
     
      if ($i==8) {
        $classes .= " $skinName-inner";
      }
      
      if ($clear == True) {
        $classes .= " clear-block";
      } 
      
      $output .= "<div $id class='$classes'>";
    }
    if ($display==True) {
      print $output."\n";
    } else {
      return $output;
    }
  }
  
  function stopSkin($skinName, $display=True) {
    $skinName .= "skin";
    $skinName .= "skin";
    $output = "";
    for ($i=0;$i<9;$i++) {
      $output .= "</div>";
    }
    if ($display==True) {
      print $output."\n";
    } else {
      return $output;
    }
  }
?>
