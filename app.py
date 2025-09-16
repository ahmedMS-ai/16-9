from __future__ import annotations
import os, re
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html as html_component

st.set_page_config(page_title="Static HTML Viewer", layout="wide")

# إزالة واجهة ستريملايت والحواف بالكامل
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
[data-testid="stSidebar"] {display: none;}
.stApp {background: transparent;}
html, body {margin:0; padding:0;}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
# اسم ملف HTML من متغير بيئة (اختياري)
env_html = os.environ.get("HTML_FILE")

# مسارات مفضلة ثم اكتشاف تلقائي
candidates = []
if env_html:
    candidates.append(Path(env_html))
candidates += [BASE_DIR / "assets" / "index.html", BASE_DIR / "index.html"]

def find_first_html(root: Path) -> Path | None:
    idx = list(root.rglob("index.html"))
    if idx: return idx[0]
    any_html = list(root.rglob("*.html"))
    return any_html[0] if any_html else None

html_path = next((p for p in candidates if p.exists()), None) or find_first_html(BASE_DIR)
if not html_path or not html_path.exists():
    st.error("⚠️ لم يتم العثور على أي ملف HTML داخل المشروع. أضف `assets/index.html` أو `index.html` أو عرّف `HTML_FILE`.")
    st.stop()

page = html_path.read_text(encoding="utf-8")

# ---------- إعادة كتابة مسارات الأصول فقط (بدون كسر الروابط الداخلية #) ----------
# عدّل RAW_BASE لو ريبوك/الفرع مختلفين
RAW_BASE = os.environ.get("RAW_REPO_BASE", "https://raw.githubusercontent.com/ahmedMS-ai/16-9/main/").rstrip("/") + "/"
# المسار داخل الريبو بالنسبة لملف HTML
rel_dir_in_repo = ""
try:
    rel_dir_in_repo = html_path.relative_to(BASE_DIR).parent.as_posix().strip("/")
except Exception:
    pass
if rel_dir_in_repo:
    RAW_BASE = f"{RAW_BASE}{rel_dir_in_repo}/"

def rewrite_urls(html_text: str, raw_base: str) -> str:
    # استبدل src/href النسبية فقط (لا تبدأ بـ http, https, #, mailto, tel, data:)
    def repl_attr(match):
        attr = match.group(1)    # src أو href
        quote = match.group(2)   # ' أو "
        url = match.group(3).strip()

        lowered = url.lower()
        if lowered.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:")):
            return match.group(0)  # اتركه كما هو

        # اجعلها مطلقة على RAW_BASE
        new_url = raw_base + url.lstrip("./")
        return f'{attr}={quote}{new_url}{quote}'

    pattern = r'(?:\s)(src|href)\s*=\s*(["\'])(.*?)\2'
    return re.sub(pattern, repl_attr, html_text, flags=re.IGNORECASE)

page = rewrite_urls(page, RAW_BASE)

# ---------- غلاف يعرض الصفحة فل-بليد + تفعيل الروابط الداخلية ----------
FRAME = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    height: 100%;
    margin: 0; padding: 0;
  }}
  .wrapper {{
    position: fixed; inset: 0;
    overflow: auto;                 /* سكرول واحد داخل الإطار */
    margin: 0; padding: 0; border: 0;
    scroll-behavior: smooth;        /* سكرول ناعم للهاش */
  }}
  /* لو عندك هيدر ثابت داخل الصفحة، اضبط المسافة هنا */
  .wrapper {{ scroll-padding-top: 80px; }}  /* عدّل 80px حسب ارتفاع الهيدر عندك */
  /* بدلاً من ذلك يمكن استخدام scroll-margin-top على كل قسم هدف */
  [id] {{ scroll-margin-top: 80px; }}
</style>
</head>
<body>
  <div class="wrapper" id="wrapper">
    {page}
  </div>

  <script>
    // اضبط ارتفاع iframe ليملىء الشاشة
    function setParentHeight(){{
      const h = window.innerHeight || document.documentElement.clientHeight;
      window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }}, "*");
    }}
    setParentHeight();
    window.addEventListener("resize", setParentHeight);

    // فعّل الروابط الداخلية داخل نفس الوثيقة حتى لو فيه base أو إعادة كتابة
    const wrapper = document.getElementById('wrapper');
    document.querySelectorAll('a[href^="#"]').forEach(function(a){{
      a.addEventListener('click', function(e){{
        const hash = this.getAttribute('href');
        const targetId = decodeURIComponent(hash.slice(1));
        const target = document.getElementById(targetId);
        if (target) {{
          e.preventDefault();
          target.scrollIntoView({{behavior:'smooth', block:'start'}});
          // حدّث الهاش في شريط العنوان داخل الإطار (اختياري)
          if (history && history.pushState) {{
            history.pushState(null, "", hash);
          }}
        }}
      }});
    }});
  </script>
</body>
</html>
"""

html_component(FRAME, height=800, scrolling=False)
