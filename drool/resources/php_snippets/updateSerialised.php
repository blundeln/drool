<?php

$originals = array();
$replacements = array();

foreach ($argv as $arg) {
  if (!strstr($arg, "->")) {
    continue;
  }
  //print $arg;
  $parts = explode("->", $arg);
  //print_r($parts);
  $originals[] = $parts[0];
  $replacements[] = $parts[1];
}





// Recursively replace references to the old site in a data structure.
function doReplacement($data) {
  global $originals, $replacements;
 
  if (is_string($data)) {
    $data = str_replace($originals, $replacements, $data);
    return $data;
  } else if (is_array($data)) {
    foreach ($data as $key => $value) {
      $data[$key] = doReplacement($value);
    }
  } else if (is_object($data)) {
    foreach ($data as $attr => $value) {
      $data->$attr = doReplacement($value);
    }
    return $data;
  }

  return $data;
}


function processData($data) {

  // Handle serialized data.
  if ($d = unserialize($data)) {
    $d = doReplacement($d);
    return serialize($d);
  }

  return doReplacement($data);
}

function processTable($table) {
  print "Processing table '$table':"; 
  
  // Process each row in the table.
  $result = db_query("SELECT * from $table");
  while ($r = db_fetch_object($result)) {

    /* Process each field in the row. */
    foreach ($r as $field => $value) {
      if (is_string($value)) {
        //print_r($field.":\n");
        //print_r($value."\n");
        $newValue = processData($value);
        /* If the value has changed, update it. */
        
        // If the value was changed, update it.
        if ($newValue != $value) {
          $update = "UPDATE $table set $field='%s' WHERE $field='%s'";
          db_query($update, $newValue, $value);
          print ".";
        }
      }
    }
  }
  print "\n";
}

/* Get an array of database tables. */
function getTables() {
  $tables = array();
  $result = db_query("SHOW tables");
  while ($t = db_fetch_array($result)) {
    $t = array_values($t);
    $tables[] = $t[0];
  }
  return $tables;
}

if (!($originals and $replacements)) {
  print "You must specify replacement terms.";
  exit(1);
}

print "Replacing:\n";
print_r($originals);
print "With:\n";
print_r($replacements);

$tables = getTables();
foreach ($tables as $table) {
  processTable($table);
}

print "DONE: Serialised string replacments.\n";
?>
