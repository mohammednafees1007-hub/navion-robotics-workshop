"""Regenerate public manual downloads from chapter source; no dependencies."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,zipfile,urllib.parse,html,os,shutil,subprocess,base64,hashlib
root=Path(__file__).resolve().parents[1]
release=json.loads((root/'config/release.json').read_text(encoding='utf8'))
sketches=['00_Serial_Test','00_Sensor_Check','01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance']
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0;self.links=[];self.in_pre=False;self.header_count=0
    def handle_starttag(self,tag,attrs):
        if tag=='button':self.skip+=1
        if self.skip:return
        if tag=='pre':self.in_pre=True;self.parts.append('\n```cpp\n');return
        if tag=='code':
            if not self.in_pre:self.parts.append('`')
            return
        if tag=='tr':self.header_count=0
        if tag=='th':self.header_count+=1
        if tag=='a':
            href=dict(attrs).get('href','');suffix=''
            if href.startswith('http'):
                self.parts.append('[');suffix=']('+href+')'
            elif 'page=download' in href:
                key=urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('file',[''])[0]
                if re.fullmatch(r'0[0-3]_[A-Za-z_]+',key):
                    self.parts.append('[');suffix='](arduino/'+key+'/'+key+'.ino)'
            elif 'page=lesson' in href:
                slug=urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('slug',[''])[0]
                number=next((i for i,c in enumerate(chapters,1) if c['slug']==slug),None)
                if number:suffix=' (Chapter '+str(number)+')'
            self.links.append(suffix)
        elif tag in ['h2','h3']:self.parts.append('\n\n'+'#'*int(tag[1])+' ')
        elif tag in ['p','section','aside','tr','ul','ol','pre','div']:self.parts.append('\n')
        elif tag=='li':self.parts.append('\n- ')
        elif tag in ['td','th']:self.parts.append(' | ')
        elif tag=='br':self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag=='button':self.skip=max(0,self.skip-1)
        if tag=='pre':self.in_pre=False;self.parts.append('\n```\n');return
        if tag=='code':
            if not self.in_pre:self.parts.append('`')
            return
        if tag=='tr':
            self.parts.append(' |\n')
            if self.header_count:self.parts.append('|'+ ' --- |'*self.header_count+'\n')
        if tag=='a' and not self.skip and self.links:self.parts.append(self.links.pop())
        if not self.skip and tag in ['p','li','h2','h3','pre','tr']:self.parts.append('\n')
    def handle_data(self,text):
        if not self.skip:self.parts.append(text)
chapters=json.loads((root/'content/manual.json').read_text(encoding='utf8'))
out=[f"# Navion Robotics - Robot Setup & User Manual\n\nRevision {release['revision']} - {release['date']}\n\nPublic practical guide. No login or database. Hardware assumptions require teacher verification.\n"]
for n,c in enumerate(chapters,1):
    source=(root/f"content/manual/{c['slug']}.html").read_text(encoding='utf8')
    source=re.sub(r'\{\{SKETCH:(.*?)\}\}',lambda m:html.escape((root/f'arduino/{m[1]}/{m[1]}.ino').read_text(encoding='utf8')) if m[1] in sketches else '',source)
    parser=Text();parser.feed(source)
    out.append(f"\n# {n:02d}. {c['title']}\n\nBefore you start: {c['need']}\n\nFinish when: {c['result']}\n"+re.sub(r'\n{3,}','\n\n',''.join(parser.parts)))
# Repository and extracted ZIP have different relative roots.
bundle_manual='\n'.join(out)
manual=root/'docs/USER_MANUAL.md';manual.write_text(bundle_manual.replace('](arduino/','](../arduino/'),encoding='utf8')
php=os.environ.get('PHP_BINARY') or shutil.which('php')
if not php:raise SystemExit('Set PHP_BINARY to the PHP 8.2+ executable for offline rendering.')
def render(page):
    return subprocess.check_output([php,str(root/'scripts/render.php'),page]).decode('utf8').replace('\r\n','\n')
offline=render('manual')
offline=re.sub(r'<script[^>]*>.*?</script>','',offline,flags=re.S)
offline=re.sub(r'<link rel="stylesheet" href="([^"]+)">',lambda m:'<style>'+(root/'public'/m[1]).read_text(encoding='utf8')+'</style>',offline)
offline=re.sub(r'<aside class="sidebar">.*?</aside>','',offline,flags=re.S)
offline=re.sub(r'<div class="page-tools[^"]*">.*?</div>','',offline,flags=re.S)
offline=re.sub(r'<button[^>]*>.*?</button>','',offline,flags=re.S)
offline=offline.replace('<body>','<body><p class="note">Offline revision '+str(release['revision'])+' · '+release['date']+'. Saved snapshot; download a fresh copy for updates. Sketch links below are embedded downloads. No PHP server is required.</p><style>.layout{display:block}.main{margin:auto}nav.sidebar{display:none}</style>')
offline=re.sub(r'src="(assets/[^"]+\.svg)"',lambda m:'src="data:image/svg+xml;base64,'+base64.b64encode((root/'public'/m[1]).read_text(encoding='utf8').encode()).decode()+'"',offline)
def offline_link(m):
    link=html.unescape(m[1]);parsed=urllib.parse.urlparse(link);q=urllib.parse.parse_qs(parsed.query)
    page=q.get('page',[''])[0];slug=q.get('slug',['intro'])[0]
    if page=='lesson':return 'href="#'+(slug+'-'+parsed.fragment if parsed.fragment else 'manual-'+slug)+'"'
    if page=='download':
        key=q.get('file',[''])[0]
        if key in sketches:
            data=base64.b64encode((root/f'arduino/{key}/{key}.ino').read_text(encoding='utf8').encode()).decode()
            return 'download="'+key+'.ino" href="data:application/octet-stream;base64,'+data+'"'
    if page:return 'href="#contents"'
    return m[0]
offline=re.sub(r'href="([^"]+)"',offline_link,offline)
downloads=root/'content/downloads';downloads.mkdir(exist_ok=True)
(downloads/'offline-manual.html').write_text(offline,encoding='utf8')
tools=render('tools')
power=re.search(r'<section id="power".*?</section>',tools,re.S)[0]
wiring=re.search(r'<section id="wiring".*?</section>',tools,re.S)[0]
cards='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Navion quick cards</title><style>body{font:18px/1.6 system-ui;margin:24px;color:#183b34}table{border-collapse:collapse;width:100%}td,th{border:1px solid #aaa;padding:8px;text-align:left}.js-only{display:none}button{font:inherit;border:0;background:none;color:inherit}section{break-before:page}h1,h2{break-after:avoid}@media print{body{font-size:11pt}}@page{size:A4;margin:15mm}</style><h1>Navion workbench cards</h1><p>Revision '+str(release['revision'])+' · '+release['date']+' · Teacher hardware checks required.</p><h2>Quick start</h2><ol>'+''.join('<li>'+html.escape(c['title'])+': '+html.escape(c['need'])+'</li>' for c in chapters[:7])+'</ol><h2>Change mode / shut down</h2><ol><li>Switch motor battery OFF. Unplug USB before changing wires or mounts.</li><li>Teacher isolates external ESP32 5 V before USB upload.</li><li>Upload the selected sketch. Carry over measured motor inversion and calibrated sensor polarity.</li><li>Unplug USB before restoring approved battery-only power. Teacher checks wiring, clear space and stop behavior before a run.</li><li>Finish with battery OFF; store cells as directed by the teacher.</li></ol>'+power+wiring+'</html>'
cards=re.sub(r' href="\?page=lesson&amp;slug=([^"]+)"',r' href="offline-manual.html#manual-\1"',cards)
(downloads/'quick-cards.html').write_text(cards,encoding='utf8')
entries={'USER_MANUAL.md':bundle_manual.encode(),'offline-manual.html':offline.encode(),'quick-cards.html':cards.encode(),'checklists.md':(root/'docs/checklists.md').read_text(encoding='utf8').encode(),'release.json':(root/'config/release.json').read_text(encoding='utf8').encode()}
for p in sorted((root/'public/assets/svg').glob('*.svg')):entries[p.name]=p.read_text(encoding='utf8').encode()
for name in sketches:
    for filename in [name+'.ino','README.md']:
        entries['arduino/'+name+'/'+filename]=(root/'arduino'/name/filename).read_text(encoding='utf8').encode()
entries['manual-print.pdf']=(downloads/'manual-print.pdf').read_bytes()
entries['SHA256SUMS.txt']=''.join(hashlib.sha256(data).hexdigest()+'  '+name+'\n' for name,data in sorted(entries.items())).encode()
with zipfile.ZipFile(downloads/'robot-setup-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(entries.items()):
        info=zipfile.ZipInfo(name,date_time=(2026,11,5,0,0,0));info.create_system=3;info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data)
print('Exported synchronized Markdown, standalone offline HTML, quick cards and deterministic ZIP.')
