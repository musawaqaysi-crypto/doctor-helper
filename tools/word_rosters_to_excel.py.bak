import zipfile, re, glob, difflib, sys
from xml.dom import minidom
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
U = sys.argv[1]; OUT = sys.argv[2]
def text(n): return " ".join(" ".join(t.firstChild.data for t in p.getElementsByTagName('w:t') if t.firstChild) for p in n.getElementsByTagName('w:p')).strip()
def tables(f):
    x = minidom.parseString(zipfile.ZipFile(f).read('word/document.xml'))
    out = []
    for t in x.getElementsByTagName('w:tbl'):
        rows = []
        for r in [r for r in t.childNodes if r.nodeName == 'w:tr']:
            row = []
            for c in [c for c in r.childNodes if c.nodeName == 'w:tc']:
                gs = c.getElementsByTagName('w:gridSpan'); n = int(gs[0].getAttribute('w:val')) if gs else 1
                row += [text(c)] * n
            rows.append(row)
        out.append(rows)
    return out
def phonebook(tbls):
    book = {}
    for rows in tbls:
        for row in rows:
            for cell in row:
                cell = re.sub(r'\([^)]*\)', ' ', cell)
                for m in re.finditer(r'((?:DR\.?\s*)?[A-Za-z][A-Za-z .\-]*?)\s*[-–]?\s*(05\d{8})', cell, re.I):
                    nm = re.sub(r'^\s*DR\.?\s*', '', m.group(1), flags=re.I).strip(" -–")
                    book[nm] = m.group(2)
        for a, b in zip(rows, rows[1:]):
            if b and all(re.fullmatch(r'\s*05\d{8}\s*', c or '') for c in b if c.strip()):
                for nm, ph in zip(a, b):
                    if ph.strip(): book[re.sub(r'^\s*DR\.?\s*', '', nm, flags=re.I).strip()] = ph.strip()
    return book
def key(s): return re.sub(r'[^a-z]', '', s.lower())
def lookup(name, book):
    k = key(name.split()[0]) if name.split() else ""
    best, score = None, 0
    for full, ph in book.items():
        for tok in [key(full)] + [key(w) for w in full.split()]:
            r = difflib.SequenceMatcher(None, k, tok).ratio()
            if r > score: best, score = (full, ph), r
    return best if score >= 0.7 else None
def day(s):
    m = re.match(r'(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})$', re.sub(r'\s+', '', s))
    if not m: return None
    y = m.group(3); y = "20" + y if len(y) == 2 else y
    return f"{y}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
def names(cell):
    cell = re.sub(r'\([^)]*\)', '', cell)
    out = []
    for n in re.split(r'/|,|&', cell):
        n = re.sub(r'^\s*DR\.?\s*', '', n.strip(), flags=re.I).strip()
        if n and not re.search(r'ROD$|^-+$|^—$|ON\s*CALL|SPECIALIST', n, re.I): out.append(n)
    return out
rows, unmatched = [], set()
def add(dept, d, lvl, cell, st, en, note, book):
    for n in names(cell):
        hit = lookup(n, book)
        if not hit: unmatched.add(f"{dept}: {n}")
        full = hit[0].title() if hit else n.title()
        rows.append([dept, d, lvl, "د. " + re.sub(r'\s+', ' ', full), hit[1] if hit else "", st, en, note])
import os
def newest(name):
    hits = [f for f in glob.glob(f"{U}/*.docx") if re.fullmatch(r"[0-9a-f]{8}-" + re.escape(name) + r"\.docx", os.path.basename(f))]
    return max(hits, key=os.path.getmtime) if hits else None
NAMES = ["GENERAL_SURGERY", "GENERAL_SURGERY_-_RESIDENT", "PEDIATRIC_SURGERY", "PSYCHIATRIC", "OBSTETRICS__GYNECOLOGY_RESIDENT",
         "OBSTETRICS__GYNECOLOGY_SPECIALIST_AND_CONSULTANT", "ADULT_INTENSIVE_CARE_UNIT", "ANESTHESIA", "CARDIOLOGY", "EMERGENCY_DEPARTMENT", "ENT"]
