<?php include_once("drool.inc");?>
<?php startSkin("block", "block-$block->module", True, 'block-'.$block->module.'-'.$block->delta);?>
<div id="block-<?php print $block->module .'-'. $block->delta; ?>" class="clear-block block block-<?php print $block->module ?>">

<?php if ($block->subject): ?>
<?php startSkin("blocktitle", "block-$block->module");?>
  <h2><?php print $block->subject ?></h2>
<?php stopSkin("blocktitle");?>
<?php endif;?>

  <div class="content"><?php print $block->content ?></div>
</div>
<?php stopSkin("block");?>
