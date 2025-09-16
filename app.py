from __future__ import annotations
import os
import re
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html as html_component

# -------------------- إعداد الصفحة + إخفاء واجهة ستريملايت --------------------
st.set_page_config(page_title="Static HTML Viewer", layout="wide")

st.markdown("""
<style>
/* اخفاء عناصر ستريملايت الافتراضية */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
/* إزالة الهوامش نهائياً */
.block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
/* اخفاء الشريط الجانبي إن وُجد */
[data-testid="stSidebar"] {display: none;}
/* خلفية شفافة حتى تكون خلفية HTML هي الظاهرة */
.stApp {background: transparent;}
html, body {margin:0; padding:0;}
</style>
""", unsafe_allow_html=True)

# -------------------- تحديد مسارات الملفات --------------------
BASE_DIR = Path(__file__).resolve().parent  # أفضل طريقة لتحديد مجلد السكربت على أي منصة
# لو عندك مسار معروف مسبقاً سيبه هنا، وإلا سنكتشفه تلقائياً
PREFERRED_HTML_PATHS = [
    BASE_DIR / "assets" / "index.html",
    BASE_DIR / "index.html",
]

# السماح بتحديد الملف بالبيئة (مفيد على الكلاود)
env_html = os.environ.get("HTML_FILE")
if env_html:
    PREFERRED_HTML_PATHS.insert(0, Path(env_html))

# وظيفة صغيرة تبحث عن أول ملف HTML متاح لو المسارات الافتراضية مش موجودة
def find_first_html(root: Path) -> Path | None:
    # أولوية: أي index.html في أي مكان، ثم أي .html عام
    index_candidates = list(root.rglob("index.html"))
    if index_candidates:
        return index_candidates[0]
    all_html = list(root.rglob("*.html"))
    if all_html:
        return all_html[0]
    return None

html_path: Path | None = None
for p in PREFERRED_HTML_PATHS:
    if p.exists():
        html_path = p
        break

if html_path is None:
    html_path = find_first_html(BASE_DIR)

if html_path is None or not html_path.exists():
    st.error("⚠️ لم يتم العثور على أي ملف HTML داخل المشروع. "
             "أضف ملفًا مثل `assets/index.html` أو `index.html`، "
             "أو ضع اسم الملف في متغيّر البيئة `HTML_FILE`.")
    st.stop()

# -------------------- قراءة محتوى الـ HTML --------------------
page = html_path.read_text(encoding="utf-8")

# -------------------- ضبط <base href> لحل المسارات النسبية --------------------
# لو ملفك بيستورد CSS/JS/صور بمسارات نسبية، هنضبط base href تلقائياً.
# الافتراضي: اجعله نسبةً لمجلد الملف نفسه داخل التطبيق.
def ensure_base_href(html_text: str, base_url: str) -> str:
    if re.search(r"<base\\s+href=", html_text, flags=re.IGNORECASE):
        return html_text  # لو موجود سيبه
    if re.search(r"<head[^>]*>", html_text, flags=re.IGNORECASE):
        return re.sub(r"(<head[^>]*>)", rf"\\1\n<base href=\"{base_url}\">",
                      html_text, count=1, flags=re.IGNORECASE)
    # لو مفيش <head>، أضفه بسرعة
    return f"<head><base href=\"{base_url}\"></head>{html_text}"

# نبني base كنسبة لمجلد الملف، بحيث المسارات النسبية تشتغل داخل iframe
# مثال: لو html_path = /mount/src/16-9/assets/index.html -> base = file:///mount/src/16-9/assets/
base_for_relative = (html_path.parent.as_uri() + "/")
page = ensure_base_href(page, base_for_relative)

# -------------------- غلاف iframe فل-بليد + ضبط الارتفاع --------------------
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
    overflow: auto; /* سكرول واحد فقط داخل الإطار */
    border: none;
    margin: 0;
    padding: 0;
  }}
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

# -------------------- العرض --------------------
# ملاحظة: الارتفاع الأولي 800، وسنضبطه فوريًا عبر postMessage
html_component(FRAME_WRAPPER, height=800, scrolling=False)
