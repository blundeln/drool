<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php print $language ?>" lang="<?php print $language ?>">

<?php include_once("access/access.inc");?>
<?php include_once("drool.inc");?>

<?php
  global $user;
?>
  
  <head>
    <title><?php print $head_title ?></title>
    <?php print $head ?>
    <?php print $styles ?>
    <?php print $scripts ?>
    <style type="text/css" media="print">@import "<?php print base_path() . path_to_theme() ?>/print.css";</style>
    
    
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/hg-layout.css";</style>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/style.css";</style>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/skin.css";</style>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/variables.css";</style>
  
    <?php print getSwitchStyles(); ?>
    
    <!--[if lt IE 7]>
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/fix-ie.css";</style>
    <![endif]-->
    
    <style type="text/css" media="all">@import "<?php print base_path() . path_to_theme() ?>/styles/final.css";</style>
   
    <?php
    $showLeftCol = showLeftColumn($sidebar_left, $sidebar_right);
    $showRightCol = showRightColumn($sidebar_left, $sidebar_right);
    ?>
   
  </head>
  
  <body<?php phptemplate_body_class($showLeftCol, $showRightCol); ?>>
  
  <div class="access-hidden">
  <h1>Accessibilty: Site Navigation</h1>
  <ul>
  <li><a href="#accesskeys" accesskey="0">Go to access key guide</a></li>
  <li><a href="/" accesskey="1">Go to home page</a></li>
  <li><a href="#main-content" accesskey="2">Skip to main content</a></li>
  <li><a href="/sitemap" accesskey="3">Go to site map</a></li>
  <li><a href="/?q=search/node" accesskey="4">Go to search page</a></li>
  <?php if ($user->uid > 0) : ?>
    <li><a href="/?q=logout" accesskey="5">Logout</a></li>
    <li><a href="/?q=node/add" accesskey="6">Go to Create Content page</a></li>
    <li><a href="/?q=admin/content/node" accesskey="7">Go to View Content List page</a></li>
    <li><a href="/?q=admin" accesskey="8">Go to main Control Panel page</a></li>
  <?php else: ?>
    <li><a href="/?q=user/login" accesskey="5">Login</a></li>
  <?php endif; ?>
  </ul>
  </div>

  <!--DROOL_CONTROLBAR-->

  <div id="page">
  <?php startSkin("page");?>
	<div id="header">
    <?php startSkin("header");?>
    <div id="header-upper">
    <?php startSkin("header-upper");?>
    <?php
      if ($logo) {
        print '<div id="logo"><a href="'. check_url($base_path) .'" title="'. 'Home page' .'">';
        print '<img src="'. check_url($logo) .'" alt="'. 'Home page' .'"/>';
        print '</a></div>';
      }
      print "<div id='name-slogan-wrap'>";
      if ($site_name) {
        print '<div id="site-name"><h1><a href="'. check_url($base_path) .'" title="'. $site_name .'">' . $site_name .'</a></h1></div>';
      }
      if ($site_slogan) {
        print "<div id='site-slogan'><h2>" . check_plain($site_slogan) . "</h2></div>";
      }
      print "</div>";

    ?>


    <div id="access-buttons">
    <?php startSkin("accessibility");?>
    <h1 class="access-hidden">Accessibilty: Site Presentation</h1>
    <?php print getSwitchButtons(); ?>
    <?php stopSkin("accessibility");?>
    </div>
    
    <div id="search-box"><?php if ($search_box): ?><div><?php print $search_box ?></div><?php endif; ?></div>
    
    <?php stopSkin("header-upper");?>
    </div>
    
    <div id="header-bar" class="clear-block">
      <?php startSkin("header-bar");?>
      <div id="primary-links">
      <?php if (isset($primary_links)) : ?>
        <h1 class="access-hidden">Primary Links</h1>
        <?php print theme('links', $primary_links, array('class' => 'links primary-links'), $skin=True) ?>
      <?php endif; ?>
      </div>
      <div id="secondary-links">
      <?php if (isset($secondary_links)) : ?>
        <h1 class="access-hidden">Secondary Links</h1>
        <?php print theme('links', $secondary_links, array('class' => 'links secondary-links'), $skin=True) ?>
      <?php endif; ?>
      </div>
      <?php stopSkin("header-bar");?>
    </div>
  
    <?php if ($header) : ?>
    <div id="header-region" class="clear-block"><?php print $header; ?></div>
    <?php endif; ?>
    
    <?php stopSkin("header");?>
   
  </div> <!-- Header -->


	<div id="container">

    
    <div id="maincontent" class="column">
      <?php startSkin("content");?>
			<?php if ($breadcrumb): print "<h1 class='access-hidden'>Current Location</h1>" . $breadcrumb; endif; ?>
      <?php if ($mission): print '<div id="mission">'. $mission .'</div>'; endif; ?>

      <h1 class="access-hidden">Main Content</h1>
      <a name="main-content"></a>
      <h1 class="title"><?php print $title ?></h1>
      <div class="tabs clear-block"><?php print $tabs ?></div>

      <?php if (isset($tabs2)): print $tabs2; endif; ?>

      <?php if ($help): print $help; endif; ?>
      <?php if ($messages): print $messages; endif; ?>
      <?php print $content ?>
      <span class="clear"></span>
      <?php print $feed_icons ?>
      <?php stopSkin("content");?>
		</div>

    <?php if ($sidebar_left or $sidebar_right) : ?>
    <h1 class="access-hidden">Side Content</h1>
    <?php endif;?>

		<div id="leftbar" class="column">
			<?php if ($showLeftCol): ?>
        <div id="sidebar-left" class="sidebar">
          <?php if ($sidebar_left) {print $sidebar_left;} ?>
        </div>
      <?php endif; ?>
		</div>

		<div id="rightbar" class="column">
      <?php if ($showRightCol): ?>
        <div id="sidebar-right" class="sidebar">
          <?php if ($sidebar_left and !$showLeftCol) {print $sidebar_left;} ?>
          <?php if ($sidebar_right) {print $sidebar_right;} ?>
        </div>
      <?php endif; ?>
    </div>

	</div>

  <?php if (!$showLeftCol and !$showRightCol) : ?>
    <?php if ($sidebar_left): ?>
      <div style="clear:both;" id="sidebar-left" class="sidebar">
        <?php print $sidebar_left; ?>
      </div>
    <?php endif; ?>
    <?php if ($sidebar_right): ?>
      <div style="clear:both;" id="sidebar-right" class="sidebar">
        <?php print $sidebar_right; ?>
      </div>
    <?php endif; ?>
  <?php endif; ?>

  <h1 class="access-hidden">Page Footer</h1>
	
  <div id="footer">
  <?php startSkin("footer");?>
  <?php print $footer_message ?>
  <?php stopSkin("footer");?>
  </div>

  <div class="access-hidden">
  <h1>Accessibilty: Quick Reference</h1>
  <a name="accesskeys"></a>
  The following browser access keys are available:
  <ul> 
  <li>Key 0: Go to access key guide</li>
  <li>Key 1: Go to home page</li>
  <li>Key 2: Skip to main content</li>
  <li>Key 3: Go to site map</li>
  <li>Key 4: Go to search page</li>
  <?php if ($user->uid > 0) : ?>
    <li>Key 5: Logout</li>
    <li>Key 6: Go to Create Content page</li>
    <li>Key 7: Go View Content List page</li>
    <li>Key 8: Go to main Control Panel page</li>
  <?php else: ?>
    <li>Key 5: Login</li>
  <?php endif; ?>
  </ul>
  Activation of these keys varies from browser to browser: in Firefox, hold alt and shift and the access key all together. 
  </div>

  <?php stopSkin("page");?>
  </div>
  
  <?php print $closure ?>
  </body>
</html>
