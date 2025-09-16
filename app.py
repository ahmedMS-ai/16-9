import streamlit as st
from streamlit.components.v1 import html as html_component

st.set_page_config(page_title="My HTML", layout="wide")

# إخفاء واجهة ستريم لايت + إزالة الهوامش
st.markdown("""
<style>
/* اخفاء القائمة والهيدر والفوتر */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* إزالة الحواف حول المحتوى */
.block-container {padding: 0 !important; margin: 0 !important;}

/* إزالة أي خلفية لتصبح الخلفية من الـ HTML نفسه */
.stApp {background: transparent;}
</style>
""", unsafe_allow_html=True)

# اقرأ ملف الـ HTML (المتكامل)
with open("index.html", "r", encoding="utf-8") as f:
    page = f.read()

# حقن الـ HTML كما هو داخل iframe بدون سكرول داخلي
# ملاحظة: height هنا سنضبطها لتملأ الشاشة ديناميكياً عبر سكريبت صغير
html_component(f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
/* اجعل الـ body يملأ النافذة تماماً */
html, body {{
  height: 100%;
  margin: 0;
}}
/* غلاف يملأ كامل الإطار */
.wrapper {{
  position: fixed;
  inset: 0;
  overflow: hidden;
  border: none;
  padding: 0;
  margin: 0;
}}
/* نحط صفحتك كما هي */
.content {{
  width: 100%;
  height: 100%;
}}
</style>
</head>
<body>
  <div class="wrapper">
    <!-- نعرض صفحتك مباشرة -->
    <div class="content">
      {page}
    </div>
  </div>
  <!-- ضبط ارتفاع مكون ستريم لايت ليملىء الشاشة -->
  <script>
    function setParentHeight() {{
      const h = window.innerHeight || document.documentElement.clientHeight;
      // Streamlit يحدد ارتفاع الـ iframe، نُبلغ الأب ليعدّله
      window.parent.postMessage({{ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: h }}, "*");
    }}
    setParentHeight();
    window.addEventListener("resize", setParentHeight);
  </script>
</body>
</html>
""", height=800, scrolling=False)
