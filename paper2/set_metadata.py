"""Set document properties on the Paper 2 submission files."""
from docx import Document
from pypdf import PdfReader, PdfWriter
import zipfile, re, os
AUTHORS = "Abhijeet Chandrakant Karve; Santosh Darade"
TITLE = ("Does a Meta-Learned Autoencoder Actually Adapt? A Measurement Study of First-Order MAML "
         "for Few-Shot Anomaly Detection on Industrial and Spacecraft Telemetry")
KEYWORDS = ("meta-learning; MAML; LSTM autoencoder; anomaly detection; industrial control systems; "
            "spacecraft telemetry; few-shot adaptation; evaluation methodology")
def fix_docx(path, title, kw=""):
    d = Document(path); cp = d.core_properties
    cp.author = AUTHORS; cp.last_modified_by = "Abhijeet Chandrakant Karve"; cp.title = title
    cp.subject = ""; cp.keywords = kw; cp.comments = ""; cp.category = ""
    d.save(path)
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/custom.xml": continue
            if item.filename == "[Content_Types].xml":
                data = re.sub(rb'<Override[^>]*PartName="/docProps/custom.xml"[^>]*/>', b"", data)
            if item.filename == "_rels/.rels":
                data = re.sub(rb'<Relationship[^>]*Target="docProps/custom.xml"[^>]*/>', b"", data)
            zout.writestr(item, data)
    os.replace(tmp, path)
def fix_pdf(path, title, kw=""):
    r = PdfReader(path); w = PdfWriter(); w.append(r)
    w.add_metadata({"/Title": title, "/Author": AUTHORS, "/Subject": "", "/Keywords": kw,
                    "/Creator": "Pandoc 3.1.3", "/Producer": "Pandoc 3.1.3"})
    with open(path, "wb") as f: w.write(f)
for f, t, kw in [("manuscript_make.docx", TITLE, KEYWORDS), ("cover_letter_make.docx", "Cover letter", ""),
                 ("suggested_reviewers.docx", "Suggested reviewers", "")]:
    if os.path.exists(f): fix_docx(f, t, kw)
for f, t, kw in [("manuscript_make.pdf", TITLE, KEYWORDS)]:
    if os.path.exists(f): fix_pdf(f, t, kw)
print("metadata set")
