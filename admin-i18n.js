// English / عربي switch for the admin page. The page is written in Arabic; in English mode every text node,
// placeholder, title and alert is translated through the phrases below (exact text first, then patterns).
// Roster data (departments, names, notes) is left as typed. The choice is remembered per device (dh-admin-lang).
(function(){
  const EN = {
    "لوحة المشرف": "Admin panel", "مُناوِب · جداول المناوبات": "Munawib · Duty rosters", "لوحة المشرف — مُناوِب": "Admin panel — Munawib",
    "التطبيق": "App", "الرقم السري": "Password", "خروج": "Sign out",
    "دخول المشرف": "Admin sign-in", "بالرقم السري": "With your password", "الإيميل": "E-mail", "دخول": "Sign in",
    "نسيت الرقم السري أو أول مرة؟ أرسل رابط دخول على الإيميل": "Forgot the password or first time? Send a sign-in link by e-mail",
    "تغيير الإيميل": "Change e-mail", "اختر رقمك السري": "Choose your password",
    "٨ خانات أو أكثر. بعدها تدخل به بدل الإيميل.": "8 characters or more. Then you sign in with it instead of the e-mail.",
    "الرقم السري الجديد": "New password", "أعده مرة ثانية": "Repeat it", "حفظ": "Save", "إلغاء": "Cancel",
    "اللوحة لسا ما ارتبطت بقاعدة البيانات. أكمل الإعداد أول.": "The panel isn't connected to the database yet. Finish the setup first.",
    "رفع جدول مناوبات": "Upload a duty roster",
    "Excel أو Word أو PDF. يستبدل جدول نفس القسم في نفس الأيام.": "Excel, Word or PDF. Replaces the same department's roster for the same days.",
    "حمّل النموذج": "Download the template", "عبّه": "Fill it", "ارفعه وراجع": "Upload and review", "احفظ": "Save",
    "تحميل النموذج": "Download template", "اختر الملف أو اسحبه هنا": "Choose the file or drop it here",
    "حوّلت الملف إلى جدول.": "The file was turned into a table.",
    "حدد فوق كل عمود وش فيه، والأعمدة اللي ما تبيها خلها «تجاهل». راجع القراءة، لأن الملفات المصوّرة ممكن يكون فيها أخطاء.":
      "Set what each column holds; leave unwanted columns as “Ignore”. Check the reading — scanned files can have errors.",
    "القسم (إذا الملف كله لقسم واحد)": "Department (if the whole file is one department)", "مثل: الباطنة": "e.g. Internal Medicine",
    "الشهر (إذا التاريخ رقم اليوم بس)": "Month (if the date is only the day number)", "تجاهل أول": "Skip first", "لا شي": "None",
    "جهّز للحفظ": "Prepare to save", "تحميل كـ Excel": "Download as Excel", "احفظ الجدول": "Save roster",
    "قرأت الجدول تلقائياً.": "Roster read automatically.",
    "راجع القسم ونوع كل عمود ووقته، وعدّل إذا لزم، وبعدها «جهّز للحفظ».": "Check the department and each column's type and hours, edit if needed, then “Prepare to save”.",
    "القسم": "Department", "الأيام": "Days", "ربط الأعمدة يدوياً": "Map columns manually",
    "العمود في الملف": "Column in the file", "النوع": "Type", "من": "From", "إلى": "To", "مثال": "Example",
    "تجاهل": "Ignore", "مقيم": "Resident", "أخصائي": "Specialist", "استشاري": "Consultant", "مناوب": "On call", "عيادة": "Clinic",
    "التاريخ / اليوم": "Date / day", "المستوى": "Level", "الاسم": "Name", "الجوال": "Mobile",
    "اسم المقيم": "Resident's name", "اسم الأخصائي": "Specialist's name", "اسم الاستشاري": "Consultant's name",
    "التاريخ": "Date", "ملاحظة": "Note",
    "مناوبات يوم": "On call by day", "راجع، عدّل، أضف طبيب، أو احذف.": "Review, edit, add a doctor, or delete.",
    "اليوم": "Day", "اليوم السابق": "Previous day", "اليوم التالي": "Next day", "إضافة مناوب": "Add on-call doctor",
    "🖨️ تقرير المناوبين (طباعة / PDF)": "🖨️ On-call report (print / PDF)", "إضافة لهذا اليوم": "Add to this day",
    "ما فيه مناوبات مسجلة لهذا اليوم.": "No on-call rows for this day.", "ما قدرت أجيب الجدول.": "Couldn't load the roster.",
    "حفظ التعديل": "Save changes", "ما انحفظ، حاول مرة ثانية": "Not saved, try again",
    "النوع (يبدأ بـ «عيادة» = يظهر في العيادات فقط)": "Type (starting with «عيادة» = shown in clinics only)",
    "اضغط مرة ثانية للتأكيد": "Press again to confirm",
    "الأطباء المسموح لهم": "Doctors allowed to sign in",
    "الطبيب يدخل التطبيق برقمه الوظيفي وآخر 4 أرقام من جواله": "A doctor signs in with the employee number and the last 4 digits of the mobile",
    "🔓 التطبيق مفتوح بدون دخول": "🔓 The app is open without sign-in", "🔒 الدخول بالرقم الوظيفي مفعّل": "🔒 Employee-number sign-in is on",
    "أي أحد عنده الرابط يشوف المناوبين وأرقامهم.": "Anyone with the link sees the on-call doctors and their numbers.",
    "ما يشوف المناوبين إلا الأطباء اللي في القائمة تحت.": "Only the doctors in the list below can see the on-call board.",
    "فعّل الدخول بالرقم الوظيفي": "Turn on employee-number sign-in", "افتحه بدون دخول": "Open without sign-in",
    "نموذج قائمة الأطباء": "Doctors list template", "رفع قائمة": "Upload list", "بحث": "Search", "اسم أو رقم وظيفي": "Name or employee no.",
    "الرقم الوظيفي": "Employee no.", "آخر 4 أرقام من الجوال": "Last 4 digits of mobile", "رقم الجوال": "Mobile number",
    "ما فيه أطباء للحين. ارفع القائمة أو أضف طبيب.": "No doctors yet. Upload the list or add a doctor.",
    "ما قدرت أجيب القائمة.": "Couldn't load the list.", "مفعّل": "Active", "موقوف": "Stopped", "آخر دخول": "Last sign-in",
    "انضاف الطبيب، ويقدر يدخل الحين.": "Doctor added; they can sign in now.", "الرقم الوظيفي فاضي": "Employee no. is empty",
    "اكتب آخر 4 أرقام من الجوال.": "Enter the last 4 digits of the mobile.", "ما تغيّر. حاول مرة ثانية.": "Not changed. Try again.",
    "ما انحفظ. تأكد من البيانات وحاول مرة ثانية.": "Not saved. Check the data and try again.",
    "ما لقيت عمود «الرقم الوظيفي». استخدم النموذج.": "No “employee number” column found. Use the template.",
    "ما قدرت أقرأ الملف. تأكد إنه Excel أو CSV.": "Couldn't read the file. Make sure it's Excel or CSV.",
    "ما قدرت أقرأ الملف. تأكد إنه Excel أو CSV أو PDF.": "Couldn't read the file. Make sure it's Excel, CSV or PDF.",
    "ما قدرت أقرأ ملف Word. تأكد إنه .docx (مو .doc القديم).": "Couldn't read the Word file. It must be .docx (not the old .doc).",
    "ما قدرت أقرأ الـ PDF. تأكد إن النت شغال وحاول مرة ثانية.": "Couldn't read the PDF. Check the internet and try again.",
    "ما لقيت جدول داخل ملف Word. لازم الجدول يكون جدول Word (إدراج ← جدول)، مو مسافات.": "No table found in the Word file. It must be a Word table (Insert → Table).",
    "ما لقيت نص في الملف.": "No text found in the file.", "أجهّز قارئ الـ PDF…": "Preparing the PDF reader…",
    "ما لقيت عناوين الأعمدة. استخدم النموذج.": "Column headers not found. Use the template.",
    "الملف فاضي.": "The file is empty.", "اكتب اسم القسم فوق.": "Enter the department above.",
    "حدد عمود «التاريخ / اليوم».": "Choose the “Date / day” column.",
    "حدد عمود الاسم، أو أعمدة «اسم المقيم / الأخصائي / الاستشاري».": "Choose the name column, or the resident / specialist / consultant name columns.",
    "اكتب اسم القسم فوق، أو حدد عمود «القسم».": "Enter the department above, or choose the “Department” column.",
    "ما طلع ولا طبيب. تأكد من اختيار الأعمدة.": "No doctors found. Check the column choices.",
    "ما طلع ولا طبيب. جرّب «ربط الأعمدة يدوياً».": "No doctors found. Try “Map columns manually”.",
    "ما انحفظ الجدول. تأكد من النت وحاول مرة ثانية.": "The roster wasn't saved. Check the internet and try again.",
    "الرقم السري أو الإيميل غير صحيح. إذا ما اخترت رقماً سرياً بعد، ادخل برابط الإيميل أول.": "Wrong password or e-mail. If you haven't chosen a password yet, sign in with the e-mail link first.",
    "اكتب إيميلك أول، ثم اضغط الرابط مرة ثانية.": "Enter your e-mail first, then press the link again.",
    "هذا الإيميل غير مسجّل كمشرف، أو صار خطأ في الإرسال. تأكد من الإيميل وحاول مرة ثانية.": "This e-mail isn't an admin, or sending failed. Check the e-mail and try again.",
    "أرسلنا رابط دخول على إيميلك. افتحه من نفس الجهاز ونفس المتصفح، وبعدها اختر رقمك السري من زر «الرقم السري».": "We sent a sign-in link to your e-mail. Open it on this device and browser, then choose your password from the “Password” button.",
    "هذا الحساب ما عنده صلاحية مشرف.": "This account isn't an admin.",
    "الرقم السري لازم يكون ٨ خانات أو أكثر.": "The password must be 8 characters or more.", "الرقمين مو متطابقين.": "The two passwords don't match.",
    "✅ انحفظ الرقم السري. المرة الجاية ادخل به.": "✅ Password saved. Sign in with it next time.",
    "المتصفح منع فتح نافذة الطباعة. اسمح بالنوافذ المنبثقة لهذا الموقع.": "The browser blocked the print window. Allow pop-ups for this site.",
    "طوال اليوم": "All day", "بدون رقم جوال": "No mobile", "إضافة": "Add", "التحقق": "Check", "حذف": "Delete", "تعديل": "Edit", "الأشعة": "Radiology",
  };
  const RX = [
    [/^انحفظ (\d+) طبيب في (\d+) قسم\. الأطباء يشوفونه الحين\.$/, "Saved $1 doctors in $2 department(s). Doctors see it now."],
    [/^قرأت (\d+) سطر و(\d+) عمود من ملف Word\.$/, "Read $1 rows and $2 columns from the Word file."],
    [/^قرأت (\d+) صفحة، (\d+) سطر و(\d+) عمود(.*)\.$/, "Read $1 page(s), $2 rows and $3 columns$4."],
    [/^أقرأ الصفحة (\d+) من (\d+)…$/, "Reading page $1 of $2…"],
    [/^قرأت (\d+) طبيب\. راجع وبعدين احفظ\.$/, "Read $1 doctors. Review, then save."],
    [/^(\d+) سطر فيه مشكلة وما راح ينحفظ:$/, "$1 row(s) have a problem and won't be saved:"],
    [/^(\d+) طبيب$/, "$1 doctors"], [/^(\d+) سطر$/, "$1 rows"], [/^(\d+) يوم\)$/, "$1 days)"],
    [/^إضافة مناوب في (.+)$/, "Add on-call doctor in $1"],
    [/^و(\d+) سطر ثاني…$/, "…and $1 more rows"],
    [/^سطر (\d+): (.+)$/, "Row $1: $2"],
    [/^انضاف أو تحدّث (\d+) طبيب\.$/, "$1 doctors added or updated."],
    [/^بدون رقم جوال:$/, "No mobile number:"], [/^\. تقدر تضيفه بعد الحفظ من ✏️\.$/, ". You can add it after saving with ✏️."],
  ];
  const tr = t => {
    const k = t.trim(); if (!k || !/[؀-ۿ]/.test(k)) return null;
    if (EN[k]) return t.replace(k, EN[k]);
    for (const [re, to] of RX) if (re.test(k)) return t.replace(k, k.replace(re, to));
    return null;
  };
  let lang = "ar"; try { lang = localStorage.getItem("dh-admin-lang") || "ar"; } catch {}
  const q = new URLSearchParams(location.search).get("lang"); if (q === "en" || q === "ar") lang = q;
  const orig = new WeakMap();  // text node -> its Arabic text, so switching back restores it
  function walk(root){
    if (lang !== "en") return;
    const it = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n; (n = it.nextNode());) {
      const p = n.parentElement; if (!p || /^(SCRIPT|STYLE|TEXTAREA)$/.test(p.tagName) || p.closest("[data-noi18n]")) continue;
      const v = tr(n.nodeValue); if (v !== null) { orig.set(n, n.nodeValue); n.nodeValue = v; }
    }
    (root.querySelectorAll ? root : document).querySelectorAll("[placeholder],[title],[aria-label]").forEach(el => {
      for (const a of ["placeholder", "title", "aria-label"]) { const v = el.getAttribute(a); const t = v && tr(v);
        if (t) { el.dataset["ar_" + a.replace("-", "")] = v; el.setAttribute(a, t); } }
    });
  }
  const mo = new MutationObserver(ms => { if (lang !== "en") return; mo.disconnect();
    for (const m of ms) { if (m.type === "characterData") walk(m.target.parentElement || document.body); else m.addedNodes.forEach(x => x.nodeType === 1 ? walk(x) : x.nodeType === 3 && walk(x.parentElement || document.body)); }
    mo.observe(document.body, {childList: true, subtree: true, characterData: true}); });
  const _alert = window.alert.bind(window), _confirm = window.confirm.bind(window);
  window.alert = m => _alert(lang === "en" ? (tr(String(m)) || m) : m);
  window.confirm = m => _confirm(lang === "en" ? (tr(String(m)) || m) : m);
  function apply(){
    document.documentElement.lang = lang; document.documentElement.dir = lang === "en" ? "ltr" : "rtl";
    btn.textContent = lang === "en" ? "عربي" : "English";
    if (lang === "en") { walk(document.body); mo.observe(document.body, {childList: true, subtree: true, characterData: true}); }
  }
  const btn = document.createElement("button");
  btn.className = "btn ghost"; btn.type = "button"; btn.setAttribute("data-noi18n", ""); btn.id = "langBtn";
  btn.onclick = () => { try { localStorage.setItem("dh-admin-lang", lang === "en" ? "ar" : "en"); } catch {} location.reload(); };
  const place = () => { const h = document.querySelector("header .wrap") || document.querySelector("header"); if (h) h.insertBefore(btn, h.querySelector(".btn")); apply(); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", place); else place();
})();
