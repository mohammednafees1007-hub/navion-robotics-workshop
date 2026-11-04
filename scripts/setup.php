<?php
declare(strict_types=1);
if(PHP_SAPI!=='cli') {http_response_code(403);exit('CLI only');}
$root=dirname(__DIR__);$path=getenv('NAVION_DB_PATH')?:$root.'/storage/workshop.sqlite';
if(!is_dir(dirname($path)))mkdir(dirname($path),0700,true);
$db=new PDO('sqlite:'.$path,null,null,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION]);
$db->exec("PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE NOT NULL,display_name TEXT NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN ('admin','student')),enabled INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS progress(user_id INTEGER REFERENCES users(id),lesson TEXT,completed_at TEXT,PRIMARY KEY(user_id,lesson));
CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY,user_id INTEGER REFERENCES users(id),quiz TEXT,score INTEGER,created_at TEXT);
CREATE TABLE IF NOT EXISTS certificates(user_id INTEGER PRIMARY KEY REFERENCES users(id),completion_id TEXT UNIQUE,completed_at TEXT);
CREATE TABLE IF NOT EXISTS login_attempts(bucket TEXT PRIMARY KEY,failures INTEGER,last_at INTEGER);
CREATE TABLE IF NOT EXISTS access(lesson TEXT PRIMARY KEY,enabled INTEGER);
CREATE TABLE IF NOT EXISTS settings(name TEXT PRIMARY KEY,value TEXT);");
if($db->query("SELECT COUNT(*) FROM users WHERE role='admin'")->fetchColumn())exit("Database ready. Admin already exists.
");
$login=readline('Admin username: ');$name=readline('Admin display name: ');
if(!preg_match('/^[a-zA-Z0-9_.-]{3,60}$/',$login)||trim($name)==='')exit("Invalid username/name
");
$pw=getenv('NAVION_SETUP_PASSWORD');
if(!$pw){$pw=bin2hex(random_bytes(12));echo "Generated admin password (save privately): $pw
";}
if(strlen($pw)<12)exit("Password must be at least 12 characters.
");
$s=$db->prepare('INSERT INTO users(username,display_name,password,role) VALUES(?,?,?,?)');$s->execute([$login,$name,password_hash($pw,PASSWORD_DEFAULT),'admin']);
echo "Setup complete. Create students in Admin. No public default credentials.
";
if(in_array('--demo',$argv,true)){
 if(getenv('NAVION_LOCAL_DEMO')!=='1')exit("Demo requires NAVION_LOCAL_DEMO=1 and is for localhost only.
");
 $p=bin2hex(random_bytes(10));$s->execute(['demo_student','Local Demo',password_hash($p,PASSWORD_DEFAULT),'student']);echo "Local demo_student password: $p
";
}
