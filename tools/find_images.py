import json, os, urllib.request, urllib.parse
UA = {'User-Agent': 'tsp-site-image-search/1.0 (github.com/Platon95/tsp)'}
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
os.makedirs('candidates', exist_ok=True)
out = []
for q in ['meat and bone meal', 'bone meal powder', 'fish meal', 'feather meal', 'animal fat tallow', 'lard', 'rendered fat', 'beef tallow', 'rendering plant']:
    p = urllib.parse.urlencode({'action':'query','format':'json','generator':'search','gsrnamespace':6,'gsrsearch':q+' filetype:bitmap','gsrlimit':6,
        'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':640})
    try: r = get('https://commons.wikimedia.org/w/api.php?'+p)
    except Exception as e: print('fail', q, e); continue
    for pg in (r.get('query',{}).get('pages',{}) or {}).values():
        ii = pg['imageinfo'][0]; md = ii.get('extmetadata',{})
        name = f"{len(out):02d}.jpg"
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii['thumburl'], headers=UA), timeout=30).read()
            open('candidates/'+name,'wb').write(data)
        except Exception as e: print('dl fail', e); continue
        out.append(dict(file=name, q=q, title=pg['title'], page=ii.get('descriptionurl'), orig=ii['url'], w=ii['width'], h=ii['height'],
            license=md.get('LicenseShortName',{}).get('value'), artist=md.get('Artist',{}).get('value','')[:200]))
geo = None
try:
    geo = get('https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':'Дмитровское шоссе 163А к2, Москва','format':'json','limit':3}))
except Exception as e: geo = str(e)
json.dump({'images':out,'geo':geo}, open('candidates/index.json','w'), ensure_ascii=False, indent=1)
