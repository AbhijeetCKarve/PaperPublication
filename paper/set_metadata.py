"""Set document properties on the submission files so that the author names,
not the build tools, appear as the creators."""
import sys
from docx import Document
from pypdf import PdfReader, PdfWriter

AUTHORS = "Abhijeet Chandrakant Karve; Santosh Darade"
TITLE = ("Drift-Aware Meta-Adaptive Anomaly Detection for Few-Shot, Non-Stationary "
         "Industrial IoT Streams: A Benchmarking Protocol and the DAMAD Detector")
KEYWORDS = ("meta-learning; few-shot learning; anomaly detection; industrial Internet of Things; "
            "concept drift; streaming data; variational autoencoder; benchmarking")

def fix_docx(path, title):
    d = Document(path)
    cp = d.core_properties
    cp.author = AUTHORS
    cp.last_modified_by = "Abhijeet Chandrakant Karve"
    cp.title = title
    cp.subject = ""
    cp.keywords = KEYWORDS if "manuscript" in path else ""
    cp.comments = ""
    cp.category = ""
    d.save(path)

def fix_pdf(path, title):
    r = PdfReader(path); w = PdfWriter()
    w.append(r)
    w.add_metadata({"/Title": title, "/Author": AUTHORS, "/Subject": "",
                    "/Keywords": KEYWORDS if "manuscript" in path else "",
                    "/Creator": "Pandoc 3.1.3", "/Producer": "Pandoc 3.1.3"})
    with open(path, "wb") as f:
        w.write(f)

fix_docx("manuscript_make.docx", TITLE)
fix_docx("cover_letter_make.docx", "Cover letter")
fix_docx("supplementary.docx", "Supplementary material: " + TITLE)
fix_docx("suggested_reviewers.docx", "Suggested reviewers")
fix_pdf("manuscript_make.pdf", TITLE)
fix_pdf("supplementary.pdf", "Supplementary material: " + TITLE)

def strip_custom_props(path):
    """Remove the custom-properties part pandoc writes (bibliography/csl names)."""
    import zipfile, shutil, re, os
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/custom.xml":
                continue
            if item.filename == "[Content_Types].xml":
                data = re.sub(rb'<Override[^>]*PartName="/docProps/custom.xml"[^>]*/>', b"", data)
            if item.filename == "_rels/.rels":
                data = re.sub(rb'<Relationship[^>]*Target="docProps/custom.xml"[^>]*/>', b"", data)
            zout.writestr(item, data)
    os.replace(tmp, path)

for f in ("manuscript_make.docx", "cover_letter_make.docx", "supplementary.docx", "suggested_reviewers.docx"):
    strip_custom_props(f)
print("metadata set")
