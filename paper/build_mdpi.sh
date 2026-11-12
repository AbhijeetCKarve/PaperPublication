#!/usr/bin/env bash
# Assemble the MDPI (Machine Learning and Knowledge Extraction) version of the manuscript:
# MDPI front matter + body (Sections 1-9) + MDPI back matter, references in MDPI style.
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
import re
p1 = open('manuscript_part1.md').read()
p2 = open('manuscript_part2.md').read()
p3 = open('manuscript_part3.md').read()
# body of part 1 starts at Section 1 (drop the pandoc front matter, abstract and keywords)
p1 = p1[p1.index('# 1 Introduction'):]
# part 3 ends before the unnumbered availability / declaration sections
p3 = p3[:p3.index('# Data and code availability')]
body = p1 + '\n' + p2 + '\n' + p3
front = open('mdpi_front.md').read()
back = open('mdpi_back.md').read()
open('manuscript_make.md', 'w').write(front + body.rstrip() + '\n' + back)
PY
# bibliography preprocessed for the MDPI style: protect the case of journal and proceedings
# names, drop a leading "Proceedings of the" (the style adds "In Proceedings of"), and keep
# the particle surname "van den Hengel" in one piece
python3 - <<'PY'
import re
b = open('references.bib').read()
def fix(m):
    key, val = m.group(1), m.group(2).strip()
    if key == 'booktitle':
        val = re.sub(r'^Proceedings of (the )?', '', val)
    return f"  {key} = {{{{{val}}}}},"
b = re.sub(r'^\s*(booktitle|journal)\s*=\s*\{(.*)\},\s*$', fix, b, flags=re.M)
b = b.replace('van den Hengel, Anton', '{van den Hengel}, Anton')
open('references_mdpi.bib', 'w').write(b)
PY
# reference.docx with the MDPI body font
pandoc -o /tmp/ref_default.docx --print-default-data-file reference.docx
python3 - <<'PY'
from docx import Document
from docx.shared import Pt
d = Document('/tmp/ref_default.docx')
for name in ('Normal', 'Body Text', 'First Paragraph', 'Compact', 'Title', 'Author', 'Heading 1', 'Heading 2', 'Heading 3', 'Caption', 'Table', 'Bibliography', 'Image Caption'):
    try:
        st = d.styles[name]
    except KeyError:
        continue
    st.font.name = 'Palatino Linotype'
    if name in ('Normal', 'Body Text', 'First Paragraph', 'Compact', 'Bibliography', 'Heading 1', 'Heading 2', 'Heading 3'):
        st.font.size = Pt(10)
    if name == 'Title':
        st.font.size = Pt(18)
d.save('reference_mdpi.docx')
PY
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1 || true)
pandoc manuscript_make.md --citeproc --bibliography references_mdpi.bib --csl mdpi.csl \
  --reference-doc reference_mdpi.docx -o manuscript_make.docx
pandoc manuscript_make.md --citeproc --bibliography references_mdpi.bib --csl mdpi.csl \
  --standalone --mathml --css style_mdpi.css --embed-resources -o manuscript_make.html
if [ -n "$CHROME" ]; then
  "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf=manuscript_make.pdf "file://$(pwd)/manuscript_make.html" 2>/dev/null
fi
pandoc cover_letter_make.md -o cover_letter_make.docx
python3 set_metadata.py
wc -w manuscript_make.md
ls -la manuscript_make.docx manuscript_make.pdf cover_letter_make.docx 2>/dev/null || true
