<?php include_once("box.inc");?>
<?php include_once("block-rename.inc");?>
<?php startBox("blockbox","block-$block->module-wrap")?>
  <div class="block block-<?php print $block->module; ?>" id="block-<?php print $block->module; ?>-<?php print $block->delta; ?>">
    <h2 class="title"><?php print blockRename($block); ?></h2>
    <div class="content"><?php print $block->content; ?></div>
  </div>
<?php stopBox("blockbox")?>
