"""Rebuild the self-contained website, CSV and per-processor detail pages from
chips.json + details/*.json. Standard library only."""
import csv
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

from figures import render, legend, hierarchy_svg

SITE = 'https://y1-w.github.io/tools/accelerator-atlas/'
COLOR = {'A1': '#78aaff', 'B1': '#67d8cb', 'B2': '#4facaa', 'C1': '#be9bfa', 'C2': '#a991fa', 'C3': '#f4bc6c', 'D1': '#ef909a'}
AXES = [('Compute organization', 'instruction-driven → spatial / hard-wired'),
        ('Explicit memory orchestration', 'hardware-managed → compiler / local state'),
        ('Programmability', 'model-fixed → broad kernel programmability')]

p = Path(__file__).resolve().parent
obj = json.loads((p / 'chips.json').read_text(encoding='utf-8'))
assert isinstance(obj['chips'], list) and obj['chips']
ids = [x['id'] for x in obj['chips']]
assert len(ids) == len(set(ids)), 'Duplicate chip IDs'
for chip in obj['chips']:
    assert chip['category'] in obj['taxonomy']
    assert all(s['url'].startswith('https://') for s in chip['sources'])
    for k in ('sram_mb', 'hbm_gb', 'hbm_tbps', 'power_w', 'die_area_mm2'):
        assert chip[k] is None or (isinstance(chip[k], (int, float)) and chip[k] >= 0)

# ---- per-processor detail records ------------------------------------------------
details = {}
for cid in ids:
    f = p / 'details' / f'{cid}.json'
    assert f.exists(), f'Missing detail record details/{cid}.json'
    d = json.loads(f.read_text(encoding='utf-8'))
    for key in ('summary', 'highlights', 'sections', 'figures', 'hierarchy'):
        assert key in d, f'{cid}: missing {key}'
    assert all(r['url'].startswith('https://') for r in d.get('refs', []))
    details[cid] = d
extra = {f.stem for f in (p / 'details').glob('*.json')} - set(ids)
assert not extra, f'Detail records without a chip: {extra}'

snapshot = date.fromisoformat(obj['snapshot_date']).strftime('%d %b %Y').lstrip('0')

