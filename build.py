import os,re,shutil,hashlib,html
from pathlib import Path
import yaml,markdown
ROOT=Path(__file__).parent; OUT=ROOT/'_site'; BASE=os.getenv('SITE_BASE_PATH','/off-we-roam').rstrip('/')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
def esc(s): return html.escape(str(s),quote=True)
def url(s): return BASE+s
def load(p):
 t=p.read_text(); _,front,body=t.split('---',2); return yaml.safe_load(front),body
posts=[]
for p in (ROOT/'content/posts').glob('*.md'):
 d,b=load(p)
 if d.get('published'): d.update(slug=p.stem,body=b,minutes=max(1,round(len(b.split())/220)));posts.append(d)
posts.sort(key=lambda d: {'Journal':0,'Guide':1,'Itinerary':2}.get(d['category'],3))
def country_slug(country):return re.sub(r'[^a-z0-9]+','-',country.lower()).strip('-')
countries=sorted({p['country'].strip() for p in posts if p.get('country','').strip()})
def country_url(country):return '/destinations/'+country_slug(country)+'/'

assets={}
for f in ['style.css','site.js','favicon.svg']:
 data=(ROOT/f).read_bytes(); name=f'{Path(f).stem}.{hashlib.sha256(data).hexdigest()[:8]}{Path(f).suffix}';(OUT/name).write_bytes(data);assets[f]=url('/'+name)
shutil.copytree(ROOT/'media',OUT/'media')
def rich(body):
 s=markdown.markdown(body,extensions=['tables','extra'])
 return re.sub(r'(href|src)="(/[^\"]*)"',lambda m:f'{m[1]}="{esc(url(m[2]))}"',s)
def card(p,large=False):
 return f'''<article class="card {'large' if large else ''}"><a class="photo" href="{url('/stories/'+p['slug']+'/')}"><img loading="lazy" src="{url(p['cover'])}" alt="{esc(p['title'])}" style="object-position:{esc(p.get('cover_position','50% 50%'))}"></a><div class="eyebrow">{p['category']} <span>— {p['minutes']} min read</span></div><h3><a href="{url('/stories/'+p['slug']+'/')}">{esc(p['title'])}</a></h3><p>{esc(p['summary'])}</p><a class="textlink" href="{url('/stories/'+p['slug']+'/')}">Come along <span>↗</span></a></article>'''
def page(path,title,body,desc='Stories, photographs and thoughtful travel guides from an Australian family of three.'):
 nav=f'<a href="{url("/journal/")}">Journal</a>'
 for label,menu_path,category in [('Destinations','/destinations/',None),('Guides','/guides/','Guide'),('Itineraries','/itineraries/','Itinerary')]:
  items=f'<a class="all-link" href="{url(menu_path)}">All {label.lower()} ↗</a>'
  for country in countries:
   chosen=[p for p in posts if p.get('country','').strip()==country and (category is None or p['category']==category)]
   if not chosen:continue
   if category is None:items+=f'<a href="{url(country_url(country))}">{esc(country)}</a>'
   else:
    items+=f'<span class="dropdown-country">{esc(country)}</span>'
    items+=''.join(f'<a href="{url("/stories/"+p["slug"]+"/")}">{esc(p["title"])}</a>' for p in chosen)
  nav+=f'<details class="nav-drop"><summary>{label}<span aria-hidden="true">⌄</span></summary><div class="dropdown">{items}</div></details>'
 nav+=f'<a href="{url("/about/")}">Our story</a>'
 footnav=''.join(f'<a href="{url(path)}">{label}</a>' for path,label in [('/journal/','Journal'),('/destinations/','Destinations'),('/guides/','Guides'),('/itineraries/','Itineraries'),('/about/','Our story')])
 doc=f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#f7f4ec"><title>{esc(title)} · Off We Roam</title><link rel="icon" href="{assets['favicon.svg']}"><link rel="stylesheet" href="{assets['style.css']}"><script defer src="{assets['site.js']}"></script></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="{url('/')}"><span class="sun">◒</span> off we roam<span class="brandnote">A FAMILY TRAVEL JOURNAL</span></a><button class="menu" aria-expanded="false" aria-controls="navigation">Menu <span>＋</span></button><nav id="navigation" aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main><footer><a class="brand" href="{url('/')}">off we roam</a><p>Three of us. A world to discover.<br>Stories and photographs from our family to yours.</p><div>{footnav}</div><small>© 2026 Off We Roam · Photographs by our family.</small></footer></body></html>'''
 dest=OUT/path/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(doc)
