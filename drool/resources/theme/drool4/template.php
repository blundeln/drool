<?php
 
/*
 * Declare the available regions implemented by this engine.
 *
 * @return
 *    An array of regions.  The first array element will be used as the default region for themes.
 *    Each array element takes the format: variable_name => t('human readable name')
 */
function drool4_regions() {
  return array(
       'left' => t('left sidebar'),
       'right' => t('right sidebar'),
       'content_top' => t('content top'),
       'content_bottom' => t('content bottom'),
       'header' => t('header'),
       'footer' => t('footer')
  );
} 


/**
* Return a themed breadcrumb trail.
*
* @param $breadcrumb
*   An array containing the breadcrumb links.
* @return a string containing the breadcrumb output.
*/
function drool4_breadcrumb($breadcrumb) {
 if (!empty($breadcrumb)) {
   return '<div class="breadcrumb">'. implode(' :: ', $breadcrumb) .'</div>';
 }
}
 

/* Sets up template variables. */
function phptemplate_preprocess_page(&$vars) {
  
  global $theme, $theme_key, $user;
  
  // if we're in the main theme
  if ($theme == $theme_key) {
    drupal_add_css($vars['directory'] .'/css/atck.css', 'theme', 'all');
    drupal_add_css($vars['directory'] .'/skin/skin.css', 'theme', 'all');
    drupal_add_css($vars['directory'] .'/css/icons.css', 'theme', 'all');
    drupal_add_css($vars['directory'] .'/main-style.css', 'theme', 'all');
    $vars['css'] = drupal_add_css($vars['directory'] .'/print.css', 'theme', 'print');
    $vars['styles'] = drupal_get_css();
    // Nick
    drupal_add_js($vars['directory'] .'/js/jqem-compressed.js');
    drupal_add_js($vars['directory'] .'/js/jquery.cookie.js');
    drupal_add_js($vars['directory'] .'/js/scripts.js');
    $vars['scripts'] = drupal_get_js();
  }
  
  // An anonymous user has a user id of zero.      
  if ($user->uid > 0) {
    // The user is logged in.
    $vars['logged_in'] = TRUE;
  }
  else {
    // The user has logged out.
    $vars['logged_in'] = FALSE;
  }
  
  $body_classes = array();
  // classes for body element
  // allows advanced theming based on context (home page, node of certain type, etc.)
  $body_classes[] = ($vars['is_front']) ? 'front' : 'not-front';
  $body_classes[] = ($vars['logged_in']) ? 'logged-in' : 'not-logged-in';
  if ($vars['node']->type) {
    // if on an individual node page, put the node type in the body classes
    $body_classes[] = 'ntype-'. drool4_id_safe($vars['node']->type);
  }
  // implode with spaces
  $vars['body_classes'] = implode(' ', $body_classes);
}


/**
* Converts a string to a suitable html ID attribute.
* - Preceeds initial numeric with 'n' character.
* - Replaces space and underscore with dash.
* - Converts entire string to lowercase.
* - Works for classes too!
* 
* @param string $string
*  the string
* @return
*  the converted string
*/
function drool4_id_safe($string) {
  if (is_numeric($string{0})) {
    // if the first character is numeric, add 'n' in front
    $string = 'n'. $string;
  }
  return strtolower(preg_replace('/[^a-zA-Z0-9-]+/', '-', $string));
}


