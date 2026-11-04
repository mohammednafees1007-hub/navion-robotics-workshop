"""Integration checks against a disposable SQLite database; no credentials are printed."""
from pathlib import Path
import os, subprocess, urllib.request, urllib.parse, urllib.error, http.cookiejar, re, json, secrets, sqlite3, time
import tempfile, shutil
SITE=Path(__file__).resolve().parents[1]
ROOT=Path(tempfile.mkdtemp(prefix='navion-test-'))
(ROOT/'tmp').mkdir()
PHP=Path(os.environ.get('PHP_BINARY',shutil.which('php') or 'php'))
DB=ROOT/'tmp/portal-test.sqlite'
if DB.exists(): DB.unlink()
env=os.environ.copy();env['NAVION_DB_PATH']=str(DB);env['NAVION_SETUP_PASSWORD']=secrets.token_urlsafe(18)
args=[str(PHP)]
if os.environ.get('PHP_EXTENSION_DIR'):args+=['-d','extension_dir='+os.environ['PHP_EXTENSION_DIR'],'-d','extension=pdo_sqlite']
subprocess.run(args+[str(SITE/'scripts/setup.php')],input='qa_admin\nQA Admin\n',env=env,text=True,capture_output=True,check=True)
log=open(ROOT/'tmp/php-test.log','w')
server=subprocess.Popen(args+['-S','127.0.0.1:8000','-t',str(SITE/'public')],env=env,stdout=log,stderr=log)
time.sleep(1)
checks=[]
class Client:
 def __init__(self): self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 def request(self,path='/',data=None):
  try:
   r=self.opener.open('http://127.0.0.1:8000/'+path,urllib.parse.urlencode(data).encode() if data is not None else None)
  except urllib.error.HTTPError as ex:r=ex
  return r.status,r.read().decode('utf-8'),r.geturl()
 def form(self,path,fields):
  status,body,url=self.request(path)
  token=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
  return self.request(path,dict(fields,csrf=token))
def check(cond,name):
 assert cond,name
 checks.append(name)
admin=Client();student=Client();anon=Client()
try:
 for p in ['?page=lesson&slug=remote','?page=download&file=01_Remote_Control','?page=certificate','?page=admin']:
  st,body,url=anon.request(p);check('page=login' in url,'Anonymous protection '+p)
 st,body,url=admin.request('?page=login',{'action':'login','username':'qa_admin','password':env['NAVION_SETUP_PASSWORD']})
 check(st==403,'CSRF rejection')
 st,body,url=admin.form('?page=login',{'action':'login','username':'qa_admin','password':env['NAVION_SETUP_PASSWORD']})
 check('Hello, QA Admin' in body,'Admin login')
 pw=secrets.token_urlsafe(18)
 st,body,url=admin.form('?page=admin',{'action':'create','username':'qa_student','display_name':'QA <Learner>','password':pw})
 check('Student account created' in body,'Admin creates student')
 st,body,url=student.form('?page=login',{'action':'login','username':'qa_student','password':pw})
 check('QA &lt;Learner&gt;' in body,'Student login and escaped display name')
 check(student.request('?page=admin')[0]==403,'Student denied admin')
 check(student.request('?page=download&file=../../config/app.php')[0]==404,'Download traversal rejected')
 check('certificate' not in student.request('?page=certificate')[1].split('Keep going')[0].lower() or 'Keep going' in student.request('?page=certificate')[1],'Certificate locked before completion')
 for item in json.loads((SITE/'content/lessons.json').read_text(encoding='utf8')):
  slug=item['slug'];st,body,url=student.request('?page=lesson&slug='+slug)
  check(st==200 and '<article' in body,'Lesson '+slug)
  check('value="'+str(0)+'"' in body and 'class="check"' in body,'Lesson quiz and comprehension '+slug)
  # Every internal href/src resolves, and downloads remain authenticated.
  for link in re.findall(r'(?:href|src)="([^"]+)"',body):
   link=link.replace('&amp;','&')
   if link.startswith(('http','#')):continue
   result=student.request(link)
   check(result[0]==200,'Internal link '+link)
  st,body,url=student.form('?page=lesson&slug='+slug,{'action':'complete','lesson':slug})
  check(st==200,'Completion '+slug)
 for key in ['remote','line','obstacle','final']:
  questions=json.loads((SITE/'content/quizzes.json').read_text())[key]
  fields={'action':'quiz','quiz':key,**{f'a[{i}]':q['answer'] for i,q in enumerate(questions)}}
  st,body,url=student.form('?page=quiz&quiz='+key,fields)
  check('Score: 100%' in body and 'Answer:' in body,'Quiz grade and feedback '+key)
 st,body,url=student.request('?page=certificate');check('Certificate of Completion' in body and 'NAV-' in body,'Certificate unlock')
 completion=re.search(r'NAV-[A-F0-9]+',body).group()
 check(completion in student.request('?page=certificate')[1],'Certificate stable completion ID')
 st,body,url=admin.form('?page=admin',{'action':'access','lesson':'remote'})
 check(student.request('?page=lesson&slug=remote')[0]==404,'Disabled lesson denied')
 check(student.request('?page=download&file=01_Remote_Control')[0]==403,'Disabled lesson download denied')
 uid=sqlite3.connect(DB).execute("select id from users where username='qa_student'").fetchone()[0]
 st,body,url=admin.form('?page=admin',{'action':'toggle','id':uid})
 check('page=login' in student.request('?page=progress')[2],'Disabled account session revoked')
 st,body,url=admin.form('?page=admin',{'action':'settings','pass_percent':80})
 check('Passing score updated' in body,'Passing criteria updated')
 for name in ['01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance']:
  code=(SITE/f'arduino/{name}/{name}.ino').read_text()
  check('IN1=25, IN2=26, IN3=27, IN4=14, ENA=32, ENB=33' in code and 'LEFT_IR=34, FRONT_IR=35, RIGHT_IR=39' in code,'GPIO synchronization '+name)
 check(not list((SITE/'public').rglob('*.sqlite')),'No public database')
 print(f'PASS: {len(checks)} checks')
 (SITE/'tests/verification-results.txt').parent.mkdir(exist_ok=True)
 (SITE/'tests/verification-results.txt').write_text('PASS: '+str(len(checks))+' checks\n'+'\n'.join(checks)+'\n',encoding='utf8')
finally:
 server.terminate();server.wait();log.close()
