<?php
/**
 * Sets the body-tag class attribute.
 *
 * Adds 'sidebar-left', 'sidebar-right' or 'sidebars' classes as needed.
 */
function oldphptemplate_body_class($sidebar_left, $sidebar_right) {
  if ($sidebar_left != '' && $sidebar_right != '') {
    $class = 'sidebars';
  } elseif ($sidebar_left != '') {
    $class = 'sidebar-left';
  } elseif ($sidebar_right != '') {
    $class = 'sidebar-right';
  } else {
    $class = 'sidebar-none';
  }
  

  if (isset($class)) {
    print ' class="'. $class .'"';
  }
}

function phptemplate_body_class($showLeft, $showRight) {
  if ($showLeft && $showRight) {
    $class = 'sidebars';
  } elseif ($showLeft) {
    $class = 'sidebar-left';
  } elseif ($showRight) {
    $class = 'sidebar-right';
  } else {
    $class = 'sidebar-none';
  }

  if (isset($class)) {
    print ' class="'. $class .'"';
  }
}

/**
 * Return a themed breadcrumb trail.
 *
 * @param $breadcrumb
 *   An array containing the breadcrumb links.
 * @return a string containing the breadcrumb output.
 */
function phptemplate_breadcrumb($breadcrumb) {
  if (!empty($breadcrumb)) {
    return '<div class="breadcrumb">'. implode(' › ', $breadcrumb) .'</div>';
  }
}

/**
 * Allow themable wrapping of all comments.
 */
function phptemplate_comment_wrapper($content, $type = null) {
  static $node_type;
  if (isset($type)) $node_type = $type;

  if (!$content || $node_type == 'forum') {
    return '<div id="comments">'. $content . '</div>';
  }
  else {
    return '<div id="comments"><h2 class="comments">'. t('Comments') .'</h2>'. $content .'</div>';
  }
}

/**
 * Override or insert PHPTemplate variables into the templates.
 */
function _phptemplate_variables($hook, $vars) {
  if ($hook == 'page') {

    if ($secondary = menu_secondary_local_tasks()) {
      $output = '<span class="clear"></span>';
      $output .= "<ul class=\"tabs secondary\">\n". $secondary ."</ul>\n";
      $vars['tabs2'] = $output;
    }

    // Hook into color.module
    if (module_exists('color')) {
      _color_page_alter($vars);
    }
    return $vars;
  }
  return array();
}

/**
 * Returns the rendered local tasks. The default implementation renders
 * them as tabs.
 *
 * @ingroup themeable
 */
function phptemplate_menu_local_tasks() {
  $output = '';

  if ($primary = menu_primary_local_tasks()) {
    $output .= "<ul class=\"tabs primary\">\n". $primary ."</ul>\n";
  }

  return $output;
}


function phptemplate_links($links, $attributes = array('class' => 'links'), $skin=False) {
  /**
  * catches the theme_links function and calls back a link.tpl.php file to determine the layout
  */
  return _phptemplate_callback('links', array('links' => $links, 'attributes' => $attributes, 'skin' => $skin));
}
