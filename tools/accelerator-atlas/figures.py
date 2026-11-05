"""Tiny, dependency-free SVG block-diagram engine for the Accelerator Atlas detail pages.

A figure is a JSON tree of boxes laid out flexbox-style:

    {"t": "Label", "s": "sub-label", "k": "kind", "d": "row"|"col",
     "f": flex-weight, "c": [children], "id": "anchor", "dash": true,
     "g": [rows, cols], "off": n_disabled_cells, "pat": ["kindA", "kindB"],
     "cl": "cell label", "shape": "wafer", "tree": {...}}

Kinds map to the colour legend below. Everything is drawn schematically and
is *not to scale*; exact cell counts are only claimed when a figure says so.
"""
from html import escape

KINDS = {
    'tensor': ('#1d4a5c', '#55d8da', 'Matrix / tensor engine'),
    'vector': ('#1e3358', '#78aaff', 'Vector / SIMT / scalar compute'),
    'ctrl':   ('#2a2f45', '#a7b4cc', 'Control, sequencing & scheduling'),
    'sram':   ('#163d33', '#71d6ab', 'Software-managed SRAM / scratchpad'),
    'cache':  ('#272a5a', '#9aa4ff', 'Hardware-managed cache'),
    'dram':   ('#3d311c', '#f4c16a', 'Off-chip DRAM (HBM / GDDR / DDR)'),
    'io':     ('#34264f', '#be9bfa', 'Interconnect, NIC & host I/O'),
    'noc':    ('#2b2440', '#c9a6ff', 'On-chip network / switches'),
    'fixed':  ('#43232a', '#ef909a', 'Model-hardwired datapath'),
    'die':    ('#111c2e', '#4d6988', None),
    'pkg':    ('#0c1524', '#33465f', None),
    'unk':    ('#151d2b', '#5f6f86', 'Not publicly disclosed'),
}
TITLE_H = 20
PAD = 7
GAP = 6
CHAR = 0.56  # average glyph width / font-size


def _fit(text, width, size, min_size=8.5):
    """Shrink then truncate text so it fits in `width` px."""
    text = str(text)
    while size > min_size and len(text) * CHAR * size > width:
        size -= 0.5
    max_chars = max(1, int(width / (CHAR * size)))
    if len(text) > max_chars:
        text = text[:max(1, max_chars - 1)] + '…'
    return text, size


class Canvas:
    def __init__(self):
        self.out = []
        self.anchors = {}
        self.used = set()

    def rect(self, x, y, w, h, kind, dash=False, rx=6, opacity=1):
        fill, stroke, _ = KINDS.get(kind, KINDS['die'])
        self.used.add(kind)
        d = ' stroke-dasharray="5 4"' if dash or kind == 'unk' else ''
        op = f' opacity="{opacity}"' if opacity != 1 else ''
        self.out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,1):.1f}" height="{max(h,1):.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.1"{d}{op}/>')

    def text(self, x, y, s, size=12, color='#e8f0ff', anchor='middle', weight=600, width=None):
        if width is not None:
            s, size = _fit(s, width, size)
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size:.1f}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>')

    def line(self, x1, y1, x2, y2, color='#8fb3d9', width=1.4, dash=False):
        d = ' stroke-dasharray="4 3"' if dash else ''
        self.out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"{d}/>')


def _draw_grid(cv, node, x, y, w, h):
    rows, cols = node['g']
    off = node.get('off', 0)
    pat = node.get('pat')
    kind = node.get('ck', node.get('k', 'vector'))
    gap = 2 if min(w / cols, h / rows) > 9 else 1
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    shape = node.get('shape')
    total = rows * cols
    idx = 0
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + c * (cw + gap), y + r * (ch + gap)
            if shape == 'wafer':
                # keep cells whose centre lies inside the inscribed circle
                mx, my = cx + cw / 2 - (x + w / 2), cy + ch / 2 - (y + h / 2)
                if (mx / (w / 2)) ** 2 + (my / (h / 2)) ** 2 > 1.02:
                    continue
            k = pat[(r + c) % len(pat)] if pat else kind
            disabled = idx >= total - off
            cv.rect(cx, cy, cw, ch, k, rx=min(3, cw / 4), opacity=0.32 if disabled else 1)
            lab = node.get('cl')
            if pat and node.get('pl'):
                lab = node['pl'][(r + c) % len(pat)]
            if lab and cw > 22 and ch > 12:
                cv.text(cx + cw / 2, cy + ch / 2 + 3.5, lab, size=min(10.5, ch * 0.55), color=KINDS[k][1], width=cw - 3)
            idx += 1


