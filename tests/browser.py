"""Behavioral browser checks. Dev-only: pip install playwright; installed Edge used.
PHP_BINARY must point to PHP. Output is local, not a physical validation report.
"""
from pathlib import Path
import os,subprocess,socket,time,urllib.request,json,re,zipfile,hashlib
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
out=root/'output/playwright';out.mkdir(parents=True,exist_ok=True)
php=os.environ['PHP_BINARY'];checks=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
class Structure(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.stack=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(tag)
    def handle_endtag(self,tag):
        assert self.stack and self.stack[-1]==tag,(tag,self.stack[-6:])
        self.stack.pop()
for file in (root/'content/manual').glob('*.html'):
    parser=Structure();parser.feed(file.read_text(encoding='utf8'));check(not parser.stack,'Balanced chapter '+file.stem)
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
log=open(out/'server.log','w');server=subprocess.Popen([php,'-S',f'127.0.0.1:{port}','-t',str(root/'public')],stdout=log,stderr=log)
base=f'http://127.0.0.1:{port}/'
try:
    for _ in range(40):
        try:urllib.request.urlopen(base);break
        except OSError:time.sleep(.1)
    with sync_playwright() as p:
        browser=p.chromium.launch(channel=os.environ.get('BROWSER_CHANNEL','msedge') or None)
        context=browser.new_context();page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        for width in [360,620,749,1280,320]:
            page.set_viewport_size({'width':width,'height':900})
            for route in ['', '?page=guide&step=serial-4','?page=tools','?page=manual']:
                page.goto(base+route)
                for size in ['normal','large']:
                    page.select_option('#text-size',size)
                    check(page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),f'No overflow {width}/{size}/{route}')
            if width in [360,1280]:
                page.goto(base);page.screenshot(path=str(out/f'home-{width}.png'),full_page=True)
        page.set_viewport_size({'width':1280,'height':900});page.goto(base+'?page=guide&step=serial-4')
        check('Send PING' in page.locator('h1').inner_text(),'Guided USB task')
        page.check('#remember-step');page.get_by_role('link',name='Next →',exact=True).click();next_url=page.url
        page.go_back();check('serial-4' in page.url,'Guide back');page.go_forward();check(page.url==next_url,'Guide forward');page.reload();check(page.locator('#remember-step').is_checked(),'Opt-in resume reload')
        page.click('#reset-local');check(page.evaluate("localStorage.getItem('navion-v3-step')===null"),'Shared lab reset')
        page.goto(base+'?page=guide&mode=remote');check('Read & calibrate' not in page.content(),'Remote guide skips sensor calibration')
        for query in ['GPIO39','no port','only moves briefly','line stops']:
            page.goto(base+'?page=search&q='+urllib.parse.quote(query));check(page.locator('article h2 a').count()>0,'Useful search '+query)
        page.goto(base+'?page=tools');page.select_option('#power-state','upload');check(page.locator('[data-power]:visible').count()==1,'Power selection')
        page.select_option('#wire-mode','line');check(not page.locator('[data-wire="FRONT_IR"]').is_visible(),'Line hides front sensor');page.click('[data-wire="RIGHT_IR"]');check('GPIO39' in page.locator('#wire-to').inner_text(),'Connection endpoints')
        for sensor in ['left','right']:
            page.select_option(f'[name={sensor}_detected]','LOW');page.select_option(f'[name={sensor}_clear]','HIGH')
        page.get_by_role('button',name='Interpret readings').click();check('DETECTED_LEVEL=LOW' in page.locator('#calibration-result').inner_text(),'Calibration measured LOW')
        page.select_option('[name=right_detected]','HIGH');page.select_option('[name=right_clear]','LOW');page.get_by_role('button',name='Interpret readings').click();check('Mixed polarity' in page.locator('#calibration-result').inner_text(),'Mixed polarity rejected')
        page.select_option('[name=right_detected]','unstable');page.get_by_role('button',name='Interpret readings').click();check('not valid' in page.locator('#calibration-result').inner_text(),'Unstable input rejected')
        page.get_by_role('button',name='USB / upload',exact=True).click();page.get_by_role('button',name='No',exact=True).click();check('data cable' in page.locator('#trouble-question').inner_text(),'Troubleshooting no port path');page.click('#trouble-back');check('COM port' in page.locator('#trouble-question').inner_text(),'Troubleshooting back')
        page.locator('#serial-form button[type=submit], #serial-form button:not([type])').click();check(page.locator('#serial-output').inner_text()=='PONG','Serial PING')
        page.select_option('#sim-ending','none');page.locator('#serial-form button:not([type])').click();page.wait_for_timeout(250);check(page.locator('#serial-output').inner_text()=='PONG','Diagnostic timeout without newline')
        page.select_option('#sim-baud','9600');page.locator('#serial-form button:not([type])').click();check('115200' in page.locator('#serial-output').inner_text(),'Wrong baud teaching feedback');page.select_option('#sim-baud','115200');page.select_option('#sim-sketch','remote');page.locator('#serial-form button:not([type])').click();page.wait_for_timeout(850);check('Timeout stop' in page.locator('#serial-output').inner_text(),'800 ms deadman simulation')
        for mode in ['line','obstacle']:
            page.select_option('#decision-mode',mode)
            for bits in range(4 if mode=='line' else 8):
                sensors=['left','right'] if mode=='line' else ['left','front','right']
                for i,s in enumerate(sensors):page.locator('#detect-'+s).set_checked(bool(bits&(1<<i)))
                page.click('#decision-reset');page.click('#decision-step')
                value=page.locator('#decision-output').inner_text()
                if mode=='line':expected=['bounded forward','Steer left','Steer right','Both black'][bits]
                else:expected='forward' if not bits&2 else ('reverse' if bits==7 else 'turn')
                check(expected in value,f'Decision {mode} {bits}')
        page.select_option('#decision-mode','line');page.uncheck('#detect-left');page.uncheck('#detect-right');page.click('#decision-reset');page.locator('#decision-step').evaluate('(button)=>{for(let i=0;i<46;i++)button.click()}');check('stop' in page.locator('#decision-output').inner_text().lower(),'Timed line search stops');page.check('#detect-left');page.click('#decision-step');check('Latched' in page.locator('#decision-output').inner_text(),'Line stop stays latched')
        page.goto(base+'?page=lesson&slug=serial');page.locator('.source-code summary').click();page.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('denied'))},configurable:true})");page.locator('[data-copy]').click();check('Code selected' in page.locator('#announcement').inner_text(),'Clipboard failure fallback');check('#include' in page.evaluate('getSelection().toString()'),'Fallback selects actual source')
        page.keyboard.press('Tab');check(page.evaluate('document.activeElement!==document.body'),'Keyboard focus')
        page.goto(base+'?page=manual');check(page.locator('h1').count()==1,'Full manual single H1')
        page.pdf(path=str(out/'manual-r3-instructions.pdf'),format='A4',print_background=True)
        page.check('#print-code');page.pdf(path=str(out/'manual-r3-with-code.pdf'),format='A4',print_background=True)
        page.goto((root/'content/downloads/offline-manual.html').as_uri());check(page.locator('h1').count()==1,'Offline opens without server');check(page.locator('a[href^="?"]').count()==0,'Offline has no PHP links');page.pdf(path=str(out/'offline-r3.pdf'),format='A4',print_background=True)
        nojs=browser.new_context(java_script_enabled=False,viewport={'width':360,'height':800});np=nojs.new_page();np.goto(base);check(np.locator('#chapter-nav').is_visible(),'No-JS mobile navigation');np.goto(base+'?page=guide&step=serial-4');np.get_by_role('link',name='Next →',exact=True).click();check('wiring' in np.url,'No-JS guided next');nojs.close()
        check(not errors,'No browser script errors: '+str(errors));browser.close()
    (out/'results.json').write_text(json.dumps(checks,indent=2),encoding='utf8');print('PASS',len(checks),'browser/structure checks')
finally:server.terminate();server.wait();log.close()
