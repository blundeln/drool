return _phptemplate_callback('page', $variables, $suggestions);
>>>
include_once "./drool/controlbar/controlbar.php";
$renderedPage = _phptemplate_callback('page', $variables, $suggestions);
  if (strstr($renderedPage, "<!--DROOL_CONTROLBAR-->")) {
    $renderedPage = str_replace("<!--DROOL_CONTROLBAR-->",$renderedControlPanel ,$renderedPage);
  } else {
    $renderedPage = preg_replace("/(<body.*>)/","$1\n".$renderedControlPanel ,$renderedPage);
  }
return $renderedPage;
