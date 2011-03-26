<?php

/*
 TODO:
  Replace references to old site with new site.
  Add taxonomy terms of data.
*/

  function attach_file($node, $file) {
    print "Attaching file '$file->filename' to '$node->title'.\n";

    # TODO: Check the file is not already attached.

    # Copy the file.
    # TODO: need to get the right target path.

    if (stristr($file->filepath, "sites/") !== FALSE) {
      $file->filepath = basename($file->filepath);
      $command = "cp '/tmp/exportedfiles/".$file->filepath."' '".file_create_path()."'";
    } else {
      $command = "cp '/tmp/exportedfiles/$file->filepath' '".dirname($file->filepath)."'";
    }
    print "$command\n";
    system($command);

    $file->fid = db_next_id('{files}_fid');
    db_query("INSERT INTO {files} (fid, nid, filename, filepath, filemime, filesize) VALUES (%d, %d, '%s', '%s', '%s', %d)", $file->fid, $node->nid, $file->filename, $file->filepath, $file->filemime, $file->filesize);
    db_query("INSERT INTO {file_revisions} (fid, vid, list, description) VALUES (%d, %d, %d, '%s')", $file->fid, $node->vid, $file->list, $file->description);

  }

  # Load the exported content.
  $content_string = file_get_contents("/tmp/drupalexport.txt", "rb");
  $content = unserialize($content_string);

  $nodes = $content["nodes"];
  //$nodes = array($content["nodes"][10]);
  foreach ($nodes as $n) {
   
    print_r($n);
    continue;

    //if ($n->nid != 16) {
    //if ($n->nid != 274) {
    //  continue;
    //}
    
    print $n->title;
    
    # Do not overwrite an existing node with the same title.
    if ($node = node_load(array("title"=>$n->title))) {
      print "A node with title '$n->title' exists alread on this site.\n";
      //continue;
      node_delete($node->nid);
      $node = Null;
    }

    print_r($n);

    // Define the new node.
    $node->title = $n->title;
    $node->body = $n->body;
    $node->status = $n->status;
    $node->type = $n->type;
    $node->created = $n->created;
    $node->changed = $n->changed;
    $node->comment = $n->comment;
    $node->format = $n->format;
    $node->path = $n->path;
    $node->images -> $n->images;
    $node->uid = 1;

    // Save the new node
    node_save($node);

    // Add any attachments
    foreach ($n->files as $fid => $file) {
      attach_file($node, $file);
    }

    // Re-save the node.
    node_save($node);
    print_r(node_load(array("nid"=>$node->nid)));

    print "Node id: $node->nid";
  }

?>