h=yaml.safe_load((ROOT/'content/homepage.yml').read_text())
page(Path(''),'Home',f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">AUSTRALIAN ROOTS. OPEN ROADS.</p><h1>{esc(h['headline'])}</h1><p class="intro">{esc(h['intro'])}</p><div class="actions"><a class="button" href="{url('/stories/lakes-and-little-moments/')}">Read our latest story ↗</a><a class="textlink" href="{url('/guides/')}">Plan a little adventure</a></div><p class="handnote">Less rushing. More remembering.</p></div><figure class="hero-photo"><img fetchpriority="high" src="{url(h['hero_image'])}" alt="Blue Moraine Lake beneath the snow-dusted Canadian Rockies" style="object-position:{esc(h['hero_position'])}"><figcaption>{esc(h['hero_note'])} <span>FROM OUR TRAVELS</span></figcaption></figure></section><section class="intro-band"><p class="eyebrow">HELLO, WE’RE OFF WE ROAM</p><h2>Two grown-ups.<br>One little explorer.</h2><p>We left our corporate jobs in Australia to see more of the world, together. This is our little corner of it: the places that stay with us, the moments in between, and the things we learn along the way.</p><a class="textlink" href="{url('/about/')}">A little about us ↗</a></section><section class="wrap stories"><div class="section-title"><div><p class="eyebrow">NOTES FROM THE ROAD</p><h2>Somewhere worth sharing.</h2></div><p>A story to settle into.<br>A guide to get you going.</p></div><div class="cards">{''.join(card(p,i==0) for i,p in enumerate(posts))}</div></section><section class="destination wrap"><img loading="lazy" src="{url('/media/mountain-autumn.jpg')}" alt="Golden autumn plants above the Lake Louise valley"><div><p class="eyebrow">LATEST DESTINATION STORY · CANADA</p><h2>Big mountains.<br>Little moments.</h2><p>Turquoise lakes, crisp mountain air and a view that makes you put your phone down. Start exploring our Canadian Rockies journal, guide and relaxed two-day route.</p><a class="button" href="{url('/destinations/canada/')}">Explore Canada ↗</a></div></section><section class="closing wrap"><span>✳</span><p>We’re collecting moments,<br>not just places.</p><small>Thanks for wandering with us.</small></section>''')
for category,slug,title in [('Journal','journal','Stories from the road'),('Guide','guides','A little help along the way'),('Itinerary','itineraries','Good days, gently planned')]:
 page(Path(slug),title,f'<section class="wrap listing"><p class="eyebrow">{category.upper()}</p><h1>{title}.</h1><p class="intro">From our family’s travels, for your next adventure.</p><div class="cards listing-cards">'+''.join(card(p) for p in posts if p['category']==category)+'</div></section>')
destination_cards=''
for country in countries:
 chosen=[p for p in posts if p.get('country','').strip()==country]
 first=chosen[0]
 destination_cards+=f'<article class="card"><a class="photo" href="{url(country_url(country))}"><img loading="lazy" src="{url(first["cover"])}" alt="{esc(country)}"></a><h3><a href="{url(country_url(country))}">{esc(country)}</a></h3><p>{len(chosen)} published pieces from our travels.</p></article>'
 page(Path('destinations')/country_slug(country),country,f'<section class="wrap listing"><p class="eyebrow">OUR TRAVELS</p><h1>{esc(country)}.</h1><p class="intro">Our stories and practical notes from {esc(country)}.</p><div class="cards">'+''.join(card(p) for p in chosen)+'</div></section>')
page(Path('destinations'),'Destinations',f'<section class="wrap listing"><p class="eyebrow">OFF WE ROAM · AROUND THE WORLD</p><h1>Places we’ve been.</h1><p class="intro">We’re an Australian family travelling the world. Our first published chapter is Canada; this is where each country’s stories will find a home as we share them.</p><div class="cards">{destination_cards}</div></section>')
a,b=load(ROOT/'content/about.md');page(Path('about'),a['title'],f'<section class="wrap about"><p class="eyebrow">OUR STORY</p><h1>{esc(a["title"])}</h1><div class="about-grid"><img src="{url("/media/moraine-shore.jpg")}" alt="The mountains reflected in Moraine Lake"><div class="prose">{rich(b)}</div></div></section>')
for p in posts:
 related=''.join(card(q) for q in posts if q!=p)
 page(Path('stories')/p['slug'],p['title'],f'''<article><div class="article-heading wrap"><a class="eyebrow" href="{url(country_url(p['country']) if p.get('country') else '/destinations/')}">{esc(p.get("country", ""))} · {esc(p.get("region", ""))}</a><h1>{esc(p['title'])}</h1><p class="intro">{esc(p['summary'])}</p><p class="article-meta">{p['category']} · {p['minutes']} min read · Off We Roam</p></div><figure class="article-cover wrap"><img src="{url(p['cover'])}" alt="{esc(p['title'])}" style="object-position:{esc(p.get('cover_position','50% 50%'))}"></figure><div class="prose article-body">{rich(p['body'])}</div></article><section class="wrap stories"><p class="eyebrow">KEEP WANDERING</p><h2>A little more from this trip.</h2><div class="cards related">{related}</div></section>''',p['summary'])
(OUT/'.nojekyll').write_text('')
print(f'Built {len(posts)} stories with base path {BASE!r}')
