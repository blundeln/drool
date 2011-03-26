<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="<?php print $language ?>" xml:lang="<?php print $language ?>">

<?php include_once("skin/skin.inc"); /* For skinning */ ?>
<?php include_once("accessibility/accessibility.inc"); /* for style switchers */ ?>

<?php 
  // Useful variables
  $themeUrl = $base_path . $directory;
?>

<?php
  /* TODO: Move this into a nice function juggleColumns(l, r) returns l, r, dropped */
  /* Figure out which columns should show, based also on font size. */
  $showLeftCol = showLeftColumn($sidebar_left, $sidebar_right);
  $showRightCol = showRightColumn($sidebar_left, $sidebar_right);
  
  if ($showLeftCol && $showRightCol) {
    $body_classes .= ' both-sidebars';
  } elseif ($showLeftCol) {
    $body_classes .= ' sidebar-left';
  } elseif ($showRightCol) {
    $body_classes .= ' sidebar-right';
  } else {
    $body_classes .= ' sidebar-none';
  }

  if ($sidebar_left and !$showLeftCol and $showRightCol) {
    $sidebar_right = $sidebar_left . $sidebar_right;
    $sidebar_left = "";
  }
  
  if (!$showLeftCol and !$showRightCol) {
    $dropped_sidebar_content = $sidebar_left . $sidebar_right;
    $sidebar_left = "";
    $sidebar_right = "";
  }

?>

<head>
  <title><?php print $head_title; ?></title>
  <?php print $head; ?>
  <?php print $styles; ?>
  <?php print $scripts; ?>
  <?php print getSwitchStyles(); ?>
</head>

<?php /* different ids allow for separate theming of the home page */ ?>
<body class="<?php print $body_classes; ?>">

  <div id="page">
  <?php startSkin("page");?>
    <div id="header">
    <?php startSkin("header");?>
      <div id="logo-title">
      
        <?php print $search_box; ?>      
        <?php if (!empty($logo)): ?>
          <a href="<?php print $base_path; ?>" title="<?php print t('Home'); ?>" rel="home">
            <img src="<?php print $logo; ?>" alt="<?php print t('Home'); ?>" id="logo" />
          </a>
        <?php endif; ?>
        
        <div id="name-and-slogan">
        
        <?php if (!empty($site_name)): ?>
          <h1 id='site-name'>
            <a href="<?php print $base_path ?>" title="<?php print t('Home'); ?>" rel="home">
              <?php print $site_name; ?>
            </a>
          </h1>
        <?php endif; ?>
        
        <?php if (!empty($site_slogan)): ?>
          <div id='site-slogan'>
            <?php print $site_slogan; ?>
          </div>
        <?php endif; ?>
        
        </div> <!-- /name-and-slogan -->
        
      </div> <!-- /logo-title -->
     
      <div id="access-buttons" class="clear-block">
        <?php startSkin("accessibility");?>
          <h1 class="access-hidden">Accessibilty: Site Presentation</h1>
          <?php print getSwitchButtons(); ?>
        <?php stopSkin("accessibility");?>
      </div>
     
  
     
      <div id="navigation" class="menu <?php if ($primary_links) { print "withprimary"; } if ($secondary_links) { print " withsecondary"; } ?> ">
          <?php if (!empty($primary_links)): ?>
            <div id="primary" class="clear-block">
              <?php //print theme('menu_links', $primary_links); ?>
              <?php print theme('links', $primary_links, array('class' => 'links primary-links'), $skin=True) ?>
            </div>
          <?php endif; ?>
          
          <?php if (!empty($secondary_links)): ?>
            <div id="secondary" class="clear-block">
              <?php //print theme('menu_links', $secondary_links); ?>
              <?php print theme('links', $secondary_links, array('class' => 'links secondary-links'), $skin=True) ?>
            </div>
          <?php endif; ?>
      </div> <!-- /navigation -->
      
      <?php if (!empty($header) || !empty($breadcrumb)): ?>
        <div id="header-region">
          <?php print $breadcrumb; ?>
          <?php print $header; ?>
        </div>
      <?php endif; ?>
      
    <?php stopSkin("header");?>
    </div> <!-- /header -->

    <div id="container" class="clear-block">
                  
      <?php if (!empty($sidebar_left)): ?>
        <div id="sidebar-left" class="column sidebar">
          <?php print $sidebar_left; ?>
        </div> <!-- /sidebar-left -->
      <?php endif; ?>  
    
      <div id="main" class="column"><div id="squeeze">
      <?php //startSkin("main"); /* This messes up IE6 */?>
        <?php if (!empty($mission)): ?><div id="mission"><?php print $mission; ?></div><?php endif; ?>
        <?php if (!empty($content_top)):?><div id="content-top"><?php print $content_top; ?></div><?php endif; ?>
        <div id="content">
          <?php if (!empty($title)): ?><h1 class="title"><?php print $title; ?></h1><?php endif; ?>
          <?php if (!empty($tabs)): ?><div class="tabs"><?php print $tabs; ?></div><?php endif; ?>
          <?php print $help; ?>
          <?php print $messages; ?>
          <?php print $content; ?>
          <?php print $feed_icons; ?>
        </div> <!-- /content -->
        <?php if (!empty($content_bottom)): ?><div id="content-bottom"><?php print $content_bottom; ?></div><?php endif; ?>
      <?php //stopSkin("main");?>
      </div></div> <!-- /squeeze /main -->

      <?php if (!empty($sidebar_right)): ?>
        <div id="sidebar-right" class="column sidebar">
          <?php print $sidebar_right; ?>
        </div> <!-- /sidebar-right -->
      <?php endif; ?>

      <?php if (!empty($dropped_sidebar_content)): ?>
        <div>
          <?php print $dropped_sidebar_content; ?>
        </div>
      <?php endif; ?>  
    
    </div> <!-- /container -->

    <div id="footer-wrapper">
    <?php startSkin("footer");?>
      <div id="footer">
        <?php print $footer_message; ?>
      </div> <!-- /footer -->
    <?php stopSkin("footer");?>
    </div> <!-- /footer-wrapper -->
    
    <?php print $closure; ?>
    
  <?php stopSkin("page");?>
  </div> <!-- /page -->

</body>
</html>
