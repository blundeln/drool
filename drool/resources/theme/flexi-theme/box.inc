<?php
  function startBox($boxName, $additionalClasses="") {
    for ($i=1;$i<9;$i++) {
      if ($i==1) {$classes = " ".$additionalClasses;}
      if ($i==8 or true) {$clear=" clear";}
      $output .= "<div class='$boxName$i$classes$clear'>";
      $classes = "";
    }
    print $output."\n";
  }
  
  function stopBox($boxName) {
    $output = "";
    for ($i=1;$i<9;$i++) {
      $output .= "</div>";
    }
    print $output."\n";
  }
?>
