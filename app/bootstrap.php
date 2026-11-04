<?php
declare(strict_types=1);
$root=dirname(__DIR__);
$config=require $root.'/config/app.php';
if(is_file($root.'/config/local.php')) $config=array_replace($config,require $root.'/config/local.php');
date_default_timezone_set('Asia/Kolkata');
ini_set('session.use_strict_mode','1');
session_set_cookie_params(['httponly'=>true,'secure'=>getenv('NAVION_SECURE_COOKIE')==='1'||(!empty($_SERVER['HTTPS'])&&$_SERVER['HTTPS']!=='off'),'samesite'=>'Lax','path'=>'/']);
session_start();
header('X-Content-Type-Options: nosniff');header('Referrer-Policy: same-origin');header("Content-Security-Policy: default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'");
header('Cache-Control: no-store');
function e(mixed $s):string{return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function redirect(string $s):never{header('Location: '.$s);exit;}
function fail(int $status,string $message):never{http_response_code($status);exit(e($message));}
function csrf():string{$_SESSION['csrf']??=bin2hex(random_bytes(32));return '<input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'">';}
function csrfCheck():void{if(!hash_equals($_SESSION['csrf']??'',(string)($_POST['csrf']??''))||empty($_SESSION['csrf']))fail(403,'Invalid form token. Reload the page.');}
$path=getenv('NAVION_DB_PATH')?:$root.'/storage/workshop.sqlite';
if(!is_file($path))fail(503,'Workshop not set up. Ask the host to run scripts/setup.php from the command line.');
$db=new PDO('sqlite:'.$path,null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
$db->exec('PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000');
function query(string $sql,array $args=[]):PDOStatement{global $db;$s=$db->prepare($sql);$s->execute($args);return $s;}
$user=isset($_SESSION['uid'])?query('SELECT * FROM users WHERE id=? AND enabled=1',[$_SESSION['uid']])->fetch():false;
if(!$user)unset($_SESSION['uid']);
$lessons=json_decode(file_get_contents($root.'/content/lessons.json'),true,512,JSON_THROW_ON_ERROR);
$quizzes=json_decode(file_get_contents($root.'/content/quizzes.json'),true,512,JSON_THROW_ON_ERROR);
$lessonMap=array_column($lessons,null,'slug');
$passSetting=query("SELECT value FROM settings WHERE name='pass_percent'")->fetchColumn();
if($passSetting!==false)$config['pass_percent']=(int)$passSetting;
function isAdmin():bool{global $user;return $user && $user['role']==='admin';}
function accessible(string $slug):bool{return isAdmin()||!query('SELECT 1 FROM access WHERE lesson=? AND enabled=0',[$slug])->fetchColumn();}
function eligible(int $uid):bool{global $lessons,$config;
 foreach($lessons as $l){if(query('SELECT 1 FROM access WHERE lesson=? AND enabled=0',[$l['slug']])->fetchColumn())continue;if(!query('SELECT 1 FROM progress WHERE user_id=? AND lesson=?',[$uid,$l['slug']])->fetchColumn())return false;}
 foreach(array_merge($config['required_projects'],['final']) as $q){if(!query('SELECT 1 FROM attempts WHERE user_id=? AND quiz=? AND score>=?',[$uid,$q,$config['pass_percent']])->fetchColumn())return false;}
 return true;
}
