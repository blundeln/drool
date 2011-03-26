<?php include_once("drool.inc");?>
<?php

$output = '';

if (count($links) > 0) {
  $output = '<ul'. drupal_attributes($attributes) .'>';

  $num_links = count($links);
  $i = 1;

  foreach ($links as $key => $link) {
    $class = '';

    // Automatically add a class to each link and also to each LI
    if (isset($link['attributes']) && isset($link['attributes']['class'])) {
      $link['attributes']['class'] .= ' ' . $key;
      $class = $key;
    }
    else {
      $link['attributes']['class'] = $key;
      $class = $key;
    }

    // Add first and last classes to the list of links to help out themers.
    $extra_class = '';
    if ($i == 1) {
      $extra_class .= 'first ';
    }
    if ($i == $num_links) {
      $extra_class .= 'last ';
    }
    $output .= '<li class="'. $extra_class . $class .'">';

    // Is the title HTML?
    $html = isset($link['html']) && $link['html'];

    // Initialize fragment and query variables.
    $link['query'] = isset($link['query']) ? $link['query'] : NULL;
    $link['fragment'] = isset($link['fragment']) ? $link['fragment'] : NULL;

    /* Is this link active. */
    if (strstr($class, "active")) {
      $active = "active";
    } else {
      $active = "";
    }
    
    if (isset($link['href'])) {
      if ($skin == True) {
        $output .= startSkin("link", $active, False) . l($link['title'], $link['href'], $link['attributes'], $link['query'], $link['fragment'], FALSE, $html) . stopSkin("link", False);
      } else {
        $output .= l($link['title'], $link['href'], $link['attributes'], $link['query'], $link['fragment'], FALSE, $html);
      }
    }
    else if ($link['title']) {
      //Some links are actually not links, but we wrap these in <span> for adding title and class attributes
      if (!$html) {
        $link['title'] = check_plain($link['title']);
      }
      $output .= '<span'. drupal_attributes($link['attributes']) .'>'. $link['title'] .'</span>';
    }

    $i++;
    $output .= "</li>\n";
  }

  $output .= '</ul>';
}

print $output;

?>
