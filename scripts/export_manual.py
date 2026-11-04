"""Regenerate public manual downloads from chapter source; no dependencies."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,zipfile,urllib.parse
root=Path(__file__).resolve().parents[1]
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
out=['# Navion Robotics — Robot Setup & User Manual\n\nRevision 2 · 2026-11-05\n\nPublic practical guide. No login or database. Hardware assumptions require teacher verification.\n']
for n,c in enumerate(chapters,1):
    parser=Text();parser.feed((root/f"content/manual/{c['slug']}.html").read_text(encoding='utf8'))
    out.append(f"\n# {n:02d}. {c['title']}\n\nBefore you start: {c['need']}\n\nFinish when: {c['result']}\n"+re.sub(r'\n{3,}','\n\n',''.join(parser.parts)))
manual=root/'docs/USER_MANUAL.md';manual.write_text('\n'.join(out),encoding='utf8')
with zipfile.ZipFile(root/'content/downloads/robot-setup-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in [manual,root/'docs/checklists.md']+list((root/'public/assets/svg').glob('*.svg')):z.write(p,p.name)
    for name in ['00_Serial_Test','00_Sensor_Check','01_Remote_Control','02_Line_Follower','03_Obstacle_Avoidance']:
        for filename in [name+'.ino','README.md']:
            p=root/'arduino'/name/filename;z.write(p,'arduino/'+name+'/'+filename)
print('Exported full text manual and setup ZIP from',len(chapters),'chapters.')
