<?php
declare(strict_types=1);
$root=dirname(__DIR__);
$config=require $root.'/config/app.php';
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: same-origin');
header("Content-Security-Policy: default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'");
function e(mixed $value):string {return htmlspecialchars((string)$value,ENT_QUOTES,'UTF-8');}
function fail(int $status,string $text):never {http_response_code($status);exit(e($text));}
function go(string $url):never {header('Location: '.$url,true,302);exit;}
$chapters=json_decode(file_get_contents($root.'/content/manual.json'),true,512,JSON_THROW_ON_ERROR);
$chapterMap=array_column($chapters,null,'slug');
function bodyFor(string $slug):string {
 global $root;
 $body=file_get_contents($root.'/content/manual/'.$slug.'.html');
 $body=preg_replace_callback('~\{\{SKETCH:(0[0-3]_[A-Za-z_]+)\}\}~',function($m)use($root){
  $allowed=['00_Serial_Test','00_Sensor_Check','01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance'];
  return in_array($m[1],$allowed,true)?e(file_get_contents($root.'/arduino/'.$m[1].'/'.$m[1].'.ino')):'';
 },$body);
 $seen=[];
 return preg_replace_callback('~<h([23])>(.*?)</h\1>~s',function($m)use(&$seen){
  $base=strtolower(trim(preg_replace('/[^a-zA-Z0-9]+/','-',strip_tags($m[2])),'-'));
  $seen[$base]=($seen[$base]??0)+1;$id=$base.($seen[$base]>1?'-'.$seen[$base]:'');
  return '<h'.$m[1].' id="'.$id.'">'.$m[2].'</h'.$m[1].'>';
 },$body);
}

$release=json_decode(file_get_contents($root.'/config/release.json'),true);
require __DIR__.'/learning.php';
