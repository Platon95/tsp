import json, os, urllib.request, urllib.parse
UA = {'User-Agent': 'tsp-site-image-search/1.0 (github.com/Platon95/tsp)'}
def get(url): return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
os.makedirs('candidates', exist_ok=True)
out = []
# образец, только для сравнения (в сайт не идёт)
for i, u in enumerate(['https://admin.askfeed.ru/storage/products/images/01JF7MAY4NYJYT08X1YN5XF7TK.jpg','https://admin.askfeed.ru/storage/products/images/01JCJB3EHK00AYF5FAXCHQVK8S.jpg']):
    try: open(f'candidates/ref{i}.jpg','wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
    except Exception as e: print('ref fail', e)
for q in ['lard', 'pork lard', 'tallow', 'beef tallow block', 'rendered animal fat', 'suet', 'animal fat', 'schmaltz', 'dripping fat', 'fat rendering']:
    p = urllib.parse.urlencode({'action':'query','format':'json','generator':'search','gsrnamespace':6,'gsrsearch':q+' filetype:bitmap','gsrlimit':8,
        'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':640})
    try: r = get('https://commons.wikimedia.org/w/api.php?'+p)
    except Exception as e: print('fail', q, e); continue
    for pg in (r.get('query',{}).get('pages',{}) or {}).values():
        ii = pg['imageinfo'][0]; md = ii.get('extmetadata',{})
        if any(x['title']==pg['title'] for x in out): continue
        name = f"{len(out):02d}.jpg"
        try: open('candidates/'+name,'wb').write(urllib.request.urlopen(urllib.request.Request(ii['thumburl'], headers=UA), timeout=30).read())
        except Exception as e: continue
        out.append(dict(file=name, q=q, title=pg['title'], page=ii.get('descriptionurl'), license=md.get('LicenseShortName',{}).get('value'), artist=md.get('Artist',{}).get('value','')[:200]))
json.dump(out, open('candidates/index.json','w'), ensure_ascii=False, indent=1)
