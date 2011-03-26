<?php
  /*
   * Drool4 theme by Nick Blundell (www.nickblundell.org.uk) 2008.
   * This theme aims to be highly-flexible, -stable (css layout), and -accessible.
   */

  $vars = get_defined_vars();
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="<?php print $language->language ?>" xml:lang="<?php print $language->language ?>">

<?php include_once("skin/skin.inc"); /* For skinning functions startSkin() and stopSkin() */ ?>
<?php include_once("accessibility/accessibility.inc"); /* for style switchers and accessibility functions */ ?>
<?php include_once("php/layout-adaptation.inc"); /* for adapting layout to browser's real text size */ ?>

<head>
  <title><?php print $head_title; ?></title>
  <?php print $head; ?>
  <?php print $styles; ?>
  <?php print $scripts; ?>
  <?php print getSwitchStyles(); ?>
  
  <!-- Tend to our little IE friends - those silly Billys ;) -->
  <!--[if IE 6]>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/css/fix-ie-6.css";</style>
  <![endif]-->
  <!--[if IE 7]>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/css/fix-ie-7.css";</style>
  <![endif]-->

</head>

<?php

/*
 * ===========================================================================================================
 * REGION RENDERING FUNCTIONS - as individual functions, we can drop them into different layouts more easily.
 * ===========================================================================================================
 */

/*
 * --------------------
 * Header
 * --------------------
 */

function renderHeader($vars) {
  /* Turn $vars into local variables - there must be an easier way, perhaps using sub-page themes. */
  foreach ($vars as $key=>$value) {
    eval("\$$key = \$vars['$key'];");
  }

  ?>
  <div id="header">
    <?php startSkin("header");?>
     
      <div class="access-hidden">
        <h1>Page Header</h1>
        The following content is the page header.
      </div>
      
      <div id="logo-title">
       
        <?php if (!empty($logo)): ?>
          <div id="logo">
          <a href="<?php print $base_path; ?>" title="<?php print t('Home'); ?>" rel="home">
            <img src="<?php print $logo; ?>" alt="<?php print t('Home'); ?>" />
          </a>
          </div>
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
        <?php //startSkin("accessibility");?>
          <h1 class="access-hidden">Accessibilty: Site Presentation</h1>
          <?php print getSwitchButtons(); ?>
        <?php //stopSkin("accessibility");?>
      </div>
      
      <?php print $search_box; ?>      
     
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

      
    <?php stopSkin("header");?>
    </div> <!-- /header -->
      
         
    <?php if (!empty($header) || !empty($breadcrumb)): ?>
      <div id="header-region">
        <?php print $breadcrumb; ?>
        <?php print $header; ?>
      </div>
    <?php endif; ?>
    

  <?
};

/*
 * --------------------
 * Main content
 * --------------------
 */

function renderContent($vars) {
  /* Turn $vars into local variable - there must be an easier way, perhaps using sub-page themes. */
  foreach ($vars as $key=>$value) {
    eval("\$$key = \$vars['$key'];");
  }
  ?>

  <?php //startSkin("content");?>
        <?php if (!empty($mission)): ?><div id="mission"><?php print $mission; ?></div><?php endif; ?>
        <?php if (!empty($content_top)):?><div id="content-top"><?php print $content_top; ?></div><?php endif; ?>
        <div id="content">
          <div class="access-hidden">
            <h1>Main Content</h1>
            The following content is the main page content.
          </div>
          <a name="main-content"></a>
          <?php if (!empty($title)): ?><h1 class="title"><?php print $title; ?></h1><?php endif; ?>
          <?php if (!empty($tabs)): ?><div class="tabs"><?php print $tabs; ?></div><?php endif; ?>
          <?php print $help; ?>
          <?php print $messages; ?>
          <?php print $content; ?>
          <?php print $feed_icons; ?>
        </div> <!-- /content -->
        <?php if (!empty($content_bottom)): ?><div id="content-bottom"><?php print $content_bottom; ?></div><?php endif; ?>
  <?php //stopSkin("content");?>
  <?
};

/*
 * --------------------
 * Sidebars and footer
 * --------------------
 */

function renderLeftSidebar($vars) {
  $left = $vars['left'];
  ?>
  <?php if (!empty($left)): ?>
    <div class="access-hidden">
      <h1>Left Sidebar</h1>
      The following content is part of the left side-content panel.
    </div>
    <div id="sidebar-left" class="column sidebar">
      <?php print $left; ?>
    </div> <!-- /sidebar-left -->
  <?php endif; ?>  
  <?
};

