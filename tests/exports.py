"""Check source equivalence, package references and reproducible exports."""
from pathlib import Path
import subprocess,os,re,html,zipfile,hashlib,json,urllib.request,socket,tempfile,shutil,time
root=Path(__file__).resolve().parents[1];php=os.environ['PHP_BINARY']
def export():subprocess.run(['python',str(root/'scripts/export_manual.py')],check=True)
export();pack=root/'content/downloads/robot-setup-pack.zip';first=pack.read_bytes();export();assert first==pack.read_bytes(),'Nonreproducible ZIP'
page=subprocess.check_output([php,str(root/'scripts/render.php'),'manual']).decode()
codes=[html.unescape(s).replace('\r\n','\n') for s in re.findall(r'<details class="source-code">.*?<pre><code>(.*?)</code></pre>',page,re.S)]
for path in (root/'arduino').glob('*/*.ino'):assert path.read_text() in codes,'Stale displayed sketch '+str(path)
for link in re.findall(r'\]\((\.\./arduino/[^)]+)\)',(root/'docs/USER_MANUAL.md').read_text(encoding='utf8')):assert (root/'docs'/link).is_file(),link
with zipfile.ZipFile(pack) as z:
    for line in z.read('SHA256SUMS.txt').decode().splitlines():
        digest,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==digest
    offline=z.read('offline-manual.html').decode();ids=set(re.findall(r'\bid="([^"]+)"',offline))
    for anchor in re.findall(r'href="#([^"]+)"',offline):assert anchor in ids,anchor
# Reproduce cPanel split-root layout in an isolated staging directory.
with tempfile.TemporaryDirectory() as temp:
    web=Path(temp)/'public_html';target=web/'workshop';shutil.copytree(root/'public',target)
    index=target/'index.php';source=index.read_text(encoding='utf8');source=source.replace("require dirname(__DIR__).'/app/bootstrap.php';","require "+repr(str(root/'app/bootstrap.php').replace('\\','/'))+';');index.write_text(source,encoding='utf8')
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    server=subprocess.Popen([php,'-S',f'127.0.0.1:{port}','-t',str(web)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    base=f'http://127.0.0.1:{port}/workshop/'
    try:
        for _ in range(40):
            try:urllib.request.urlopen(base);break
            except OSError:time.sleep(.1)
        for suffix in ['', '?page=guide&step=serial-4','?page=tools','?page=search&q=no+port','?page=download&file=bundle','assets/css/learning.css','assets/js/tools.js']:
            response=urllib.request.urlopen(base+suffix);assert response.status==200,suffix
        # Missing allowlisted artifacts return 404, not a partial/empty download.
        index.write_text(source.replace("'docs/checklists.md'","'docs/absent-file.md'"),encoding='utf8')
        try:urllib.request.urlopen(base+'?page=download&file=checklist');raise AssertionError('Missing file accepted')
        except urllib.error.HTTPError as e:assert e.code==404
        try:urllib.request.urlopen(urllib.request.Request(base,data=b'x',method='POST'));raise AssertionError('POST accepted')
        except urllib.error.HTTPError as e:assert e.code==405
    finally:server.terminate();server.wait()
print('PASS source equivalence, export links/checksums/reproducibility, split-root subfolder, missing file and read-only HTTP checks')
