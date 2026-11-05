"""Public manual integration checks; no database/extensions/credentials required."""
from pathlib import Path
import os,subprocess,urllib.request,urllib.error,urllib.parse,re,json,zipfile,io,socket,tempfile,shutil,time
root=Path(__file__).resolve().parents[1]
php=os.environ.get('PHP_BINARY') or shutil.which('php') or 'php'
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
base=f'http://127.0.0.1:{port}/'
log=tempfile.TemporaryFile()
env=os.environ.copy();env['NAVION_DB_PATH']='this-database-does-not-exist.sqlite'
server=subprocess.Popen([php,'-S',f'127.0.0.1:{port}','-t',str(root/'public')],stdout=log,stderr=log,env=env)
checks=[];visited={}
def check(ok,label):
    assert ok,label
    checks.append(label)
def get(url):
    if url in visited:return visited[url]
    try:r=urllib.request.urlopen(url)
    except urllib.error.HTTPError as ex:r=ex
    value=(r.status,r.read(),r.geturl(),r.headers);visited[url]=value;return value
try:
    for _ in range(30):
        try:result=get(base);break
        except urllib.error.URLError:time.sleep(.1)
    else:raise RuntimeError('PHP did not start')
    check(result[0]==200 and b'FINISH WHEN' in result[1],'Home opens without database or login')
    check('Set-Cookie' not in result[3],'Public pages create no session cookie')
    chapters=json.loads((root/'content/manual.json').read_text(encoding='utf8'))
    check(len(chapters)==14,'14 practical chapters')
    pages=[base]+[base+'?page='+p for p in ['downloads','manual','guide','tools','search']]+[base+'?page=lesson&slug='+c['slug'] for c in chapters]
    for url in pages:
        status,data,final,headers=get(url);body=data.decode()
        check(status==200,'Public route '+url.removeprefix(base))
        check('name="password"' not in body and 'Sign out' not in body and 'Submit quiz' not in body,'No account/course controls '+url.removeprefix(base))
        check('PHP Warning' not in body and 'Fatal error' not in body,'No PHP runtime errors '+url.removeprefix(base))
        ids=re.findall(r'\bid="([^"]+)"',body)
        check(len(ids)==len(set(ids)),'Unique page anchors '+url.removeprefix(base))
        for link in re.findall(r'(?:href|src)="([^"]+)"',body):
            link=link.replace('&amp;','&');target=urllib.parse.urljoin(url,link)
            parsed=urllib.parse.urlparse(target)
            if parsed.netloc!=urllib.parse.urlparse(base).netloc:continue
            clean=urllib.parse.urldefrag(target)[0]
            st,content,_,_=get(clean)
            check(st==200,'Internal link '+link)
            if parsed.fragment:check(f'id="{parsed.fragment}"' in content.decode(),'Anchor target '+link)
    for old in ['login','admin','dashboard','progress','quiz','certificate']:
        st,data,url,_=get(base+'?page='+old);check(st==200 and '?page=home' in url,'Removed route redirects '+old)
    for slug in ['basics','cpp','calibration','challenges','faq']:
        check(get(base+'?page=lesson&slug='+slug)[0]==200,'Legacy lesson link '+slug)
    for path in ['?page=download&file=../../config/app.php','?page=download&file=unknown','?page=lesson&slug=../../config/app','?page=unknown']:
        check(get(base+path)[0]==404,'Invalid route rejected '+path)
    for name in ['00_Serial_Test','00_Sensor_Check','01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance']:
        _,data,_,h=get(base+'?page=download&file='+name)
        check(data==(root/f'arduino/{name}/{name}.ino').read_bytes(),'Sketch download byte match '+name)
        check('attachment;' in h.get('Content-Disposition',''),'Download attachment '+name)
    _,bundle,_,_=get(base+'?page=download&file=bundle')
    with zipfile.ZipFile(io.BytesIO(bundle)) as z:
        check(z.testzip() is None,'ZIP integrity')
        check({'offline-manual.html','quick-cards.html','SHA256SUMS.txt','release.json'}.issubset(z.namelist()),'ZIP includes offline manual, cards and release metadata')
        check(z.read('USER_MANUAL.md').decode().replace('](arduino/','](../arduino/')==(root/'docs/USER_MANUAL.md').read_text(encoding='utf8'),'ZIP manual synchronized with correct relative links')
        for link in re.findall(r'\]\((arduino/[^)]+)\)',z.read('USER_MANUAL.md').decode()):check(link in z.namelist(),'ZIP sketch reference '+link)
        check(not any(n.endswith(('.sqlite','.env')) or '.git/' in n for n in z.namelist()),'ZIP has no runtime data')
    for name in ['01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance']:
        source=(root/f'arduino/{name}/{name}.ino').read_text()
        check('IN1=25, IN2=26, IN3=27, IN4=14, ENA=32, ENB=33' in source,'Motor GPIO map '+name)
        check('LEFT_IR=34, FRONT_IR=35, RIGHT_IR=39' in source,'Sensor GPIO map '+name)
    check('session_start' not in (root/'app/bootstrap.php').read_text(),'No session dependency')
    check('PDO' not in (root/'app/bootstrap.php').read_text(),'No database dependency')
    for filename in root.rglob('*.php'):
        lint=subprocess.run([php,'-l',str(filename)],capture_output=True,text=True)
        check(lint.returncode==0,'PHP syntax '+str(filename.relative_to(root)))
    (root/'tests/manual-results.txt').write_text('PASS: '+str(len(checks))+' checks\n'+'\n'.join(checks)+'\n',encoding='utf8')
    print('PASS:',len(checks),'checks')
finally:
    server.terminate();server.wait();log.close()
