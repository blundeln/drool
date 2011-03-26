<?php
  function blockRename($block) {
    
    /* Edit this to rename blocks */
    if ($block->subject == "Events") {return "Events";}
    else if ($block->subject == "User login") {return "User login";}
    
    return $block->subject;
  }
?>
