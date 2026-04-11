import streamlit as st
from supabase import create_client
import time, random, string, smtplib, base64
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="AKFunded — Prove Your Edge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── SUPABASE ──────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_KEY"]
    )
supabase = get_supabase()

# ─── GLOBAL STYLES ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
  --gold:#D4A843;
  --gold-dim:#5c450e;
  --gold-glow:rgba(212,168,67,.15);
  --black:#050505;
  --s0:#080808;
  --s1:#0d0d0d;
  --s2:#111111;
  --s3:#161616;
  --border:#1e1e1e;
  --border2:#252525;
  --border3:#2e2e2e;
  --text:#D8D8D8;
  --dim:#505050;
  --dim2:#3a3a3a;
  --green:#00B87A;
  --green-dim:rgba(0,184,122,.1);
  --red:#E03A52;
  --red-dim:rgba(224,58,82,.1);
  --purple:#7B6EF6;
  --blue:#2D7DD2;
  --cyan:#00B4D8;
}

html, body {
  background:#050505!important;
  font-family:'Space Grotesk',sans-serif;
}
[class*="css"],.main,.stApp,.stApp>div,section.main,
div[data-testid="stAppViewContainer"],div[data-testid="stHeader"],
div[data-testid="stToolbar"],div[data-testid="stDecoration"],
div[data-testid="stBottom"],.appview-container,.reportview-container,
.main .block-container,iframe {
  background-color:#050505!important;background:#050505!important;
}
* { font-family:'Space Grotesk',sans-serif; color:var(--text); }
#MainMenu,footer,header { visibility:hidden!important;display:none!important; }
.block-container { padding:1rem 2.5rem 3rem!important;max-width:1400px!important; }
::-webkit-scrollbar { width:2px; }
::-webkit-scrollbar-thumb { background:var(--gold-dim); }

/* ── INSTAGRAM SIDEBAR ── */
.ig-sidebar {
  position:fixed;
  right:0;
  top:50%;
  transform:translateY(-50%);
  z-index:9999;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:0;
}
.ig-tab {
  background:linear-gradient(135deg,#833ab4,#fd1d1d,#f77737);
  color:#fff;
  padding:.6rem .5rem;
  border-radius:8px 0 0 8px;
  writing-mode:vertical-rl;
  text-orientation:mixed;
  transform:rotate(180deg);
  font-size:.62rem;
  font-weight:700;
  letter-spacing:2px;
  text-transform:uppercase;
  cursor:pointer;
  text-decoration:none;
  display:flex;
  align-items:center;
  gap:.4rem;
  transition:all .25s;
  box-shadow:-3px 0 20px rgba(131,58,180,.3);
  border:1px solid rgba(255,255,255,.1);
  border-right:none;
}
.ig-tab:hover {
  padding-right:.9rem;
  box-shadow:-5px 0 30px rgba(131,58,180,.5);
}
.ig-icon-wrap {
  background:linear-gradient(135deg,#833ab4,#fd1d1d,#f77737);
  border-radius:0 0 8px 8px;
  padding:.5rem;
  display:flex;
  align-items:center;
  justify-content:center;
  box-shadow:-3px 3px 20px rgba(131,58,180,.3);
  border:1px solid rgba(255,255,255,.1);
  border-top:none;
  border-right:none;
}
.ig-icon-wrap svg { width:18px;height:18px;fill:#fff; }

/* ── NAV ── */
.ak-nav {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:1.2rem 0;
  border-bottom:1px solid var(--border);
  margin-bottom:2rem;
  position:relative;
}
.ak-nav::after {
  content:'';
  position:absolute;
  bottom:-1px;
  left:0;
  width:120px;
  height:1px;
  background:linear-gradient(90deg,var(--gold),transparent);
}
.ak-logo {
  font-family:'Bebas Neue',sans-serif;
  font-size:2.2rem;
  letter-spacing:6px;
  display:inline-flex;
  align-items:baseline;
  gap:2px;
}
.ak-part { color:var(--gold); }
.funded-part { color:#fff; }
.ak-beta {
  background:var(--gold);
  color:#000;
  font-size:.5rem;
  font-weight:700;
  padding:2px 6px;
  border-radius:3px;
  letter-spacing:1.5px;
  vertical-align:super;
  margin-left:5px;
  font-family:'Space Grotesk',sans-serif;
}
.ak-tagline {
  font-size:.6rem;
  color:var(--dim);
  letter-spacing:3px;
  text-transform:uppercase;
  margin-top:2px;
}

/* ── TICKER ── */
.ticker-wrap {
  overflow:hidden;
  background:var(--s1);
  border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);
  padding:.45rem 0;
  margin-bottom:2rem;
}
.ticker-inner {
  display:flex;
  gap:3.5rem;
  animation:ticker 35s linear infinite;
  white-space:nowrap;
}
@keyframes ticker { 0%{transform:translateX(0);} 100%{transform:translateX(-50%);} }
.ticker-item { display:inline-flex;align-items:center;gap:.6rem;font-size:.72rem; }
.ticker-sep { color:var(--border3); }
.ticker-sym { font-weight:600;color:var(--text);font-family:'Space Grotesk',sans-serif;letter-spacing:.5px; }
.ticker-price { font-family:'JetBrains Mono',monospace;color:var(--dim);font-size:.7rem; }
.ticker-chg { font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:600; }
.ticker-chg.up { color:var(--green); }
.ticker-chg.dn { color:var(--red); }

/* ── HERO ── */
.hero-v2 {
  position:relative;
  text-align:center;
  padding:7rem 2rem 5rem;
  overflow:hidden;
}
.hero-v2::before {
  content:'';
  position:absolute;
  top:-20%;
  left:50%;
  transform:translateX(-50%);
  width:900px;
  height:600px;
  background:radial-gradient(ellipse,rgba(212,168,67,.07) 0%,transparent 65%);
  pointer-events:none;
}
.hero-v2::after {
  content:'';
  position:absolute;
  top:0;left:0;right:0;bottom:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 60px,rgba(255,255,255,.008) 60px,rgba(255,255,255,.008) 61px),
    repeating-linear-gradient(90deg,transparent,transparent 60px,rgba(255,255,255,.008) 60px,rgba(255,255,255,.008) 61px);
  pointer-events:none;
}
.eyebrow {
  display:inline-flex;
  align-items:center;
  gap:.6rem;
  border:1px solid var(--gold-dim);
  color:var(--gold);
  font-size:.6rem;
  letter-spacing:3px;
  padding:5px 18px;
  border-radius:2px;
  margin-bottom:2.5rem;
  text-transform:uppercase;
  background:rgba(212,168,67,.04);
  font-family:'Space Grotesk',sans-serif;
  font-weight:600;
}
.eyebrow-dot {
  width:5px;height:5px;
  background:var(--gold);
  border-radius:50%;
  display:inline-block;
  animation:blink 2s infinite;
}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.2;}}
.hero-v2 h1 {
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(4rem,10vw,10.5rem);
  line-height:.88;
  letter-spacing:6px;
  margin:0 0 1.8rem;
  color:#fff;
}
.hero-v2 h1 em { color:var(--gold);font-style:normal; }
.hero-v2 .sub {
  font-size:1rem;
  color:#4a4a4a;
  max-width:480px;
  margin:0 auto 3rem;
  line-height:1.9;
  font-weight:300;
  letter-spacing:.3px;
}

/* ── STATS BAR ── */
.hstats {
  display:flex;
  justify-content:center;
  gap:0;
  border:1px solid var(--border);
  margin-bottom:4rem;
  border-radius:4px;
  overflow:hidden;
}
.hstat {
  flex:1;
  padding:1.5rem 2rem;
  border-right:1px solid var(--border);
  text-align:center;
}
.hstat:last-child { border-right:none; }
.hstat .n {
  font-family:'Bebas Neue',sans-serif;
  font-size:2rem;
  color:var(--gold);
  letter-spacing:2px;
  display:block;
  margin-bottom:.2rem;
}
.hstat .l {
  font-size:.58rem;
  color:var(--dim);
  letter-spacing:2.5px;
  text-transform:uppercase;
}

/* ── METRIC CARDS ── */
.metric-row { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-bottom:1px;background:var(--border); }
.m-card {
  background:var(--s1);
  padding:1.4rem 1.6rem;
  position:relative;
  overflow:hidden;
}
.m-card::before {
  content:'';
  position:absolute;
  top:0;left:0;
  width:2px;height:100%;
  background:var(--gold);
  opacity:.4;
}
.m-label {
  font-size:.58rem;
  color:var(--dim);
  letter-spacing:2.5px;
  text-transform:uppercase;
  margin-bottom:.6rem;
  font-weight:600;
}
.m-val {
  font-family:'Bebas Neue',sans-serif;
  font-size:1.9rem;
  letter-spacing:2px;
  line-height:1;
}
.m-val.g { color:var(--green); }
.m-val.r { color:var(--red); }
.m-val.o { color:var(--gold); }
.m-val.w { color:var(--text); }
.m-sub { font-size:.65rem;color:var(--dim);margin-top:.5rem;font-family:'JetBrains Mono',monospace; }

/* ── STATS ROW ── */
.stats-row { display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border); }
.stat-box { background:var(--s1);padding:1.1rem 1rem;text-align:center; }
.stat-box .sv { font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:2px;line-height:1; }
.stat-box .sl { font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:.4rem; }
.sv.g { color:var(--green); }
.sv.r { color:var(--red); }
.sv.o { color:var(--gold); }
.sv.w { color:var(--text); }

/* ── RULES TRACKER ── */
.rules-box {
  background:var(--s1);
  border:1px solid var(--border);
  border-radius:0;
  padding:1.6rem;
  margin-bottom:1.5rem;
}
.r-row { display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem; }
.r-name { font-size:.75rem;color:var(--dim);letter-spacing:.5px; }
.r-val { font-family:'JetBrains Mono',monospace;font-size:.75rem;font-weight:600; }
.r-val.ok { color:var(--green); }
.r-val.bad { color:var(--red); }
.prog { height:2px;background:var(--border3);margin-bottom:1.2rem; }
.prog-fill { height:100%; }

/* ── TRADE TABLE ── */
.t-header,.t-row {
  display:grid;
  grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.2fr;
  padding:.65rem 1rem;
  font-size:.75rem;
  align-items:center;
}
.t-header {
  color:var(--dim);
  font-size:.58rem;
  letter-spacing:2px;
  text-transform:uppercase;
  border-bottom:1px solid var(--border);
  font-weight:600;
}
.t-row { border-bottom:1px solid var(--border); }
.t-row:hover { background:var(--s2); }
.t-row:last-child { border-bottom:none; }
.tag-b { background:rgba(0,184,122,.1);color:var(--green);padding:2px 8px;border-radius:2px;font-size:.62rem;font-weight:700;letter-spacing:1px; }
.tag-s { background:rgba(224,58,82,.1);color:var(--red);padding:2px 8px;border-radius:2px;font-size:.62rem;font-weight:700;letter-spacing:1px; }

/* ── LEADERBOARD ── */
.lb-item {
  display:flex;
  align-items:center;
  gap:1.2rem;
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid transparent;
  padding:1rem 1.4rem;
  margin-bottom:2px;
  transition:border-color .2s;
}
.lb-item:hover { border-left-color:var(--gold); }
.lb-rank { font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--dim);width:36px;text-align:center; }
.lb-rank.top { color:var(--gold); }
.lb-info { flex:1; }
.lb-name { font-weight:600;font-size:.88rem;letter-spacing:.3px; }
.lb-country { font-size:.68rem;color:var(--dim);margin-top:2px; }
.lb-pnl { font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);font-size:.95rem; }
.lb-badge { font-size:.55rem;padding:2px 8px;border-radius:2px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase; }
.funded-b { background:rgba(212,168,67,.1);color:var(--gold);border:1px solid var(--gold-dim); }
.active-b { background:rgba(0,184,122,.08);color:var(--green);border:1px solid rgba(0,184,122,.2); }

/* ── JOURNAL ── */
.journal-entry {
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid var(--border3);
  padding:1.2rem 1.5rem;
  margin-bottom:2px;
  transition:border-left-color .2s;
}
.journal-entry:hover { border-left-color:var(--gold); }
.je-date { font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:.4rem;font-family:'JetBrains Mono',monospace; }
.je-note { font-size:.85rem;color:var(--text);line-height:1.7;font-weight:300; }
.je-tags { display:flex;gap:.4rem;margin-top:.7rem;flex-wrap:wrap; }
.je-tag { font-size:.58rem;padding:2px 8px;border-radius:2px;background:var(--gold-dim);color:var(--gold);font-weight:700;letter-spacing:1px; }
.je-tag.win { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.2); }
.je-tag.loss { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.2); }

/* ── CHALLENGE HISTORY ── */
.ch-card {
  background:var(--s1);
  border:1px solid var(--border);
  padding:1.4rem 1.8rem;
  margin-bottom:2px;
  display:grid;
  grid-template-columns:1fr 1fr 1fr 1fr auto;
  align-items:center;
  gap:1rem;
}
.ch-plan { font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:3px;color:var(--gold); }
.ch-status { padding:3px 12px;border-radius:2px;font-size:.58rem;font-weight:700;letter-spacing:2px;text-align:center;text-transform:uppercase; }
.ch-status.passed { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.2); }
.ch-status.failed { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.2); }
.ch-status.active { background:rgba(212,168,67,.1);color:var(--gold);border:1px solid var(--gold-dim); }

