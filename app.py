import streamlit as st
from streamlit.components.v1 import html

# 1) صفحة عريضة + أول سطر (حسب الدوك)
st.set_page_config(page_title="محمد نبيل — مرشح مجلس النواب", page_icon="🗳️", layout="wide")

# 2) تنظيف حواف واجهة ستريمليت + تكبير عرض الحاوية
st.markdown("""
<style>
/* إخفاء القائمة والفوتر لإحساس لاندينج أنظف */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* تضييق الحواف الرأسية وتوسيع عرض المحتوى */
.appview-container .main .block-container{
  padding-top: 0.8rem;
  padding-bottom: 0.8rem;
  max-width: 1400px;
}

/* RTL عام */
html, body { direction: rtl; }
</style>
""", unsafe_allow_html=True)

# --------- محتوى قابل للتعديل سريعًا ---------
TITLE = "محمد نبيل"
SUBTITLE = "مرشح مجلس النواب"
TAGLINE = "معًا نبني غدًا أفضل للشباب والأهالي"
MEDICAL_CAMPS = 3
LAST_CAMP = "الثلاثاء 16 سبتمبر 2025"
HASHTAG = "#الشباب_يقدر"

HERO_IMG = "assets/hero.jpg"  # بدّل حسب صورتك
LOGO_IMG = "assets/logo.png"  # اختياري

# 3) هيرو Full-viewport بدون iframe (سكروول واحد فقط للصفحة)
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri:wght@700&display=swap" rel="stylesheet">
<style>
:root {{
  --primary:#2563eb; --accent:#059669; --yellow:#fbbf24;
  --bg1:#0b1220; --bg2:#0f172a; --text:#fff;
}}
* {{ box-sizing: border-box; }}
body {{ background:var(--bg1); color:var(--text); font-family:'Cairo', system-ui; }}

