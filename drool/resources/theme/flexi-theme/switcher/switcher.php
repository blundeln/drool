<?php
/* N Blundell 2006 */
$switchcookie = $_GET['switchcookie'];
if ($switchcookie == "reset") {
  foreach (array("graphical","colourscheme","textsize") as $cookie) {
    setcookie("switchstyles-".$cookie, 0, time()+31536000, '/','',0);
  }
} else {
  $value = $_COOKIE[$switchcookie];
  $value = $value + 1;
  setcookie ($switchcookie, $value, time()+31536000, '/', '', 0);
}
  header("Location: $_SERVER[HTTP_REFERER]");
?>
