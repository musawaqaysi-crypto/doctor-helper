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
                cell = re.sub(r'(?<=\b0)\s+(?=5\d{8})', '', cell)
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
    for n in re.split(r'/|,|&|\+', cell):
        n = re.sub(r'^\s*DR\.?\s*', '', n.strip(), flags=re.I).strip()
        if n and not re.search(r'ROD$|^-+$|^—$|ON\s*CALL|SPECIALIST|OPERATING|ROOM|VACATION|LEAVE|^OFF$', n, re.I): out.append(n)
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
         "OBSTETRICS__GYNECOLOGY_SPECIALIST_AND_CONSULTANT", "ADULT_INTENSIVE_CARE_UNIT", "ANESTHESIA", "CARDIOLOGY", "EMERGENCY_DEPARTMENT", "ENT", "RADIOLOGY", "INTERNAL_MEDICINE", "OPHTHALMOLOGY", "DERMATOLOGY", "LABORATORY", "NEPHROLOGY-2", "ORTHOPEDIC_SURGERY", "UROLOGY", "NEUROLOGY", "DENTAL_DUTY", "EBOLA", "PEDIATRIC_SPECIALIST_AND_CONSULTANT"]

def clinic_times(cell, st, en):
    # "Dr. Noor (8:00am—4:00pm)" carries its own hours; otherwise the column's hours
    m = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)\s*[—–-]+\s*(\d{1,2}):(\d{2})\s*(am|pm)', cell, re.I)
    if not m: return st, en
    h = lambda hh, ap: (int(hh) % 12) + (12 if ap.lower() == "pm" else 0)
    return f"{h(m.group(1), m.group(3)):02d}:{m.group(2)}", f"{h(m.group(4), m.group(6)):02d}:{m.group(5)}"