.hero {{
  position:relative; overflow:hidden; width:100%;
  background:
    radial-gradient(circle at 10% 10%, rgba(255,255,255,0.07), transparent 30%),
    radial-gradient(circle at 90% 20%, rgba(255,255,255,0.05), transparent 35%),
    linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #059669 100%);
  border-radius: 22px;
  min-height: 90vh;
  display:flex; align-items:center;
}}
.hero::after {{
  content:""; position:absolute; inset:0;
  background: linear-gradient(90deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15), rgba(0,0,0,0.35));
}}
.hero-inner {{
  position:relative; z-index:1;
  display:flex; gap:36px; align-items:center; justify-content:space-between;
  width:100%; padding: 40px 36px;
}}
.badge {{
  display:inline-block; padding:8px 14px; border-radius:999px;
  background: rgba(255,255,255,0.10); border:1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(6px); font-weight:800;
}}
.title {{ font-size:clamp(28px, 5.2vw, 56px); font-weight:900; line-height:1.1; text-shadow:0 8px 26px rgba(0,0,0,0.35); }}
.subtitle {{ font-size:clamp(18px, 2vw, 26px); color:#e2e8f0; margin-top:8px; }}
.stats {{ display:flex; gap:14px; flex-wrap:wrap; margin-top:16px; }}
.stat {{
  background: rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.12);
  padding:10px 14px; border-radius:12px; font-weight:700;
}}
.cta {{
  display:inline-block; margin-top:20px; padding:12px 18px; border-radius:12px;
  background: var(--primary); color:white; text-decoration:none; font-weight:800;
  box-shadow: 0 14px 34px rgba(37,99,235,0.38);
  transition: transform .18s ease, box-shadow .18s ease;
}}
.cta:hover {{ transform: translateY(-2px); box-shadow: 0 18px 44px rgba(37,99,235,0.48); }}
.hero-media {{
  position:relative; width:min(44%, 520px); min-width:280px;
  border-radius:18px; overflow:hidden; box-shadow:0 26px 60px rgba(0,0,0,0.35);
}}
.hero-media img {{ width:100%; display:block; }}
.float-icon {{
  position:absolute; width:80px; opacity:.28; animation: floaty 8s ease-in-out infinite;
  filter: drop-shadow(0 10px 30px rgba(0,0,0,0.2));
}}
.float-icon.i1 {{ left:-10px; top:-10px; animation-duration:9s; }}
.float-icon.i2 {{ right:-12px; bottom:-12px; animation-duration:7s; }}
@keyframes floaty {{
  0% {{ transform: translateY(0px) rotate(0deg); }}
  50% {{ transform: translateY(-16px) rotate(8deg); }}
  100% {{ transform: translateY(0px) rotate(0deg); }}
}}

.section {{ padding: 60px 8px; }}
.kpis {{
  display:grid; grid-template-columns: repeat(4, 1fr); gap:16px;
}}
.kpi {{
  background: var(--bg2); border:1px solid rgba(255,255,255,0.08);
  border-radius:14px; padding:16px; text-align:center;
}}
.kpi strong {{ display:block; font-size:28px; }}
.cards {{
  display:grid; grid-template-columns: repeat(3, 1fr); gap:18px;
}}
.card {{
  background: var(--bg2); border:1px solid rgba(255,255,255,0.08);
  border-radius:16px; padding:18px; transition: transform .18s ease, box-shadow .18s ease;
}}
.card:hover {{ transform: translateY(-6px); box-shadow: 0 18px 46px rgba(0,0,0,0.35); }}
.timeline {{ display:grid; gap:14px; }}
.step {{
  background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
  border-radius:12px; padding:14px 16px;
}}
.footer {{ opacity:.75; font-size:14px; padding: 14px 0 28px; text-align:center; }}

@media (max-width: 1080px) {{
  .hero-inner {{ flex-direction:column; text-align:right; }}
  .hero-media {{ width:100%; }}
  .kpis {{ grid-template-columns: repeat(2, 1fr); }}
  .cards {{ grid-template-columns: 1fr; }}
}}
</style>

<div class="hero">
  <div class="hero-inner">
    <div style="max-width: 640px;">
      <span class="badge">{SUBTITLE}</span>
      <h1 class="title">{TITLE}</h1>
      <div class="subtitle">{TAGLINE}</div>
      <div class="stats">
        <div class="stat">القوافل الطبية: {MEDICAL_CAMPS}</div>
        <div class="stat">آخر قافلة: {LAST_CAMP}</div>
        <div class="stat">{HASHTAG}</div>
      </div>
      <a class="cta" href="#about">تعرف أكثر</a>
    </div>
    <div class="hero-media">
      <img src="{HERO_IMG}" alt="محمد نبيل"/>
      <img class="float-icon i1" src="{LOGO_IMG}" alt="" onerror="this.style.display='none'"/>
      <img class="float-icon i2" src="{LOGO_IMG}" alt="" onerror="this.style.display='none'"/>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# 4) شريط KPIs
st.markdown(f"""
<div class="section">
  <div class="kpis">
    <div class="kpi"><strong>{MEDICAL_CAMPS}</strong>قوافل طبية</div>
    <div class="kpi"><strong>+25</strong>فرصة تدريب/عمل للشباب</div>
    <div class="kpi"><strong>+12</strong>مبادرة مجتمعية</div>
    <div class="kpi"><strong>+8</strong>شراكات محلية</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 5) أقسام الميزات
st.markdown("""
<div id="about" class="section">
  <h2 style="margin-bottom: 10px;">أولوياتنا</h2>
  <div class="cards">
    <div class="card"><h3>تمكين الشباب</h3><p>مسارات تدريب وتوظيف، دعم رواد الأعمال، وتمويل صغير.</p></div>
    <div class="card"><h3>الخدمات الصحية</h3><p>استمرار القوافل الطبية وتطوير وحدات الرعاية الأولية.</p></div>
    <div class="card"><h3>خدمة المجتمع</h3><p>تشجير، نظافة، دعم المدارس والأنشطة الثقافية والرياضية.</p></div>
  </div>
</div>
""", unsafe_allow_html=True)

# 6) تايملاين مختصر
st.markdown(f"""
<div class="section">
  <h2 style="margin-bottom: 10px;">خطوات على الأرض</h2>
  <div class="timeline">
    <div class="step">✅ إطلاق {MEDICAL_CAMPS} قوافل طبية — آخرها {LAST_CAMP}.</div>
    <div class="step">✅ لقاءات دورية مع الأهالي لسماع المقترحات وتحديد الأولويات.</div>
    <div class="step">🛠️ قادمًا: توسعة القوافل وخدمات لذوي الهمم والشباب.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 7) سلايدر شهادات (Swiper) — داخل iframe صغير بدون سكروول داخلي
swiper_html = """
<link rel="stylesheet" href="https://unpkg.com/swiper@9/swiper-bundle.min.css"/>
<div class="swiper" style="width:100%;max-width:1200px;">
  <div class="swiper-wrapper">
    <div class="swiper-slide" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px;">💬 “مبادرات ملموسة على الأرض وتواصل محترم مع الأهالي.”</div>
    <div class="swiper-slide" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px;">💬 “القوافل الطبية الأخيرة كانت منظمة ومفيدة جدًا.”</div>
    <div class="swiper-slide" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:18px;">💬 “فريق عمل نشط ووعود تتحقق بخطوات واضحة.”</div>
  </div>
  <div class="swiper-pagination"></div>
</div>
<script src="https://unpkg.com/swiper@9/swiper-bundle.min.js"></script>
<script>
const s = new Swiper('.swiper', {{
  loop: true,
  autoplay: {{ delay: 4000, disableOnInteraction: false }},
  pagination: {{ el: '.swiper-pagination', clickable: true }},
}});
</script>
"""
st.markdown('<div class="section"><h2 style="margin-bottom:10px;">قالوا عنّا</h2></div>', unsafe_allow_html=True)
# scrolling=False لتجنّب سكروول داخل الإطار (الدوك توضح السلوك)
html(swiper_html, height=240, scrolling=False)  # ← سكروول داخلي معطّل وفق الدوك

# 8) CTA + فوتر
st.markdown(f"""
<div class="section" style="text-align:center;">
  <a class="cta" href="#about">انضم وادعم {TITLE}</a>
</div>
<div class="footer">&copy; {TITLE} — {SUBTITLE}</div>
""", unsafe_allow_html=True)