F = {n: newest(n) for n in NAMES}
print("files:", {k: os.path.basename(v) if v else None for k, v in F.items()})
F.update({"GYNECOLOGY_RESIDENT": F["OBSTETRICS__GYNECOLOGY_RESIDENT"], "SPECIALIST_AND_CONSULTANT": F["OBSTETRICS__GYNECOLOGY_SPECIALIST_AND_CONSULTANT"], "INTENSIVE_CARE": F["ADULT_INTENSIVE_CARE_UNIT"]})
# General surgery: 2nd on-call (specialist, 24h) + consultant on call
t = tables(F["GENERAL_SURGERY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("الجراحة العامة", d, "أخصائي", r[2], "", "", "المناوب الثاني 24 ساعة", book)
    add("الجراحة العامة", d, "استشاري", r[3], "", "", "استشاري مناوب", book)
# General surgery residents: day 08-20, night 20-08
t = tables(F["GENERAL_SURGERY_-_RESIDENT"]); book = phonebook(t); book["M.Salah Sallahudin"] = book.get("Sallahudin", "")
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("الجراحة العامة", d, "مقيم", r[2], "08:00", "20:00", "مقيم نهاري", book)
    add("الجراحة العامة", d, "مقيم", r[3], "20:00", "08:00", "مقيم ليلي", book)
# Pediatric surgery: one on-call doctor on listed days
t = tables(F["PEDIATRIC_SURGERY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d: add("جراحة الأطفال", d, "مناوب", r[2], "", "", "مناوب", book)
# Psychiatry: morning on call
t = tables(F["PSYCHIATRIC"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d: add("الطب النفسي", d, "مناوب", r[6], "08:00", "16:00", "مناوب صباحي", book)
# OB/GYN residents: morning / evening / night
t = tables(F["GYNECOLOGY_RESIDENT"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("النساء والولادة", d, "مقيم", r[2], "08:00", "16:00", "صباحي", book)
    add("النساء والولادة", d, "مقيم", r[3], "16:00", "00:00", "مسائي", book)
    add("النساء والولادة", d, "مقيم", r[4], "00:00", "08:00", "ليلي", book)
# OB/GYN specialists & consultants: on-duty specialist 16h from 4 PM, consultant on call, morning delivery-room specialist
t = tables(F["SPECIALIST_AND_CONSULTANT"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("النساء والولادة", d, "أخصائي", r[4], "08:00", "16:00", "غرفة الولادة صباحاً", book)
    add("النساء والولادة", d, "أخصائي", r[2], "16:00", "08:00", "مناوب 16 ساعة من 4 العصر", book)
    add("النساء والولادة", d, "استشاري", r[3], "", "", "استشاري مناوب", book)
# Adult ICU: 1st on-call morning 08-20 / evening 20-08 (specialist), 2nd on-call (consultant)
t = tables(F["INTENSIVE_CARE"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("العناية المركزة", d, "أخصائي", r[2], "08:00", "20:00", "المناوب الأول صباحي", book)
    add("العناية المركزة", d, "أخصائي", r[3], "20:00", "08:00", "المناوب الأول مسائي", book)
    add("العناية المركزة", d, "استشاري", r[4], "", "", "المناوب الثاني", book)
# Anesthesia: on call morning 07:30-16:00, afternoon 16:00-07:30 (specialists), 2nd on call (consultant)
t = tables(F["ANESTHESIA"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("التخدير", d, "أخصائي", r[6], "07:30", "16:00", "مناوب صباحي", book)
    add("التخدير", d, "أخصائي", r[7], "16:00", "07:30", "مناوب مسائي", book)
    add("التخدير", d, "استشاري", r[8], "", "", "المناوب الثاني", book)
# Cardiology: 2nd on call (1st on call is the medical specialist)
t = tables(F["CARDIOLOGY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    add("القلب", d, "أخصائي", r[2], "", "", "المناوب الأول", book)
    add("القلب", d, "استشاري", r[3], "", "", "المناوب الثاني", book)
# Emergency: male / female ER, morning 07:30-19:30 and night 19:30-07:30 (day and date columns swapped)
t = tables(F["EMERGENCY_DEPARTMENT"]); book = phonebook(t)
for r in t[0]:
    d = (day(r[0]) or day(r[1])) if len(r) > 1 else None
    if not d: continue
    add("الطوارئ", d, "مناوب", r[2], "07:30", "19:30", "طوارئ رجال صباحي", book)
    add("الطوارئ", d, "مناوب", r[3], "07:30", "19:30", "طوارئ نساء صباحي", book)
    add("الطوارئ", d, "مناوب", r[4], "19:30", "07:30", "طوارئ رجال ليلي", book)
    add("الطوارئ", d, "مناوب", r[5], "19:30", "07:30", "طوارئ نساء ليلي", book)
# ENT: on call with its own hours, e.g. "Thomas(7:30am—4:00pm)"
t = tables(F["ENT"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d: add("الأنف والأذن والحنجرة", d, "مناوب", r[2], "07:30", "16:00", "مناوب", book)
wb = Workbook(); ws = wb.active; ws.title = "المناوبات"; ws.sheet_view.rightToLeft = True
ws.append(["القسم", "التاريخ", "المستوى", "الاسم", "الجوال", "من", "إلى", "ملاحظة"])
for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1C2230"); c.alignment = Alignment(horizontal="center")
for r in rows: ws.append(r)
for col, w in zip("ABCDEFGH", (16, 12, 10, 26, 14, 8, 8, 26)): ws.column_dimensions[col].width = w
wb.save(OUT)
from collections import Counter
print("rows:", len(rows)); print(Counter((r[0], r[2]) for r in rows))
print("dates:", min(r[1] for r in rows), "→", max(r[1] for r in rows))
print("no phone:", sorted(unmatched) or "none")
print("sample:", rows[0], rows[-1])
