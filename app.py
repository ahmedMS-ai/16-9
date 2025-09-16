import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="محمد نبيل — مرشح مجلس النواب", page_icon="🗳️", layout="wide")

# روابط أصولك (بدّلها بروابط GitHub raw أو من assets/)
HERO_IMG = "assets/hero.png"  # بدّل للصورة المناسبة
LOGO_IMG = "assets/logo.png"  # اختياري

# نصوص أساسية (محدّثة)
TITLE = "محمد نبيل"
SUBTITLE = "مرشح مجلس النواب"
TAGLINE = "معًا نبني غدًا أفضل للشباب والأهالي"
MEDICAL_CAMPS = 3
LAST_CAMP = "الثلاثاء 16 سبتمبر 2025"
HASHTAG = "#الشباب_يقدر"

# HTML/CSS/JS — هيرو + حركات + أقسام بسيطة
page = f"""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Amiri:wght@700&display=swap" rel="stylesheet">
<style>
  :root {{
    --primary:#2563eb; /* أزرق */
    --accent:#059669;  /* أخضر */
    --yellow:#fbbf24;  /* أصفر */
    --bg1:#0b1220;     /* خلفية داكنة */
    --bg2:#0f172a;
    --text:#ffffff;
  }}
  html,body {{
    margin:0; padding:0; background: var(--bg1); color: var(--text);
    font-family: 'Cairo', system-ui, -apple-system, Segoe UI, Roboto, 'Helvetica Neue', Arial, sans-serif;
    direction: rtl;
  }}
  .container {{ max-width:1200px; margin:0 auto; padding: 24px; }}
  .hero {{
    position:relative; overflow:hidden; border-radius: 18px;
    background:
      radial-gradient(circle at 10% 10%, rgba(255,255,255,0.06), transparent 30%),
      radial-gradient(circle at 90% 20%, rgba(255,255,255,0.05), transparent 35%),
      linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #059669 100%);
    padding: 48px 28px; min-height: 70vh;
  }}
  .hero::after {{
    /* overlay لتغميق النص */
    content:""; position:absolute; inset:0;
    background: linear-gradient(90deg, rgba(0,0,0,0.35), rgba(0,0,0,0.15), rgba(0,0,0,0.35));
    pointer-events:none;
  }}
  .hero-inner {{ position:relative; display:flex; gap:32px; align-items:center; justify-content:space-between; z-index:2; }}
  .title {{ font-size: clamp(28px, 5vw, 54px); font-weight:900; line-height:1.1; text-shadow: 0 6px 22px rgba(0,0,0,0.35); }}
  .subtitle {{ font-size: clamp(18px, 2.2vw, 28px); color: #e2e8f0; margin-top: 8px; }}
  .badge {{
    display:inline-block; padding:10px 14px; border-radius:999px;
    background: rgba(255,255,255,0.08); backdrop-filter: blur(6px);
    color:#fff; border:1px solid rgba(255,255,255,0.15); font-weight:700; margin-bottom:14px;
  }}
  .stats {{
    display:flex; gap:18px; flex-wrap:wrap; margin-top:18px;
  }}
  .stat {{
    background: rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.12);
    padding:12px 16px; border-radius:12px; font-weight:700;
  }}
  .cta {{
    display:inline-block; margin-top:22px; padding:12px 18px; border-radius:12px;
    background: var(--primary); color:white; text-decoration:none; font-weight:800;
    box-shadow: 0 10px 30px rgba(37,99,235,0.35);
    transition: transform .2s ease, box-shadow .2s ease;
  }}
  .cta:hover {{ transform: translateY(-2px); box-shadow: 0 16px 38px rgba(37,99,235,0.45); }}

  .hero-media {{
    position:relative; width: 44%; min-width:320px;
    border-radius:18px; overflow:hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.35);
    transform: translateZ(0);
  }}
  .hero-media img {{ width:100%; display:block; }}
  .float-icon {{
    position:absolute; width:84px; opacity:.28; animation: floaty 8s ease-in-out infinite;
    filter: drop-shadow(0 10px 30px rgba(0,0,0,0.2));
  }}
  .float-icon.i1 {{ left: -18px; top: -18px; animation-duration: 9s; }}
  .float-icon.i2 {{ right: -12px; bottom: -12px; animation-duration: 7s; }}
  @keyframes floaty {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-16px) rotate(8deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
  }}

  /* أقسام لاحقة */
  section {{ padding:56px 0; }}
  .cards {{ display:grid; grid-template-columns: repeat(3, 1fr); gap:18px; }}
  .card {{
    background: var(--bg2); border:1px solid rgba(255,255,255,0.08);
    border-radius:16px; padding:18px; transition: transform .2s ease, box-shadow .2s ease;
  }}
  .card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 50px rgba(0,0,0,0.35); }}

  /* reveal بسيط عند scroll */
  .reveal {{ opacity:0; transform: translateY(18px); transition: all .7s ease; }}
  .reveal.visible {{ opacity:1; transform: none; }}

  /* سلايدر بسيط بالـ CSS (يمكنك لاحقًا استبداله بـ Swiper.js) */
  .slider {{ position:relative; overflow:hidden; border-radius:16px; }}
  .slides {{ display:flex; width:300%; animation: slide 18s infinite; }}
  .slide {{ width:100%; padding:28px; background: rgba(255,255,255,0.03); }}
  @keyframes slide {{
    0%, 28% {{ transform: translateX(0%); }}
    33%, 61% {{ transform: translateX(-100%); }}
    66%, 94% {{ transform: translateX(-200%); }}
    100% {{ transform: translateX(0%); }}
  }}

  @media (max-width: 980px) {{
    .hero-inner {{ flex-direction:column; }}
    .hero-media {{ width:100%; }}
    .cards {{ grid-template-columns: 1fr; }}
  }}
</style>

<div class="container">
  <header style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
    <div style="display:flex; align-items:center; gap:10px;">
      <img src="{LOGO_IMG}" alt="logo" style="height:44px; border-radius:8px;" onerror="this.style.display='none'"/>
      <strong>{HASHTAG}</strong>
    </div>
  </header>

  <section class="hero">
    <div class="hero-inner">
      <div style="position:relative; z-index:2; max-width: 54%;">
        <span class="badge">{SUBTITLE}</span>
        <h1 class="title">{TITLE}</h1>
        <div class="subtitle">{TAGLINE}</div>
        <div class="stats">
          <div class="stat">القوافل الطبية: {MEDICAL_CAMPS}</div>
          <div class="stat">آخر قافلة: {LAST_CAMP}</div>
        </div>
        <a class="cta" href="#about">تعرف أكثر</a>
      </div>

      <div class="hero-media">
        <img src="{HERO_IMG}" alt="محمد نبيل"/>
        <img class="float-icon i1" src="{LOGO_IMG}" alt="" onerror="this.style.display='none'"/>
        <img class="float-icon i2" src="{LOGO_IMG}" alt="" onerror="this.style.display='none'"/>
      </div>
    </div>
  </section>

  <section id="about">
    <h2 style="margin-bottom:12px;">أهدافنا</h2>
    <div class="cards">
      <div class="card reveal"><h3>تمكين الشباب</h3><p>برامج تدريبية، فرص عمل، ومسارات ريادة أعمال.</p></div>
      <div class="card reveal"><h3>الخدمات الصحية</h3><p>استمرار القوافل الطبية ودعم الوحدات الصحية.</p></div>
      <div class="card reveal"><h3>خدمة المجتمع</h3><p>مبادرات نظافة وتشجير ودعم مدارس وأنشطة ثقافية.</p></div>
    </div>
  </section>

  <section>
    <h2 style="margin-bottom:12px;">قالوا عنّا</h2>
    <div class="slider">
      <div class="slides">
        <div class="slide">💬 “مبادرات ملموسة على الأرض وتواصل محترم مع الأهالي.”</div>
        <div class="slide">💬 “القوافل الطبية الأخيرة كانت منظمة ومفيدة جدًا.”</div>
        <div class="slide">💬 “فريق عمل نشط ووعود تتحقق بخطوات واضحة.”</div>
      </div>
    </div>
  </section>

  <footer style="opacity:.7; font-size:14px; padding: 8px 0 16px;">
    &copy; {TITLE} — {SUBTITLE}
  </footer>
</div>

<script>
  // reveal on scroll
  const reveals = () => {{
    document.querySelectorAll('.reveal').forEach(el => {{
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 80) el.classList.add('visible');
    }});
  }};
  document.addEventListener('scroll', reveals);
  window.addEventListener('load', reveals);
</script>
"""

html(page, height=1100, scrolling=True)
