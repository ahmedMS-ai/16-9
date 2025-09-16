# app.py
# — عرض صفحة HTML "كما هي" على Streamlit بدون حواف + دعم الأصول النسبية عبر <base href> —
# يعمل مع ريبو: github.com/ahmedMS-ai/16-9  (تمت مراجعته)
# لو نقلت المشروع لمكان آخر، عدّل RAW_REPO_BASE تحت.

from __future__ import annotations
from pathlib import Path
import re
import os
import streamlit as st
from streamlit.components.v1 import html as html_component

# =============== إعدادات أساسية ===============
st.set_page_config(page_title="HTML Full-Bleed", layout="wide")

# إخفاء واجهة ستريم لايت بالكامل + إزالة كل الهوامش
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
/* إزالة هوامش حاوية المحتوى */
.block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
/* خلي الخلفية شفافة عشان HTML بتاعك يتحكم */
.stApp {background: transparent;}
/* إخفاء الشريط الجانبي لو موجود */
[data-testid="stSidebar"] {display: none;}
html, body {margin:0; padding:0;}
</style>
""", unsafe_allow_html=True)

# =============== إعدادات المسارات ===============
BASE_DIR = Path(__file__).resolve().parent

# ضع مسار ملف الـ HTML بالنسبة لمجلد المشروع:
# لو ملفك في الجذر باسم index.html، غيّرها لـ "index.html"
# أنا مفترض انه عندك داخل assets/ بناءً على هيكل الريبو الحالي.
HTML_RELATIVE_PATH = Path("assets/index.html")

# قاعدة الروابط لأصول الريبو على GitHub Raw:
# لو غيرت اسم المستخدم/الريبو/الفرع، عدّل السطر ده.
RAW_REPO_BASE = "https://raw.githubusercontent.com/ahmedMS-ai/16-9/main/"

# تقدر تخلّيها متغيرة من البيئة لو بتنشر فوركات:
RAW_REPO_BASE = os.environ.get("RAW_REPO_BASE", RAW_REPO_BASE).rstrip("/") + "/"

# =============== قراءة ملف الـ HTML ===============
html_path = (BASE_DIR / HTML_RELATIVE_PATH)
if not html_path.exists():
    # كخطة بديلة: لو فيه index.html في الجذر
    fallback = BASE_DIR / "index.html"
    if fallback.exists():
        html_path = fallback
    else:
        st.error(f"لم يتم العثور على ملف HTML عند: {HTML_RELATIVE_PATH} ولا في الجذر.")
        st.stop()

page = html_path.read_text(encoding="utf-8")

# =============== حقن <base href> للأصول النسبية ===============
# الهدف: لو الـ HTML بيشير لمسارات نسبية (css/ img/ js/ ...)، نخليها تتحلّ عبر GitHub Raw
# بنحدد المجلد النسبي داخل الريبو (مثلاً 'assets/' أو الجذر '').
relative_folder_inside_repo = ""
try:
    # استنتج المسار داخل الريبو بالنسبة لمجلد المشروع:
    # مثال: لو الملف assets/index.html -> relative_folder_inside_repo = 'assets/'
    rel = html_path.relative_to(BASE_DIR).parent.as_posix()
    relative_folder_inside_repo = (rel + "/") if rel not in ("", ".") else ""
except Exception:
    relative_folder_inside_repo = ""

base_href = RAW_REPO_BASE + relative_folder_inside_repo  # مثال: https://raw.../main/assets/

# سنضيف <base href="..."> داخل <head> لو مش موجود
def inject_base_href(html_text: str, href: str) -> str:
    # لو فيه <base> بالفعل، نسيبه زي ما هو
    if re.search(r"<base\\s+href=", html_text, flags=re.IGNORECASE):
        return html_text
    # نحاول ندخل بعد <head> مباشرة
    if re.search(r"<head[^>]*>", html_text, flags=re.IGNORECASE):
        return re.sub(r"(<head[^>]*>)", rf"\\1\n<base href=\"{href}\">", html_text, count=1, flags=re.IGNORECASE)
    # لو مفيش <head>، نضيفه يدوياً
    return f"<head><base href=\"{href}\"></head>{html_text}"

page = inject_base_href(page, base_href)

# =============== ضمان فل-بليد داخل الـ iframe ===============
# - نضمن أن html, body بلا هوامش/حشوات
# - نضبط ارتفاع الإطار ليملأ الشاشة، ويتحدّث مع تغيير المقاس
FRAME_WRAPPER = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html, body {{
  height: 100%;
  margin: 0;
  padding: 0;
}}
.wrapper {{
  position: fixed;
  inset: 0;
  overflow: auto; /* لو صفحتك طويلة، نخلي سكرول واحد فقط */
  border: none;
  margin: 0;
  padding: 0;
}}
/* اختياري: منع سكرولينج مزدوج */
</style>
</head>
<body>
  <div class="wrapper">
    {page}
  </div>
  <script>
    function setParentHeight() {{
      const h = window.innerHeight || document.documentElement.clientHeight;
      window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }}, "*");
    }}
    setParentHeight();
    window.addEventListener("resize", setParentHeight);
  </script>
</body>
</html>
"""

# =============== العرض ===============
# ملاحظة: scrolling=False يمنع سكرول مزدوج في بعض الحالات،
# لكن بما إننا عملنا overflow:auto في .wrapper، نترك scrolling=False.
html_component(FRAME_WRAPPER, height=800, scrolling=False)
