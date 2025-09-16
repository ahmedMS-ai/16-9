# app.py
import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide", page_title="كيفية تحميل نموذج برنامج انتخابي لإنشاء صفحة هبوط", page_icon="📄", initial_sidebar_state="collapsed")

# Load CSS and hide Streamlit chrome
st.markdown('<link rel="stylesheet" href="/static/css/theme.css">', unsafe_allow_html=True)

# Smooth scroll + header offset + anchor handling
st.markdown(
    """
    <script>
    window.addEventListener('load', () => {
      const header = document.querySelector('.site-header');
      const headerH = header ? header.offsetHeight : 0;
      document.documentElement.style.scrollPaddingTop = (headerH + 12) + 'px';
      // Smooth internal anchor navigation
      document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', (e) => {
          const id = a.getAttribute('href').slice(1);
          const el = document.getElementById(id);
          if (el) {
            e.preventDefault();
            el.scrollIntoView({behavior: 'smooth', block:'start'});
            history.replaceState(null, '', '#' + id);
          }
        });
      });
    });
    </script>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Rebuilt", "Original"])

with tab1:
    st.markdown(f"""
    <header class="site-header">
      <div class="nav-inner">
        <div class="brand">16-9 • Rebuilt</div>
        <nav class="nav">
          <a href="#hero">الرئيسية</a>
          <a href="#about">عن النموذج</a>
          <a href="#features">المزايا</a>
          <a href="#gallery">الصور</a>
          <a href="#contact">تواصل</a>
        </nav>
      </div>
    </header>

    <main id="hero" class="hero">
      <div class="hero-bg"></div>
      <div class="inner">
        <h1>كيفية تحميل نموذج برنامج انتخابي لإنشاء صفحة هبوط</h1>
        <p>إعادة بناء كاملة للتصميم داخل Streamlit بأسلوب بكسل-مثالي مع تمرير سلس وروابط مراسي.</p>
        <div class="cta-wrap">
          <a class="btn primary" href="#features">اكتشف المزايا</a>
          <a class="btn" href="#contact">تواصل معنا</a>
        </div>
        <div class="hero-image">
          
        </div>
      </div>
    </main>

    <section id="about" class="section">
      <div class="wrap">
        <h2>عن الصفحة</h2>
        <p class="lead">تمت إعادة بناء التخطيط (رأس، بطل، مزايا، معرض، تذييل) باستخدام HTML/CSS نظيفين داخل Streamlit،
        مع تقديم الأصول من مجلد <code>static/</code> وخيارات مقارنة النسخة الأصلية.</p>
      </div>
    </section>

    <section id="features" class="section">
      <div class="wrap">
        <h2>المزايا</h2>
        <div class="features-grid">
          
    <div class="feature-card">
      
      <h3>ميزة 1</h3>
      <p>نص وصفي مختصر لهذه الميزة يطابق التصور البصري الأصلي قدر الإمكان.</p>
    </div>
    
    <div class="feature-card">
      
      <h3>ميزة 2</h3>
      <p>نص وصفي مختصر لهذه الميزة يطابق التصور البصري الأصلي قدر الإمكان.</p>
    </div>
    
    <div class="feature-card">
      
      <h3>ميزة 3</h3>
      <p>نص وصفي مختصر لهذه الميزة يطابق التصور البصري الأصلي قدر الإمكان.</p>
    </div>
    
        </div>
      </div>
    </section>

    <section id="gallery" class="section">
      <div class="wrap">
        <h2>المعرض</h2>
        <div class="gallery-grid">
          
        </div>
      </div>
    </section>

    <section id="contact" class="section">
      <div class="wrap">
        <h2>تواصل</h2>
        <p class="lead">اترك لنا رسالة أو تابع المستودع على GitHub بعد رفع الحزمة.</p>
        <div class="cta-wrap">
          <a class="btn primary" href="#hero">العودة للأعلى</a>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="wrap">
        <div>© 2025 – 16-9 Rebuilt</div>
        <div>يتم تقديم الموارد من <code>/static</code> وتم إخفاء واجهة Streamlit.</div>
      </div>
    </footer>
    """, unsafe_allow_html=True)

with tab2:
    # Show the original HTML in an isolated iframe for side-by-side comparison
    import streamlit.components.v1 as components
    src_path = Path("source/index.html")
    if src_path.exists():
        html_string = src_path.read_text(encoding="utf-8", errors="ignore")
        # Large height to allow full scroll; container is full-bleed already per CSS
        components.html(html_string, height=1000, scrolling=True)
    else:
        st.error("Original HTML not found at source/index.html")
