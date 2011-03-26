<?php include_once("skin/skin.inc");?>

<div id="block-<?php print $block->module .'-'. $block->delta; ?>" class="block block-<?php print $block->module ?>">  
  <?php startSkin("block", "block-$block->module", True, 'block-'.$block->module.'-'.$block->delta);?>
    <div class="blockinner">
      
      <?php if ($block->subject): ?>
        <?php startSkin("blocktitle", "block-$block->module");?>
          <h2 class="title"> <?php print $block->subject; ?> </h2>
        <?php stopSkin("blocktitle");?>
      <?php endif;?>
      
      <div class="content">
        <?php print $block->content; ?>
      </div>    
    </div>
  <?php stopSkin("block");?>
</div>