def clinic(dept, d, cell, st, en, label, book):
    for part in [c for c in re.split(r'/|,|&', cell) if c.strip()]:
        a, b = clinic_times(part, st, en)
        add(dept, d, "عيادة", part, a, b, "عيادة · " + label, book)

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
# Outpatient clinics (OPD columns) → shown in each department's clinics box
t = tables(F["GENERAL_SURGERY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    clinic("الجراحة العامة", d, r[4], "08:00", "12:00", "صباحية", book)
    clinic("الجراحة العامة", d, r[5], "13:00", "16:00", "مسائية", book)
t = tables(F["PEDIATRIC_SURGERY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d and len(r) > 3: clinic("جراحة الأطفال", d, r[3], "08:00", "16:00", "العيادة الخارجية", book)
t = tables(F["SPECIALIST_AND_CONSULTANT"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d and len(r) > 7: clinic("النساء والولادة", d, r[7], "08:00", "16:00", "العيادة الخارجية", book)
t = tables(F["PSYCHIATRIC"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    clinic("الطب النفسي", d, r[3], "08:00", "16:00", "العيادة الخارجية", book)
    clinic("الطب النفسي", d, r[4], "08:00", "16:00", "عيادة إرادة", book)
    clinic("الطب النفسي", d, r[5], "08:00", "16:00", "العيادة الافتراضية", book)
t = tables(F["ANESTHESIA"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d and len(r) > 10: clinic("التخدير", d, r[10], "08:00", "16:00", "عيادة ما قبل التخدير", book)
t = tables(F["CARDIOLOGY"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if not d: continue
    clinic("القلب", d, r[4], "08:00", "12:00", "صباحية", book)
    clinic("القلب", d, r[5], "13:00", "16:00", "مسائية", book)
t = tables(F["ENT"]); book = phonebook(t)
for r in t[0]:
    d = day(r[0]) if r else None
    if d and len(r) > 3: clinic("الأنف والأذن والحنجرة", d, r[3], "08:00", "16:00", "العيادة الخارجية", book)
# Internal medicine: specialist + consultant on call; four clinics
if F.get("INTERNAL_MEDICINE"):
    t = tables(F["INTERNAL_MEDICINE"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        add("الباطنة", d, "أخصائي", r[2], "", "", "أخصائي مناوب", book)
        add("الباطنة", d, "استشاري", r[3], "", "", "استشاري مناوب", book)
        clinic("الباطنة", d, r[4], "08:00", "12:00", "صباحية", book)
        clinic("الباطنة", d, r[5], "08:00", "16:00", "العيادة الافتراضية", book)
        clinic("الباطنة", d, r[6], "13:00", "16:00", "مسائية", book)
        if len(r) > 7: clinic("الباطنة", d, r[7], "08:00", "16:00", "عيادة الكبد", book)
# Ophthalmology: on call with its own hours, morning/afternoon clinics
if F.get("OPHTHALMOLOGY"):
    t = tables(F["OPHTHALMOLOGY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        clinic("العيون", d, r[2], "08:00", "12:00", "صباحية", book)
        clinic("العيون", d, r[3], "13:00", "16:00", "مسائية", book)
        if r[5].strip(): add("العيون", d, "مناوب", re.sub(r'\d.*', '', r[5]), "07:30", "19:30", "مناوب", book)
# Radiology: doctors are written as codes; the code table maps them to names and phones
if F.get("RADIOLOGY"):
    t = tables(F["RADIOLOGY"]); codes = {}
    for row in t[1][1:]:
        for i in range(0, len(row) - 2, 3):
            c, nm, ph = row[i].strip(), re.sub(r'\(.*?\)', '', row[i + 1]).strip(), re.findall(r'05\d{8}', row[i + 2])
            if c: codes[c] = (re.sub(r'^\s*Dr\.?\s*', '', nm, flags=re.I).strip(), ph[0] if ph else "")
    def radd(d, cell, lvl, st, en, note):
        for c in [x.strip() for x in re.split(r'[-/,]', cell) if x.strip()]:
            nm, ph = codes.get(c, (c, ""))
            if c not in codes: unmatched.add(f"الأشعة: {c}")
            rows.append(["الأشعة", d, lvl, "د. " + re.sub(r'\s+', ' ', nm).title(), ph, st, en, note])
    mods = t[0][1][2:8]
    for r in t[0][2:]:
        d = day(r[0]) if r else None
        if not d: continue
        radd(d, r[8], "مناوب", "", "", "مناوب الأشعة")
# Dermatology: morning/afternoon clinics, one on call
if F.get("DERMATOLOGY"):
    t = tables(F["DERMATOLOGY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        clinic("الجلدية", d, r[2], "08:00", "12:00", "صباحية", book)
        clinic("الجلدية", d, r[3], "13:00", "16:00", "مسائية", book)
        add("الجلدية", d, "مناوب", r[4], "", "", "مناوب", book)
# Laboratory & blood bank: morning duty, two doctors joined by "and"
if F.get("LABORATORY"):
    t = tables(F["LABORATORY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if d: add("المختبر وبنك الدم", d, "مناوب", re.sub(r'\s+and\s+', '/', r[2], flags=re.I), "08:00", "16:00", "مناوب صباحي", book)
# Nephrology: hemodialysis cover, 1st (specialist) and 2nd (consultant) on call, clinics
if F.get("NEPHROLOGY-2"):
    t = tables(F["NEPHROLOGY-2"]); book = phonebook(t)
    for r in t[0]:
        d = (day(r[0]) or day(r[1])) if len(r) > 1 else None
        if not d: continue
        add("الكلى", d, "مناوب", r[2], "07:30", "23:30", "وحدة الغسيل الكلوي", book)
        add("الكلى", d, "أخصائي", r[3], "", "", "المناوب الأول", book)
        add("الكلى", d, "استشاري", r[4], "", "", "المناوب الثاني", book)
        if len(r) > 5: clinic("الكلى", d, r[5], "08:00", "16:00", "العيادة الخارجية", book)
# Orthopedics: 1st on call day/night (specialist), 2nd on call 24h (consultant), clinic, residents day/night
if F.get("ORTHOPEDIC_SURGERY"):
    t = tables(F["ORTHOPEDIC_SURGERY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        add("العظام", d, "أخصائي", r[2], "08:00", "20:00", "المناوب الأول نهاري", book)
        add("العظام", d, "أخصائي", r[3], "20:00", "08:00", "المناوب الأول ليلي", book)
        add("العظام", d, "استشاري", r[4], "", "", "المناوب الثاني 24 ساعة", book)
        clinic("العظام", d, r[5], "08:00", "16:00", "العيادة الخارجية", book)
        add("العظام", d, "مقيم", r[6], "08:00", "20:00", "مقيم نهاري", book)
        if len(r) > 7: add("العظام", d, "مقيم", r[7], "20:00", "08:00", "مقيم ليلي", book)
# Urology: clinics; specialist on call split by hours ("7.30 AM – 4 PM: X; 4 PM ONWARDS: Y"); consultant on call
if F.get("UROLOGY"):
    t = tables(F["UROLOGY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        clinic("المسالك البولية", d, r[2], "08:00", "12:00", "صباحية", book)
        clinic("المسالك البولية", d, r[3], "13:00", "16:00", "مسائية", book)
        for seg in [x for x in r[4].split(";") if ":" in x]:
            when, who = seg.rsplit(":", 1)
            st, en = ("16:00", "07:30") if re.search(r'onward', when, re.I) else ("07:30", "16:00")
            add("المسالك البولية", d, "أخصائي", who, st, en, "أخصائي مناوب", book)
        add("المسالك البولية", d, "استشاري", r[5], "", "", "استشاري مناوب", book)
# Neurology: 24h on call, clinic
if F.get("NEUROLOGY"):
    t = tables(F["NEUROLOGY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        add("الأعصاب", d, "مناوب", r[2], "", "", "مناوب 24 ساعة", book)
        clinic("الأعصاب", d, r[3], "08:00", "16:00", "العيادة الخارجية", book)
# Dental: daily duty per service
if F.get("DENTAL_DUTY"):
    t = tables(F["DENTAL_DUTY"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        add("الأسنان", d, "مناوب", r[2], "", "", "علاج العصب (ENDO)", book)
        add("الأسنان", d, "مناوب", r[3], "", "", "جراحة الوجه والفكين (OMFS)", book)
        add("الأسنان", d, "مناوب", r[4], "", "", "OMFS و ENDO · الرعاية الأولية", book)
# Ebola team: one on call per day
if F.get("EBOLA"):
    t = tables(F["EBOLA"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if d: add("فريق الإيبولا", d, "مناوب", r[2], "", "", "مناوب", book)
# Pediatrics: morning call, NICU, on call (specialists), consultant on call, clinic
if F.get("PEDIATRIC_SPECIALIST_AND_CONSULTANT"):
    t = tables(F["PEDIATRIC_SPECIALIST_AND_CONSULTANT"]); book = phonebook(t)
    for r in t[0]:
        d = day(r[0]) if r else None
        if not d: continue
        add("الأطفال", d, "أخصائي", r[2], "08:00", "16:00", "المناوب الصباحي", book)
        add("الأطفال", d, "أخصائي", r[3], "", "", "حديثي الولادة NICU", book)
        add("الأطفال", d, "أخصائي", r[4], "", "", "أخصائي مناوب", book)
        add("الأطفال", d, "استشاري", r[5], "", "", "استشاري مناوب", book)
        clinic("الأطفال", d, r[6], "08:00", "16:00", "العيادة الخارجية", book)
# Corrections the user gave for numbers missing or mistyped in the rosters
PHONE_FIX = {"sadeq": "0568963362", "anas": "0567568068", "safiah": "0508334081", "laila": "0554539584", "sofian": "0501552909"}
for r in rows:
    r[3] = re.sub(r'^د\. D\s*R\.?\s*', 'د. ', r[3], flags=re.I)
    k = key(r[3].replace("د. ", "").split()[0]) if r[3].replace("د. ", "").split() else ""
    if not r[4] and k in PHONE_FIX: r[4] = PHONE_FIX[k]; unmatched.discard(f"{r[0]}: {r[3].replace('د. ', '').upper()}"); unmatched.discard(f"{r[0]}: {r[3].replace('د. ', '')}")
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