# ---- main page -------------------------------------------------------------------
encoded = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
tmpl = (p / 'index.template.html').read_text(encoding='utf8')
assert tmpl.count('__JSON__') == 1
(p / 'index.html').write_text(tmpl.replace('__JSON__', encoded).replace('__SNAPSHOT__', snapshot), encoding='utf8')
cols = 'vendor,name,category,year,status,compute,memory_model,sram_mb,hbm_gb,hbm_type,hbm_tbps,power_w,power_scope,node,die_area_mm2,interconnect,scale,scheduling,workload,verification,last_verified,notes'.split(',')
with (p / 'chips.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for chip in obj['chips']:
        w.writerow({c: chip.get(c) for c in cols})


# ---- detail pages ----------------------------------------------------------------
def fmt(v, unit=''):
    if v is None or v == '':
        return '—'
    if isinstance(v, (int, float)):
        return f'{v:,.2f}'.rstrip('0').rstrip('.') + unit
    return str(v)


def e(s):
    return escape(str(s), quote=True)


def chip_page(i, c):
    d = details[c['id']]
    tax = obj['taxonomy'][c['category']]
    parts = []
    parts.append(f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/tools/">Tools</a> / <a href="../../">Accelerator Atlas</a> / '
                 f'<a href="../../#database">{e(c["category"])} · {e(tax["label"])}</a> / {e(c["name"])}</nav>')
    tiles = ''.join(f'<div class="tile"><div class="l">{e(h[0])}</div><div class="v">{e(h[1])}</div>'
                    + (f'<div class="n">{e(h[2])}</div>' if len(h) > 2 and h[2] else '') + '</div>' for h in d['highlights'])
    parts.append(f'<section class="hero" style="padding-top:14px"><div class="eyebrow">{e(c["vendor"])} · {e(c["status"])} · {e(c["year"])}</div>'
                 f'<h1>{e(c["name"])}</h1><span class="classpill"><b>{e(c["category"])}</b> {e(tax["family"])} — {e(tax["label"])}</span>'
                 f'<p class="lede">{e(d["summary"])}</p><div class="tiles">{tiles}</div></section>')
    parts.append('<nav class="toc" aria-label="On this page"><a href="#architecture">Architecture figures</a><a href="#analysis">Analysis</a>'
                 '<a href="#memory">Memory hierarchy</a><a href="#specs">Specifications</a><a href="#evidence">Evidence &amp; caveats</a></nav>')

    # figures
    figs = []
    for n, fig in enumerate(d['figures'], 1):
        fid = f'fig-{c["id"]}-{n}'
        svg, used = render(fig, fid)
        figs.append(f'<figure id="figure-{n}"><div class="figbar"><strong><span class="fignum">Figure {n}</span>{e(fig["title"])}</strong>'
                    f'<div class="figtools"><button type="button" data-zoom="{fid}" data-title="Figure {n} · {e(fig["title"])}">Expand ⤢</button>'
                    f'<button type="button" data-dl="{fid}" data-name="{e(c["id"])}-figure-{n}">SVG ↓</button></div></div>'
                    f'<div class="figscroll">{svg}</div><div class="legend">{legend(used)}</div>'
                    f'<figcaption>{e(fig.get("caption", ""))}</figcaption></figure>')
    parts.append(f'<section id="architecture"><h2><span class="num">01</span>Architecture figures</h2>{"".join(figs)}</section>')

    # analysis prose
    prose = ''.join(f'<h3>{e(s["h"])}</h3>' + ''.join(f'<p>{e(x)}</p>' for x in s.get('p', [])) for s in d['sections'])
    parts.append(f'<section id="analysis"><h2><span class="num">02</span>Architectural analysis</h2><div class="prose">{prose}</div></section>')

    # hierarchy
    hn = len(d['figures']) + 1
    hid = f'fig-{c["id"]}-mem'
    hsvg, hused = hierarchy_svg(d['hierarchy'], hid)
    parts.append(f'<section id="memory"><h2><span class="num">03</span>Memory &amp; communication hierarchy</h2>'
                 f'<figure><div class="figbar"><strong><span class="fignum">Figure {hn}</span>Memory hierarchy · {e(c["memory_model"])}</strong>'
                 f'<div class="figtools"><button type="button" data-zoom="{hid}" data-title="Figure {hn} · Memory hierarchy">Expand ⤢</button>'
                 f'<button type="button" data-dl="{hid}" data-name="{e(c["id"])}-memory-hierarchy">SVG ↓</button></div></div>'
                 f'<div class="figscroll">{hsvg}</div><div class="legend">{legend(hused)}</div>'
                 f'<figcaption>Levels ordered from closest to the datapath to furthest. Green = software-managed, indigo = hardware cache, amber = off-chip DRAM, '
                 f'violet = interconnect. "Not disclosed" means the cited sources give no value — not that the level is absent.</figcaption></figure></section>')

    # specs + scores
    rows = [('Architectural class', f'{c["category"]} · {tax["label"]}'), ('Compute', c['compute']), ('Memory semantics', c['memory_model']),
            ('On-chip SRAM / cache', fmt(c['sram_mb'], ' MB')), ('Off-chip memory', fmt(c['hbm_gb'], ' GB') + (' · ' + c['hbm_type'] if c.get('hbm_type') else '')),
            ('Off-chip bandwidth', fmt(c['hbm_tbps'], ' TB/s')), ('Power', fmt(c['power_w'], ' W') + (f' ({c["power_scope"]})' if c.get('power_scope') else '')),
            ('Process', fmt(c['node'])), ('Die / wafer area', fmt(c['die_area_mm2'], ' mm²')), ('Packaging', fmt(c.get('packaging'))),
            ('Interconnect', c['interconnect']), ('System scale', c['scale']), ('Scheduling', c['scheduling']), ('Workload', c['workload']),
            ('Lifecycle', c['status']), ('Disclosure', c['verification']), ('Record verified', c['last_verified'])]
    table = ''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in rows)
    scores = ''.join(f'<div class="score"><div class="row"><span><b>{e(a)}</b> · {e(b)}</span><span>{v:.1f} / 5</span></div>'
                     f'<div class="bar"><i style="width:{max(0, min(5, v)) / 5 * 100:.0f}%"></i></div></div>' for (a, b), v in zip(AXES, c['scores']))
    related = [x for x in obj['chips'] if x['category'] == c['category'] and x['id'] != c['id']]
    rel = ''.join(f'<a href="../{e(x["id"])}/">{e(x["name"])}</a>' for x in related) or '<span class="note">No other records in this class yet.</span>'
    parts.append(f'<section id="specs"><h2><span class="num">04</span>Specifications</h2><div class="twocol"><div class="pane"><table>{table}</table></div>'
                 f'<div><div class="pane"><div class="scores">{scores}</div></div><p class="note">Editorial, qualitative design-space coordinates — not benchmark scores.</p>'
                 f'<h3>Also in {e(c["category"])}</h3><div class="related">{rel}</div></div></div>'
                 f'<p class="note">Blank (—) means not disclosed or not comparable, not zero. Values match the atlas database; see caveats before ranking.</p></section>')

    # evidence
    cav = [c['notes']] + d.get('caveats', [])
    cav_html = ''.join(f'<li>{e(x)}</li>' for x in cav if x)
    srcs = ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])} ↗</a><span class="tag">database source</span></li>' for s in c['sources'])
    srcs += ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["title"])} ↗</a><span class="tag">figure / analysis reference</span></li>' for s in d.get('refs', []))
    parts.append(f'<section id="evidence"><h2><span class="num">05</span>Evidence &amp; caveats</h2><div class="warning"><strong>Read before comparing</strong><ul>{cav_html}</ul></div>'
                 f'<h3>References</h3><div class="pane"><ul class="sources">{srcs}</ul></div></section>')

    prev_c, next_c = obj['chips'][i - 1], obj['chips'][(i + 1) % len(obj['chips'])]
    parts.append(f'<nav class="pager" aria-label="Other processors"><a href="../{e(prev_c["id"])}/"><small>← Previous</small>{e(prev_c["name"])}</a>'
                 f'<a class="next" href="../{e(next_c["id"])}/"><small>Next →</small>{e(next_c["name"])}</a></nav>')

    shell = (p / 'chip.template.html').read_text(encoding='utf8')
    desc = d['summary'][:300]
    return (shell.replace('__TITLE__', e(c['name'])).replace('__DESC__', e(desc)).replace('__CANON__', f'{SITE}chips/{c["id"]}/')
            .replace('__ACCENT__', COLOR.get(c['category'], '#55d8da')).replace('__SNAPSHOT__', snapshot).replace('__BODY__', '\n'.join(parts)))


out = p / 'chips'
if out.exists():
    shutil.rmtree(out)
for i, c in enumerate(obj['chips']):
    (out / c['id']).mkdir(parents=True, exist_ok=True)
    (out / c['id'] / 'index.html').write_text(chip_page(i, c), encoding='utf8')
print('Built', len(obj['chips']), 'records and', len(obj['chips']), 'detail pages')
