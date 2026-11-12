"""Turn the manuscript Markdown into a LaTeX body for the MDPI class.

Section numbers, figure numbers, table numbers and equation numbers become
automatic; captions move into the proper caption slots; stray Unicode symbols
become math; citations become natbib commands."""
import re, subprocess, pathlib

here = pathlib.Path(__file__).parent
p1 = (here / 'manuscript_part1.md').read_text()
p2 = (here / 'manuscript_part2.md').read_text()
p3 = (here / 'manuscript_part3.md').read_text()
p1 = p1[p1.index('# 1 Introduction'):]
p3 = p3[:p3.index('# Data and code availability')]
md = p1 + '\n' + p2 + '\n' + p3

# headings: drop the manual numbers
md = re.sub(r'^(#+) \d+(?:\.\d+)* ', r'\1 ', md, flags=re.M)

# equations: \qquad \text{(n)} -> equation environment (numbered automatically)
md = re.sub(r'^\$\$\s*(.*?)\s*\\qquad \\text\{\(\d+\)\}\s*\$\$\s*$',
            lambda m: '\\begin{equation}\n' + m.group(1) + '\n\\end{equation}', md, flags=re.M | re.S)

# figures: strip "Figure N." from the caption, give a width
def fig(m):
    cap, path, attrs = m.group(1), m.group(2), m.group(3) or ''
    ident = re.search(r'#[\w:-]+', attrs)
    width = '100%' if 'architecture' in path or 'gapmap' in path or 'trace' in path else '92%'
    idpart = (ident.group(0) + ' ') if ident else ''
    return f'![{cap}]({path}){{{idpart}width={width}}}'
md = re.sub(r'!\[Figure \d+\. (.*?)\]\((\S+?)\)(\{[^}\n]*\})?', fig, md, flags=re.S)

# tables: "Table N. caption" paragraph before a pipe table -> caption line after the table
lines = md.split('\n'); out = []; i = 0
while i < len(lines):
    m = re.match(r'^Table \d+\. (.*)$', lines[i])
    if m and i + 2 < len(lines) and lines[i + 1].strip() == '' and lines[i + 2].startswith('|'):
        cap = m.group(1); i += 2
        while i < len(lines) and lines[i].startswith('|'):
            out.append(lines[i]); i += 1
        out.append(''); out.append(': ' + cap); out.append('')
        continue
    out.append(lines[i]); i += 1
md = '\n'.join(out)

# symbols outside math -> math
for ch, tex in {'θ': r'\ensuremath{\theta}', 'τ': r'\ensuremath{\tau}', '≈': r'\ensuremath{\approx}',
                '→': r'\ensuremath{\rightarrow}', '−': r'\ensuremath{-}', '∈': r'\ensuremath{\in}',
                '²': r'\ensuremath{^{2}}', '×': r'\ensuremath{\times}', '±': r'\ensuremath{\pm}'}.items():
    parts = re.split(r'(\$\$.*?\$\$|\$[^$\n]*\$|\\begin\{equation\}.*?\\end\{equation\})', md, flags=re.S)
    md = ''.join(p if (p.startswith('$') or p.startswith('\\begin')) else p.replace(ch, tex) for p in parts)

(here / 'latex' / 'body.md').write_text(md)
subprocess.run(['pandoc', 'latex/body.md', '-t', 'latex', '--natbib', '--wrap=none',
                '--resource-path=.', '-o', 'latex/body.tex'], check=True, cwd=here)
tex = (here / 'latex' / 'body.tex').read_text()
tex = tex.replace('../figures/', 'figures/')
(here / 'latex' / 'body.tex').write_text(tex)
print('body.tex written:', len(tex), 'chars')