def _draw_tree(cv, node, x, y, w, h):
    """Binary tree for distribution (down) or reduction (up) networks."""
    t = node['tree']
    leaves = t.get('leaves', 16)
    levels = max(1, (leaves - 1).bit_length()) + 1
    up = t.get('dir', 'down') == 'up'
    kind = node.get('k', 'noc')
    nodes = []
    for lvl in range(levels):
        n = 2 ** lvl
        yy = y + h * (lvl + 0.5) / levels
        if up:
            yy = y + h - (yy - y)
        nodes.append([(x + w * (i + 0.5) / n, yy) for i in range(n)])
    for lvl in range(levels - 1):
        for i, (px, py) in enumerate(nodes[lvl]):
            for j in (2 * i, 2 * i + 1):
                qx, qy = nodes[lvl + 1][j]
                cv.line(px, py, qx, qy, color=KINDS[kind][1], width=1.1)
    if t.get('aug'):
        for lvl in range(1, levels):
            row = nodes[lvl]
            for i in range(1, len(row) - 1, 2):
                (ax, ay), (bx, by) = row[i], row[i + 1]
                cv.line(ax, ay, bx, by, color='#f4c16a', width=1.6, dash=True)
    r = max(3.2, min(7, w / (2 ** levels) / 3))
    for lvl, row in enumerate(nodes):
        for (px, py) in row:
            fill, stroke, _ = KINDS[kind]
            cv.out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.1"/>')
    cv.used.add(kind)
    return nodes


def layout(cv, node, x, y, w, h):
    kind = node.get('k', 'die')
    kids = node.get('c')
    has_body = bool(kids) or 'g' in node or 'tree' in node
    title = node.get('t', '')
    sub = node.get('s', '')
    if node.get('id'):
        cv.anchors[node['id']] = (x, y, w, h)
    if node.get('bare'):
        bx, by, bw, bh = x, y, w, h
    else:
        cv.rect(x, y, w, h, kind, dash=node.get('dash', False), rx=8 if has_body else 6)
        if has_body:
            if title:
                tw = w - 2 * PAD
                cv.text(x + PAD, y + 14, title + (f'  ·  {sub}' if sub else ''), size=11.5,
                        color=KINDS[kind][1] if kind not in ('die', 'pkg') else '#c9d7e9', anchor='start', weight=650, width=tw)
            th = TITLE_H if title else PAD
            bx, by, bw, bh = x + PAD, y + th, w - 2 * PAD, h - th - PAD
        else:
            color = KINDS[kind][1]
            if sub and h >= 34:
                cv.text(x + w / 2, y + h / 2 - 2, title, size=12, color='#eef4ff', width=w - 8)
                cv.text(x + w / 2, y + h / 2 + 12, sub, size=10, color=color, weight=500, width=w - 8)
            else:
                cv.text(x + w / 2, y + h / 2 + 4, title if not sub or h < 34 else title, size=11.5, color='#eef4ff', width=w - 8)
            return
    if 'g' in node:
        _draw_grid(cv, node, bx, by, bw, bh)
        return
    if 'tree' in node:
        _draw_tree(cv, node, bx, by, bw, bh)
        return
    d = node.get('d', 'col')
    expanded = []
    for k in kids:
        expanded.extend([k] * int(k.get('n', 1)))
    total = sum(float(k.get('f', 1)) for k in expanded)
    space = (bw if d == 'row' else bh) - GAP * (len(expanded) - 1)
    pos = bx if d == 'row' else by
    for k in expanded:
        size = space * float(k.get('f', 1)) / total
        if d == 'row':
            layout(cv, k, pos, by, size, bh)
        else:
            layout(cv, k, bx, pos, bw, size)
        pos += size + GAP


