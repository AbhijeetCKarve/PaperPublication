"""Rewrite pandoc's longtables as MDPI-style table + tabularx blocks.

Column widths are derived from the cell contents; tables with many columns
use the full page width (adjustwidth + \\fulllength) as the MDPI template shows."""
import re, sys

def brace_arg(s, i):
    """s[i] == '{'; return (content, index after closing brace)."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i+1:j], j+1
    raise ValueError('unbalanced')

def cells_of_header(block):
    return [c.strip() for c in re.findall(r'\\begin\{minipage\}\[b\]\{\\linewidth\}\\raggedright\n(.*?)\n\\end\{minipage\}', block, re.S)]

def split_row(line):
    # split on ' & ' not inside braces or math
    cells, depth, cur, inmath = [], 0, '', False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
        elif ch == '$': inmath = not inmath
        if depth == 0 and not inmath and line.startswith(' & ', i):
            cells.append(cur.strip()); cur = ''; i += 3; continue
        cur += ch; i += 1
    cells.append(cur.strip())
    return cells

def visible_len(s):
    s = re.sub(r'\\[a-zA-Z]+(\{[^}]*\})?', 'x', s)
    return len(s)

def convert(block):
    m = re.search(r'\\caption\{', block)
    cap, _ = brace_arg(block, m.end()-1)
    ncol = len(re.findall(r'\\real\{', block)) or len(re.search(r'\\begin\{longtable\}\[\]\{@\{\}([lcr]+)@\{\}\}', block).group(1))
    head_block = block[:block.index('\\endfirsthead')]
    header = cells_of_header(head_block)
    if not header:  # simple tables: header is a plain row
        hb = head_block[head_block.index('\\toprule'):]
        header = split_row([l for l in hb.split('\n') if l.strip().endswith('\\\\')][0].rstrip('\\').strip())
    if '\\endlastfoot' in block:
        body_src = block[block.index('\\endlastfoot')+len('\\endlastfoot'):block.rindex('\\end{longtable}')]
    else:
        body_src = block[block.index('\\endhead')+len('\\endhead'):block.index('\\bottomrule')]
    rows = [split_row(l.strip()[:-2].strip()) for l in body_src.split('\n') if l.strip().endswith('\\\\')]
    ncol = len(header)
    # column weights from content
    lens = []
    for c in range(ncol):
        col = [header[c]] + [r[c] for r in rows if len(r) > c]
        longest = max(visible_len(x) for x in col)
        lens.append(max(5, min(longest, 48)))
    total = sum(lens)
    weights = [l / total * ncol for l in lens]
    if ncol >= 6 and weights[0] < 1.5:          # dense result tables: keep the label column readable
        extra = 1.5 - weights[0]
        weights[0] = 1.5
        rest = sum(weights[1:])
        weights[1:] = [w * (rest - extra) / rest for w in weights[1:]]
    short = [all(visible_len(r[c]) <= 12 for r in rows if len(r) > c) and visible_len(header[c]) <= 12 for c in range(ncol)]
    spec = ''.join(('>{\\centering\\arraybackslash\\hsize=%.3f\\hsize}X' if short[c] and c > 0 else '>{\\raggedright\\arraybackslash\\hsize=%.3f\\hsize}X') % weights[c] for c in range(ncol))
    wide = ncol >= 7 or total > 150
    width = '\\fulllength' if wide else '\\textwidth'
    size = '\\small' if wide or total > 110 else ''
    out = ['\\begin{table}[H]', '\\caption{%s}' % cap]
    if wide: out.append('\\begin{adjustwidth}{-\\extralength}{0cm}')
    out.append('\\centering' + size)
    out.append('\\begin{tabularx}{%s}{%s}' % (width, spec))
    out.append('\\toprule')
    out.append(' & '.join('\\textbf{%s}' % h for h in header) + ' \\\\')
    out.append('\\midrule')
    for r in rows:
        out.append(' & '.join(r) + ' \\\\')
    out.append('\\bottomrule')
    out.append('\\end{tabularx}')
    if wide: out.append('\\end{adjustwidth}')
    out.append('\\end{table}')
    return '\n'.join(out)

tex = open(sys.argv[1]).read()
parts = re.split(r'(\\begin\{longtable\}.*?\\end\{longtable\})', tex, flags=re.S)
n = 0
for i, p in enumerate(parts):
    if p.startswith('\\begin{longtable}'):
        parts[i] = convert(p); n += 1
tex2=''.join(parts).replace('height=\\textheight', 'height=0.78\\textheight')
open(sys.argv[1], 'w').write(tex2)
print('tables converted:', n)