/* ── NOTIFICATIONS ── */
.notif-item {
  display:flex;
  align-items:flex-start;
  gap:1.2rem;
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid var(--border3);
  padding:1rem 1.4rem;
  margin-bottom:2px;
}
.notif-item.unread { border-left:2px solid var(--gold); }
.notif-icon { font-size:1rem;flex-shrink:0;margin-top:2px;opacity:.7; }
.notif-body { flex:1; }
.notif-title { font-weight:600;font-size:.85rem;color:var(--text);margin-bottom:3px; }
.notif-msg { font-size:.75rem;color:var(--dim);line-height:1.5; }
.notif-time { font-size:.6rem;color:var(--dim2);letter-spacing:1px;margin-top:5px;font-family:'JetBrains Mono',monospace; }
.notif-badge { background:var(--gold);color:#000;font-size:.5rem;font-weight:800;padding:1px 6px;border-radius:2px;margin-left:6px;vertical-align:middle;letter-spacing:1px; }

/* ── PROFILE ── */
.profile-hero {
  background:var(--s1);
  border:1px solid var(--border);
  padding:2rem 2.5rem;
  margin-bottom:1.5rem;
  display:flex;
  gap:2.5rem;
  align-items:center;
}
.profile-avatar {
  width:72px;height:72px;
  border:1px solid var(--border3);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:'Bebas Neue',sans-serif;
  font-size:2rem;
  color:var(--gold);
  flex-shrink:0;
  background:var(--s2);
}
.profile-name { font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:4px;color:var(--text);line-height:1; }
.profile-email { font-size:.75rem;color:var(--dim);margin-top:5px;font-family:'JetBrains Mono',monospace; }
.funded-badge-inline {
  display:inline-block;
  background:transparent;
  border:1px solid var(--gold-dim);
  color:var(--gold);
  font-size:.6rem;
  letter-spacing:2.5px;
  padding:3px 12px;
  margin-top:8px;
  font-weight:700;
  text-transform:uppercase;
}

/* ── ADMIN ── */
.admin-row {
  display:grid;
  grid-template-columns:2fr 1fr 1fr 1fr 1fr auto;
  align-items:center;
  gap:1rem;
  padding:.8rem 1rem;
  border-bottom:1px solid var(--border);
  font-size:.78rem;
}
.admin-row.header { color:var(--dim);font-size:.58rem;letter-spacing:2px;text-transform:uppercase; }
.admin-status { padding:2px 10px;border-radius:2px;font-size:.58rem;font-weight:700;letter-spacing:1.5px;text-align:center;text-transform:uppercase; }
.admin-status.active { background:rgba(212,168,67,.1);color:var(--gold); }
.admin-status.passed { background:rgba(0,184,122,.1);color:var(--green); }
.admin-status.failed { background:rgba(224,58,82,.1);color:var(--red); }

/* ── PLAN CARDS ── */
.plan-rules { list-style:none;padding:0;margin:0 0 1.2rem; }
.plan-rules li {
  display:flex;
  justify-content:space-between;
  padding:.45rem 0;
  border-bottom:1px solid var(--border);
  font-size:.75rem;
  color:var(--dim);
}
.plan-rules li b { color:var(--text);font-weight:500; }

/* ── CERTIFICATE ── */
.cert-outer {
  max-width:760px;
  margin:0 auto;
  background:var(--s1);
  border:1px solid var(--border3);
  position:relative;
  overflow:hidden;
}
.cert-outer::before {
  content:'';
  position:absolute;
  top:0;left:0;right:0;
  height:2px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}
.cert-outer::after {
  content:'';
  position:absolute;
  bottom:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);
}
.cert-grid-bg {
  position:absolute;
  top:0;left:0;right:0;bottom:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 40px,rgba(212,168,67,.025) 40px,rgba(212,168,67,.025) 41px),
    repeating-linear-gradient(90deg,transparent,transparent 40px,rgba(212,168,67,.025) 40px,rgba(212,168,67,.025) 41px);
  pointer-events:none;
}
.cert-body { position:relative;padding:3.5rem 4rem;text-align:center; }
.cert-header-label {
  font-size:.58rem;
  color:var(--dim);
  letter-spacing:4px;
  text-transform:uppercase;
  margin-bottom:1rem;
  font-family:'Space Grotesk',sans-serif;
  font-weight:600;
}
.cert-title {
  font-family:'Bebas Neue',sans-serif;
  font-size:3.2rem;
  letter-spacing:8px;
  color:var(--gold);
  line-height:1;
  margin-bottom:.5rem;
}
.cert-subtitle {
  font-size:.62rem;
  color:var(--dim);
  letter-spacing:3px;
  text-transform:uppercase;
  margin-bottom:2.5rem;
}
.cert-divider {
  display:flex;
  align-items:center;
  gap:1rem;
  margin:1.5rem 0;
}
.cert-divider::before,.cert-divider::after {
  content:'';flex:1;
  height:1px;
  background:linear-gradient(90deg,transparent,var(--border3));
}
.cert-divider::after {
  background:linear-gradient(90deg,var(--border3),transparent);
}
.cert-divider-text {
  font-size:.55rem;
  color:var(--dim2);
  letter-spacing:3px;
  text-transform:uppercase;
}
.cert-name {
  font-family:'Bebas Neue',sans-serif;
  font-size:2.4rem;
  letter-spacing:5px;
  color:var(--text);
  margin:.8rem 0;
  line-height:1;
}
.cert-challenge-tag {
  display:inline-block;
  border:1px solid var(--gold-dim);
  color:var(--gold);
  font-size:.62rem;
  letter-spacing:3px;
  padding:5px 20px;
  font-weight:700;
  text-transform:uppercase;
  margin:.8rem 0 2rem;
  background:rgba(212,168,67,.04);
}
.cert-stats-row {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:0;
  border:1px solid var(--border3);
  margin:1.5rem 0;
}
.cert-stat {
  padding:1.2rem;
  border-right:1px solid var(--border3);
}
.cert-stat:last-child { border-right:none; }
.cert-stat-val {
  font-family:'Bebas Neue',sans-serif;
  font-size:1.8rem;
  letter-spacing:2px;
  line-height:1;
  margin-bottom:.3rem;
}
.cert-stat-label {
  font-size:.55rem;
  color:var(--dim);
  letter-spacing:2.5px;
  text-transform:uppercase;
}
.cert-footer-bar {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:1rem 4rem;
  border-top:1px solid var(--border);
  background:var(--s0);
  position:relative;
}
.cert-footer-text {
  font-size:.58rem;
  color:var(--dim2);
  letter-spacing:2px;
  text-transform:uppercase;
}
.cert-seal {
  width:48px;height:48px;
  border:1px solid var(--gold-dim);
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  color:var(--gold);
  font-size:.55rem;
  letter-spacing:1px;
  font-weight:700;
  text-align:center;
  line-height:1.3;
}

/* ── AI CHAT ── */
.chat-container { background:var(--s1);border:1px solid var(--border);overflow:hidden;margin-bottom:1rem; }
.chat-header { padding:1rem 1.4rem;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.8rem; }
.chat-ai-dot { width:6px;height:6px;background:var(--green);border-radius:50%;animation:pulse 2s infinite; }
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
.chat-messages { padding:1.2rem;max-height:380px;overflow-y:auto; }
.chat-msg { margin-bottom:1rem;display:flex;gap:.8rem;align-items:flex-start; }
.chat-msg.user { flex-direction:row-reverse; }
.chat-bubble { padding:.7rem 1rem;font-size:.82rem;line-height:1.6;max-width:78%; }
.chat-bubble.ai { background:var(--s2);border:1px solid var(--border);color:var(--text); }
.chat-bubble.user { background:var(--gold);color:#000;font-weight:500; }
.chat-avatar { width:26px;height:26px;font-size:.7rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:var(--s2);border:1px solid var(--border);font-weight:700; }
.chat-avatar.user { background:var(--gold);color:#000; }

/* ── RISK ── */
.risk-card { background:var(--s1);border:1px solid var(--border);padding:1.5rem; }
.risk-result { background:var(--s2);border:1px solid var(--border);padding:1.1rem;text-align:center;margin-top:1rem; }
.risk-val { font-family:'Bebas Neue',sans-serif;font-size:2.2rem;letter-spacing:2px; }

/* ── REFERRAL ── */
.ref-code-box {
  background:var(--s2);
  border:1px solid var(--border3);
  border-left:2px solid var(--gold);
  padding:1rem 1.4rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin:1rem 0;
}
.ref-code { font-family:'JetBrains Mono',monospace;font-size:1.4rem;color:var(--gold);font-weight:700;letter-spacing:5px; }
.ref-stats { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:1rem 0;background:var(--border); }

/* ── HEATMAP ── */
.heatmap-grid { display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin-top:1rem;background:var(--border); }
.hmap-cell { padding:.8rem .5rem;text-align:center;cursor:default; }
.hmap-sym { font-size:.68rem;font-weight:600;color:var(--text);letter-spacing:.5px; }
.hmap-chg { font-size:.75rem;font-family:'JetBrains Mono',monospace;margin-top:3px; }

/* ── SCANNER ── */
.scan-row {
  display:flex;
  align-items:center;
  justify-content:space-between;
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid transparent;
  padding:.85rem 1.2rem;
  margin-bottom:2px;
  transition:border-left-color .15s;
}
.scan-row:hover { border-left-color:var(--gold); }
.scan-sym { font-weight:600;font-size:.85rem;letter-spacing:.5px; }
.scan-signal { font-size:.58rem;font-weight:700;letter-spacing:2px;padding:3px 10px;border-radius:2px;text-transform:uppercase; }
.scan-signal.bull { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.25); }
.scan-signal.bear { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.25); }
.scan-signal.neut { background:rgba(212,168,67,.1);color:var(--gold);border:1px solid var(--gold-dim); }

/* ── WATCHLIST ── */
.wl-row { display:flex;align-items:center;justify-content:space-between;padding:.7rem .5rem;border-bottom:1px solid var(--border); }
.wl-row:last-child { border-bottom:none; }

/* ── ORDER BOOK ── */
.ob-row { display:grid;grid-template-columns:1fr 1fr 1fr;padding:.3rem .8rem;font-size:.73rem;font-family:'JetBrains Mono',monospace; }
.ob-bid { color:var(--green); }
.ob-ask { color:var(--red); }
.ob-vol { color:var(--dim);text-align:right; }

/* ── STEPS ── */
.steps-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:3rem 0;background:var(--border); }
.step-card { background:var(--s1);padding:2rem 1.5rem; }
.step-num { font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:var(--gold);line-height:1;margin-bottom:.5rem;letter-spacing:2px; }
.step-title { font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2.5px;color:var(--text);margin-bottom:.6rem; }
.step-desc { font-size:.78rem;color:var(--dim);line-height:1.7;font-weight:300; }

/* ── TESTIMONIALS ── */
.testi-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:2rem 0;background:var(--border); }
.testi-card { background:var(--s1);padding:1.8rem; }
.testi-quote { font-size:.85rem;color:var(--text);line-height:1.8;margin-bottom:1.2rem;font-weight:300;border-left:2px solid var(--gold-dim);padding-left:1rem; }
.testi-name { font-weight:600;font-size:.8rem;color:var(--gold);letter-spacing:.5px; }
.testi-meta { font-size:.68rem;color:var(--dim);margin-top:3px; }

/* ── FOOTER ── */
.ak-footer {
  text-align:center;
  padding:2.5rem 0 1.5rem;
  border-top:1px solid var(--border);
  margin-top:5rem;
  color:var(--dim);
  font-size:.68rem;
  letter-spacing:1px;
  position:relative;
}
.ak-footer::before {
  content:'';
  position:absolute;
  top:-1px;
  left:50%;
  transform:translateX(-50%);
  width:120px;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);
}
.ak-footer b { color:var(--gold); }

/* ── STREAMLIT OVERRIDES ── */
.stButton>button {
  background:var(--gold)!important;
  color:#000!important;
  font-weight:700!important;
  border:none!important;
  border-radius:2px!important;
  font-family:'Space Grotesk',sans-serif!important;
  letter-spacing:1px!important;
  white-space:nowrap!important;
  text-transform:uppercase!important;
  font-size:.75rem!important;
}
.stButton>button:hover { opacity:.85!important;transform:translateY(-1px)!important; }
.stButton>button p { color:#000!important; }
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background:var(--s1)!important;
  border:1px solid var(--border)!important;
  border-radius:2px!important;
  padding:3px!important;
  gap:3px!important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] { color:var(--dim)!important;font-family:'Space Grotesk',sans-serif!important;font-size:.75rem!important;letter-spacing:.5px!important; }
