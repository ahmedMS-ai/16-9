from __future__ import annotations
import os, re
from pathlib import Path
import streamlit as st
from streamlit.components.v1 import html as html_component

st.set_page_config(page_title="Static HTML Full-Bleed", layout="wide")

# إزالة واجهة ستريمليت والحواف
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
ENV_HTML = os.environ.get("HTML_FILE")

def find_first_html(root: Path) -> Path | None:
    for candidate in [root / "assets" / "index.html", root / "index.html"]:
        if candidate.exists():
            return candidate
    idx = list(root.rglob("index.html"))
    if idx: return idx[0]
    htmls = list(root.rglob("*.html"))
    return htmls[0] if htmls else None

html_path = Path(ENV_HTML) if ENV_HTML else find_first_html(BASE_DIR)
if not html_path or not html_path.exists():
    st.error("⚠️ لم يتم العثور على أي ملف HTML. ضع `assets/index.html` أو `index.html` أو عرّف `HTML_FILE`.")
    st.stop()

page = html_path.read_text(encoding="utf-8")

# 1) إزالة أي <base ...> لتجنّب كسر الروابط الداخلية (#)
page = re.sub(r"<base\\b[^>]*>", "", page, flags=re.IGNORECASE)

# 2) إعادة كتابة مسارات الأصول النسبية فقط (src/href) بدون التأثير على الروابط الداخلية
#    - لا نلمس: http(s):, #, mailto:, tel:, data:
RAW_BASE = os.environ.get(
    "RAW_REPO_BASE",
    "https://raw.githubusercontent.com/ahmedMS-ai/16-9/main/"
).rstrip("/") + "/"

# احسب المسار النسبي داخل الريبو بالنسبة لمكان ملف HTML
rel_dir_in_repo = ""
try:
    rel_dir_in_repo = html_path.relative_to(BASE_DIR).parent.as_posix().strip("/")
except Exception:
    pass
if rel_dir_in_repo:
    RAW_BASE = f"{RAW_BASE}{rel_dir_in_repo}/"

def rewrite_asset_urls(html_text: str, raw_base: str) -> str:
    def repl(m):
        attr, quote, url = m.group(1), m.group(2), m.group(3).strip()
        low = url.lower()
        if low.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:")):
            return m.group(0)
        # أمثلة نسبية: ./img.png , css/style.css , index.html (لو ملف فرعي)
        # نخليها مطلقة على RAW_BASE حتى لا يحصل تنقّل خارج الإطار
        new_url = raw_base + url.lstrip("./")
        return f'{attr}={quote}{new_url}{quote}'
    return re.sub(r'(\\s)(src|href)\\s*=\\s*(["\\\'])(.*?)\\3',
                  lambda m: m.group(1) + repl(m), html_text, flags=re.IGNORECASE)

page = rewrite_asset_urls(page, RAW_BASE)

# 3) غلاف فل-بليد + تفعيل الروابط الداخلية بأي صيغة (#id أو index.html#id)
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
    scroll-behavior: smooth;        /* سكرول ناعم */
    scroll-padding-top: 80px;       /* اضبطها حسب ارتفاع الهيدر داخل صفحتك */
  }}
  [id] {{ scroll-margin-top: 80px; }} /* لتفادي تغطية الهيدر للعنصر الهدف */
</style>
</head>
<body>
  <div class="wrapper" id="wrapper">
    {page}
  </div>

  <script>
    // اضبط ارتفاع iframe
    function setParentHeight(){{
      const h = window.innerHeight || document.documentElement.clientHeight;
      window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }}, "*");
    }}
    setParentHeight();
    window.addEventListener("resize", setParentHeight);

    // مساعد: هل الرابط داخلي لنفس الصفحة؟
    function isSameDocLink(href) {{
      if (!href) return false;
      const l = href.toLowerCase();
      if (l.startsWith("#")) return true;
      // صيغ مثل: index.html#section أو ./index.html#section
      if (l.endsWith(".html") || l.includes(".html#")) {{
        // لو بيشير لنفس الملف، اعتبره داخلي
        try {{
          const a = document.createElement('a'); a.href = href;
          // في srcdoc، pathname بيكون فارغ؛ نستخدم فقط وجود hash
          return !!a.hash;
        }} catch(e){{}}
      }}
      return false;
    }}

    // فعّل التنقّل الداخلي بالسكرول بدل تغيير الصفحة
    document.addEventListener('click', function(e) {{
      const a = e.target.closest('a');
      if (!a) return;

      const href = a.getAttribute('href');
      if (!isSameDocLink(href)) return;

      // امنع التنقل الافتراضي (الذي يسبب شاشة بيضاء أحياناً)
      e.preventDefault();

      // استخرج الـ id الهدف من الهاش
      let hash = '';
      if (href.startsWith('#')) {{
        hash = href;
      }} else {{
        // مثل index.html#about -> #about
        const idx = href.indexOf('#');
        hash = idx >= 0 ? href.slice(idx) : '';
      }}
      const id = decodeURIComponent(hash.replace('#',''));
      if (!id) return;

      const target = document.getElementById(id);
      if (target) {{
        target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        // اختياري: حدث الهاش داخل الإطار
        if (history && history.pushState) {{
          history.pushState(null, "", "#" + id);
        }}
      }}
    }}, true);
  </script>
</body>
</html>
"""

html_component(FRAME, height=800, scrolling=False)
