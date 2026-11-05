<?php
// Development-only CLI renderer. Never copy scripts/ into the web root.
if(PHP_SAPI!=='cli')exit(1);
$_SERVER['REQUEST_METHOD']='GET';
$_GET=['page'=>($argv[1]??'manual')];
require dirname(__DIR__).'/public/index.php';