div[data-testid="stTabs"] [aria-selected="true"] { background:var(--gold)!important;color:#000!important;border-radius:2px!important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"] { display:none!important; }
.stSelectbox>div>div,
.stNumberInput>div>div>input,
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
  background:var(--s2)!important;
  border:1px solid var(--border)!important;
  color:var(--text)!important;
  border-radius:2px!important;
  font-family:'Space Grotesk',sans-serif!important;
}
label[data-testid="stWidgetLabel"] { color:var(--dim)!important;font-size:.68rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important; }
div[data-testid="stVerticalBlock"],div[data-testid="stHorizontalBlock"],
div[data-testid="column"],div[data-testid="stMarkdownContainer"],
div.element-container,div.stMarkdown { background:transparent!important; }
.stSlider [data-baseweb="slider"] [data-testid="stSliderThumb"] { background:var(--gold)!important; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────
LOGO_URL = "https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.PNG"
IG_HANDLE = "@akfunded"
IG_URL    = "https://www.instagram.com/akfunded"

RULES = {
    "starter":      {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "pro":          {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "elite":        {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "1phase_10k":   {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "1phase_25k":   {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "1phase_50k":   {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "1phase_100k":  {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "1phase_200k":  {"target":8,"daily_loss":4,"total_loss":8, "min_days":5},
    "2phase_10k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4},
    "2phase_25k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4},
    "2phase_50k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4},
    "2phase_100k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":4},
    "2phase_200k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":4},
}

PLANS_1P = [
    {"name":"$10,000",  "capital":10000,  "price":119,"slug":"1phase_10k",  "split":80},
    {"name":"$25,000",  "capital":25000,  "price":219,"slug":"1phase_25k",  "split":80},
    {"name":"$50,000",  "capital":50000,  "price":299,"slug":"1phase_50k",  "split":80},
    {"name":"$100,000", "capital":100000, "price":459,"slug":"1phase_100k", "split":80},
    {"name":"$200,000", "capital":200000, "price":799,"slug":"1phase_200k", "split":80},
]
PLANS_2P = [
    {"name":"$10,000",  "capital":10000,  "price":49, "slug":"2phase_10k",  "split":90},
    {"name":"$25,000",  "capital":25000,  "price":99, "slug":"2phase_25k",  "split":90},
    {"name":"$50,000",  "capital":50000,  "price":149,"slug":"2phase_50k",  "split":90},
    {"name":"$100,000", "capital":100000, "price":249,"slug":"2phase_100k", "split":90},
    {"name":"$200,000", "capital":200000, "price":449,"slug":"2phase_200k", "split":90},
]

SYMBOLS = {
    "NSE Indices": ["NIFTY","BANKNIFTY","FINNIFTY","MIDCPNIFTY"],
    "NSE Stocks":  ["RELIANCE","TCS","INFY","HDFCBANK","TATAMOTORS","WIPRO","SBIN","ICICIBANK","BAJFINANCE","ADANIENT"],
    "Crypto":      ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT"],
    "Forex":       ["EURUSD","GBPUSD","USDJPY","USDINR","AUDUSD"],
    "Commodities": ["GOLD","SILVER","CRUDEOIL","NATURALGAS"],
}
TV_PREFIX = {
    "NSE Indices":"NSE:","NSE Stocks":"NSE:",
    "Crypto":"BINANCE:","Forex":"FX:","Commodities":"TVC:"
}

MARKET_DATA = {
    "NIFTY":    {"price":22450.50,"change":+0.62,"vol":"High"},
    "BANKNIFTY":{"price":47820.25,"change":-0.31,"vol":"Medium"},
    "BTCUSDT":  {"price":67430.00,"change":+2.14,"vol":"Very High"},
    "ETHUSDT":  {"price":3542.80, "change":+1.87,"vol":"High"},
    "GOLD":     {"price":71250.00,"change":+0.45,"vol":"Medium"},
    "EURUSD":   {"price":1.0842,  "change":-0.12,"vol":"Low"},
    "RELIANCE": {"price":2980.45, "change":+1.20,"vol":"High"},
    "TCS":      {"price":3870.30, "change":-0.55,"vol":"Medium"},
    "INFY":     {"price":1540.00, "change":+0.88,"vol":"Medium"},
    "HDFCBANK": {"price":1620.75, "change":-0.22,"vol":"Medium"},
}

# ─── SESSION STATE ──────────────────────────────────────────────
for k, v in [
    ("user",None),("page","home"),("notifications",[]),
    ("chat_history",[]),("watchlist",["NIFTY","BANKNIFTY","BTCUSDT","GOLD"]),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── DATABASE HELPERS ──────────────────────────────────────────
def db_get_profile(uid):
    try:
        r = supabase.table("profiles").select("*").eq("id",uid).execute()
        return r.data[0] if r.data else None
    except: return None

def db_save_profile(uid, name, email, country):
    existing = db_get_profile(uid)
    if existing:
        supabase.table("profiles").update({"name":name,"email":email,"country":country}).eq("id",uid).execute()
    else:
        supabase.table("profiles").insert({"id":uid,"name":name,"email":email,"country":country}).execute()

def db_get_active_challenge(uid):
    try:
        r = supabase.table("challenges").select("*").eq("user_id",uid).eq("status","active").execute()
        return r.data[0] if r.data else None
    except: return None

def db_get_account(challenge_id):
    try:
        r = supabase.table("accounts").select("*").eq("challenge_id",challenge_id).execute()
        return r.data[0] if r.data else None
    except: return None

def db_get_trades(uid, challenge_id=None, limit=25):
    try:
        q = supabase.table("trades").select("*").eq("user_id",uid)
        if challenge_id: q = q.eq("challenge_id",challenge_id)
        return q.order("closed_at",desc=True).limit(limit).execute().data or []
    except: return []

def db_get_all_challenges(uid):
    try:
        return supabase.table("challenges").select("*").eq("user_id",uid).order("started_at",desc=True).execute().data or []
    except: return []

def db_get_journal(uid):
    try:
        return supabase.table("journal_entries").select("*").eq("user_id",uid).order("created_at",desc=True).limit(30).execute().data or []
    except: return []

def db_get_leaderboard():
    try:
        challenges = supabase.table("challenges").select("*").in_("status",["passed","active"]).execute().data or []
        result = []
        for ch in challenges:
            acc = db_get_account(ch["id"])
            if not acc: continue
            prof = db_get_profile(ch["user_id"])
            if not prof: continue
            cap = acc.get("initial_capital",1); bal = acc.get("balance",cap)
            result.append({
                "name":prof.get("name","Trader"),"country":prof.get("country",""),
                "profit_pct":round((bal-cap)/cap*100,2) if cap else 0,
                "plan":ch.get("plan",""),"status":ch.get("status","active"),
                "days_traded":acc.get("days_traded",0),
            })
        return sorted(result, key=lambda x: x["profit_pct"], reverse=True)[:20]
    except: return []

def db_get_all_accounts():
    try:
        challenges = supabase.table("challenges").select("*").execute().data or []
        result = []
        for ch in challenges:
            acc = db_get_account(ch["id"]); prof = db_get_profile(ch["user_id"])
            if not acc or not prof: continue
            cap = acc.get("initial_capital",1); bal = acc.get("balance",cap)
            result.append({
                "name":prof.get("name","?"),"email":prof.get("email","?"),
                "plan":ch.get("plan","?"),"status":ch.get("status","active"),
                "capital":cap,"balance":bal,
                "pnl_pct":round((bal-cap)/cap*100,2) if cap else 0,
                "days_traded":acc.get("days_traded",0),
                "started_at":ch.get("started_at","")[:10],
                "challenge_id":ch.get("id",""),"user_id":ch.get("user_id",""),
            })
        return sorted(result, key=lambda x: x["started_at"], reverse=True)
    except: return []

def db_update_profile(uid, name, country, bio=""):
    try:
        supabase.table("profiles").update({"name":name,"country":country,"bio":bio}).eq("id",uid).execute()
        return True
    except: return False

def push_notification(uid, icon, title, msg):
    notifs = st.session_state.get("notifications",[])
    notifs.insert(0,{"uid":uid,"icon":icon,"title":title,"msg":msg,
                     "time":datetime.utcnow().strftime("%H:%M"),"unread":True})
    st.session_state.notifications = notifs[:20]

def generate_referral_code(name):
    prefix = name[:3].upper().replace(" ","")
    return f"{prefix}{''.join(random.choices(string.digits, k=4))}"

def db_get_referral(uid):
    try:
        r = supabase.table("referrals").select("*").eq("user_id",uid).execute()
        return r.data[0] if r.data else None
    except: return None

def db_create_referral(uid, code):
    try:
        supabase.table("referrals").insert({"user_id":uid,"code":code,"uses":0,"created_at":datetime.utcnow().isoformat()}).execute()
        return True
    except: return False

def send_email_with_certificate(to_email, subject, body_html, cert_html=None):
    """Send email, optionally with certificate HTML embedded"""
    try:
        smtp_email = st.secrets.get("SMTP_EMAIL","")
        smtp_pass  = st.secrets.get("SMTP_PASSWORD","")
        if not smtp_email or not smtp_pass: return False
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"AKFunded <{smtp_email}>"
        msg["To"]      = to_email
        # If certificate, embed it in the email body
        full_html = body_html
        if cert_html:
            full_html = body_html + cert_html
        msg.attach(MIMEText(full_html,"html"))
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
            s.login(smtp_email, smtp_pass)
            s.sendmail(smtp_email, to_email, msg.as_string())
        return True
    except: return False

def call_ai(messages, system_prompt):
    try:
        import requests
        headers = {"Authorization":f"Bearer {st.secrets.get('GROQ_API_KEY','')}","Content-Type":"application/json"}
        body = {"model":"llama-3.3-70b-versatile","max_tokens":1000,
                "messages":[{"role":"system","content":system_prompt},*messages]}
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",json=body,headers=headers,timeout=30)
        data = r.json()
        return data["choices"][0]["message"]["content"] if data.get("choices") else "Unable to process request."
    except Exception as e:
        return f"AI unavailable. ({e})"

def compute_stats(trades):
    if not trades: return 0,0,0,0,0
    pnls = [t.get("pnl",0) for t in trades]
    wins = [p for p in pnls if p > 0]
    total = len(pnls)
    return (
        round(len(wins)/total*100,1) if total else 0,
        round(sum(pnls)/total,2)     if total else 0,
        max(pnls) if pnls else 0,
        min(pnls) if pnls else 0,
        total
    )

def compute_streaks(trades):
    if not trades: return 0, 0
    pnls = [t.get("pnl",0) for t in reversed(trades)]
    win_streak = loss_streak = cur_win = cur_loss = 0
    for p in pnls:
        if p > 0:   cur_win += 1; cur_loss = 0
        elif p < 0: cur_loss += 1; cur_win = 0
        win_streak  = max(win_streak,  cur_win)
        loss_streak = max(loss_streak, cur_loss)
    return win_streak, loss_streak

def get_simulated_price(symbol, base_price=None):
    if base_price is None:
        base_price = MARKET_DATA.get(symbol,{}).get("price",100.0)
    return round(base_price * (1 + random.uniform(-0.003, 0.003)), 2)

def build_certificate_html(name, plan, capital, pnl_pct, days, date_str):
    """Returns a self-contained HTML string for the certificate — used both for display and email"""
    cap_str = f"${capital//1000}K"
    return f"""
<div class="cert-outer" style="max-width:760px;margin:0 auto;background:#0d0d0d;border:1px solid #252525;position:relative;overflow:hidden;font-family:'Space Grotesk',sans-serif;">
  <div class="cert-grid-bg" style="position:absolute;top:0;left:0;right:0;bottom:0;
    background:repeating-linear-gradient(0deg,transparent,transparent 40px,rgba(212,168,67,.02) 40px,rgba(212,168,67,.02) 41px),
    repeating-linear-gradient(90deg,transparent,transparent 40px,rgba(212,168,67,.02) 40px,rgba(212,168,67,.02) 41px);
    pointer-events:none;"></div>
  <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#D4A843,transparent);"></div>

  <div style="position:relative;padding:3.5rem 4rem;text-align:center;">
    <!-- Logo -->
    <div style="margin-bottom:1.5rem;">
      <img src="{LOGO_URL}" onerror="this.style.display='none'"
           style="height:52px;width:52px;object-fit:contain;opacity:.9;" />
    </div>

    <div style="font-size:.55rem;color:#505050;letter-spacing:4px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">
      AKFUNDED &nbsp;&middot;&nbsp; OFFICIAL DOCUMENT
    </div>

    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:8px;color:#D4A843;line-height:1;margin-bottom:.4rem;">
      CERTIFICATE
    </div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:6px;color:#3a3a3a;margin-bottom:2rem;">
      OF ACHIEVEMENT
    </div>

    <div style="display:flex;align-items:center;gap:1rem;margin:1.5rem 0;">
      <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#252525);"></div>
      <div style="font-size:.52rem;color:#3a3a3a;letter-spacing:3px;text-transform:uppercase;">THIS CERTIFIES THAT</div>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,#252525,transparent);"></div>
    </div>

    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;letter-spacing:5px;color:#D8D8D8;margin:.6rem 0;line-height:1;">
      {name.upper()}
    </div>

    <div style="font-size:.78rem;color:#505050;margin:.8rem 0 1.5rem;font-weight:300;line-height:1.8;">
      has successfully demonstrated exceptional trading discipline and<br>
      met all requirements of the AKFunded Prop Trading Challenge.
    </div>

    <div style="display:inline-block;border:1px solid #5c450e;color:#D4A843;font-size:.6rem;letter-spacing:3px;padding:6px 24px;font-weight:700;text-transform:uppercase;background:rgba(212,168,67,.04);margin-bottom:2rem;">
      {plan.upper()} CHALLENGE &nbsp;&middot;&nbsp; {cap_str} ACCOUNT
    </div>

    <div style="display:grid;grid-template-columns:repeat(3,1fr);border:1px solid #252525;margin:1.5rem 0;">
      <div style="padding:1.4rem;border-right:1px solid #252525;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:2px;color:#00B87A;line-height:1;margin-bottom:.3rem;">+{pnl_pct:.2f}%</div>
        <div style="font-size:.52rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Profit Achieved</div>
      </div>
      <div style="padding:1.4rem;border-right:1px solid #252525;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:2px;color:#D4A843;line-height:1;margin-bottom:.3rem;">{days}</div>
        <div style="font-size:.52rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Trading Days</div>
      </div>
      <div style="padding:1.4rem;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:2px;color:#D8D8D8;line-height:1;margin-bottom:.3rem;">{date_str}</div>
        <div style="font-size:.52rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Date Issued</div>
      </div>
    </div>

    <div style="margin-top:1.5rem;display:flex;align-items:center;justify-content:space-between;">
      <div style="text-align:left;">
        <div style="font-size:.78rem;color:#D4A843;font-weight:600;letter-spacing:.5px;">Akash Injeti</div>
        <div style="font-size:.6rem;color:#505050;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Founder, AKFunded</div>
        <div style="width:80px;height:1px;background:#252525;margin-top:.6rem;"></div>
      </div>
      <div style="width:52px;height:52px;border:1px solid #5c450e;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#D4A843;font-size:.48rem;letter-spacing:.8px;font-weight:700;text-align:center;line-height:1.4;">
        AK<br>FUNDED<br>VERIFIED
      </div>
      <div style="text-align:right;">
        <div style="font-size:.78rem;color:#D4A843;font-weight:600;letter-spacing:.5px;">AKFunded Platform</div>
        <div style="font-size:.6rem;color:#505050;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Prop Trading Firm</div>
        <div style="width:80px;height:1px;background:#252525;margin-top:.6rem;margin-left:auto;"></div>
      </div>
    </div>
  </div>

  <div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 4rem;border-top:1px solid #1e1e1e;background:#080808;">
    <div style="font-size:.55rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">akfunded.streamlit.app</div>
    <div style="font-size:.55rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">instagram: @akfunded</div>
    <div style="font-size:.55rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">Simulated Trading Platform</div>
  </div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,#5c450e,transparent);"></div>
</div>"""

def build_certificate_email_html(name, plan, capital, pnl_pct, days, date_str):
    """Full email wrapper with certificate embedded — works in email clients"""
    cap_str = f"${capital//1000}K"
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#050505;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
<div style="max-width:760px;margin:0 auto;padding:2rem 1rem;">

  <!-- Header -->
  <div style="text-align:center;padding:2rem 0 1.5rem;border-bottom:1px solid #1e1e1e;margin-bottom:2rem;">
    <img src="{LOGO_URL}" width="48" height="48" style="object-fit:contain;display:block;margin:0 auto .8rem;" alt="AKFunded" />
    <div style="font-family:'Helvetica Neue',sans-serif;font-size:1.4rem;font-weight:700;letter-spacing:4px;color:#D4A843;">AKFUNDED</div>
    <div style="font-size:.62rem;color:#505050;letter-spacing:3px;text-transform:uppercase;margin-top:4px;">Prop Trading Platform</div>
  </div>

  <!-- Intro -->
  <div style="text-align:center;margin-bottom:2rem;">
    <div style="font-size:1rem;color:#D8D8D8;font-weight:300;line-height:1.8;">
      Congratulations, <strong style="color:#D4A843;">{name}</strong>.<br>
      You have passed the AKFunded {plan.upper()} Challenge and earned your certificate.
    </div>
  </div>

  <!-- Certificate Block -->
  <div style="background:#0d0d0d;border:1px solid #252525;position:relative;overflow:hidden;">
    <div style="height:2px;background:linear-gradient(90deg,transparent,#D4A843,transparent);"></div>

    <div style="padding:3rem;text-align:center;">
      <div style="font-size:.55rem;color:#505050;letter-spacing:4px;text-transform:uppercase;margin-bottom:1rem;">AKFUNDED &middot; OFFICIAL CERTIFICATE</div>
      <div style="font-size:2.2rem;font-weight:800;letter-spacing:6px;color:#D4A843;line-height:1;margin-bottom:.3rem;">CERTIFICATE</div>
      <div style="font-size:1rem;letter-spacing:5px;color:#3a3a3a;margin-bottom:2rem;">OF ACHIEVEMENT</div>

      <div style="font-size:.62rem;color:#505050;letter-spacing:3px;text-transform:uppercase;margin-bottom:.5rem;">THIS CERTIFIES THAT</div>
      <div style="font-size:1.8rem;font-weight:700;letter-spacing:4px;color:#D8D8D8;margin:.5rem 0 1rem;">{name.upper()}</div>
      <div style="font-size:.8rem;color:#505050;font-weight:300;line-height:1.8;margin-bottom:1.5rem;">
        has successfully completed all requirements of the<br>AKFunded Prop Trading Challenge.
      </div>

      <div style="display:inline-block;border:1px solid #5c450e;color:#D4A843;font-size:.6rem;letter-spacing:2px;padding:5px 20px;font-weight:700;text-transform:uppercase;background:rgba(212,168,67,.04);margin-bottom:2rem;">
        {plan.upper()} CHALLENGE &middot; {cap_str} ACCOUNT
      </div>

      <!-- Stats Table -->
      <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #252525;margin:1.5rem 0;">
        <tr>
          <td style="padding:1.2rem;border-right:1px solid #252525;text-align:center;width:33%;">
            <div style="font-size:1.6rem;font-weight:800;color:#00B87A;letter-spacing:2px;line-height:1;margin-bottom:.3rem;">+{pnl_pct:.2f}%</div>
            <div style="font-size:.5rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Profit Achieved</div>
          </td>
          <td style="padding:1.2rem;border-right:1px solid #252525;text-align:center;width:33%;">
            <div style="font-size:1.6rem;font-weight:800;color:#D4A843;letter-spacing:2px;line-height:1;margin-bottom:.3rem;">{days}</div>
            <div style="font-size:.5rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Trading Days</div>
          </td>
          <td style="padding:1.2rem;text-align:center;width:33%;">
            <div style="font-size:1.3rem;font-weight:800;color:#D8D8D8;letter-spacing:2px;line-height:1;margin-bottom:.3rem;">{date_str}</div>
            <div style="font-size:.5rem;color:#505050;letter-spacing:2.5px;text-transform:uppercase;">Date Issued</div>
          </td>
        </tr>
      </table>

      <!-- Signatures -->
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:1.5rem;">
        <tr>
          <td style="text-align:left;width:33%;">
            <div style="font-size:.75rem;color:#D4A843;font-weight:600;">Akash Injeti</div>
            <div style="font-size:.55rem;color:#505050;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Founder, AKFunded</div>
            <div style="width:70px;height:1px;background:#252525;margin-top:.6rem;"></div>
          </td>
          <td style="text-align:center;width:33%;">
            <div style="width:48px;height:48px;border:1px solid #5c450e;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#D4A843;font-size:.42rem;letter-spacing:.5px;font-weight:700;text-align:center;line-height:1.5;">
              AK<br>FUNDED<br>VERIFIED
            </div>
          </td>
          <td style="text-align:right;width:33%;">
            <div style="font-size:.75rem;color:#D4A843;font-weight:600;">AKFunded Platform</div>
            <div style="font-size:.55rem;color:#505050;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Prop Trading Firm</div>
            <div style="width:70px;height:1px;background:#252525;margin-top:.6rem;margin-left:auto;"></div>
          </td>
        </tr>
      </table>
    </div>

    <div style="padding:.8rem 3rem;border-top:1px solid #1e1e1e;background:#080808;display:flex;justify-content:space-between;">
      <span style="font-size:.5rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">akfunded.streamlit.app</span>
      <span style="font-size:.5rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">@akfunded</span>
      <span style="font-size:.5rem;color:#3a3a3a;letter-spacing:2px;text-transform:uppercase;">Simulated Trading Platform</span>
    </div>
  </div>

  <!-- CTA -->
  <div style="text-align:center;margin-top:2rem;padding:1.5rem;border:1px solid #1e1e1e;background:#0d0d0d;">
    <div style="font-size:.72rem;color:#505050;line-height:1.8;">
      Share your achievement on Instagram <strong style="color:#D4A843;">@akfunded</strong><br>
      <span style="color:#3a3a3a;">This certificate is issued for a simulated trading challenge. AKFunded is a prop trading simulator.</span>
    </div>
  </div>

</div>
</body>
</html>"""

def goto(page):
    st.session_state.page = page
    st.rerun()

# ─── INSTAGRAM SIDEBAR (rendered on every page) ───────────────
def render_ig_sidebar():
    st.markdown(f"""
    <div class="ig-sidebar">
      <a href="{IG_URL}" target="_blank" class="ig-tab" title="Follow us on Instagram">
        <svg viewBox="0 0 24 24" style="width:12px;height:12px;fill:#fff;transform:rotate(180deg);">
          <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
        </svg>
        FOLLOW US
      </a>
      <div class="ig-icon-wrap">
        <a href="{IG_URL}" target="_blank" style="display:flex;align-items:center;justify-content:center;">
          <svg viewBox="0 0 24 24" style="width:18px;height:18px;fill:#fff;">
            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
          </svg>
        </a>
      </div>
    </div>""", unsafe_allow_html=True)

# ─── UI HELPERS ────────────────────────────────────────────────
def nav():
    logged_in = st.session_state.user is not None
    st.markdown(f"""
    <div class="ak-nav">
      <div style="display:flex;align-items:center;gap:14px;">
        <img src="{LOGO_URL}" onerror="this.style.display='none'"
             style="height:34px;width:34px;object-fit:contain;" />
        <div>
          <div class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span><span class="ak-beta">BETA</span></div>
          <div class="ak-tagline">Prove Your Edge — Get Funded</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    if logged_in:
        is_admin = st.session_state.user.get("email","") == st.secrets.get("ADMIN_EMAIL","admin@akfunded.com")
        if is_admin:
            c0,c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1.2,.8,.8,.8,.8,.8,1,.7,.7,.4])
            with c7:
                if st.button("Alerts" + (f" ({sum(1 for n in st.session_state.notifications if n.get('unread'))})" if any(n.get('unread') for n in st.session_state.notifications) else ""), key="nb"): goto("notifications")
            with c8:
                if st.button("Admin", key="na"): goto("admin")
            with c9:
                if st.button("Me", key="npr"): goto("profile")
        else:
            c0,c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1.2,.8,.8,.8,.8,.8,1,.7,.4])
            with c7:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("Alerts" + (f" ({unread})" if unread else ""), key="nb"): goto("notifications")
            with c8:
                if st.button("Me", key="npr"): goto("profile")
        with c1:
            if st.button("Dashboard", key="nd"): goto("dashboard")
        with c2:
            if st.button("Markets",   key="nm"): goto("markets")
        with c3:
            if st.button("Portfolio", key="np"): goto("portfolio")
        with c4:
            if st.button("Journal",   key="nj"): goto("journal")
        with c5:
            if st.button("History",   key="nh"): goto("history")
        with c6:
            if st.button("Leaderboard", key="nl"): goto("leaderboard")
    else:
        c1,c2,c3 = st.columns([5,1,1])
        with c2:
            if st.button("Leaderboard", key="nl2"): goto("leaderboard")
        with c3:
            if st.button("Sign In", key="nl3"): goto("auth")

def footer():
    st.markdown(f"""
    <div class="ak-footer">
      <div style="display:flex;align-items:center;justify-content:center;gap:1rem;margin-bottom:1rem;">
        <img src="{LOGO_URL}" onerror="this.style.display='none'"
             style="height:24px;width:24px;object-fit:contain;opacity:.5;" />
        <span style="font-size:.75rem;letter-spacing:4px;color:#2e2e2e;font-weight:700;">AKFUNDED</span>
        <span style="color:#1e1e1e;">|</span>
        <a href="{IG_URL}" target="_blank" style="color:#505050;text-decoration:none;font-size:.68rem;letter-spacing:1.5px;transition:color .2s;"
           onmouseover="this.style.color='#D4A843'" onmouseout="this.style.color='#505050'">
          Instagram: <b>{IG_HANDLE}</b>
        </a>
      </div>
      <div>
        Built by <b>Akash Injeti</b>
        &nbsp;&middot;&nbsp; Simulate. Prove. Get Funded.
        &nbsp;&middot;&nbsp; <span style="color:#2e2e2e;">All accounts are simulated demo accounts.</span>
      </div>
    </div>""", unsafe_allow_html=True)

def sec(title, sub=""):
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.7rem;letter-spacing:4px;color:var(--text);line-height:1;">{title}</div>
      {"<div style='color:var(--dim);font-size:.75rem;margin-top:.4rem;letter-spacing:.5px;font-weight:300;'>"+sub+"</div>" if sub else ""}
      <div style="width:40px;height:1px;background:var(--gold);margin-top:.6rem;opacity:.6;"></div>
    </div>""", unsafe_allow_html=True)

def render_live_ticker():
    items = ""
    for sym, data in MARKET_DATA.items():
        chg  = data["change"]
        cls  = "up" if chg >= 0 else "dn"
        sign = "+" if chg >= 0 else ""
        items += f'<span class="ticker-sep">&#8212;</span><div class="ticker-item"><span class="ticker-sym">{sym}</span><span class="ticker-price">{data["price"]:,.2f}</span><span class="ticker-chg {cls}">{sign}{chg:.2f}%</span></div>'
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{items+items}</div></div>', unsafe_allow_html=True)

def render_market_heatmap():
    cells = ""
    for sym, data in MARKET_DATA.items():
        chg = data["change"]
        if chg > 1.5:    bg,bord = "rgba(0,184,122,.2)","rgba(0,184,122,.3)"
        elif chg > 0.3:  bg,bord = "rgba(0,184,122,.1)","rgba(0,184,122,.15)"
        elif chg > 0:    bg,bord = "rgba(0,184,122,.04)","#1e1e1e"
        elif chg > -0.3: bg,bord = "rgba(224,58,82,.04)","#1e1e1e"
        elif chg > -1.5: bg,bord = "rgba(224,58,82,.1)","rgba(224,58,82,.15)"
        else:             bg,bord = "rgba(224,58,82,.2)","rgba(224,58,82,.3)"
        sign = "+" if chg >= 0 else ""
        col  = "var(--green)" if chg >= 0 else "var(--red)"
        cells += f'<div class="hmap-cell" style="background:{bg};border:1px solid {bord};"><div class="hmap-sym">{sym}</div><div class="hmap-chg" style="color:{col};">{sign}{chg:.2f}%</div></div>'
    st.markdown(f'<div class="heatmap-grid">{cells}</div>', unsafe_allow_html=True)

def render_signal_scanner():
    for sym, data in MARKET_DATA.items():
        chg = data["change"]; vol = data["vol"]
        if chg > 1.5 and vol in ["High","Very High"]:
            sig,cls = "STRONG BUY","bull"
        elif chg > 0.3:
            sig,cls = "BUY","bull"
        elif chg < -1.5 and vol in ["High","Very High"]:
            sig,cls = "STRONG SELL","bear"
        elif chg < -0.3:
            sig,cls = "SELL","bear"
        else:
            sig,cls = "NEUTRAL","neut"
        rsi  = random.randint(30,70)
        sign = "+" if chg >= 0 else ""
        col  = "var(--green)" if chg >= 0 else "var(--red)"
        st.markdown(f"""
        <div class="scan-row">
          <div>
            <div class="scan-sym">{sym}</div>
            <div style="font-size:.65rem;color:var(--dim);font-family:'JetBrains Mono',monospace;margin-top:2px;">RSI {rsi} &nbsp;|&nbsp; Vol: {vol}</div>
          </div>
          <div style="text-align:right;">
            <div class="scan-signal {cls}">{sig}</div>
            <div style="font-size:.68rem;color:{col};font-family:'JetBrains Mono',monospace;margin-top:4px;">{sign}{chg:.2f}%</div>
          </div>
        </div>""", unsafe_allow_html=True)

def pbar(pct, col):
    return f'<div class="prog"><div class="prog-fill" style="width:{pct:.1f}%;background:{col};"></div></div>'

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    render_ig_sidebar()
    nav()
    render_live_ticker()

    st.markdown(f"""
    <div class="hero-v2">
      <div style="margin-bottom:2rem;">
        <img src="{LOGO_URL}" onerror="this.style.display='none'"
             style="height:64px;width:64px;object-fit:contain;" />
      </div>
      <div class="eyebrow"><span class="eyebrow-dot"></span> India's Premier Prop Trading Firm</div>
      <h1>TRADE OUR<br><em>CAPITAL.</em></h1>
      <p class="sub">Pass the challenge. Get funded up to $200,000.<br>Keep up to 90% of your profits. Join 3,500+ funded traders worldwide.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("Start Challenge", use_container_width=True): goto("plans")

    st.markdown("""
    <div class="hstats" style="margin-top:2.5rem;">
      <div class="hstat"><span class="n">$2M+</span><span class="l">Total Payouts</span></div>
      <div class="hstat"><span class="n">3,500+</span><span class="l">Funded Traders</span></div>
      <div class="hstat"><span class="n">180+</span><span class="l">Countries</span></div>
      <div class="hstat"><span class="n">90%</span><span class="l">Profit Split</span></div>
      <div class="hstat"><span class="n">24hr</span><span class="l">Payouts</span></div>
    </div>""", unsafe_allow_html=True)

    # Market snapshot
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3rem 0 .5rem;">LIVE MARKET SNAPSHOT</div><div style="width:30px;height:1px;background:var(--gold);margin-bottom:1.5rem;opacity:.6;"></div>', unsafe_allow_html=True)
    render_market_heatmap()

    # Programs
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;">CHOOSE YOUR PROGRAM</div><div style="width:30px;height:1px;background:var(--gold);margin-bottom:1.5rem;opacity:.6;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div style="background:var(--s1);border:1px solid var(--border);padding:2rem;position:relative;">
          <div style="font-size:.58rem;color:var(--dim);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;">ONE-PHASE</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Target</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">8%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Drawdown</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">8%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Daily Loss</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">4%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Split</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--gold);">80%</div></div>
          </div>
          <div style="font-size:.65rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;">ONE-TIME FEE FROM</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:var(--text);letter-spacing:2px;">$119</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Get One-Phase", use_container_width=True, key="h_1p"):
            st.session_state["selected_phase"] = "one"; goto("plans")

    with col2:
        st.markdown("""
        <div style="background:var(--s1);border:1px solid #3d3260;padding:2rem;position:relative;">
          <div style="position:absolute;top:.8rem;right:.8rem;background:var(--purple);color:#fff;font-size:.52rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;border-radius:2px;">BEST VALUE</div>
          <div style="font-size:.58rem;color:var(--purple);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;">TWO-PHASE</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Phase 1 Target</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">8%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Phase 2 Target</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">5%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Drawdown</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">10%</div></div>
            <div style="background:var(--s2);padding:.8rem 1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Split</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--purple);">90%</div></div>
          </div>
          <div style="font-size:.65rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;">ONE-TIME FEE FROM</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:var(--text);letter-spacing:2px;">$49</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Get Two-Phase", use_container_width=True, key="h_2p"):
            st.session_state["selected_phase"] = "two"; goto("plans")

    # How it works
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;">HOW IT WORKS</div><div style="width:30px;height:1px;background:var(--gold);margin-bottom:1.5rem;opacity:.6;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="steps-grid">
      <div class="step-card"><div class="step-num">01</div><div class="step-title">Choose a Plan</div><div class="step-desc">Select One-Phase or Two-Phase. Account sizes from $10K to $200K. Single payment, no subscriptions.</div></div>
      <div class="step-card"><div class="step-num">02</div><div class="step-title">Pass the Challenge</div><div class="step-desc">Hit the profit target while maintaining drawdown discipline. Trade Forex, Crypto, Indices and Commodities.</div></div>
      <div class="step-card"><div class="step-num">03</div><div class="step-title">Get Funded</div><div class="step-desc">Complete verification and receive your funded account. Real capital, strict rules, 24-hour payouts.</div></div>
      <div class="step-card"><div class="step-num">04</div><div class="step-title">Scale Up</div><div class="step-desc">Keep up to 90% of profits. Scale your account to $2,000,000 with consistent performance.</div></div>
    </div>""", unsafe_allow_html=True)

    # Testimonials
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:2.5rem 0 .5rem;">FUNDED TRADERS</div><div style="width:30px;height:1px;background:var(--gold);margin-bottom:1.5rem;opacity:.6;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="testi-grid">
      <div class="testi-card">
        <div class="testi-quote">Passed the $100K One-Phase challenge in 6 days. Withdrawal processed within 24 hours. The rules are clear and the platform is reliable.</div>
        <div class="testi-name">Rahul S.</div>
        <div class="testi-meta">$100K Funded &nbsp;|&nbsp; +$8,200 payout &nbsp;|&nbsp; One-Phase</div>
      </div>
      <div class="testi-card">
        <div class="testi-quote">The Two-Phase program gave me 90% profit split at a fraction of the cost. Already running my second funded account.</div>
        <div class="testi-name">Priya M.</div>
        <div class="testi-meta">$50K Funded &nbsp;|&nbsp; +$4,500 payout &nbsp;|&nbsp; Two-Phase</div>
      </div>
      <div class="testi-card">
        <div class="testi-quote">Transparent rules, fast payouts, genuine support. AKFunded operates like a professional prop firm, not a side project.</div>
        <div class="testi-name">Kiran T.</div>
        <div class="testi-meta">$25K Funded &nbsp;|&nbsp; 3 challenges completed</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("Start Now", use_container_width=True, key="cta2"): goto("plans")

    footer()

# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "auth":
    render_ig_sidebar()
    nav()
    st.markdown("<br>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.2,1])
    with col:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:4px;color:var(--text);margin-bottom:.3rem;">ACCESS AKFUNDED</div><div style="width:30px;height:1px;background:var(--gold);margin-bottom:1.5rem;opacity:.6;"></div>', unsafe_allow_html=True)
        t1,t2 = st.tabs(["  Sign In  ","  Create Account  "])
        with t1:
            email = st.text_input("Email", placeholder="you@email.com", key="si_e")
            pwd   = st.text_input("Password", type="password", placeholder="Password", key="si_p")
            if st.button("Sign In", use_container_width=True, key="si_btn"):
                if not email or not pwd:
                    st.warning("Enter your email and password.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password({"email":email,"password":pwd})
                        uid = res.user.id
                        prof = db_get_profile(uid)
                        if not prof:
                            db_save_profile(uid, email.split("@")[0], email, "India")
                            prof = db_get_profile(uid)
                        st.session_state.user = {"id":uid,"email":res.user.email,"name":prof.get("name",email.split("@")[0]) if prof else email.split("@")[0]}
                        st.success("Access granted.")
                        time.sleep(0.5); goto("dashboard")
                    except Exception as e:
                        err = str(e)
                        if "Email not confirmed" in err: st.error("Verify your email first.")
                        elif "Invalid login credentials" in err: st.error("Incorrect email or password.")
                        else: st.error(f"Error: {err}")
        with t2:
            name    = st.text_input("Full Name", placeholder="Your Name", key="su_n")
            email2  = st.text_input("Email", placeholder="you@email.com", key="su_e")
            pwd2    = st.text_input("Password", type="password", placeholder="Min 6 characters", key="su_p")
            country = st.selectbox("Country", ["India","USA","UK","UAE","Singapore","Other"])
            if st.button("Create Account", use_container_width=True, key="su_btn"):
                if not name or not email2 or not pwd2: st.warning("Fill in all fields.")
                elif len(pwd2) < 6: st.warning("Password must be at least 6 characters.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email":email2,"password":pwd2})
                        uid = res.user.id
                        db_save_profile(uid, name, email2, country)
                        st.session_state.user = {"id":uid,"email":email2,"name":name}
                        try:
                            supabase.auth.sign_in_with_password({"email":email2,"password":pwd2})
                            st.success("Account created."); time.sleep(1); goto("plans")
                        except:
                            st.success("Account created. Check your email to verify, then sign in.")
                    except Exception as e:
                        err = str(e)
                        if "already registered" in err or "already exists" in err: st.error("Email already registered.")
                        else: st.error(f"Error: {err}")
    footer()

# ══════════════════════════════════════════════════════════════
# PLANS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "plans":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    name = st.session_state.user.get("name","Trader")
    sec(f"CHALLENGE SELECTION", f"One-time fee — no subscription — {name}")

    tab1, tab2 = st.tabs(["  One-Phase Challenge  ","  Two-Phase Challenge  "])

    def render_plan_card(plan, phase):
        r   = RULES.get(plan["slug"], RULES["1phase_10k"])
        hot = plan["capital"] == 100000
        border = "var(--gold)" if hot else "var(--border)"
        pop    = '<div style="position:absolute;top:.6rem;right:.6rem;background:var(--gold);color:#000;font-size:.5rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;border-radius:2px;">POPULAR</div>' if hot else ""
        sc     = "var(--purple)" if phase == 2 else "var(--gold)"
        if phase == 1:
            rules_html = f"""
            <li><span>Profit Target</span><b style="color:var(--green);">+{r['target']}%</b></li>
            <li><span>Max Daily Loss</span><b style="color:var(--red);">-{r['daily_loss']}%</b></li>
            <li><span>Max Drawdown</span><b style="color:var(--red);">-{r['total_loss']}%</b></li>
            <li><span>Min Trading Days</span><b>{r['min_days']} days</b></li>
            <li><span>Profit Split</span><b style="color:{sc};">80%</b></li>
            <li><span>Leverage</span><b>1:100</b></li>"""
        else:
            rules_html = f"""
            <li><span>Phase 1 Target</span><b style="color:var(--green);">+8%</b></li>
            <li><span>Phase 2 Target</span><b style="color:var(--green);">+5%</b></li>
            <li><span>Max Daily Loss</span><b style="color:var(--red);">-{r['daily_loss']}%</b></li>
            <li><span>Max Drawdown</span><b style="color:var(--red);">-{r['total_loss']}%</b></li>
            <li><span>Profit Split</span><b style="color:{sc};">90%</b></li>
            <li><span>Leverage</span><b>1:100</b></li>"""
        st.markdown(f"""
        <div style="background:var(--s1);border:1px solid {border};padding:1.5rem;position:relative;overflow:hidden;">
          {pop}
          <div style="font-size:.55rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.3rem;">Account Size</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;color:var(--gold);letter-spacing:2px;line-height:1;margin-bottom:1.2rem;">{plan['name']}</div>
          <ul class="plan-rules">{rules_html}</ul>
          <div style="border-top:1px solid var(--border);padding-top:.8rem;">
            <div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">One-time fee</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:var(--text);letter-spacing:2px;">${plan['price']}</div>
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"Select ${plan['price']}", key=f"buy_{plan['slug']}", use_container_width=True):
            rz = st.secrets.get("RAZORPAY_KEY_ID","rzp_test_placeholder")
            inr_amount = plan['price'] * 84 * 100
            st.markdown(f"""<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <script>var rzp=new Razorpay({{key:"{rz}",amount:{inr_amount},currency:"INR",name:"AKFunded",
            description:"{plan['name']} {['One','Two'][phase-1]}-Phase",
            prefill:{{email:"{st.session_state.user.get('email','')}"}},
            theme:{{color:"#D4A843"}},
            handler:function(r){{alert("Payment confirmed. Challenge activating.");}}}});rzp.open();</script>""", unsafe_allow_html=True)
            uid   = st.session_state.user["id"]
            ch    = supabase.table("challenges").insert({"user_id":uid,"plan":plan["slug"],"capital":plan["capital"],"status":"active"}).execute()
            ch_id = ch.data[0]["id"]
            supabase.table("accounts").insert({"user_id":uid,"challenge_id":ch_id,"balance":plan["capital"],"initial_capital":plan["capital"],"daily_loss":0,"total_loss":0,"days_traded":0}).execute()
            st.success(f"{plan['name']} {['One','Two'][phase-1]}-Phase activated.")
            st.session_state.pop("selected_phase",None)
            time.sleep(1); goto("dashboard")

    with tab1:
        st.markdown('<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--gold);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.75rem;color:var(--dim);">Single phase — faster path to funding — 80% profit split — no time limit — 24-hour payouts</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_1P):
            with cols[i]: render_plan_card(plan, 1)

    with tab2:
        st.markdown('<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--purple);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.75rem;color:var(--dim);">90% profit split — lower entry fees — two verification phases — scale to $2M — 24-hour payouts</div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_2P):
            with cols[i]: render_plan_card(plan, 2)

    # Compare
    st.markdown('<br><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:3px;color:var(--dim);margin-bottom:1rem;">PROGRAM COMPARISON</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:.8rem 1.2rem;background:var(--s2);font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;font-weight:600;border-bottom:1px solid var(--border);"><span>Feature</span><span style="text-align:center;">One-Phase</span><span style="text-align:center;">Two-Phase</span></div>', unsafe_allow_html=True)
    for feat,v1,v2 in [("Entry Fee","$119 – $799","$49 – $449"),("Profit Target","8%","8% + 5%"),("Max Drawdown","8%","10%"),("Profit Split","80%","90%"),("Phases","1","2"),("Time Limit","None","None"),("Payout Speed","24 hours","24 hours"),("Scale Up To","$2,000,000","$2,000,000")]:
        st.markdown(f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:.65rem 1.2rem;border-bottom:1px solid var(--border);font-size:.78rem;"><span style="color:var(--dim);">{feat}</span><span style="text-align:center;color:var(--text);">{v1}</span><span style="text-align:center;color:var(--purple);">{v2}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    render_live_ticker()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")

    challenge = db_get_active_challenge(uid)
    account   = db_get_account(challenge["id"]) if challenge else None

    if not challenge or not account:
        st.markdown(f"""
        <div style="text-align:center;padding:6rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:5px;color:var(--text);">Welcome, {name.upper()}</div>
          <div style="font-size:.85rem;color:var(--dim);margin:.5rem 0 2rem;font-weight:300;letter-spacing:.5px;">No active challenge. Purchase a plan to begin trading.</div>
        </div>""", unsafe_allow_html=True)
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("Buy a Challenge", use_container_width=True): goto("plans")
        footer(); st.stop()

    balance = float(account.get("balance",0))
    initial = float(account.get("initial_capital",1))
    pnl     = balance - initial
    pnl_pct = (pnl/initial)*100
    days    = int(account.get("days_traded",0))
    r       = RULES.get(challenge["plan"], RULES["pro"])
    all_trades = db_get_trades(uid, challenge["id"], limit=500)
    wr,ap,bt,wt,tt = compute_stats(all_trades)
    win_streak, loss_streak = compute_streaks(all_trades)

    pc = "g" if pnl>=0 else "r"
    ps = "+" if pnl>=0 else ""
    tc = "g" if pnl_pct>=r["target"] else "o"

    # Header
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1.5rem;">
      <div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:4px;color:var(--text);line-height:1;">Trading Dashboard</div>
        <div style="font-size:.72rem;color:var(--dim);margin-top:.3rem;letter-spacing:.5px;">{name} &nbsp;|&nbsp; {challenge['plan'].upper()} &nbsp;|&nbsp; Day {days} of {r['min_days']}</div>
        <div style="width:30px;height:1px;background:var(--gold);margin-top:.6rem;opacity:.6;"></div>
      </div>
      <div style="border:1px solid var(--gold-dim);padding:4px 14px;font-size:.58rem;color:var(--gold);letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">Active</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row" style="margin-bottom:1px;">
      <div class="m-card"><div class="m-label">Account Balance</div><div class="m-val o">₹{balance:,.0f}</div><div class="m-sub">Base: ₹{initial:,.0f}</div></div>
      <div class="m-card"><div class="m-label">Total P&L</div><div class="m-val {pc}">{ps}₹{pnl:,.0f}</div><div class="m-sub">{ps}{pnl_pct:.2f}% return</div></div>
      <div class="m-card"><div class="m-label">Profit Target</div><div class="m-val {tc}">+{r['target']}%</div><div class="m-sub">{ps}{pnl_pct:.2f}% achieved</div></div>
      <div class="m-card"><div class="m-label">Days Traded</div><div class="m-val w">{days} / {r['min_days']}</div><div class="m-sub">Minimum {r['min_days']} required</div></div>
    </div>""", unsafe_allow_html=True)

    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
      <div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>
      <div class="stat-box"><div class="sv {apc}">{aps}₹{ap:,.0f}</div><div class="sl">Avg P&L</div></div>
      <div class="stat-box"><div class="sv g">{win_streak}</div><div class="sl">Win Streak</div></div>
      <div class="stat-box"><div class="sv r">{loss_streak}</div><div class="sl">Loss Streak</div></div>
    </div>""", unsafe_allow_html=True)

    profit_prog = min((pnl_pct/r["target"])*100,100) if r["target"] else 0
    dl_limit = initial*r["daily_loss"]/100; tl_limit = initial*r["total_loss"]/100
    dl_used  = min(abs(account.get("daily_loss",0))/dl_limit*100,100) if dl_limit else 0
    tl_used  = min(abs(account.get("total_loss",0))/tl_limit*100,100) if tl_limit else 0
    dl_cls = "bad" if dl_used>75 else "ok"; tl_cls = "bad" if tl_used>75 else "ok"

    st.markdown(f"""
    <div class="rules-box" style="margin-top:1px;">
      <div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1.2rem;font-weight:600;">Challenge Rules Tracker</div>
      <div class="r-row"><span class="r-name">Profit Target +{r['target']}%</span><span class="r-val ok">{pnl_pct:.2f}% / +{r['target']}% {'— Target Met' if profit_prog>=100 else ''}</span></div>
      {pbar(profit_prog,'var(--green)' if profit_prog>=100 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">Max Daily Loss -{r['daily_loss']}%</span><span class="r-val {dl_cls}">{dl_used:.1f}% of limit consumed</span></div>
      {pbar(dl_used,'var(--red)' if dl_used>75 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">Max Total Loss -{r['total_loss']}%</span><span class="r-val {tl_cls}">{tl_used:.1f}% of limit consumed</span></div>
      {pbar(tl_used,'var(--red)' if tl_used>75 else 'var(--gold)')}
    </div>""", unsafe_allow_html=True)

    col_chart, col_trade = st.columns([2,1], gap="medium")
    with col_chart:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Live Chart — TradingView</div>', unsafe_allow_html=True)
        mkt      = st.selectbox("Market", list(SYMBOLS.keys()), key="mkt")
        sym_list = SYMBOLS[mkt]
        sym_pick = st.selectbox("Symbol", sym_list, key="csym")
        tv_sym   = TV_PREFIX[mkt] + sym_pick
        st.components.v1.html(f"""
        <div style="height:400px;width:100%;">
          <div id="tvc" style="height:100%;width:100%;"></div>
          <script src="https://s3.tradingview.com/tv.js"></script>
          <script>new TradingView.widget({{width:"100%",height:400,symbol:"{tv_sym}",interval:"15",timezone:"Asia/Kolkata",theme:"dark",style:"1",locale:"en",toolbar_bg:"#0d0d0d",enable_publishing:false,container_id:"tvc",backgroundColor:"#050505",gridColor:"rgba(30,30,30,0.6)"}});</script>
        </div>""", height=410)

    with col_trade:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Execute Trade</div>', unsafe_allow_html=True)
        t_sym   = st.selectbox("Symbol", sym_list, key="tsym")
        live_px = get_simulated_price(t_sym)
        t_dir   = st.selectbox("Direction", ["BUY","SELL"], key="ttype")
        t_entry = st.number_input("Entry Price (₹)", min_value=0.01, value=float(live_px), step=0.5, key="tentry")
        t_qty   = st.number_input("Quantity", min_value=1, value=10, step=1, key="tqty")
        t_exit  = st.number_input("Exit Price (₹)", min_value=0.01, value=float(round(live_px*1.02,2)), step=0.5, key="texit")
        t_sl    = st.number_input("Stop Loss (₹)", min_value=0.01, value=float(round(live_px*0.98,2)), step=0.5, key="tsl")

        est        = (t_exit-t_entry)*t_qty if t_dir=="BUY" else (t_entry-t_exit)*t_qty
        risk_trade = abs(t_entry-t_sl)*t_qty
        ec         = "var(--green)" if est>=0 else "var(--red)"
        es         = "+" if est>=0 else ""
        roi        = (est/(t_entry*t_qty))*100 if (t_entry*t_qty)>0 else 0
        rr         = abs(est)/risk_trade if risk_trade>0 else 0

        st.markdown(f"""
        <div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid {ec};padding:1rem;margin:.8rem 0;">
          <div style="font-size:.55rem;color:var(--dim);letter-spacing:2.5px;margin-bottom:4px;text-transform:uppercase;">Estimated P&L</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:{ec};letter-spacing:2px;line-height:1;">{es}₹{est:,.0f}</div>
          <div style="font-size:.68rem;color:{ec};margin-top:4px;font-family:'JetBrains Mono',monospace;">{es}{roi:.2f}% ROI &nbsp;|&nbsp; R:R 1:{rr:.1f}</div>
          <div style="font-size:.65rem;color:var(--red);margin-top:4px;font-family:'JetBrains Mono',monospace;">Risk: ₹{risk_trade:,.0f}</div>
        </div>
        <div style="background:var(--s2);border:1px solid var(--border);padding:.6rem 1rem;margin-bottom:.8rem;display:flex;justify-content:space-between;align-items:center;">
          <div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">Simulated Price</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:1rem;color:var(--gold);">₹{live_px:,.2f}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("Execute Trade", use_container_width=True, key="exec"):
            ch_id   = challenge["id"]
            new_bal = balance + est
            new_tl  = min(0.0, new_bal-initial)
            new_days = days+1
            supabase.table("trades").insert({"user_id":uid,"challenge_id":ch_id,"symbol":t_sym,"type":t_dir,"entry_price":t_entry,"exit_price":t_exit,"quantity":t_qty,"pnl":est,"closed_at":datetime.utcnow().isoformat()}).execute()
            supabase.table("accounts").update({"balance":new_bal,"total_loss":new_tl,"days_traded":new_days,"updated_at":datetime.utcnow().isoformat()}).eq("challenge_id",ch_id).execute()
            new_pct = ((new_bal-initial)/initial)*100
            if new_pct>=r["target"] and new_days>=r["min_days"]:
                supabase.table("challenges").update({"status":"passed"}).eq("id",ch_id).execute()
                push_notification(uid,"","Challenge Passed",f"Profit target of +{r['target']}% achieved. Certificate ready.")
                st.balloons(); st.success("Challenge passed. Certificate available in the Certificate page.")
            elif new_pct<=-r["total_loss"]:
                supabase.table("challenges").update({"status":"failed"}).eq("id",ch_id).execute()
                push_notification(uid,"","Challenge Failed",f"Max total loss of -{r['total_loss']}% reached.")
                st.error("Challenge failed — maximum total loss limit reached.")
            else:
                push_notification(uid,"","Trade Executed",f"{t_dir} {t_sym} — P&L: {es}₹{est:,.0f}")
                if est>=0: st.success(f"Trade executed. P&L: {es}₹{est:,.0f}")
                else: st.warning(f"Trade executed. P&L: ₹{est:,.0f}")
            time.sleep(1); st.rerun()

    # Recent trades
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Recent Trades</div>', unsafe_allow_html=True)
    trades = db_get_trades(uid, challenge["id"], limit=20)
    if trades:
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div class="t-header"><span>Symbol</span><span>Type</span><span>Entry</span><span>Exit</span><span>Qty</span><span>P&L</span></div>', unsafe_allow_html=True)
        for t in trades:
            p=t.get("pnl",0); pc3="var(--green)" if p>=0 else "var(--red)"; ps3="+" if p>=0 else ""
            tag='<span class="tag-b">BUY</span>' if t.get("type")=="BUY" else '<span class="tag-s">SELL</span>'
            dt=t.get("closed_at","")[:10]
            st.markdown(f'<div class="t-row"><span style="font-weight:600;">{t.get("symbol","")} <span style="font-size:.62rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">{dt}</span></span>{tag}<span style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;">₹{t.get("entry_price",0):,.1f}</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;">₹{t.get("exit_price",0):,.1f}</span><span>{t.get("quantity",0)}</span><span style="color:{pc3};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps3}₹{p:,.0f}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:2.5rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;letter-spacing:.5px;">No trades yet. Place your first trade above.</div>', unsafe_allow_html=True)

    # Quick tools
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Quick Access</div>', unsafe_allow_html=True)
    tc1,tc2,tc3,tc4,tc5,tc6 = st.columns(6)
    with tc1:
        if st.button("AI Coach",     use_container_width=True, key="qt_ai"):   goto("ai_chat")
    with tc2:
        if st.button("Risk Calc",    use_container_width=True, key="qt_rc"):   goto("risk_calc")
    with tc3:
        if st.button("Certificate",  use_container_width=True, key="qt_cert"): goto("certificate")
    with tc4:
        if st.button("Refer & Earn", use_container_width=True, key="qt_ref"):  goto("referral")
    with tc5:
        if st.button("Markets",      use_container_width=True, key="qt_mkt"):  goto("markets")
    with tc6:
        if st.button("Analytics",    use_container_width=True, key="qt_an"):   goto("analytics")
    footer()

# ══════════════════════════════════════════════════════════════
# MARKETS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "markets":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    render_live_ticker()
    sec("Live Markets","Simulated prices, signals, order book and watchlist")

    tab_hm, tab_sc, tab_ob, tab_wl = st.tabs(["  Heatmap  ","  Signal Scanner  ","  Order Book  ","  Watchlist  "])

    with tab_hm:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Market Heatmap — All Instruments</div>', unsafe_allow_html=True)
        render_market_heatmap()
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;padding:.8rem 1.2rem;background:var(--s2);font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;font-weight:600;border-bottom:1px solid var(--border);"><span>Symbol</span><span>Price</span><span>Change</span><span>Volume</span><span>Signal</span></div>', unsafe_allow_html=True)
        for sym, data in MARKET_DATA.items():
            chg=data["change"]; col="var(--green)" if chg>=0 else "var(--red)"; sign="+" if chg>=0 else ""
            sig="BUY" if chg>0.5 else ("SELL" if chg<-0.5 else "HOLD")
            sc="bull" if sig=="BUY" else ("bear" if sig=="SELL" else "neut")
            st.markdown(f'<div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;padding:.65rem 1.2rem;border-top:1px solid var(--border);align-items:center;"><span style="font-weight:600;color:var(--text);">{sym}</span><span style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">₹{data["price"]:,.2f}</span><span style="color:{col};font-weight:700;font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">{sign}{chg:.2f}%</span><span style="font-size:.72rem;color:var(--dim);">{data["vol"]}</span><span class="scan-signal {sc}" style="width:fit-content;">{sig}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_sc:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">Signal Scanner — Live Alerts</div>', unsafe_allow_html=True)
        render_signal_scanner()
        st.markdown('<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--gold-dim);padding:.7rem 1rem;margin-top:1rem;font-size:.72rem;color:var(--dim);">Signals are generated using simulated price momentum and volume. Always apply independent risk management.</div>', unsafe_allow_html=True)

    with tab_ob:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">Simulated Order Book</div>', unsafe_allow_html=True)
        ob_sym = st.selectbox("Symbol", list(MARKET_DATA.keys()), key="ob_sym")
        base   = MARKET_DATA[ob_sym]["price"]
        col_bid, col_ask = st.columns(2)
        with col_bid:
            st.markdown('<div style="font-size:.65rem;color:var(--green);letter-spacing:2px;font-weight:600;margin-bottom:.5rem;">BIDS</div><div style="background:var(--s1);border:1px solid var(--border);"><div class="ob-row" style="color:var(--dim);font-size:.58rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);font-weight:600;"><span>Price</span><span>Size</span><span>Total</span></div>', unsafe_allow_html=True)
            for i in range(8):
                px=round(base-(i+1)*base*0.0005,2); sz=random.randint(100,5000)
                st.markdown(f'<div class="ob-row"><span class="ob-bid">₹{px:,.2f}</span><span style="color:var(--text);">{sz:,}</span><span class="ob-vol">₹{px*sz:,.0f}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_ask:
            st.markdown('<div style="font-size:.65rem;color:var(--red);letter-spacing:2px;font-weight:600;margin-bottom:.5rem;">ASKS</div><div style="background:var(--s1);border:1px solid var(--border);"><div class="ob-row" style="color:var(--dim);font-size:.58rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);font-weight:600;"><span>Price</span><span>Size</span><span>Total</span></div>', unsafe_allow_html=True)
            for i in range(8):
                px=round(base+(i+1)*base*0.0005,2); sz=random.randint(100,5000)
                st.markdown(f'<div class="ob-row"><span class="ob-ask">₹{px:,.2f}</span><span style="color:var(--text);">{sz:,}</span><span class="ob-vol">₹{px*sz:,.0f}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;background:var(--s2);border:1px solid var(--border);padding:.8rem;margin-top:1rem;"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:3px;text-transform:uppercase;">Last Price</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:var(--gold);">₹{base:,.2f}</div></div>', unsafe_allow_html=True)

    with tab_wl:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">Watchlist</div>', unsafe_allow_html=True)
        all_syms = [s for g in SYMBOLS.values() for s in g]
        c1,c2 = st.columns([3,1])
        with c1:
            add_sym = st.selectbox("Add symbol", [s for s in all_syms if s not in st.session_state.watchlist], key="wl_add")
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add", use_container_width=True, key="wl_add_btn"):
                st.session_state.watchlist.append(add_sym); st.rerun()
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);padding:.5rem 1rem;">', unsafe_allow_html=True)
        for sym in st.session_state.watchlist:
            data=MARKET_DATA.get(sym,{"price":100.0,"change":0.0,"vol":"N/A"})
            chg=data["change"]; col="var(--green)" if chg>=0 else "var(--red)"; sign="+" if chg>=0 else ""
            st.markdown(f'<div class="wl-row"><div><div style="font-weight:600;color:var(--text);">{sym}</div><div style="font-size:.65rem;color:var(--dim);">{data["vol"]} volume</div></div><div style="font-family:\'JetBrains Mono\',monospace;color:var(--text);font-size:.82rem;">₹{data["price"]:,.2f}</div><div style="font-weight:700;color:{col};font-family:\'JetBrains Mono\',monospace;font-size:.78rem;">{sign}{chg:.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Clear Watchlist", key="wl_clear"):
            st.session_state.watchlist = []; st.rerun()
    footer()

# ══════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "analytics":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid = st.session_state.user["id"]
    sec("Trade Analytics","Deep performance breakdown")

    challenge  = db_get_active_challenge(uid)
    all_trades = db_get_trades(uid, challenge["id"] if challenge else None, limit=500)
    wr,ap,bt,wt,tt = compute_stats(all_trades)
    win_streak, loss_streak = compute_streaks(all_trades)

    if not all_trades:
        st.markdown('<div style="text-align:center;padding:4rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No trades to analyse. Execute some trades first.</div>', unsafe_allow_html=True)
        footer(); st.stop()

    wins=[ t for t in all_trades if t.get("pnl",0)>0 ]
    losses=[t for t in all_trades if t.get("pnl",0)<0]
    gross_profit = sum(t.get("pnl",0) for t in wins)
    gross_loss   = abs(sum(t.get("pnl",0) for t in losses))
    pf           = round(gross_profit/gross_loss,2) if gross_loss>0 else 99.0
    avg_win      = round(gross_profit/len(wins),0)  if wins   else 0
    avg_loss     = round(gross_loss/len(losses),0)  if losses else 0
    expectancy   = round(wr/100*avg_win-(1-wr/100)*avg_loss,2)

    st.markdown(f"""
    <div class="metric-row">
      <div class="m-card"><div class="m-label">Profit Factor</div><div class="m-val {'g' if pf>=1.5 else 'r'}">{pf}x</div><div class="m-sub">{'Strong edge' if pf>=1.5 else 'Needs improvement'}</div></div>
      <div class="m-card"><div class="m-label">Expectancy / Trade</div><div class="m-val {'g' if expectancy>0 else 'r'}">{'+'if expectancy>0 else ''}₹{expectancy:,.0f}</div><div class="m-sub">Expected P&L per trade</div></div>
      <div class="m-card"><div class="m-label">Avg Win</div><div class="m-val g">+₹{avg_win:,.0f}</div><div class="m-sub">{len(wins)} winning trades</div></div>
      <div class="m-card"><div class="m-label">Avg Loss</div><div class="m-val r">-₹{avg_loss:,.0f}</div><div class="m-sub">{len(losses)} losing trades</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv g">{win_streak}</div><div class="sl">Best Win Streak</div></div>
      <div class="stat-box"><div class="sv r">{loss_streak}</div><div class="sl">Worst Loss Streak</div></div>
      <div class="stat-box"><div class="sv g">+₹{bt:,.0f}</div><div class="sl">Best Trade</div></div>
      <div class="stat-box"><div class="sv r">₹{wt:,.0f}</div><div class="sl">Worst Trade</div></div>
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
    </div>""", unsafe_allow_html=True)

    # Symbol breakdown
    sym_pnl={}; sym_cnt={}; sym_wins={}
    for t in all_trades:
        s=t.get("symbol","?"); p=t.get("pnl",0)
        sym_pnl[s]=sym_pnl.get(s,0)+p; sym_cnt[s]=sym_cnt.get(s,0)+1
        sym_wins[s]=sym_wins.get(s,0)+(1 if p>0 else 0)

    st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin:.8rem 0;font-weight:600;">P&L by Symbol</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;padding:.8rem 1.2rem;background:var(--s2);font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;font-weight:600;border-bottom:1px solid var(--border);"><span>Symbol</span><span>Total P&L</span><span>Trades</span><span>Win Rate</span></div>', unsafe_allow_html=True)
    for sym,total in sorted(sym_pnl.items(),key=lambda x:x[1],reverse=True):
        pc=("var(--green)" if total>=0 else "var(--red)"); ps2=("+" if total>=0 else "")
        cnt=sym_cnt.get(sym,1); wr2=round(sym_wins.get(sym,0)/cnt*100,0)
        wrc2="var(--green)" if wr2>=50 else "var(--red)"
        st.markdown(f'<div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;padding:.65rem 1.2rem;border-top:1px solid var(--border);align-items:center;"><span style="font-weight:600;color:var(--text);">{sym}</span><span style="color:{pc};font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">{ps2}₹{total:,.0f}</span><span style="color:var(--text);">{cnt}</span><span style="color:{wrc2};font-weight:700;">{wr2:.0f}%</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    buys=[ t for t in all_trades if t.get("type")=="BUY" ]
    sells=[t for t in all_trades if t.get("type")=="SELL"]
    buy_pnl=sum(t.get("pnl",0) for t in buys); sell_pnl=sum(t.get("pnl",0) for t in sells)
    col1,col2 = st.columns(2)
    with col1:
        pc="g" if buy_pnl>=0 else "r"
        st.markdown(f'<div class="m-card" style="margin-top:1rem;"><div class="m-label">BUY Trades ({len(buys)})</div><div class="m-val {pc}">{"+"if buy_pnl>=0 else ""}₹{buy_pnl:,.0f}</div><div class="m-sub">Total P&L from long positions</div></div>', unsafe_allow_html=True)
    with col2:
        pc="g" if sell_pnl>=0 else "r"
        st.markdown(f'<div class="m-card" style="margin-top:1rem;"><div class="m-label">SELL Trades ({len(sells)})</div><div class="m-val {pc}">{"+"if sell_pnl>=0 else ""}₹{sell_pnl:,.0f}</div><div class="m-sub">Total P&L from short positions</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PORTFOLIO
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "portfolio":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")
    sec("Portfolio Overview","Performance across all challenges")

    all_trades=db_get_trades(uid,limit=500); all_challenges=db_get_all_challenges(uid)
    wr,ap,bt,wt,tt=compute_stats(all_trades)
    passed=sum(1 for c in all_challenges if c.get("status")=="passed")
    failed=sum(1 for c in all_challenges if c.get("status")=="failed")

    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
      <div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>
      <div class="stat-box"><div class="sv {apc}">{aps}₹{ap:,.0f}</div><div class="sl">Avg P&L</div></div>
      <div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed</div></div>
      <div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed</div></div>
    </div>""", unsafe_allow_html=True)

    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    if challenge and account:
        bal=account["balance"]; init=account["initial_capital"]; p=bal-init; pp=(p/init)*100
        r=RULES.get(challenge["plan"],RULES["pro"]); pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
        st.markdown(f"""
        <div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin:1rem 0 .5rem;font-weight:600;">Active Challenge</div>
        <div style="background:var(--s1);border:1px solid var(--gold-dim);border-left:2px solid var(--gold);padding:1.8rem 2rem;margin-bottom:1.5rem;">
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;">
            <div><div class="m-label">Plan</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--gold);">{challenge['plan'].upper()}</div></div>
            <div><div class="m-label">Balance</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--text);">₹{bal:,.0f}</div></div>
            <div><div class="m-label">P&L</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:{pc};">{ps}₹{p:,.0f}</div></div>
            <div><div class="m-label">Progress</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:{'var(--green)' if pp>=r['target'] else 'var(--gold)'};">{ps}{pp:.1f}% / +{r['target']}%</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

    if all_trades:
        sym_pnl={}
        for t in all_trades:
            s=t.get("symbol","?"); sym_pnl[s]=sym_pnl.get(s,0)+t.get("pnl",0)
        top5=sorted(sym_pnl.items(),key=lambda x:x[1],reverse=True)[:5]
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Top Symbols by P&L</div>', unsafe_allow_html=True)
        cols=st.columns(len(top5)) if top5 else st.columns(1)
        for i,(sym,pval) in enumerate(top5):
            with cols[i]:
                pc2="var(--green)" if pval>=0 else "var(--red)"; ps2="+" if pval>=0 else ""
                st.markdown(f'<div class="stat-box"><div class="sv" style="color:{pc2};font-size:1.3rem;">{ps2}₹{pval:,.0f}</div><div class="sl">{sym}</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# JOURNAL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "journal":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]; challenge=db_get_active_challenge(uid)
    sec("Trade Journal","Document your setups, outcomes and decisions")

    with st.expander("Add New Entry", expanded=True):
        ca,cb = st.columns(2)
        with ca:
            j_sym=st.selectbox("Symbol",[s for g in SYMBOLS.values() for s in g],key="jsym")
            j_out=st.selectbox("Outcome",["WIN","LOSS","BREAKEVEN"],key="jout")
        with cb:
            j_setup=st.text_input("Setup / Pattern",placeholder="e.g. Breakout retest",key="jsetup")
            j_emo=st.selectbox("Emotional State",["Calm","Confident","Anxious","Greedy","Fearful","FOMO"],key="jemo")
        j_note=st.text_area("Journal Note",placeholder="What did you observe? Why did you enter? What would you improve?",height=100,key="jnote")
        if st.button("Save Entry",use_container_width=True,key="jsave"):
            if j_note.strip():
                try:
                    supabase.table("journal_entries").insert({"user_id":uid,"challenge_id":challenge["id"] if challenge else None,"symbol":j_sym,"outcome":j_out.lower(),"setup":j_setup,"emotion":j_emo,"note":j_note,"created_at":datetime.utcnow().isoformat()}).execute()
                    st.success("Entry saved."); time.sleep(1); st.rerun()
                except Exception as e: st.error(f"Error: {e}")
            else: st.warning("Write a note before saving.")

    st.markdown("<br>", unsafe_allow_html=True)
    entries=db_get_journal(uid)
    if entries:
        for e in entries:
            out=e.get("outcome",""); tc="win" if out=="win" else ("loss" if out=="loss" else "")
            tl=out.upper()
            dt=e.get("created_at","")[:10]
            setup_tag=f'<span class="je-tag">{e["setup"]}</span>' if e.get("setup") else ""
            st.markdown(f'<div class="journal-entry"><div class="je-date">{dt} &nbsp;|&nbsp; {e.get("symbol","")} &nbsp;|&nbsp; {e.get("emotion","")}</div><div class="je-note">{e.get("note","")}</div><div class="je-tags"><span class="je-tag {tc}">{tl}</span>{setup_tag}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No entries yet. Log your first trade above.</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]
    sec("Challenge History","All past and active challenge attempts")

    all_ch=db_get_all_challenges(uid)
    if not all_ch:
        st.markdown('<div style="text-align:center;padding:4rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No challenges yet.</div>', unsafe_allow_html=True)
        _,c,_=st.columns([2,1,2])
        with c:
            if st.button("Buy a Plan",use_container_width=True): goto("plans")
    else:
        total=len(all_ch); passed=sum(1 for c in all_ch if c.get("status")=="passed")
        failed=sum(1 for c in all_ch if c.get("status")=="failed"); active=sum(1 for c in all_ch if c.get("status")=="active")
        st.markdown(f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border);"><div class="stat-box"><div class="sv w">{total}</div><div class="sl">Total</div></div><div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed</div></div><div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed</div></div><div class="stat-box"><div class="sv o">{active}</div><div class="sl">Active</div></div></div>', unsafe_allow_html=True)
        for ch in all_ch:
            acc=db_get_account(ch["id"]) or {}; cap=ch.get("capital",0); bal=acc.get("balance",cap)
            p=bal-cap; pp=(p/cap*100) if cap else 0; status=ch.get("status","active"); d=acc.get("days_traded",0)
            cap_str=f"${cap//1000}K"; date_str=ch.get("started_at","")[:10]
            pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
            st.markdown(f'<div class="ch-card"><div><div class="ch-plan">{ch.get("plan","").upper()}</div><div style="font-size:.68rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">{cap_str} &nbsp;|&nbsp; {date_str}</div></div><div style="font-size:.8rem;">Balance: <b style="color:var(--text);">₹{bal:,.0f}</b></div><div style="font-size:.8rem;color:{pc};">P&L: <b>{ps}₹{p:,.0f} ({ps}{pp:.1f}%)</b></div><div style="font-size:.8rem;color:var(--dim);">Days: <b style="color:var(--text);">{d}</b></div><div class="ch-status {status}">{status.upper()}</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "leaderboard":
    render_ig_sidebar()
    nav()
    sec("Leaderboard","Top traders ranked by profit percentage — live")

    data=db_get_leaderboard()
    if not data:
        data=[
            {"name":"Rahul S.","country":"India","profit_pct":18.4,"status":"passed","plan":"elite"},
            {"name":"Priya M.","country":"India","profit_pct":15.2,"status":"passed","plan":"pro"},
            {"name":"Kiran T.","country":"India","profit_pct":12.7,"status":"active","plan":"pro"},
            {"name":"Arun K.","country":"India","profit_pct":11.1,"status":"passed","plan":"starter"},
            {"name":"Sneha R.","country":"India","profit_pct":9.8, "status":"active","plan":"pro"},
        ]
    medals=["01","02","03"]
    for i,t in enumerate(data):
        rank=i+1; medal=medals[i] if i<3 else f"{rank:02d}"
        rc="top" if rank<=3 else ""; funded=t.get("status")=="passed"
        bc="funded-b" if funded else "active-b"; bt2="Funded" if funded else "Active"
        profit=t.get("profit_pct",0)
        st.markdown(f'<div class="lb-item"><div class="lb-rank {rc}">{medal}</div><div class="lb-info"><div class="lb-name">{t.get("name","Trader")}</div><div class="lb-country">{t.get("country","")} &nbsp;|&nbsp; {t.get("plan","").upper()}</div></div><div class="lb-pnl">+{profit:.2f}%</div><div class="lb-badge {bc}">{bt2}</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PROFILE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]; email=st.session_state.user.get("email","")
    prof=db_get_profile(uid) or {}
    name=prof.get("name",email.split("@")[0]); country=prof.get("country","India"); bio=prof.get("bio","")
    all_challenges=db_get_all_challenges(uid); all_trades=db_get_trades(uid,limit=500)
    wr,ap,bt,wt,tt=compute_stats(all_trades)
    passed=sum(1 for c in all_challenges if c.get("status")=="passed")
    failed=sum(1 for c in all_challenges if c.get("status")=="failed")
    funded_badge=passed>0
    initials="".join([w[0].upper() for w in name.split()[:2]])

    sec("My Profile","Trader identity and performance summary")

    badge_html='<div class="funded-badge-inline">Funded Trader</div>' if funded_badge else ""
    st.markdown(f"""
    <div class="profile-hero">
      <div class="profile-avatar">{initials}</div>
      <div>
        <div class="profile-name">{name.upper()}</div>
        <div class="profile-email">{email}</div>
        <div style="font-size:.68rem;color:var(--dim);margin-top:4px;letter-spacing:.5px;">{country}</div>
        {badge_html}
      </div>
      <div style="margin-left:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;text-align:center;">
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--gold);">{tt}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Trades</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:{'var(--green)' if wr>=50 else 'var(--red)'};">{wr:.0f}%</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Win Rate</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--green);">{passed}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Passed</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--red);">{failed}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Failed</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    with st.form("edit_profile"):
        c1,c2=st.columns(2)
        with c1:
            new_name=st.text_input("Full Name",value=name,key="pf_name")
            new_country=st.text_input("Country",value=country,key="pf_country")
        with c2:
            new_bio=st.text_area("Bio",value=bio,placeholder="e.g. Nifty scalper. Disciplined risk manager.",height=100,key="pf_bio")
        if st.form_submit_button("Save Profile",use_container_width=True):
            if db_update_profile(uid,new_name,new_country,new_bio):
                st.session_state.user["name"]=new_name
                st.success("Profile saved."); time.sleep(1); st.rerun()
            else: st.error("Save failed — ensure 'bio' column exists in profiles table.")

    col_a,col_b=st.columns(2)
    with col_a:
        st.markdown(f'<div class="m-card"><div class="m-label">Email</div><div style="font-size:.85rem;color:var(--text);margin-top:4px;font-family:\'JetBrains Mono\',monospace;">{email}</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="m-card"><div class="m-label">Member Since</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--gold);">{all_challenges[-1].get("started_at","")[:7] if all_challenges else "New"}</div></div>', unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        if st.button("Sign Out",use_container_width=True,key="profile_logout"):
            supabase.auth.sign_out(); st.session_state.user=None; st.session_state.notifications=[]; goto("home")
    with c2:
        if st.button("Send Test Email",use_container_width=True,key="test_email"):
            ok=send_email_with_certificate(email,"AKFunded — Email Configured",f'<div style="font-family:Arial,sans-serif;background:#050505;color:#D8D8D8;padding:2rem;max-width:500px;"><h2 style="color:#D4A843;">AKFUNDED</h2><p>Email is working correctly, {name}.</p></div>')
            if ok: st.success(f"Test email sent to {email}.")
            else: st.error("Failed — configure SMTP_EMAIL and SMTP_PASSWORD in secrets.")
    footer()

# ══════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "notifications":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]
    sec("Notifications","Trade alerts, challenge updates and system messages")

    notifs=[n for n in st.session_state.notifications if n.get("uid")==uid]
    col_a,col_b=st.columns([4,1])
    with col_b:
        if st.button("Mark All Read",key="mark_read"):
            for n in st.session_state.notifications: n["unread"]=False
            st.rerun()

    if not notifs:
        st.markdown('<div style="text-align:center;padding:4rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No notifications yet. They appear when you trade or when challenge status changes.</div>', unsafe_allow_html=True)
    else:
        for n in notifs:
            uc="unread" if n.get("unread") else ""
            st.markdown(f'<div class="notif-item {uc}"><div class="notif-body"><div class="notif-title">{n.get("title","Notification")}{"<span class=\'notif-badge\'>NEW</span>" if n.get("unread") else ""}</div><div class="notif-msg">{n.get("msg","")}</div><div class="notif-time">{n.get("time","")}</div></div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":
    if not st.session_state.user: goto("auth")
    if st.session_state.user.get("email","") != st.secrets.get("ADMIN_EMAIL","admin@akfunded.com"):
        st.error("Access denied."); st.stop()
    render_ig_sidebar()
    nav()
    sec("Admin Panel","Platform overview — all traders and challenges")

    all_data=db_get_all_accounts()
    total_traders=len(set(r["user_id"] for r in all_data)); total_ch=len(all_data)
    total_passed=sum(1 for r in all_data if r["status"]=="passed")
    total_active=sum(1 for r in all_data if r["status"]=="active")
    total_failed=sum(1 for r in all_data if r["status"]=="failed")
    total_capital=sum(r["capital"] for r in all_data)

    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border);"><div class="stat-box"><div class="sv w">{total_traders}</div><div class="sl">Traders</div></div><div class="stat-box"><div class="sv w">{total_ch}</div><div class="sl">Challenges</div></div><div class="stat-box"><div class="sv o">{total_active}</div><div class="sl">Active</div></div><div class="stat-box"><div class="sv g">{total_passed}</div><div class="sl">Passed</div></div><div class="stat-box"><div class="sv r">{total_failed}</div><div class="sl">Failed</div></div><div class="stat-box"><div class="sv o">${total_capital//1000}K</div><div class="sl">Capital</div></div></div>', unsafe_allow_html=True)

    search=st.text_input("Search by name or email",placeholder="Filter...",key="admin_search")
    status_filter=st.selectbox("Status filter",["All","active","passed","failed"],key="admin_status")
    filtered=all_data
    if search: filtered=[r for r in filtered if search.lower() in r["name"].lower() or search.lower() in r["email"].lower()]
    if status_filter!="All": filtered=[r for r in filtered if r["status"]==status_filter]
    st.markdown(f'<div style="font-size:.68rem;color:var(--dim);margin-bottom:.8rem;">{len(filtered)} results</div>', unsafe_allow_html=True)

    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div class="admin-row header"><span>Trader</span><span>Plan</span><span>Balance</span><span>P&L %</span><span>Days</span><span>Status</span></div>', unsafe_allow_html=True)
    for r in filtered[:50]:
        pc="var(--green)" if r["pnl_pct"]>=0 else "var(--red)"; ps="+" if r["pnl_pct"]>=0 else ""
        cap_str=f"${r['capital']//1000}K"
        st.markdown(f'<div class="admin-row"><div><div style="font-weight:600;color:var(--text);">{r["name"]}</div><div style="font-size:.65rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">{r["email"]}</div></div><div style="color:var(--gold);font-size:.75rem;">{r["plan"].upper()} ({cap_str})</div><div style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">₹{r["balance"]:,.0f}</div><div style="color:{pc};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps}{r["pnl_pct"]:.2f}%</div><div style="color:var(--text);">{r["days_traded"]}</div><div class="admin-status {r["status"]}">{r["status"].upper()}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# AI CHAT
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "ai_chat":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]; name=st.session_state.user.get("name","Trader")
    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    trades=db_get_trades(uid,challenge["id"] if challenge else None,limit=10)
    balance=account.get("balance",0) if account else 0; initial=account.get("initial_capital",1) if account else 1
    pnl_pct=((balance-initial)/initial*100) if initial else 0; plan=challenge.get("plan","") if challenge else ""

    SYSTEM=f"""You are a professional AI trading coach for AKFunded, a prop trading simulator.
Trader: {name}, {plan.upper()} challenge. P&L: {pnl_pct:.1f}%. Balance: {balance:,.0f}.
Recent: {[t.get('symbol','')+' '+t.get('type','')+' '+str(t.get('pnl',0)) for t in trades[:5]]}.
Give concise, professional trading advice. Focus on risk management, discipline, passing the challenge, and technical analysis for Indian markets.
Keep replies under 130 words. Be direct. No filler phrases."""

    sec("AI Trading Coach","Powered by Groq — LLaMA 3.3 70B")

    st.markdown('<div class="chat-container"><div class="chat-header"><div class="chat-ai-dot"></div><div><div style="font-weight:600;font-size:.85rem;color:var(--text);">AK Trading Coach</div><div style="font-size:.65rem;color:var(--green);letter-spacing:1px;">Online — LLaMA 3.3 70B via Groq</div></div></div></div>', unsafe_allow_html=True)

    chat=st.session_state.chat_history
    if not chat:
        st.markdown(f'<div class="chat-messages"><div class="chat-msg"><div class="chat-avatar ai">AI</div><div class="chat-bubble ai">Hello {name}. I have visibility into your challenge data. Ask me about risk management, trade setups, drawdown recovery, or how to pass your challenge efficiently.</div></div></div>', unsafe_allow_html=True)
    else:
        msgs_html=""
        for m in chat[-10:]:
            role=m["role"]; txt=m["content"]; cls="user" if role=="user" else "ai"
            av=name[0].upper() if role=="user" else "AI"
            msgs_html+=f'<div class="chat-msg {cls}"><div class="chat-avatar {cls}">{av}</div><div class="chat-bubble {cls}">{txt}</div></div>'
        st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)

    quick=["Risk management","Should I trade today?","How to pass faster","Recovering from drawdown","Nifty setup guide"]
    qcols=st.columns(len(quick))
    for i,q in enumerate(quick):
        with qcols[i]:
            if st.button(q,key=f"qp_{i}",use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Processing..."):
                    resp=call_ai(st.session_state.chat_history,SYSTEM)
                st.session_state.chat_history.append({"role":"assistant","content":resp}); st.rerun()

    user_input=st.text_input("Message",placeholder="Ask your coach anything...",key="chat_input",label_visibility="collapsed")
    c1,c2=st.columns([5,1])
    with c2:
        send=st.button("Send",use_container_width=True,key="chat_send")
    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner("Processing..."):
            resp=call_ai(st.session_state.chat_history,SYSTEM)
        st.session_state.chat_history.append({"role":"assistant","content":resp}); st.rerun()

    if st.button("Clear Conversation",key="clear_chat"):
        st.session_state.chat_history=[]; st.rerun()
    footer()

# ══════════════════════════════════════════════════════════════
# RISK CALCULATOR
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "risk_calc":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]
    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    balance=float(account.get("balance",100000)) if account else 100000.0
    sec("Risk Calculator","Position sizing, R:R analysis and challenge limits")

    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Position Size Calculator</div>', unsafe_allow_html=True)
        acc_size=st.number_input("Account Balance (₹)",value=balance,min_value=1000.0,step=1000.0,key="rc_bal")
        risk_pct=st.slider("Risk per trade (%)",0.1,5.0,1.0,0.1,key="rc_risk")
        entry_p=st.number_input("Entry Price (₹)",value=100.0,min_value=0.01,step=0.5,key="rc_entry")
        stop_loss=st.number_input("Stop Loss (₹)",value=97.0,min_value=0.01,step=0.5,key="rc_sl")
        target_p=st.number_input("Target Price (₹)",value=106.0,min_value=0.01,step=0.5,key="rc_tp")

        risk_amt=acc_size*risk_pct/100; sl_dist=abs(entry_p-stop_loss); tp_dist=abs(target_p-entry_p)
        qty=int(risk_amt/sl_dist) if sl_dist>0 else 0; reward_amt=qty*tp_dist
        rr_ratio=tp_dist/sl_dist if sl_dist>0 else 0; margin=qty*entry_p
        rc="var(--green)" if rr_ratio>=2 else ("var(--gold)" if rr_ratio>=1 else "var(--red)")
        st.markdown(f"""
        <div class="risk-card" style="margin-top:1rem;">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);">
            <div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Position Size</div><div class="risk-val" style="color:var(--gold);">{qty:,}</div><div style="font-size:.65rem;color:var(--dim);">shares / lots</div></div>
            <div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Risk Amount</div><div class="risk-val" style="color:var(--red);">₹{risk_amt:,.0f}</div><div style="font-size:.65rem;color:var(--dim);">{risk_pct}% of account</div></div>
            <div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Reward</div><div class="risk-val" style="color:var(--green);">₹{reward_amt:,.0f}</div><div style="font-size:.65rem;color:var(--dim);">if target hit</div></div>
            <div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">R:R Ratio</div><div class="risk-val" style="color:{rc};">1:{rr_ratio:.1f}</div><div style="font-size:.65rem;color:var(--dim);">{'Acceptable' if rr_ratio>=2 else 'Marginal' if rr_ratio>=1 else 'Poor'}</div></div>
          </div>
          <div style="margin-top:1px;padding:.8rem;background:var(--s2);font-size:.72rem;color:var(--dim);font-family:'JetBrains Mono',monospace;">
            Capital required: ₹{margin:,.0f} &nbsp;|&nbsp; SL: ₹{sl_dist:.2f} &nbsp;|&nbsp; TP: ₹{tp_dist:.2f}
          </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Challenge Risk Limits</div>', unsafe_allow_html=True)
        if challenge and account:
            r=RULES.get(challenge["plan"],RULES["pro"]); init=float(account.get("initial_capital",1))
            daily_lim=init*r["daily_loss"]/100; total_lim=init*r["total_loss"]/100
            daily_rem=daily_lim-abs(account.get("daily_loss",0)); total_rem=total_lim-abs(account.get("total_loss",0))
            trades_needed=max(0,r["min_days"]-account.get("days_traded",0))
            st.markdown(f"""
            <div class="risk-card">
              <div style="margin-bottom:1.2rem;"><div class="m-label">Daily Loss Remaining</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{'var(--green)' if daily_rem>daily_lim*0.5 else 'var(--red)'};">₹{daily_rem:,.0f}</div><div style="font-size:.65rem;color:var(--dim);font-family:'JetBrains Mono',monospace;">of ₹{daily_lim:,.0f}</div></div>
              <div style="margin-bottom:1.2rem;"><div class="m-label">Total Loss Remaining</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{'var(--green)' if total_rem>total_lim*0.5 else 'var(--red)'};">₹{total_rem:,.0f}</div><div style="font-size:.65rem;color:var(--dim);font-family:'JetBrains Mono',monospace;">of ₹{total_lim:,.0f}</div></div>
              <div><div class="m-label">Days Remaining</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--gold);">{trades_needed}</div><div style="font-size:.65rem;color:var(--dim);">more days required to pass</div></div>
            </div>""", unsafe_allow_html=True)
            safe_risk=min(daily_rem*0.25,total_rem*0.1)
            st.markdown(f'<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--green);padding:1rem;margin-top:1px;"><div class="m-label">Recommended Max Risk / Trade</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:var(--green);">₹{safe_risk:,.0f}</div><div style="font-size:.65rem;color:var(--dim);">Protects both daily and total loss limits</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:var(--dim);padding:2rem;text-align:center;background:var(--s1);border:1px solid var(--border);font-size:.8rem;">Purchase a challenge to see your risk limits.</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# CERTIFICATE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "certificate":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]; name=st.session_state.user.get("name","Trader")
    sec("Achievement Certificate","Official funded trader certificate")

    all_ch=db_get_all_challenges(uid); passed_ch=[c for c in all_ch if c.get("status")=="passed"]

    if not passed_ch:
        st.markdown('<div style="text-align:center;padding:5rem;background:var(--s1);border:1px solid var(--border);"><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:4px;color:var(--dim);margin-bottom:.5rem;">No Certificate Yet</div><div style="font-size:.8rem;color:var(--dim);font-weight:300;">Pass a challenge to earn your funded trader certificate.</div></div>', unsafe_allow_html=True)
        _,c,_=st.columns([2,1,2])
        with c:
            if st.button("Buy a Challenge",use_container_width=True): goto("plans")
    else:
        if len(passed_ch)>1:
            ch_options=[f"{c['plan'].upper()} — {c.get('started_at','')[:10]}" for c in passed_ch]
            selected=st.selectbox("Select Challenge",ch_options,key="cert_sel")
            ch=passed_ch[ch_options.index(selected)]
        else:
            ch=passed_ch[0]

        acc=db_get_account(ch["id"]) or {}
        cap=ch.get("capital",0); bal=acc.get("balance",cap)
        pnl_pct=(bal-cap)/cap*100 if cap else 0
        days=acc.get("days_traded",0); date_str=ch.get("started_at","")[:10]

        # Display certificate
        cert_html = build_certificate_html(name, ch["plan"], cap, pnl_pct, days, date_str)
        st.markdown(cert_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Email Certificate", use_container_width=True, key="email_cert"):
                email_addr = st.session_state.user.get("email","")
                cert_email_html = build_certificate_email_html(name, ch["plan"], cap, pnl_pct, days, date_str)
                ok = send_email_with_certificate(
                    email_addr,
                    f"AKFunded — Certificate of Achievement",
                    cert_email_html
                )
                if ok:
                    st.success(f"Certificate emailed to {email_addr}. Check your inbox.")
                else:
                    st.info("Configure SMTP_EMAIL and SMTP_PASSWORD in secrets to enable email.")
        with col2:
            if st.button("Copy Share Text", use_container_width=True, key="share_cert"):
                cap_str = f"${cap//1000}K"
                share = f"I passed the AKFunded {ch['plan'].upper()} Challenge ({cap_str}) with +{pnl_pct:.1f}% profit in {days} trading days. @akfunded #AKFunded #PropTrading"
                st.code(share, language=None)
        with col3:
            if st.button("Share on Instagram", use_container_width=True, key="ig_cert"):
                st.markdown(f'<a href="{IG_URL}" target="_blank" style="color:var(--gold);">Open Instagram @akfunded to share your win!</a>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--gold-dim);padding:1rem 1.4rem;margin-top:1rem;">
          <div style="font-size:.72rem;color:var(--dim);line-height:1.7;">
            Your certificate has been issued and can be emailed directly to your inbox for download and sharing.
            Tag <b style="color:var(--gold);">@akfunded</b> on Instagram when you share your achievement.
          </div>
        </div>""", unsafe_allow_html=True)

    footer()

# ══════════════════════════════════════════════════════════════
# REFERRAL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "referral":
    if not st.session_state.user: goto("auth")
    render_ig_sidebar()
    nav()
    uid=st.session_state.user["id"]; name=st.session_state.user.get("name","Trader"); email=st.session_state.user.get("email","")
    sec("Refer & Earn","Invite traders — earn rewards when they purchase a challenge")

    ref=db_get_referral(uid)
    if not ref:
        code=generate_referral_code(name); db_create_referral(uid,code)
        ref=db_get_referral(uid) or {"code":code,"uses":0}

    code=ref.get("code",""); uses=ref.get("uses",0); earnings=uses*50

    st.markdown(f"""
    <div style="background:var(--s1);border:1px solid var(--border);border-left:2px solid var(--gold);padding:2rem;margin-bottom:1.5rem;">
      <div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Your Referral Code</div>
      <div class="ref-code-box">
        <div class="ref-code">{code}</div>
        <div style="font-size:.65rem;color:var(--dim);">Unique code</div>
      </div>
      <div class="ref-stats">
        <div class="stat-box"><div class="sv o">{uses}</div><div class="sl">Referrals</div></div>
        <div class="stat-box"><div class="sv g">₹{earnings}</div><div class="sl">Earned</div></div>
        <div class="stat-box"><div class="sv w">₹50</div><div class="sl">Per Referral</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    share_url=f"https://akfunded.streamlit.app/?ref={code}"
    share_text=f"Join AKFunded — prop trading simulator. Use code {code}. {share_url}"
    st.code(share_url,language=None)

    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("Copy Link",use_container_width=True,key="copy_link"):
            st.code(share_url); st.success("Copy the link above.")
    with c2:
        wa=f"https://wa.me/?text={share_text.replace(' ','%20')}"
        st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%;background:var(--gold);color:#000;font-weight:700;border:none;padding:.55rem;font-family:\'Space Grotesk\',sans-serif;cursor:pointer;letter-spacing:1px;font-size:.75rem;text-transform:uppercase;">Share on WhatsApp</button></a>', unsafe_allow_html=True)
    with c3:
        if st.button("Email Invite",use_container_width=True,key="email_invite"):
            html_invite=f"""<div style="font-family:Arial,sans-serif;max-width:580px;background:#050505;color:#D8D8D8;padding:2rem;">
              <h2 style="color:#D4A843;letter-spacing:4px;">AKFUNDED</h2>
              <p>{name} has invited you to AKFunded.</p>
              <div style="background:#0d0d0d;border-left:2px solid #D4A843;padding:1rem;margin:1rem 0;">
                <div style="font-size:1.4rem;font-weight:700;color:#D4A843;letter-spacing:4px;">{code}</div>
                <div style="font-size:.75rem;color:#505050;margin-top:4px;">Use this referral code</div>
              </div>
              <p style="color:#505050;font-size:.82rem;"><a href="{share_url}" style="color:#D4A843;">Join here</a></p>
            </div>"""
            ok=send_email_with_certificate(email,f"{name} invited you to AKFunded",html_invite)
            if ok: st.success("Invite sent.")
            else: st.info("Configure SMTP settings to send invites.")

    st.markdown("""
    <br>
    <div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">How Referrals Work</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--border);">
      <div class="stat-box" style="text-align:left;padding:1.4rem;">
        <div style="font-size:.72rem;color:var(--gold);font-weight:700;margin-bottom:.4rem;letter-spacing:.5px;">Share Your Code</div>
        <div style="font-size:.75rem;color:var(--dim);font-weight:300;line-height:1.7;">Send your referral link to traders in your network.</div>
      </div>
      <div class="stat-box" style="text-align:left;padding:1.4rem;">
        <div style="font-size:.72rem;color:var(--gold);font-weight:700;margin-bottom:.4rem;letter-spacing:.5px;">They Purchase</div>
        <div style="font-size:.75rem;color:var(--dim);font-weight:300;line-height:1.7;">When they buy any challenge plan using your code.</div>
      </div>
      <div class="stat-box" style="text-align:left;padding:1.4rem;">
        <div style="font-size:.72rem;color:var(--gold);font-weight:700;margin-bottom:.4rem;letter-spacing:.5px;">You Earn ₹50</div>
        <div style="font-size:.75rem;color:var(--dim);font-weight:300;line-height:1.7;">₹50 credited per successful referral purchase.</div>
      </div>
    </div>""", unsafe_allow_html=True)
    footer()
