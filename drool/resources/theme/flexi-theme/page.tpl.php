<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- Nick Blundell 2006 -->
<html xmlns="http://www.w3.org/1999/xhtml" lang="<?php print $language ?>" xml:lang="<?php print $language ?>">

<?php include_once("flexi.inc");?>
<?php include_once("box.inc");?>

<head>
  <title><?php print $head_title ?></title>
  <?php print $head ?>
  <?php print $styles ?>
  <script type="text/javascript"><?php /* Needed to avoid Flash of Unstyle Content in IE */ ?> </script>
  <script language="JavaScript" src="<?php print $base_path . $directory .'/javascript.js';?>"></script>
  
  <script language="JavaScript"> preloadImages("<?php print $base_path . $directory?>"); </script>

  <?php importSwitchStyles(); ?>
 
  <?php if ($ieStyle) : ?>
  <!--[if IE]>
    <style type="text/css" media="all">@import "<?php print $base_path . $directory .'/styles/ie.css'; ?>"; </style>
  <![endif]-->
  <?php endif; ?>

  <style type="text/css" media="all">@import "<?php print $base_path . $directory .'/styles/final.css';?>";</style>
</head>

<body>

<?php startBox("pagebox");?>
<div id="container">

<?php startBox("headerbox");?>
<div id="header" class="clear">
    <div class="v-spacer">&nbsp;</div>
    <div id="logo"><?php if ($logo) { ?><a href="<?php print $base_path ?>" title="<?php print t('Home') ?>"><img src="<?php print $logo ?>" alt="<?php print t('Home') ?>" /></a><?php } ?></div>
    <?php if ($site_name) { ?><div class='site-name'><a href="<?php print $base_path ?>" title="<?php print t('Home') ?>"><?php print $site_name ?></a></div><?php } ?>
    <?php if ($site_slogan) { ?><div class='site-slogan'><?php print $site_slogan ?></div><?php } ?>
  
    <?php print $search_box ?>

    <?php displaySwitchButtons(); ?>
      
    <div id="primlinks">
      <?php if (count($primary_links)) : ?>
        <ul id="primary">
          <?php foreach ($primary_links as $link): ?>
            <?php $class = ""; ?>
            <?php if ( stristr($link, 'active')  ) :  ?>
              <?php $class = 'id="current"'; ?>
            <?php endif; ?>
            <li <?php print $class?>><?php print $link?></li> 
          <?php endforeach; ?>
        </ul>
      <?php endif; ?>
    </div>

    <?php if (0 and isset($secondary_links)) { ?><div id="secondary"><?php print theme('links', $secondary_links) ?></div><?php } ?>
  <div class="spacer">&nbsp;</div>
</div>
<?php stopBox("headerbox");?>

<div><?php print $header ?></div>
<?php print $breadcrumb ?>

<?php if (!$simpleLayout) : ?>
<table border="0" cellpadding="0" cellspacing="0" id="content">
  <tr>
    <?php if ($sidebar_left) : ?>
    <td id="sidebar-left">
      <?php print $sidebar_left ?>
    </td><?php endif; ?>
    <td valign="top">
<?php endif; ?>

      <?php startBox("contentbox");?>
      <?php if ($mission) { ?><div id="mission"><?php print $mission ?></div><?php } ?>
      <div id="main" class="<?php print $node->type ?> path-<?php print drupal_get_path_alias($_GET["q"]);?>">
        <h1 class="title"><?php print $title ?></h1>
        <div class="tabs"><?php print $tabs ?></div>
        <?php print $help ?>
        <?php print $messages ?>
        <?php print $content; ?>
      </div>
      <?php stopBox("contentbox");?>

<?php if (!$simpleLayout) : ?>
    </td>
    <?php if ($sidebar_right) : ?>
    <td id="sidebar-right">
      <?php print $sidebar_right ?>
    </td><?php endif; ?>
  </tr>
</table>
<?php else : ?>    
<br/>
<?php endif; ?>    

<?php if ($simpleLayout) {print $sidebar_left;} ?>
<?php if ($simpleLayout) {print $sidebar_right;} ?>

<div id="footer">
  <p><?php print $footer_message ?> <a href="/rss.xml">[RSS]</a> <a href="/user/login">[login]</a></p>
  <p>Website designed and hosted by <a href="http://www.nickblundell.org.uk">www.nickblundell.org.uk</a></p>
</div>
<?php print $closure ?>
</div>
<?php stopBox("pagebox");?>
</body>
</html>
