import json, pathlib, urllib.request
from PIL import Image,ImageDraw
ROOT=pathlib.Path(__file__).resolve().parent; BASE='http://127.0.0.1:8791'
def get(path):
 with urllib.request.urlopen(BASE+path) as r:return json.load(r)
roster=get('/api/roster')['pokemon']; catalog=get('/api/effect-catalog')
(ROOT/'icons').mkdir(exist_ok=True)
for mon in roster:
 target=ROOT/'icons'/f"{mon['id']:03d}.png"
 try:
  with urllib.request.urlopen(BASE+mon['icon']) as r: target.write_bytes(r.read())
  im=Image.open(target).convert('RGBA');im.thumbnail((160,160),Image.Resampling.LANCZOS);im.save(target,optimize=True)
 except Exception:
  im=Image.new('RGBA',(160,160),(20,40,64,255));d=ImageDraw.Draw(im);d.ellipse((35,35,125,125),outline='white',width=8);d.line((0,80,160,80),fill='white',width=8);im.save(target)
payload={'pokemon':roster,'moves':catalog['moves'],'abilities':catalog['abilities'],'items':catalog['items']}
(ROOT/'data.js').write_text('window.CHAMPIONS_DATA='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
for n,size in [('icon-192.png',192),('icon-512.png',512)]:
 im=Image.new('RGB',(size,size),'#102b50');d=ImageDraw.Draw(im);d.ellipse((size*.16,size*.16,size*.84,size*.84),outline='white',width=max(8,size//30));d.line((0,size//2,size,size//2),fill='white',width=max(8,size//30));im.save(ROOT/n)
files=['./','index.html','app.css','app.js','data.js','manifest.webmanifest','icon-192.png','icon-512.png']+[f'icons/{m["id"]:03d}.png' for m in roster]
(ROOT/'precache.json').write_text(json.dumps(files,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'pokemon':len(roster),'moves':len(catalog['moves']),'abilities':len(catalog['abilities']),'items':len(catalog['items']),'files':len(files)},ensure_ascii=False))
