"""Original vector fixtures. Fictional titles; never used by the installed theme."""
from pathlib import Path
from html import escape

out = Path(__file__).parent / 'assets'
out.mkdir(exist_ok=True)
specs = [
    ('dune', 'DUNE RUNNER', '#26251d', '#dbaf69', '#8b5b36'),
    ('orbital', 'ORBITAL', '#162431', '#a9c7cf', '#386477'),
    ('garden', 'THE LAST GARDEN', '#19302a', '#b5cba4', '#4d785b'),
    ('circuit', 'NEON CIRCUIT', '#2a1c29', '#dcb386', '#825575'),
    ('current', 'DEEP CURRENT', '#132e39', '#95c6c4', '#296276'),
    ('ember', 'EMBER TRAIL', '#33231e', '#e5af67', '#9a5236'),
]
for idx, (slug, title, bg, light, mid) in enumerate(specs):
    for portrait in [False, True]:
        w, h = (600, 850) if portrait else (1200, 675)
        cx, cy = w * .68, h * .36
        geom = ''
        if idx in [0, 5]:
            geom = f'<circle cx="{cx}" cy="{cy}" r="{w*.14}" fill="{light}"/>'
            for n in range(5):
                y = h * (.57 + n * .10)
                geom += f'<path d="M-100 {y+80} Q{w*.35} {y-210} {w*.68} {y} T{w+100} {y+40} L{w+100} {h+100} H-100Z" fill="{mid if n%2==0 else bg}"/>'
            geom += f'<path d="M{w*.68} {h*.54} l-10 40 h20Z" fill="{light}"/><path d="M{w*.68} {h*.60} q-80 80 -10 160" fill="none" stroke="{light}" stroke-width="3" opacity=".6"/>'
        elif idx == 1:
            geom = f'<circle cx="{cx}" cy="{cy}" r="{w*.23}" fill="{mid}"/><ellipse cx="{cx}" cy="{cy}" rx="{w*.36}" ry="{w*.075}" fill="none" stroke="{light}" stroke-width="5" transform="rotate(-26 {cx} {cy})"/><path d="M{w*.47} {h*.73} l45 -16 -12 36Z" fill="{light}"/>'
            for n in range(45):
                geom += f'<circle cx="{(n*97+31)%w}" cy="{(n*137+21)%h}" r="{1+n%2}" fill="{light}" opacity=".6"/>'
        elif idx == 2:
            for n in range(9):
                x, y = n*w/8, h*.3+(n%3)*h*.08
                geom += f'<path d="M{x} {h} Q{x-70} {y+160} {x+30} {y}" fill="none" stroke="{mid}" stroke-width="15"/><ellipse cx="{x+30}" cy="{y+40}" rx="{w*.065}" ry="{h*.18}" transform="rotate({n*20-60} {x+30} {y+40})" fill="{mid}"/>'
            geom += f'<circle cx="{cx}" cy="{h*.55}" r="38" fill="{light}"/><path d="M{cx} {h*.6} v100" stroke="{light}" stroke-width="5"/>'
        elif idx == 3:
            for n in range(13):
                x, hh = n*w/12, h*(.2+(n*7%5)*.07)
                geom += f'<rect x="{x}" y="{h*.75-hh}" width="{w/15}" height="{hh}" fill="{mid}"/>'
            geom += f'<path d="M0 {h} L{w*.58} {h*.65} L{w} {h}" fill="none" stroke="{light}" stroke-width="6"/><path d="M{w*.66} {h*.81} h110 l-30 -32 h-56Z" fill="{light}"/>'
        else:
            for n in range(9):
                geom += f'<path d="M-20 {h*.3+n*54} Q{w*.3} {h*.1+n*54} {w*.6} {h*.3+n*54} T{w+80} {h*.25+n*54}" fill="none" stroke="{mid}" stroke-width="18"/>'
            geom += f'<ellipse cx="{cx}" cy="{h*.54}" rx="75" ry="30" fill="{light}"/><circle cx="{cx+34}" cy="{h*.54}" r="12" fill="{bg}"/>'
        # Portrait carries its own cover title; landscape lets the theme title do the work.
        words = ''
        if portrait:
            for n, word in enumerate(title.split()):
                words += f'<text x="40" y="{80+n*56}" font-family="sans-serif" font-weight="bold" font-size="49" fill="{light}">{escape(word)}</text>'
            words += f'<text x="40" y="{h-36}" font-family="monospace" font-size="16" fill="{light}">ZAMAN PREVIEW / FICTIONAL GAME</text>'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{geom}{words}</svg>'
        (out/(slug + ('-poster' if portrait else '')+'.svg')).write_text(svg)