def _draw_links(cv, links):
    for ln in links or []:
        a, b = cv.anchors.get(ln['a']), cv.anchors.get(ln['b'])
        if not a or not b:
            continue
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        horiz = bx >= ax + aw - 1
        if horiz:      # b right of a
            x1, x2 = ax + aw, bx
            ym = max(ay, by) + (min(ay + ah, by + bh) - max(ay, by)) / 2
            y1 = y2 = ym
        elif by >= ay + ah - 1:    # b below a
            y1, y2 = ay + ah, by
            xm = max(ax, bx) + (min(ax + aw, bx + bw) - max(ax, bx)) / 2
            x1 = x2 = xm
        else:
            continue
        cv.line(x1, y1, x2, y2, color='#f4c16a', width=3)
        if ln.get('t'):
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            label, size = _fit(ln['t'], 150, 10.5)
            tw = len(label) * CHAR * size + 10
            if horiz:  # park the pill in the empty right end of a's title row
                my = max(ay, by) + 10
                mx = x1 - tw / 2 - 4
            cv.out.append(f'<rect x="{mx - tw / 2:.1f}" y="{my - 9:.1f}" width="{tw:.1f}" height="17" rx="8" fill="#3a2c18" stroke="#f4c16a" stroke-width="1"/>')
            cv.text(mx, my + 3.6, label, size=size, color='#ffe3ae', weight=650)


def render(fig, fid):
    """Return (svg_markup, used_kinds) for a figure spec."""
    W = fig.get('w', 960)
    H = fig.get('h', 380)
    cv = Canvas()
    layout(cv, fig['root'], 1, 1, W - 2, H - 2)
    _draw_links(cv, fig.get('links'))
    title = escape(fig.get('title', 'Architecture figure'))
    body = '\n'.join(cv.out)
    svg = (f'<svg id="{fid}" class="archfig" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-labelledby="{fid}-t"><title id="{fid}-t">{title}</title>'
           f'<style>text{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif}}</style>'
           f'{body}</svg>')
    return svg, cv.used


def legend(kinds):
    items = []
    for k in KINDS:
        if k in kinds and KINDS[k][2]:
            fill, stroke, label = KINDS[k]
            dash = ';border-style:dashed' if k == 'unk' else ''
            items.append(f'<span class="lg"><i style="background:{fill};border-color:{stroke}{dash}"></i>{escape(label)}</span>')
    return ''.join(items)


def hierarchy_svg(levels, fid):
    """Memory-hierarchy ladder: one bar per level, widening towards off-chip."""
    W, rowh, gap = 960, 46, 8
    H = len(levels) * (rowh + gap) + 34
    out = []
    n = len(levels)
    for i, lv in enumerate(levels):
        kind = lv.get('k', 'sram')
        fill, stroke, _ = KINDS[kind]
        frac = 0.42 + 0.58 * (i / max(1, n - 1))
        bw = 600 * frac
        x = 20 + (600 - bw) / 2
        y = 14 + i * (rowh + gap)
        dash = ' stroke-dasharray="5 4"' if kind in ('unk',) or lv.get('dash') else ''
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{rowh}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.2"{dash}/>')
        name, size = _fit(lv['name'], bw - 16, 13)
        out.append(f'<text x="{20 + 300:.1f}" y="{y + 19}" font-size="{size}" fill="#eef4ff" text-anchor="middle" font-weight="650">{escape(name)}</text>')
        scope, s2 = _fit(lv.get('scope', ''), bw - 16, 10.5)
        out.append(f'<text x="{20 + 300:.1f}" y="{y + 35}" font-size="{s2}" fill="{stroke}" text-anchor="middle" font-weight="500">{escape(scope)}</text>')
        cap, s3 = _fit(lv.get('cap', '—'), 150, 13)
        out.append(f'<text x="650" y="{y + 28}" font-size="{s3}" fill="#eef4ff" font-weight="650">{escape(cap)}</text>')
        bwt, s4 = _fit(lv.get('bw', ''), 160, 12)
        out.append(f'<text x="800" y="{y + 28}" font-size="{s4}" fill="#9aabc3" font-weight="500">{escape(bwt)}</text>')
    out.append(f'<text x="650" y="{H - 8}" font-size="10.5" fill="#7d94b3" font-weight="600" letter-spacing=".08em">CAPACITY</text>')
    out.append(f'<text x="800" y="{H - 8}" font-size="10.5" fill="#7d94b3" font-weight="600" letter-spacing=".08em">BANDWIDTH</text>')
    out.append(f'<text x="320" y="{H - 8}" font-size="10.5" fill="#7d94b3" text-anchor="middle" font-weight="600" letter-spacing=".08em">CLOSER TO COMPUTE  ↑     ↓  FURTHER / LARGER</text>')
    used = {lv.get('k', 'sram') for lv in levels}
    svg = (f'<svg id="{fid}" class="archfig" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{fid}-t">'
           f'<title id="{fid}-t">Memory hierarchy</title><style>text{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Arial,sans-serif}}</style>'
           + ''.join(out) + '</svg>')
    return svg, used
