<?php

  #
  # Get file attachments, images
  #

  # Get nodes
  $nodes = array();
  $result = db_query('SELECT n.nid FROM {node} n');
  while ($n = db_fetch_object($result)) {
    $node = node_load(array("nid"=>$n->nid));
    $nodes[] = $node;
  }


  # Get comments
  $comments = array();
  $result = db_query('SELECT * FROM {comments}');
  while ($comment = db_fetch_object($result)) {
    $comments[] = $comment;
  }

  # Get taxonomies
  $taxonomies = array();


  # Package it all
  $content = array(
    "nodes" => $nodes,
    //"comments" => $comments,
    //"taxonomy" => $taxonomies,
  );
  
  # Store it all.
  $content_string = serialize($content);
  $file = fopen("/tmp/drupalexport.txt", "wb");
  fwrite($file, $content_string);
  fclose($file);

  # Copy the files folder.
  $filesPath = file_create_path();
  system("rm -fr '/tmp/exportedfiles'");
  system("cp -a '$filesPath' '/tmp/exportedfiles'");

?>