function renderRightSidebar($vars) {
  $right = $vars['right'];
  ?>
  <?php if (!empty($right)): ?>
    <div class="access-hidden">
      <h1>Right Sidebar</h1>
      The following content is part of the right side-content panel.
    </div>
    <div id="sidebar-right" class="column sidebar">
      <?php print $right; ?>
    </div> <!-- /sidebar-right -->
  <?php endif; ?>  
  <?
};

function renderFooter($vars) {
  $footer = $vars['footer_message'];
  ?>
  <?php startSkin("footer");?>
    <div id="footer">
      <div class="access-hidden">
        <h1>Page Footer</h1>
        The following content is the page footer.
      </div>
      <?php print $footer; ?>
    </div> <!-- /footer -->
  <?php stopSkin("footer");?>
  <?
}

?>


<?php
/*
 * ===========================================================================================================
 * HTML LAYOUT - by separating this from the regional HTML, we can easily change the html layout of the page.
 * ===========================================================================================================
 */
?>

<?php
  /*
   * Here we prepare the ATCK grid layout variables, allowing layout adaptation for browser font size.
   */
  global $body_classes;

  /* Set default ATCK grid layout modes, allowing them to be adapted based on current font size. */
  /* For more info on configuring ATCK layouts, see http://atck.highervisibilitywebsites.com */
  $pageStyle = adaptStyle("fixed-md",16,"fluid");
  $layoutStyle = adaptStyle("classic",16,"standard");

  /* Adapt columns based on current text size. */
  $adaptedColumns = adaptColumns($left, $right);
  $vars["left"] = $adaptedColumns["left"];
  $vars["right"] = $adaptedColumns["right"];
  $vars["dropped_sidebar_content"] = $adaptedColumns["dropped_sidebar_content"];

  /* Determine ATCK grid layout for columns based on the presence sidebar content. */
  if ($vars["left"] && $vars["right"]) {
    $layoutColumns="a-b-c";
  } 
  elseif ($vars["left"]) {
    $layoutColumns="a-b";
  } elseif ($vars["right"]) {
    $layoutColumns="b-c";
  };

  /* Allow style to be altered based on sidebar display. */
  if ($vars["left"] && $vars["right"]) {
    $body_classes .= ' both-sidebars';
  } elseif ($vars["left"]) {
    $body_classes .= ' sidebar-left';
  } elseif ($vars["right"]) {
    $body_classes .= ' sidebar-right';
  } else {
    $body_classes .= ' sidebar-none';
  }

?>

<?php /* different ids allow for separate theming of the home page */ ?>
<body class="<?php print $body_classes; ?> center">

  <?php displayAccessKeys($logged_in); /* We want this right at the top of the page. */ ?>
  
  <!--DROOL_CONTROLBAR-->
  
  <div id="container" class="<?php print $pageStyle; ?>">  
    
    <div id="page">
    <?php startSkin("page");?>
      
      <?php /* HEADER */ ?>
      <div class="section" id="hd"><?php renderHeader($vars); ?></div>  
      
      <?php /* MAIN */ ?>
      <div class="section" id="bd">
        <div class="<?php print $layoutStyle; ?>">  
           <div class="layout <?php print $layoutColumns;?>">  
             
             <?php /* LEFT SIDEBAR */ ?>
             <?php if (!empty($vars["left"])): ?>
               <div class="gr a"><?php renderLeftSidebar($vars); ?></div>  
             <?php endif; ?>
             
             <?php /* CONTENT */ ?>
             <div class="gr b front"><?php renderContent($vars); ?></div>  
             
             <?php /* RIGHT SIDEBAR */ ?>
             <?php if (!empty($vars["right"])): ?>
               <div class="gr c"><?php renderRightSidebar($vars); ?></div>  
             <?php endif; ?>
           
           </div>

        </div> 
      </div>  
     
      <?php /* If the font is too big for sidebars, their content will drop down to here. */ ?>
      <?php if (!empty($vars["dropped_sidebar_content"])): ?>
        <div class="section" id="droppedcontent">
          <?php print $vars["dropped_sidebar_content"]; ?>
        </div>
      <?php endif; ?>
      
      <?php /* FOOTER */ ?>
      <div class="section" id="ft">
        <?php renderFooter($vars); ?>
      </div>  
    
    <?php stopSkin("page");?>
    </div> <!-- /page -->
  
  </div> <!-- container -->
  <?php displayAccessKeys($logged_in); /* Screen reader users find this repeated content useful */ ?>

  <?php print $closure; ?>

</body>
</html>
