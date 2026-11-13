#!/usr/bin/env bash
# Build the supplementary archive: Table S1, Figure S1 (PRISMA flow), PRISMA 2020 checklist, index.
set -euo pipefail
cd "$(dirname "$0")"
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1 || true)
python3 ../review/make_prisma_flow.py >/dev/null
python3 - <<'PY'
from PIL import Image, PngImagePlugin
f='../figures/fig_prisma_flow.png'; im=Image.open(f); im.load(); im.save(f, format='PNG', dpi=(600,600), pnginfo=PngImagePlugin.PngInfo())
PY
S=supplementary_build; rm -rf $S; mkdir -p $S
for src in supplementary prisma_checklist supplementary_cover; do
  pandoc $src.md --standalone --css style.css --embed-resources -o $S/$src.html
  pandoc $src.md -o $S/$src.docx
  [ -n "$CHROME" ] && "$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
      --print-to-pdf=$S/$src.pdf "file://$(pwd)/$S/$src.html" 2>/dev/null
done
cp $S/supplementary.pdf supplementary.pdf
cp $S/supplementary.docx supplementary.docx
cp $S/prisma_checklist.pdf prisma_checklist.pdf
cp $S/prisma_checklist.docx prisma_checklist.docx
python3 set_metadata.py >/dev/null
python3 - <<'PY'
from pypdf import PdfReader, PdfWriter
from docx import Document
A="Abhijeet Chandrakant Karve; Santosh Darade"
for f,t in [('supplementary_build/prisma_checklist.pdf','PRISMA 2020 checklist'),('supplementary_build/supplementary_cover.pdf','Supplementary Materials index'),('prisma_checklist.pdf','PRISMA 2020 checklist')]:
    r=PdfReader(f); w=PdfWriter(); w.append(r); w.add_metadata({'/Title':t,'/Author':A,'/Creator':'Pandoc 3.1.3','/Producer':'Pandoc 3.1.3'}); open(f,'wb').write(b'') ; w.write(f)
for f,t in [('prisma_checklist.docx','PRISMA 2020 checklist')]:
    d=Document(f); d.core_properties.author=A; d.core_properties.last_modified_by="Abhijeet Chandrakant Karve"; d.core_properties.title=t; d.save(f)
PY
Z=supplementary_zip; rm -rf $Z; mkdir -p $Z
cp supplementary.pdf $Z/Table_S1_review_corpus.pdf
cp ../figures/fig_prisma_flow.png $Z/Figure_S1_PRISMA_flow.png
cp prisma_checklist.pdf $Z/PRISMA_2020_checklist.pdf
cp $S/supplementary_cover.pdf $Z/README_supplementary.pdf
rm -f Supplementary_Materials.zip
(cd $Z && zip -q ../Supplementary_Materials.zip *)
ls -la Supplementary_Materials.zip
