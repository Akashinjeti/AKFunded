import streamlit as st
import streamlit.components.v1 as _stc
from supabase import create_client
import time, random, string, smtplib, base64, io
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="AKFunded — Trade Crypto. Get Funded.",
    page_icon="https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.PNG",
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
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&family=Caveat:wght@500;600;700&display=swap');

:root {
  --gold:#D4AF37; /* Royal Gold */
  --gold-dim:#40350a;
  --gold-glow:rgba(212, 175, 55, 0.25);
  --black:#030303; /* Royal Black */
  --s0:#080808;
  --s1:rgba(18, 18, 18, 0.65); /* Glass Black */
  --s2:rgba(25, 25, 25, 0.75);
  --s3:rgba(35, 35, 35, 0.85);
  --border:rgba(212, 175, 55, 0.2); 
  --border2:rgba(212, 175, 55, 0.35);
  --border3:rgba(212, 175, 55, 0.5);
  --text:#f9f9f9;
  --dim:#a3a3a3;
  --dim2:#666666;
  --green:#00c853; /* Success Green */
  --green-dim:rgba(0, 200, 83, 0.15);
  --red:#ff3d00; /* Danger Red */
  --red-dim:rgba(255, 61, 0, 0.15);
  --purple:#F4D03F; /* Bright Gold */
  --blue:#E5B80B;
  --cyan:#F3E5AB; /* Vanilla Gold Accent */
  --cyan-dim:rgba(243, 229, 171, 0.15);
  --neon:#FFDF00; /* Pure Gold */
}

html, body {
  background:#030303!important;
  font-family:'Rajdhani',sans-serif;
}
[class*="css"],.main,.stApp,.stApp>div,section.main,
div[data-testid="stAppViewContainer"],div[data-testid="stHeader"],
div[data-testid="stToolbar"],div[data-testid="stDecoration"],
div[data-testid="stBottom"],.appview-container,.reportview-container,
.main .block-container,iframe {
  background-color:#050505!important;background:#050505!important;
}
* { font-family:'Rajdhani',sans-serif; color:var(--text); }
#MainMenu,footer,header { visibility:hidden!important;display:none!important; }
.block-container { padding:1rem 2.5rem 3rem!important;max-width:1400px!important; }
::-webkit-scrollbar { width:2px; }
::-webkit-scrollbar-thumb { background:var(--gold-dim); }

body::after {
  content:'';
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.03) 2px,rgba(0,0,0,.03) 4px);
  pointer-events:none;
  z-index:0;
}

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
  width:200px;
  height:1px;
  background:linear-gradient(90deg,var(--cyan),transparent);
}
.ak-logo {
  font-family:'Bebas Neue',sans-serif;
  font-size:2.2rem;
  letter-spacing:6px;
  display:inline-flex;
  align-items:baseline;
  gap:2px;
}
.ak-part { color:var(--cyan); text-shadow:0 0 20px rgba(0,212,255,.4); }
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
  font-family:'Rajdhani',sans-serif;
}
.ak-tagline {
  font-size:.6rem;
  color:var(--dim);
  letter-spacing:3px;
  text-transform:uppercase;
  margin-top:2px;
}

.ticker-wrap {
  overflow:hidden;
  background:var(--s1);
  border-top:1px solid rgba(0,212,255,.15);
  border-bottom:1px solid rgba(0,212,255,.15);
  padding:.45rem 0;
  margin-bottom:2rem;
  position:relative;
}
.ticker-wrap::before {
  content:'LIVE';
  position:absolute;
  left:0;
  top:50%;
  transform:translateY(-50%);
  background:var(--cyan);
  color:#000;
  font-size:.5rem;
  font-weight:700;
  padding:3px 10px;
  letter-spacing:2px;
  z-index:2;
}
.ticker-inner {
  display:flex;
  gap:3.5rem;
  animation:ticker 45s linear infinite;
  white-space:nowrap;
  padding-left:60px;
}
@keyframes ticker { 0%{transform:translateX(0);} 100%{transform:translateX(-50%);} }
.ticker-item { display:inline-flex;align-items:center;gap:.6rem;font-size:.72rem; }
.ticker-sep { color:rgba(0,212,255,.3); }
.ticker-sym { font-weight:700;color:var(--text);font-family:'Rajdhani',sans-serif;letter-spacing:1px; }
.ticker-price { font-family:'JetBrains Mono',monospace;color:var(--dim);font-size:.7rem; }
.ticker-chg { font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:700; }
.ticker-chg.up { color:var(--green); }
.ticker-chg.dn { color:var(--red); }

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
  background:radial-gradient(ellipse,rgba(0,212,255,.05) 0%,transparent 65%);
  pointer-events:none;
}
.hero-v2::after {
  content:'';
  position:absolute;
  top:0;left:0;right:0;bottom:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 60px,rgba(0,212,255,.008) 60px,rgba(0,212,255,.008) 61px),
    repeating-linear-gradient(90deg,transparent,transparent 60px,rgba(0,212,255,.008) 60px,rgba(0,212,255,.008) 61px);
  pointer-events:none;
}
.eyebrow {
  display:inline-flex;
  align-items:center;
  gap:.6rem;
  border:1px solid rgba(0,212,255,.2);
  color:var(--cyan);
  font-size:.6rem;
  letter-spacing:3px;
  padding:5px 18px;
  border-radius:2px;
  margin-bottom:2.5rem;
  text-transform:uppercase;
  background:rgba(0,212,255,.04);
  font-family:'Rajdhani',sans-serif;
  font-weight:600;
}
.eyebrow-dot {
  width:5px;height:5px;
  background:var(--cyan);
  border-radius:50%;
  display:inline-block;
  animation:blink 2s infinite;
  box-shadow:0 0 8px var(--cyan);
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
.hero-v2 h1 em { color:var(--cyan);font-style:normal;text-shadow:0 0 40px rgba(0,212,255,.3); }
.hero-v2 .sub {
  font-size:1rem;
  color:#3a3a3a;
  max-width:480px;
  margin:0 auto 3rem;
  line-height:1.9;
  font-weight:400;
  letter-spacing:.3px;
}

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
  position:relative;
  overflow:hidden;
}
.hstat::before {
  content:'';
  position:absolute;
  top:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,212,255,.3),transparent);
}
.hstat:last-child { border-right:none; }
.hstat .n {
  font-family:'Bebas Neue',sans-serif;
  font-size:2rem;
  color:var(--cyan);
  letter-spacing:2px;
  display:block;
  margin-bottom:.2rem;
  text-shadow:0 0 20px rgba(0,212,255,.2);
}
.hstat .l {
  font-size:.58rem;
  color:var(--dim);
  letter-spacing:2.5px;
  text-transform:uppercase;
}

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
  background:var(--cyan);
  opacity:.3;
}
.m-card::after {
  content:'';
  position:absolute;
  top:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,var(--cyan),transparent);
  opacity:.2;
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
.m-val.c { color:var(--cyan); }
.m-val.w { color:var(--text); }
.m-sub { font-size:.65rem;color:var(--dim);margin-top:.5rem;font-family:'JetBrains Mono',monospace; }

.stats-row { display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border); }
.stat-box { background:var(--s1);padding:1.1rem 1rem;text-align:center; }
.stat-box .sv { font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:2px;line-height:1; }
.stat-box .sl { font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:.4rem; }
.sv.g { color:var(--green); }
.sv.r { color:var(--red); }
.sv.o { color:var(--gold); }
.sv.c { color:var(--cyan); }
.sv.w { color:var(--text); }

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
.lb-item:hover { border-left-color:var(--cyan); }
.lb-rank { font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--dim);width:36px;text-align:center; }
.lb-rank.top { color:var(--cyan); text-shadow:0 0 15px rgba(0,212,255,.4); }
.lb-info { flex:1; }
.lb-name { font-weight:600;font-size:.88rem;letter-spacing:.3px; }
.lb-country { font-size:.68rem;color:var(--dim);margin-top:2px; }
.lb-pnl { font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);font-size:.95rem; }
.lb-badge { font-size:.55rem;padding:2px 8px;border-radius:2px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase; }
.funded-b { background:rgba(0,212,255,.1);color:var(--cyan);border:1px solid rgba(0,212,255,.2); }
.active-b { background:rgba(0,184,122,.08);color:var(--green);border:1px solid rgba(0,184,122,.2); }

.journal-entry {
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid var(--border3);
  padding:1.2rem 1.5rem;
  margin-bottom:2px;
  transition:border-left-color .2s;
}
.journal-entry:hover { border-left-color:var(--cyan); }
.je-date { font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:.4rem;font-family:'JetBrains Mono',monospace; }
.je-note { font-size:.85rem;color:var(--text);line-height:1.7;font-weight:300; }
.je-tags { display:flex;gap:.4rem;margin-top:.7rem;flex-wrap:wrap; }
.je-tag { font-size:.58rem;padding:2px 8px;border-radius:2px;background:rgba(0,212,255,.08);color:var(--cyan);font-weight:700;letter-spacing:1px; }
.je-tag.win { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.2); }
.je-tag.loss { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.2); }

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
.ch-plan { font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:3px;color:var(--cyan); }
.ch-status { padding:3px 12px;border-radius:2px;font-size:.58rem;font-weight:700;letter-spacing:2px;text-align:center;text-transform:uppercase; }
.ch-status.passed { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.2); }
.ch-status.failed { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.2); }
.ch-status.active { background:rgba(0,212,255,.08);color:var(--cyan);border:1px solid rgba(0,212,255,.2); }

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
.notif-item.unread { border-left:2px solid var(--cyan); }
.notif-icon { font-size:1rem;flex-shrink:0;margin-top:2px;opacity:.7; }
.notif-body { flex:1; }
.notif-title { font-weight:600;font-size:.85rem;color:var(--text);margin-bottom:3px; }
.notif-msg { font-size:.75rem;color:var(--dim);line-height:1.5; }
.notif-time { font-size:.6rem;color:var(--dim2);letter-spacing:1px;margin-top:5px;font-family:'JetBrains Mono',monospace; }
.notif-badge { background:var(--cyan);color:#000;font-size:.5rem;font-weight:800;padding:1px 6px;border-radius:2px;margin-left:6px;vertical-align:middle;letter-spacing:1px; }

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
  border:1px solid rgba(0,212,255,.3);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:'Bebas Neue',sans-serif;
  font-size:2rem;
  color:var(--cyan);
  flex-shrink:0;
  background:var(--s2);
  box-shadow:inset 0 0 20px rgba(0,212,255,.05);
}
.profile-name { font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:4px;color:var(--text);line-height:1; }
.profile-email { font-size:.75rem;color:var(--dim);margin-top:5px;font-family:'JetBrains Mono',monospace; }
.funded-badge-inline {
  display:inline-block;
  background:transparent;
  border:1px solid rgba(0,212,255,.2);
  color:var(--cyan);
  font-size:.6rem;
  letter-spacing:2.5px;
  padding:3px 12px;
  margin-top:8px;
  font-weight:700;
  text-transform:uppercase;
}

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
.admin-status.active { background:rgba(0,212,255,.08);color:var(--cyan); }
.admin-status.passed { background:rgba(0,184,122,.1);color:var(--green); }
.admin-status.failed { background:rgba(224,58,82,.1);color:var(--red); }

.plan-rules { list-style:none;padding:0;margin:0 0 1.2rem; }
.plan-rules li {
  display:flex;
  justify-content:space-between;
  padding:.45rem 0;
  border-bottom:1px solid var(--border);
  font-size:.78rem;
  color:var(--dim);
}
.plan-rules li b { color:var(--text);font-weight:500; }

.chat-container { background:var(--s1);border:1px solid var(--border);overflow:hidden;margin-bottom:1rem; }
.chat-header { padding:1rem 1.4rem;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.8rem; }
.chat-ai-dot { width:6px;height:6px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;box-shadow:0 0 8px var(--green); }
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
.chat-messages { padding:1.2rem;max-height:380px;overflow-y:auto; }
.chat-msg { margin-bottom:1rem;display:flex;gap:.8rem;align-items:flex-start; }
.chat-msg.user { flex-direction:row-reverse; }
.chat-bubble { padding:.7rem 1rem;font-size:.82rem;line-height:1.6;max-width:78%; }
.chat-bubble.ai { background:var(--s2);border:1px solid var(--border);color:var(--text); }
.chat-bubble.user { background:var(--cyan);color:#000;font-weight:500; }
.chat-avatar { width:26px;height:26px;font-size:.7rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:var(--s2);border:1px solid var(--border);font-weight:700; }
.chat-avatar.user { background:var(--cyan);color:#000; }

.risk-card { background:var(--s1);border:1px solid var(--border);padding:1.5rem; }
.risk-result { background:var(--s2);border:1px solid var(--border);padding:1.1rem;text-align:center;margin-top:1rem; }
.risk-val { font-family:'Bebas Neue',sans-serif;font-size:2.2rem;letter-spacing:2px; }

.ref-code-box {
  background:var(--s2);
  border:1px solid var(--border3);
  border-left:2px solid var(--cyan);
  padding:1rem 1.4rem;
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin:1rem 0;
}
.ref-code { font-family:'JetBrains Mono',monospace;font-size:1.4rem;color:var(--cyan);font-weight:700;letter-spacing:5px; }
.ref-stats { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:1rem 0;background:var(--border); }

.heatmap-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:1rem;background:var(--border); }
.hmap-cell { padding:.8rem .5rem;text-align:center;cursor:default; }
.hmap-sym { font-size:.68rem;font-weight:700;color:var(--text);letter-spacing:1px; }
.hmap-chg { font-size:.75rem;font-family:'JetBrains Mono',monospace;margin-top:3px; }

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
.scan-row:hover { border-left-color:var(--cyan); }
.scan-sym { font-weight:700;font-size:.85rem;letter-spacing:.5px; }
.scan-signal { font-size:.58rem;font-weight:700;letter-spacing:2px;padding:3px 10px;border-radius:2px;text-transform:uppercase; }
.scan-signal.bull { background:rgba(0,184,122,.1);color:var(--green);border:1px solid rgba(0,184,122,.25); }
.scan-signal.bear { background:rgba(224,58,82,.1);color:var(--red);border:1px solid rgba(224,58,82,.25); }
.scan-signal.neut { background:rgba(0,212,255,.08);color:var(--cyan);border:1px solid rgba(0,212,255,.2); }

.wl-row { display:flex;align-items:center;justify-content:space-between;padding:.7rem .5rem;border-bottom:1px solid var(--border); }
.wl-row:last-child { border-bottom:none; }

.ob-row { display:grid;grid-template-columns:1fr 1fr 1fr;padding:.3rem .8rem;font-size:.73rem;font-family:'JetBrains Mono',monospace; }
.ob-bid { color:var(--green); }
.ob-ask { color:var(--red); }
.ob-vol { color:var(--dim);text-align:right; }

.steps-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:3rem 0;background:var(--border); }
.step-card { background:var(--s1);padding:2rem 1.5rem;position:relative;overflow:hidden; }
.step-card::after {
  content:'';
  position:absolute;
  top:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,var(--cyan),transparent);
  opacity:.2;
}
.step-num { font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:var(--cyan);line-height:1;margin-bottom:.5rem;letter-spacing:2px;opacity:.5; }
.step-title { font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2.5px;color:var(--text);margin-bottom:.6rem; }
.step-desc { font-size:.82rem;color:var(--dim);line-height:1.7;font-weight:400; }

.testi-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:2rem 0;background:var(--border); }
.testi-card { background:var(--s1);padding:1.8rem; }
.testi-quote { font-size:.85rem;color:var(--text);line-height:1.8;margin-bottom:1.2rem;font-weight:300;border-left:2px solid rgba(0,212,255,.2);padding-left:1rem; }
.testi-name { font-weight:700;font-size:.8rem;color:var(--cyan);letter-spacing:.5px; }
.testi-meta { font-size:.68rem;color:var(--dim);margin-top:3px; }

.xp-bar { height:6px; background:var(--border3); border-radius:2px; overflow:hidden; }
.xp-fill { height:100%; background:linear-gradient(90deg,var(--cyan),var(--green)); border-radius:2px; }
.badge-locked { opacity:.22 !important; }
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
  background:linear-gradient(90deg,transparent,rgba(0,212,255,.3),transparent);
}
.ak-footer b { color:var(--cyan); }

.breach-alert {
  background:rgba(224,58,82,.08);
  border:1px solid rgba(224,58,82,.3);
  border-left:3px solid var(--red);
  padding:1.2rem 1.6rem;
  margin-bottom:1rem;
}

.stButton>button {
  background:var(--s2)!important;
  color:var(--cyan)!important;
  font-weight:700!important;
  border:1px solid rgba(0,212,255,.3)!important;
  border-radius:2px!important;
  font-family:'Rajdhani',sans-serif!important;
  letter-spacing:2px!important;
  white-space:nowrap!important;
  text-transform:uppercase!important;
  font-size:.78rem!important;
  transition:all .2s!important;
}
.stButton>button:hover {
  background:rgba(0,212,255,.1)!important;
  border-color:var(--cyan)!important;
  box-shadow:0 0 15px rgba(0,212,255,.15)!important;
}
.stButton>button p { color:var(--cyan)!important; }
.stButton>button[kind="primary"],
.stButton>button[data-testid*="primary"] {
  background:var(--cyan)!important;
  color:#000!important;
  border-color:var(--cyan)!important;
}
.stButton>button[kind="primary"] p { color:#000!important; }
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background:var(--s1)!important;
  border:1px solid var(--border)!important;
  border-radius:2px!important;
  padding:3px!important;
  gap:3px!important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] { color:var(--dim)!important;font-family:'Rajdhani',sans-serif!important;font-size:.78rem!important;letter-spacing:1px!important; }
div[data-testid="stTabs"] [aria-selected="true"] { background:rgba(0,212,255,.1)!important;color:var(--cyan)!important;border-radius:2px!important;border:1px solid rgba(0,212,255,.2)!important; }
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
  font-family:'Rajdhani',sans-serif!important;
}
.stSelectbox>div>div:focus-within,
.stNumberInput>div>div>input:focus,
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
  border-color:rgba(0,212,255,.4)!important;
  box-shadow:0 0 10px rgba(0,212,255,.1)!important;
}
label[data-testid="stWidgetLabel"] { color:var(--dim)!important;font-size:.68rem!important;letter-spacing:1.5px!important;text-transform:uppercase!important; }
div[data-testid="stVerticalBlock"],div[data-testid="stHorizontalBlock"],
div[data-testid="column"],div[data-testid="stMarkdownContainer"],
div.element-container,div.stMarkdown { background:transparent!important; }
.stSlider [data-baseweb="slider"] [data-testid="stSliderThumb"] { background:var(--cyan)!important; }

.card, .feat-card, .step-card, .plan-card, .metric-card {
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
  transform-style: preserve-3d;
}
.card:hover, .feat-card:hover, .step-card:hover, .plan-card:hover, .metric-card:hover {
  transform: perspective(1000px) rotateX(4deg) rotateY(-4deg) scale3d(1.03, 1.03, 1.03) translateY(-8px);
  box-shadow: 20px 20px 40px rgba(0,0,0,0.8), -1px -1px 2px rgba(224, 102, 255, 0.3) inset;
}
.btn-primary, .btn-secondary {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.btn-primary:hover {
  transform: perspective(500px) translateZ(20px) scale(1.05);
  box-shadow: 0 0 30px rgba(157, 0, 255, 0.6);
}
.gs-val {
  transition: transform 0.3s ease;
}
.gs:hover .gs-val {
  transform: perspective(400px) translateZ(40px) scale(1.15);
  text-shadow: 0 0 20px var(--cyan);
}
\n</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────
LOGO_URL     = "https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.PNG"
IG_HANDLE    = "@akfunded"
IG_URL       = "https://www.instagram.com/akfunded"
PLATFORM_URL = "https://akfunded.streamlit.app"

SYMBOLS = {
    "Crypto Majors": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"],
    "Crypto Altcoins": ["XRPUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT", "AVAXUSDT", "LINKUSDT", "MATICUSDT", "LTCUSDT"],
}
TV_SYMBOL_MAP = {
    "BTCUSDT":"BINANCE:BTCUSDT", "ETHUSDT":"BINANCE:ETHUSDT",
    "BNBUSDT":"BINANCE:BNBUSDT", "SOLUSDT":"BINANCE:SOLUSDT",
    "XRPUSDT":"BINANCE:XRPUSDT", "ADAUSDT":"BINANCE:ADAUSDT",
    "DOGEUSDT":"BINANCE:DOGEUSDT", "DOTUSDT":"BINANCE:DOTUSDT",
    "AVAXUSDT":"BINANCE:AVAXUSDT", "LINKUSDT":"BINANCE:LINKUSDT",
    "MATICUSDT":"BINANCE:MATICUSDT", "LTCUSDT":"BINANCE:LTCUSDT",
}

import requests
@st.cache_data(ttl=1)
def get_all_market_data():
    try:
        r = requests.get("https://data-api.binance.vision/api/v3/ticker/24hr", timeout=10)
        r.raise_for_status()
        data = r.json()
        
        my_symbols = [s for g in SYMBOLS.values() for s in g]
        market_data = {}
        for d in data:
            sym = d['symbol']
            if sym in my_symbols:
                market_data[sym] = {
                    "price": float(d['lastPrice']),
                    "change": float(d['priceChangePercent']),
                    "vol": "High" if float(d['quoteVolume']) > 100000000 else "Medium",
                    "name": sym.replace("USDT", " / USDT")
                }
        for s in my_symbols:
            if s not in market_data:
                market_data[s] = {"price":1.0, "change":0.0, "vol":"Low", "name":s}
        return market_data
    except Exception as e:
        import traceback
        err_msg = f"Binance API Error: {e}\\n{traceback.format_exc()}"
        with open("binance_error.log", "w") as _errF: _errF.write(err_msg)
        my_symbols = [s for g in SYMBOLS.values() for s in g]
        return {s: {"price": 1.0, "change": 0.0, "vol": "Low", "name": s} for s in my_symbols}


PLANS_INSTANT = [
    {"name":"$5,000",   "capital":5000,   "price":299,  "slug":"instant_5k",   "split":70, "phase":"instant"},
    {"name":"$10,000",  "capital":10000,  "price":499,  "slug":"instant_10k",  "split":70, "phase":"instant"},
    {"name":"$25,000",  "capital":25000,  "price":999,  "slug":"instant_25k",  "split":70, "phase":"instant"},
    {"name":"$50,000",  "capital":50000,  "price":1799, "slug":"instant_50k",  "split":75, "phase":"instant"},
    {"name":"$100,000", "capital":100000, "price":2999, "slug":"instant_100k", "split":75, "phase":"instant"},
]
PLANS_1P = [
    {"name":"$5,000",   "capital":5000,   "price":79,  "slug":"1phase_5k",   "split":80, "phase":"1step"},
    {"name":"$10,000",  "capital":10000,  "price":129, "slug":"1phase_10k",  "split":80, "phase":"1step"},
    {"name":"$25,000",  "capital":25000,  "price":249, "slug":"1phase_25k",  "split":80, "phase":"1step"},
    {"name":"$50,000",  "capital":50000,  "price":349, "slug":"1phase_50k",  "split":80, "phase":"1step"},
    {"name":"$100,000", "capital":100000, "price":529, "slug":"1phase_100k", "split":80, "phase":"1step"},
]
PLANS_2P = [
    {"name":"$5,000",   "capital":5000,   "price":49,  "slug":"2phase_5k",   "split":90, "phase":"2step"},
    {"name":"$10,000",  "capital":10000,  "price":89,  "slug":"2phase_10k",  "split":90, "phase":"2step"},
    {"name":"$25,000",  "capital":25000,  "price":169, "slug":"2phase_25k",  "split":90, "phase":"2step"},
    {"name":"$50,000",  "capital":50000,  "price":299, "slug":"2phase_50k",  "split":90, "phase":"2step"},
    {"name":"$100,000", "capital":100000, "price":499, "slug":"2phase_100k", "split":90, "phase":"2step"},
]

RULES = {
    "instant_5k":   {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_10k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_25k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_50k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_100k": {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "1phase_5k":    {"target":8,"daily_loss":5,"total_loss":10,"min_days":5,"phase":"1step"},
    "1phase_10k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":5,"phase":"1step"},
    "1phase_25k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":5,"phase":"1step"},
    "1phase_50k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":5,"phase":"1step"},
    "1phase_100k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":5,"phase":"1step"},
    "2phase_5k":    {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"2step"},
    "2phase_10k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"2step"},
    "2phase_25k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"2step"},
    "2phase_50k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"2step"},
    "2phase_100k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"2step"},
}

# ─── SESSION STATE ──────────────────────────────────────────────
query_params = st.query_params
initial_page = query_params.get("page", "home")

for k, v in [
    ("user",None),("page",initial_page),("notifications",[]),
    ("chat_history",[]),("watchlist",["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT"]),
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

def db_add_journal_entry(uid, text, mood, symbol):
    try:
        supabase.table("journal_entries").insert({
            "user_id": uid,
            "entry_text": text,
            "mood": mood,
            "symbol": symbol
        }).execute()
        return True
    except: return False

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

def send_email_html(to_email, subject, body_html):
    try:
        smtp_email = st.secrets.get("SMTP_EMAIL","")
        smtp_pass  = st.secrets.get("SMTP_PASSWORD","")
        if not smtp_email or not smtp_pass: return False
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"AKFunded <{smtp_email}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(body_html,"html"))
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as s:
            s.login(smtp_email, smtp_pass)
            s.sendmail(smtp_email, to_email, msg.as_string())
        return True
    except: return False

def send_breach_email(to_email, name, reason, plan, capital):
    cap_str = f"${capital//1000}K"
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'></head>"
        "<body style='margin:0;padding:0;background:#050505;font-family:Helvetica Neue,sans-serif;'>"
        "<div style='max-width:600px;margin:0 auto;padding:2rem;'>"
        "<div style='text-align:center;border-bottom:1px solid #1e1e1e;padding-bottom:1.5rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:1.4rem;font-weight:700;letter-spacing:4px;color:#00D4FF;'>AKFUNDED</div>"
        "<div style='font-size:.6rem;color:#505050;letter-spacing:3px;text-transform:uppercase;margin-top:4px;'>Account Alert</div>"
        "</div>"
        "<div style='background:#1a0808;border:1px solid rgba(224,58,82,.3);border-left:3px solid #E03A52;padding:1.5rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:.65rem;color:#E03A52;letter-spacing:3px;text-transform:uppercase;margin-bottom:.5rem;font-weight:700;'>ACCOUNT BREACHED</div>"
        f"<div style='font-size:1.1rem;color:#D8D8D8;margin-bottom:.5rem;'>Hello <strong style='color:#fff;'>{name}</strong>,</div>"
        f"<div style='font-size:.88rem;color:#888;line-height:1.8;'>Your <strong style='color:#fff;'>{plan.upper()} {cap_str}</strong> account has been marked as <strong style='color:#E03A52;'>FAILED</strong>.</div>"
        "</div>"
        "<div style='background:#111;border:1px solid #1e1e1e;padding:1.2rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:.6rem;color:#505050;letter-spacing:2px;text-transform:uppercase;margin-bottom:.8rem;'>Reason</div>"
        f"<div style='font-size:.88rem;color:#D8D8D8;line-height:1.7;'>{reason}</div>"
        "</div>"
        f"<div style='background:#111;border:1px solid #1e1e1e;padding:1.2rem;'>"
        f"<div style='font-size:.75rem;color:#888;line-height:1.8;'>Start a new challenge at <a href='{PLATFORM_URL}' style='color:#00D4FF;text-decoration:none;'>{PLATFORM_URL}</a></div>"
        "</div>"
        "<div style='text-align:center;font-size:.6rem;color:#3a3a3a;letter-spacing:1.5px;margin-top:1.5rem;'>AKFunded &middot; Simulated Prop Trading &middot; @akfunded</div>"
        "</div></body></html>"
    )
    return send_email_html(to_email, "Account Breached - AKFunded", html)

def send_passed_email(to_email, name, target, plan, capital):
    cap_str = f"${capital//1000}K"
    html = (
        "<!DOCTYPE html><html><head><meta charset='UTF-8'></head>"
        "<body style='margin:0;padding:0;background:#030303;font-family:Helvetica Neue,sans-serif;'>"
        "<div style='max-width:600px;margin:0 auto;padding:2rem;'>"
        "<div style='text-align:center;border-bottom:1px solid #1e1e1e;padding-bottom:1.5rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:1.4rem;font-weight:700;letter-spacing:4px;color:#D4AF37;'>AKFUNDED</div>"
        "<div style='font-size:.6rem;color:#505050;letter-spacing:3px;text-transform:uppercase;margin-top:4px;'>Achievement Alert</div>"
        "</div>"
        "<div style='background:#1a1708;border:1px solid rgba(212,175,55,.3);border-left:3px solid #D4AF37;padding:1.5rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:.65rem;color:#D4AF37;letter-spacing:3px;text-transform:uppercase;margin-bottom:.5rem;font-weight:700;'>CHALLENGE PASSED</div>"
        f"<div style='font-size:1.1rem;color:#D8D8D8;margin-bottom:.5rem;'>Congratulations <strong style='color:#fff;'>{name}</strong>!</div>"
        f"<div style='font-size:.88rem;color:#888;line-height:1.8;'>You have successfully passed the <strong style='color:#D4AF37;'>{plan.upper()} {cap_str}</strong> evaluation by hitting your {target}% target!</div>"
        "</div>"
        "<div style='background:#111;border:1px solid #1e1e1e;padding:1.2rem;margin-bottom:1.5rem;'>"
        "<div style='font-size:.6rem;color:#505050;letter-spacing:2px;text-transform:uppercase;margin-bottom:.8rem;'>Next Steps</div>"
        f"<div style='font-size:.88rem;color:#D8D8D8;line-height:1.7;'>Your certificate is now available in your dashboard. Login to proceed to your funded account.</div>"
        "</div>"
        f"<div style='background:#111;border:1px solid #1e1e1e;padding:1.2rem;'>"
        f"<div style='font-size:.75rem;color:#888;line-height:1.8;'>Access your dashboard at <a href='{PLATFORM_URL}' style='color:#D4AF37;text-decoration:none;'>{PLATFORM_URL}</a></div>"
        "</div>"
        "<div style='text-align:center;font-size:.6rem;color:#3a3a3a;letter-spacing:1.5px;margin-top:1.5rem;'>AKFunded &middot; Simulated Prop Trading &middot; @akfunded</div>"
        "</div></body></html>"
    )
    return send_email_html(to_email, "Challenge Passed! - AKFunded", html)

def call_ai(messages, system_prompt):
    try:
        import requests
        key = st.secrets.get('GROQ_API_KEY','')
        if not key:
            return "⚠️ Please add your GROQ_API_KEY to your Streamlit secrets to activate the AI Coach."
            
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        body = {"model": "llama3-70b-8192", "max_tokens": 1000,
                "messages": [{"role": "system", "content": system_prompt}, *messages]}
                
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers, timeout=30)
        if r.status_code == 401: return "⚠️ Unauthorized: Your GROQ_API_KEY is invalid."
        
        data = r.json()
        return data["choices"][0]["message"]["content"] if data.get("choices") else f"API Error: {data.get('error', {}).get('message', 'Unknown')}"
    except Exception as e:
        return f"⚠️ AI service unavailable. Error: {e}"

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

def get_live_price(symbol):
    return float(get_all_market_data().get(symbol, {}).get("price", 1.0))

def check_and_breach(uid, challenge, account, email, name):
    r = RULES.get(challenge["plan"], {})
    if not r: return False, ""
    initial = float(account.get("initial_capital",1))
    balance = float(account.get("balance",initial))
    daily_loss = float(account.get("daily_loss",0))
    total_loss_pct = ((initial - balance) / initial * 100) if balance < initial else 0
    daily_loss_pct = (abs(daily_loss) / initial * 100) if daily_loss < 0 else 0
    breach_reason = None
    if total_loss_pct >= r["total_loss"]:
        breach_reason = f"Maximum total loss of {r['total_loss']}% has been reached."
    elif daily_loss_pct >= r["daily_loss"]:
        breach_reason = f"Maximum daily loss of {r['daily_loss']}% has been reached for today."
    if breach_reason:
        try:
            supabase.table("challenges").update({"status":"failed"}).eq("id",challenge["id"]).execute()
            push_notification(uid, "⚠", "Account Breached", breach_reason[:80])
            send_breach_email(email, name, breach_reason, challenge["plan"], int(account.get("initial_capital",0)))
        except: pass
        return True, breach_reason
    return False, ""

# ─── CERTIFICATE: on-screen (flex/grid OK for browser) ─────────
def build_certificate_html(name, plan, capital, pnl_pct, days, date_str, challenge_id):
    cap_str = f"${capital // 1000}K"
    r = RULES.get(plan, {})
    phase_type = r.get("phase", "1step")
    if phase_type == "instant":   phase_label = "INSTANT FUNDED"
    elif phase_type == "1step":   phase_label = "ONE-STEP CHALLENGE"
    else:                         phase_label = "TWO-STEP CHALLENGE"

    accent      = "#00B87A"
    accent_glow = "rgba(0,184,122,0.3)"
    accent_dim  = "rgba(0,184,122,0.06)"
    accent_bord = "#1a3a1a"
    accent_bd2  = "#0f200f"
    mid_bord    = "rgba(0,184,122,0.18)"

    return (
        '<div style="width:1123px;height:794px;max-width:100%;margin:0 auto;'
        'background:linear-gradient(160deg,#070d07 0%,#060a06 60%,#050905 100%);'
        'position:relative;overflow:hidden;box-sizing:border-box;'
        f'border:1px solid {accent_bord};font-family:Rajdhani,sans-serif;'
        'display:flex;flex-direction:column;">'

        '<div style="position:absolute;inset:0;background:'
        'repeating-linear-gradient(0deg,transparent,transparent 40px,rgba(0,184,122,0.013) 40px,rgba(0,184,122,0.013) 41px),'
        'repeating-linear-gradient(90deg,transparent,transparent 40px,rgba(0,184,122,0.013) 40px,rgba(0,184,122,0.013) 41px);'
        'pointer-events:none;z-index:0;"></div>'

        '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);'
        'width:700px;height:500px;'
        f'background:radial-gradient(ellipse,rgba(0,184,122,0.05) 0%,transparent 65%);'
        'pointer-events:none;z-index:0;"></div>'

        f'<div style="position:absolute;top:0;left:0;width:72px;height:72px;border-top:2px solid {accent};border-left:2px solid {accent};z-index:1;"></div>'
        f'<div style="position:absolute;top:0;right:0;width:72px;height:72px;border-top:2px solid {accent};border-right:2px solid {accent};z-index:1;"></div>'
        f'<div style="position:absolute;bottom:0;left:0;width:72px;height:72px;border-bottom:2px solid {accent};border-left:2px solid {accent};z-index:1;"></div>'
        f'<div style="position:absolute;bottom:0;right:0;width:72px;height:72px;border-bottom:2px solid {accent};border-right:2px solid {accent};z-index:1;"></div>'

        '<div style="position:relative;z-index:2;flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:36px 90px 12px;">'

        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\'none\'" style="height:44px;width:44px;object-fit:contain;opacity:0.9;" />'
        '<div>'
        '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:6px;color:#00D4FF;line-height:1;">AKFUNDED</div>'
        '<div style="font-size:0.48rem;color:#3a6a5a;letter-spacing:3px;text-transform:uppercase;">Prop Trading Platform</div>'
        '</div></div>'

        f'<div style="display:flex;align-items:center;gap:14px;width:100%;margin-bottom:14px;">'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,{accent_bord});"></div>'
        f'<div style="width:5px;height:5px;background:{accent};border-radius:50%;box-shadow:0 0 8px {accent};flex-shrink:0;"></div>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,{accent_bord},transparent);"></div>'
        '</div>'

        '<div style="font-size:0.52rem;color:#3a6a4a;letter-spacing:4px;text-transform:uppercase;margin-bottom:6px;font-weight:600;">OFFICIAL CERTIFICATE</div>'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:3.6rem;letter-spacing:10px;color:{accent};line-height:1;margin-bottom:1px;text-shadow:0 0 40px {accent_glow};">CERTIFICATE</div>'
        '<div style="font-size:0.8rem;letter-spacing:8px;color:#2a5a3a;margin-bottom:10px;font-weight:700;text-transform:uppercase;">OF RECOGNITION</div>'

        f'<div style="display:flex;align-items:center;gap:14px;width:100%;margin-bottom:10px;">'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,{accent_bord});"></div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:3px;text-transform:uppercase;white-space:nowrap;">This certificate is proudly presented to</div>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,{accent_bord},transparent);"></div>'
        '</div>'

        '<div style="text-align:center;margin-bottom:6px;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.9rem;color:#EFEFEF;line-height:1.1;letter-spacing:6px;">{name.upper()}</div>'
        f'<div style="width:320px;height:1px;background:linear-gradient(90deg,transparent,{accent},transparent);margin:7px auto 0;"></div>'
        '</div>'

        '<div style="font-size:0.72rem;color:#4a7a5a;margin:6px 0 10px;line-height:1.8;font-weight:400;text-align:center;">'
        'This trader demonstrated exceptional discipline and risk management<br>'
        'in the AKFunded prop trading evaluation.'
        '</div>'

        f'<div style="display:inline-block;border:1px solid {mid_bord};background:{accent_dim};padding:3px 22px;margin-bottom:16px;border-radius:1px;">'
        f'<div style="font-size:0.58rem;color:{accent};letter-spacing:3px;font-weight:700;text-transform:uppercase;">{phase_label} &nbsp;&middot;&nbsp; {cap_str} ACCOUNT</div>'
        '</div>'

        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);width:100%;border:1px solid {accent_bord};background:{accent_bd2};">'
        f'<div style="padding:12px 16px;border-right:1px solid {accent_bord};text-align:center;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;letter-spacing:2px;color:{accent};line-height:1;margin-bottom:3px;">+{pnl_pct:.2f}%</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Profit Achieved</div>'
        '</div>'
        f'<div style="padding:12px 16px;border-right:1px solid {accent_bord};text-align:center;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;letter-spacing:2px;color:#D4A843;line-height:1;margin-bottom:3px;">{days}</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Trading Days</div>'
        '</div>'
        f'<div style="padding:12px 16px;text-align:center;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.45rem;letter-spacing:2px;color:#D8D8D8;line-height:1;margin-bottom:3px;">{date_str}</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Date Issued</div>'
        '</div>'
        '</div>'
        '</div>'

        f'<div style="position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;padding:16px 90px 26px;border-top:1px solid {accent_bord};">'
        '<div style="text-align:center;">'
        f'<div style="font-family:\\\'Caveat\\\',cursive;font-size:3.2rem;color:var(--neon);text-shadow:0 0 15px rgba(223,0,255,0.6);line-height:0.9;letter-spacing:1px;font-weight:600;">Akash Injeti</div>'
        f'<div style="width:130px;height:1px;background:{accent_bord};margin:5px auto;"></div>'
        '<div style="font-size:0.5rem;color:var(--dim);letter-spacing:1.5px;text-transform:uppercase;">Akash Injeti</div>'
        '<div style="font-size:0.48rem;color:var(--dim2);letter-spacing:1px;text-transform:uppercase;">Founder, AKFunded</div>'
        '</div>'
        f'<div style="text-align:center;">'
        f'<div style="width:54px;height:54px;border:2px solid {accent_bord};border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto;background:{accent_bd2};">'
        f'<div style="font-size:0.36rem;color:{accent};font-weight:700;text-align:center;line-height:1.9;letter-spacing:0.4px;">AK<br>FUNDED<br>&#10003;</div>'
        '</div>'
        '<div style="font-size:0.44rem;color:#2a5a3a;letter-spacing:1.5px;margin-top:4px;text-transform:uppercase;">Verified</div>'
        '</div>'
        '<div style="text-align:right;">'
        '<div style="font-size:0.48rem;color:#2a4a2a;letter-spacing:2px;text-transform:uppercase;margin-bottom:2px;">akfunded.streamlit.app</div>'
        '<div style="font-size:0.48rem;color:#2a4a2a;letter-spacing:2px;text-transform:uppercase;margin-bottom:2px;">@akfunded</div>'
        '<div style="font-size:0.48rem;color:#2a4a2a;letter-spacing:2px;text-transform:uppercase;">Simulated Prop Trading</div>'
        '</div>'
        '</div>'
        '</div>'
    )


# ─── CERTIFICATE: EMAIL-SAFE (table-based, Gmail-compatible) ───
def build_certificate_email_html(name, plan, capital, pnl_pct, days, date_str):
    cap_str = f"${capital // 1000}K"
    r = RULES.get(plan, {})
    phase_type = r.get("phase", "1step")
    if phase_type == "instant":   phase_label = "INSTANT FUNDED"
    elif phase_type == "1step":   phase_label = "ONE-STEP CHALLENGE"
    else:                         phase_label = "TWO-STEP CHALLENGE"

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AKFunded Certificate of Recognition</title></head>
<body style="margin:0;padding:0;background:#050505;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#050505;">
<tr><td align="center" style="padding:24px 10px;">

<table width="660" cellpadding="0" cellspacing="0" border="0"
  style="background:#060d06;border:2px solid #1a3a1a;max-width:660px;width:100%;">

  <tr><td colspan="3" height="3" style="background:#00B87A;font-size:1px;line-height:1px;">&nbsp;</td></tr>

  <tr>
    <td align="center" style="padding:28px 30px 8px;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr><td align="center">
          <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:22px;font-weight:bold;
            letter-spacing:6px;color:#00D4FF;">AKFUNDED</p>
          <p style="margin:4px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:9px;
            color:#3a6a5a;letter-spacing:3px;text-transform:uppercase;">PROP TRADING PLATFORM</p>
        </td></tr>
      </table>
    </td>
  </tr>

  <tr>
    <td style="padding:4px 40px 10px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="border-top:1px solid #1a3a1a;">&nbsp;</td>
          <td width="12" align="center" valign="middle">
            <table cellpadding="0" cellspacing="0" border="0"><tr><td width="8" height="8"
              style="background:#00B87A;border-radius:4px;">&nbsp;</td></tr></table>
          </td>
          <td style="border-top:1px solid #1a3a1a;">&nbsp;</td>
        </tr>
      </table>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:0 30px 4px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:9px;font-weight:bold;
        letter-spacing:4px;color:#3a6a4a;text-transform:uppercase;">OFFICIAL CERTIFICATE</p>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:2px 30px 2px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:52px;font-weight:bold;
        letter-spacing:8px;color:#00B87A;line-height:1.1;">CERTIFICATE</p>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:0 30px 8px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;
        letter-spacing:7px;color:#2a5a3a;text-transform:uppercase;">OF RECOGNITION</p>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:0 40px 6px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="border-top:1px solid #1a3a1a;">&nbsp;</td>
          <td width="220" align="center" style="padding:0 8px;">
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#3a6a4a;letter-spacing:2px;white-space:nowrap;">
              This certificate is proudly presented to</p>
          </td>
          <td style="border-top:1px solid #1a3a1a;">&nbsp;</td>
        </tr>
      </table>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:4px 30px 0;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:34px;font-weight:bold;
        letter-spacing:5px;color:#EFEFEF;">{name.upper()}</p>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:6px 30px 10px;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr><td width="300" height="1" style="background:#00B87A;font-size:1px;line-height:1px;">&nbsp;</td></tr>
      </table>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:0 60px 10px;">
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:11px;
        color:#4a7a5a;line-height:1.8;text-align:center;">
        This trader demonstrated exceptional discipline and risk management<br>
        in the AKFunded prop trading evaluation.
      </p>
    </td>
  </tr>

  <tr>
    <td align="center" style="padding:0 30px 16px;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="background:#0a1f0a;border:1px solid #1a7a5a;padding:8px 28px;">
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:10px;font-weight:bold;
              color:#00B87A;letter-spacing:3px;text-transform:uppercase;">
              {phase_label} &nbsp;&middot;&nbsp; {cap_str} ACCOUNT
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <tr>
    <td style="padding:0 30px 18px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td width="32%" align="center" valign="top"
            style="background:#0f200f;border:1px solid #1a3a1a;padding:16px 8px;">
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:28px;font-weight:bold;
              color:#00B87A;letter-spacing:2px;">+{pnl_pct:.2f}%</p>
            <p style="margin:8px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#3a6a4a;letter-spacing:2px;text-transform:uppercase;">PROFIT ACHIEVED</p>
          </td>
          <td width="2%" style="background:#060d06;">&nbsp;</td>
          <td width="32%" align="center" valign="top"
            style="background:#0f200f;border:1px solid #1a3a1a;padding:16px 8px;">
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:28px;font-weight:bold;
              color:#D4A843;letter-spacing:2px;">{days}</p>
            <p style="margin:8px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#3a6a4a;letter-spacing:2px;text-transform:uppercase;">TRADING DAYS</p>
          </td>
          <td width="2%" style="background:#060d06;">&nbsp;</td>
          <td width="32%" align="center" valign="top"
            style="background:#0f200f;border:1px solid #1a3a1a;padding:16px 8px;">
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:18px;font-weight:bold;
              color:#D8D8D8;letter-spacing:2px;">{date_str}</p>
            <p style="margin:8px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#3a6a4a;letter-spacing:2px;text-transform:uppercase;">DATE ISSUED</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <tr>
    <td height="1" style="background:#1a3a1a;font-size:1px;line-height:1px;">&nbsp;</td>
  </tr>

  <tr>
    <td style="padding:18px 30px 26px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr valign="middle">
          <td width="38%" align="left" valign="middle">
            <p style="margin:0;font-family:'Caveat',cursive;font-size:26px;font-weight:600;
              color:#c300ff;text-shadow:0 0 10px rgba(195,0,255,0.4);">Akash Injeti</p>
            <table cellpadding="0" cellspacing="0" border="0">
              <tr><td width="140" height="1"
                style="background:#35005c;font-size:1px;line-height:1px;padding-top:6px;">&nbsp;</td></tr>
            </table>
            <p style="margin:6px 0 2px;font-family:Arial,Helvetica,sans-serif;font-size:7px;
              color:#9c7eb5;letter-spacing:1.5px;text-transform:uppercase;">AKASH INJETI</p>
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:7px;
              color:#2a5a3a;letter-spacing:1px;text-transform:uppercase;">FOUNDER, AKFUNDED</p>
          </td>

          <td width="24%" align="center" valign="middle">
            <table cellpadding="0" cellspacing="0" border="0" align="center">
              <tr><td align="center" width="60" height="60"
                style="background:#0f200f;border:2px solid #1a3a1a;border-radius:30px;">
                <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:7px;
                  font-weight:bold;color:#00B87A;line-height:2;text-align:center;">
                  AK<br>FUNDED<br>&#10003;</p>
              </td></tr>
              <tr><td align="center" style="padding-top:6px;">
                <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:6px;
                  color:#2a5a3a;letter-spacing:1.5px;text-transform:uppercase;">VERIFIED</p>
              </td></tr>
            </table>
          </td>

          <td width="38%" align="right" valign="middle">
            <p style="margin:0 0 5px;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#2a5a3a;letter-spacing:1.5px;">akfunded.streamlit.app</p>
            <p style="margin:0 0 5px;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#2a5a3a;letter-spacing:1.5px;">@akfunded</p>
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:8px;
              color:#2a5a3a;letter-spacing:1.5px;">Simulated Prop Trading</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <tr><td height="3" style="background:#00B87A;font-size:1px;line-height:1px;">&nbsp;</td></tr>

</table>

<table width="660" cellpadding="0" cellspacing="0" border="0" style="max-width:660px;">
  <tr><td align="center" style="padding:14px 0;">
    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:9px;
      color:#2a2a2a;letter-spacing:1.5px;">
      AKFunded &middot; Simulated Prop Trading &middot; @akfunded
    </p>
  </td></tr>
</table>

</td></tr></table>
</body></html>"""


# ─── CERTIFICATE: PDF (reportlab) ──────────────────────────────
def build_certificate_pdf(name, plan, capital, pnl_pct, days, date_str):
    try:
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.pdfgen import canvas as rlcanvas
        from reportlab.lib.colors import HexColor, Color

        buf = io.BytesIO()
        W, H = landscape(A4)
        c = rlcanvas.Canvas(buf, pagesize=(W, H))

        # Background
        c.setFillColor(HexColor('#060d06'))
        c.rect(0, 0, W, H, fill=1, stroke=0)

        # Subtle grid lines
        c.setStrokeColor(HexColor('#0c1f0c'))
        c.setLineWidth(0.4)
        for x in range(0, int(W) + 40, 40):
            c.line(x, 0, x, H)
        for y in range(0, int(H) + 40, 40):
            c.line(0, y, W, y)

        # Radial glow centre
        c.setFillColor(Color(0, 0.45, 0.3, alpha=0.04))
        c.circle(W / 2, H / 2, 260, fill=1, stroke=0)

        # Corner brackets
        accent = HexColor('#00B87A')
        bsz = 52
        c.setStrokeColor(accent)
        c.setLineWidth(2)
        # TL
        c.line(18, H - 18, 18 + bsz, H - 18); c.line(18, H - 18, 18, H - 18 - bsz)
        # TR
        c.line(W - 18, H - 18, W - 18 - bsz, H - 18); c.line(W - 18, H - 18, W - 18, H - 18 - bsz)
        # BL
        c.line(18, 18, 18 + bsz, 18); c.line(18, 18, 18, 18 + bsz)
        # BR
        c.line(W - 18, 18, W - 18 - bsz, 18); c.line(W - 18, 18, W - 18, 18 + bsz)

        # Outer border
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.setLineWidth(0.8)
        c.rect(10, 10, W - 20, H - 20, fill=0, stroke=1)

        # Top green bar
        c.setFillColor(accent)
        c.rect(10, H - 13, W - 20, 3, fill=1, stroke=0)

        cy = H - 52

        # AKFUNDED header
        c.setFont('Helvetica-Bold', 16)
        c.setFillColor(HexColor('#00D4FF'))
        c.drawCentredString(W / 2, cy, 'AKFUNDED')
        cy -= 16
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#3a6a5a'))
        c.drawCentredString(W / 2, cy, 'PROP TRADING PLATFORM')
        cy -= 20

        # Divider with dot
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.setLineWidth(0.7)
        c.line(W / 2 - 220, cy, W / 2 - 8, cy)
        c.line(W / 2 + 8,   cy, W / 2 + 220, cy)
        c.setFillColor(accent)
        c.circle(W / 2, cy, 3.5, fill=1, stroke=0)
        cy -= 18

        # OFFICIAL CERTIFICATE label
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(HexColor('#3a6a4a'))
        c.drawCentredString(W / 2, cy, 'OFFICIAL CERTIFICATE')
        cy -= 6

        # Big CERTIFICATE word
        c.setFont('Helvetica-Bold', 52)
        c.setFillColor(accent)
        c.drawCentredString(W / 2, cy - 46, 'CERTIFICATE')
        cy -= 54

        # OF RECOGNITION
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(HexColor('#2a5a3a'))
        c.drawCentredString(W / 2, cy, 'OF RECOGNITION')
        cy -= 18

        # Presented-to divider
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.line(W / 2 - 200, cy, W / 2 - 88, cy)
        c.line(W / 2 + 88,  cy, W / 2 + 200, cy)
        c.setFont('Helvetica', 7)
        c.setFillColor(HexColor('#3a6a4a'))
        c.drawCentredString(W / 2, cy - 6, 'This certificate is proudly presented to')
        cy -= 14

        # Trader name
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(HexColor('#EFEFEF'))
        c.drawCentredString(W / 2, cy - 34, name.upper())
        cy -= 42

        # Name underline
        c.setStrokeColor(accent)
        c.setLineWidth(1)
        c.line(W / 2 - 180, cy, W / 2 + 180, cy)
        cy -= 14

        # Description
        c.setFont('Helvetica', 9)
        c.setFillColor(HexColor('#4a7a5a'))
        c.drawCentredString(W / 2, cy,
            'This trader demonstrated exceptional discipline and risk management in the AKFunded prop trading evaluation.')
        cy -= 22

        # Phase badge box
        r_rules = RULES.get(plan, {})
        phase_type  = r_rules.get("phase", "1step")
        phase_label = ("INSTANT FUNDED"    if phase_type == "instant"
                       else "ONE-STEP CHALLENGE" if phase_type == "1step"
                       else "TWO-STEP CHALLENGE")
        cap_str = f"${capital // 1000}K"
        badge_w, badge_h = 290, 22
        bx = W / 2 - badge_w / 2
        c.setFillColor(Color(0, 0.45, 0.3, alpha=0.06))
        c.setStrokeColor(HexColor('#1a7a5a'))
        c.setLineWidth(0.8)
        c.rect(bx, cy - badge_h + 6, badge_w, badge_h, fill=1, stroke=1)
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(accent)
        c.drawCentredString(W / 2, cy - 4, f'{phase_label}  \u00b7  {cap_str} ACCOUNT')
        cy -= 32

        # Stats boxes
        box_w, box_h, gap = 195, 55, 8
        total_bw = 3 * box_w + 2 * gap
        sx = W / 2 - total_bw / 2
        sy = cy - box_h

        stats_data = [
            (f'+{pnl_pct:.2f}%', 'PROFIT ACHIEVED', HexColor('#00B87A')),
            (str(days),           'TRADING DAYS',    HexColor('#D4A843')),
            (date_str,            'DATE ISSUED',     HexColor('#D8D8D8')),
        ]
        for i, (val, label, color) in enumerate(stats_data):
            bx2 = sx + i * (box_w + gap)
            c.setFillColor(HexColor('#0f200f'))
            c.setStrokeColor(HexColor('#1a3a1a'))
            c.setLineWidth(0.8)
            c.rect(bx2, sy, box_w, box_h, fill=1, stroke=1)
            c.setFont('Helvetica-Bold', 22)
            c.setFillColor(color)
            c.drawCentredString(bx2 + box_w / 2, sy + box_h - 26, val)
            c.setFont('Helvetica', 7)
            c.setFillColor(HexColor('#3a6a4a'))
            c.drawCentredString(bx2 + box_w / 2, sy + 9, label)

        cy = sy - 20

        # Footer divider
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.setLineWidth(0.8)
        c.line(28, cy, W - 28, cy)
        cy -= 20

        # Signature – left
        c.setFont('Helvetica-BoldOblique', 20)
        c.setFillColor(accent)
        c.drawString(68, cy - 2, 'Akash Injeti')
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.setLineWidth(0.7)
        c.line(68, cy - 9, 218, cy - 9)
        c.setFont('Helvetica', 6.5)
        c.setFillColor(HexColor('#3a6a4a'))
        c.drawString(68, cy - 20, 'AKASH INJETI')
        c.drawString(68, cy - 30, 'FOUNDER, AKFUNDED')

        # Seal – centre
        cx2 = W / 2
        c.setFillColor(HexColor('#0f200f'))
        c.setStrokeColor(HexColor('#1a3a1a'))
        c.setLineWidth(1.2)
        c.circle(cx2, cy - 12, 28, fill=1, stroke=1)
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(accent)
        c.drawCentredString(cx2, cy - 5,  'AK')
        c.drawCentredString(cx2, cy - 14, 'FUNDED')
        c.drawCentredString(cx2, cy - 23, '\u2713')
        c.setFont('Helvetica', 5.5)
        c.setFillColor(HexColor('#2a5a3a'))
        c.drawCentredString(cx2, cy - 44, 'VERIFIED')

        # Right info
        c.setFont('Helvetica', 7.5)
        c.setFillColor(HexColor('#2a5a3a'))
        c.drawRightString(W - 68, cy - 4,  'akfunded.streamlit.app')
        c.drawRightString(W - 68, cy - 16, '@akfunded')
        c.drawRightString(W - 68, cy - 28, 'Simulated Prop Trading')

        # Bottom green bar
        c.setFillColor(accent)
        c.rect(10, 10, W - 20, 3, fill=1, stroke=0)

        c.save()
        buf.seek(0)
        return buf.read()

    except ImportError:
        return None


def goto(page):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()

# ─── UI HELPERS ────────────────────────────────────────────────
def nav():
    logged_in = st.session_state.user is not None
    st.markdown(
        '<div class="ak-nav">'
        f'<div style="display:flex;align-items:center;gap:14px;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\'none\'" style="height:34px;width:34px;object-fit:contain;" />'
        '<div>'
        '<div class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span><span class="ak-beta">BETA</span></div>'
        '<div class="ak-tagline">Trade Crypto. Get Funded. — Get Funded</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )
    if logged_in:
        is_admin = st.session_state.user.get("email","") == st.secrets.get("ADMIN_EMAIL","admin@akfunded.com")
        if is_admin:
            c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = st.columns([0.8,.8,.8,.8,.8,.8,.8,1,.7,.7,.8])
            with c8:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("Alerts"+(f" ({unread})" if unread else ""),key="nb"): goto("notifications")
            with c9:
                if st.button("Admin",key="na"): goto("admin")
            with c10:
                if st.button("My Profile",key="npr"): goto("profile")
        else:
            c0,c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([0.8,.8,.8,.8,.8,.8,.8,1,.7,.8])
            with c8:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("Alerts"+(f" ({unread})" if unread else ""),key="nb"): goto("notifications")
            with c9:
                if st.button("My Profile",key="npr"): goto("profile")
        with c1:
            if st.button("Dashboard",key="nd"): goto("dashboard")
        with c2:
            if st.button("Markets",  key="nm"): goto("markets")
        with c3:
            if st.button("Portfolio",key="np"): goto("portfolio")
        with c4:
            if st.button("Journal",  key="nj"): goto("journal")
        with c5:
            if st.button("History",  key="nh"): goto("history")
        with c6:
            if st.button("Payouts",  key="npo"): goto("payouts")
        with c7:
            if st.button("Leaderboard",key="nl"): goto("leaderboard")
    else:
        c1,c2,c3 = st.columns([5,1,1])
        with c2:
            if st.button("Leaderboard",key="nl2"): goto("leaderboard")
        with c3:
            if st.button("Sign In",key="nl3"): goto("auth")

def footer():
    st.markdown(
        '<div class="ak-footer">'
        f'<div style="display:flex;align-items:center;justify-content:center;gap:1.5rem;margin-bottom:2rem;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\\\'none\\\'" style="height:20px;width:20px;object-fit:contain;opacity:.4;" />'
        '<span style="font-size:.72rem;letter-spacing:4px;color:var(--dim2);font-weight:700;">AKFUNDED</span>'
        '<span style="color:var(--dim2);">|</span>'
        f'<a href="{IG_URL}" target="_blank" style="color:var(--dim);text-decoration:none;font-size:.68rem;letter-spacing:1.5px;">Instagram: <b style="color:var(--cyan);">{IG_HANDLE}</b></a>'
        '</div>'
        '<div style="text-align:center;margin-bottom:1.5rem;">'
        '<div style="font-size:0.55rem;color:var(--dim);letter-spacing:3px;text-transform:uppercase;">Akash Injeti &nbsp;&middot;&nbsp; Founder</div>'
        '</div>'
        '<div style="color:var(--dim2);font-size:.65rem;letter-spacing:1px;text-transform:uppercase;">Simulate. Prove. Get Funded. &nbsp;&middot;&nbsp; All accounts are simulated.</div>'
        '</div>',
        unsafe_allow_html=True
    )

def sec(title, sub=""):
    sub_html = f'<div style="color:var(--dim);font-size:.78rem;margin-top:.4rem;letter-spacing:.5px;font-weight:400;">{sub}</div>' if sub else ""
    st.markdown(
        '<div style="margin-bottom:1.5rem;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.7rem;letter-spacing:4px;color:var(--text);line-height:1;">{title}</div>'
        f'{sub_html}'
        '<div style="width:40px;height:1px;background:var(--cyan);margin-top:.6rem;opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_live_ticker():
    items = ""
    for sym, data in get_all_market_data().items():
        chg  = data["change"]
        cls  = "up" if chg >= 0 else "dn"
        sign = "+" if chg >= 0 else ""
        dec  = 5 if data["price"] < 10 else 2
        items += (
            f'<span class="ticker-sep">&#9670;</span>'
            f'<div class="ticker-item">'
            f'<span class="ticker-sym">{sym}</span>'
            f'<span class="ticker-price">{data["price"]:,.{dec}f}</span>'
            f'<span class="ticker-chg {cls}">{sign}{chg:.2f}%</span>'
            f'</div>'
        )
    st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{items+items}</div></div>', unsafe_allow_html=True)

def render_market_heatmap():
    cells = ""
    for sym, data in get_all_market_data().items():
        chg = data["change"]
        if chg > 1.5:    bg,bord = "rgba(0,184,122,.2)","rgba(0,184,122,.3)"
        elif chg > 0.3:  bg,bord = "rgba(0,184,122,.1)","rgba(0,184,122,.15)"
        elif chg > 0:    bg,bord = "rgba(0,184,122,.04)","#1e1e1e"
        elif chg > -0.3: bg,bord = "rgba(224,58,82,.04)","#1e1e1e"
        elif chg > -1.5: bg,bord = "rgba(224,58,82,.1)","rgba(224,58,82,.15)"
        else:             bg,bord = "rgba(224,58,82,.2)","rgba(224,58,82,.3)"
        sign = "+" if chg >= 0 else ""
        col  = "var(--green)" if chg >= 0 else "var(--red)"
        name = data.get("name", sym)
        cells += (
            f'<div class="hmap-cell" style="background:{bg};border:1px solid {bord};">'
            f'<div class="hmap-sym">{sym}</div>'
            f'<div style="font-size:.6rem;color:var(--dim);margin-top:1px;">{name}</div>'
            f'<div class="hmap-chg" style="color:{col};">{sign}{chg:.2f}%</div>'
            f'</div>'
        )
    st.markdown(f'<div class="heatmap-grid">{cells}</div>', unsafe_allow_html=True)

def render_signal_scanner():
    for sym, data in get_all_market_data().items():
        chg = data["change"]; vol = data["vol"]
        if chg > 1.5 and vol in ["High","Very High"]:   sig,cls = "STRONG BUY","bull"
        elif chg > 0.3:                                  sig,cls = "BUY","bull"
        elif chg < -1.5 and vol in ["High","Very High"]: sig,cls = "STRONG SELL","bear"
        elif chg < -0.3:                                 sig,cls = "SELL","bear"
        else:                                            sig,cls = "NEUTRAL","neut"
        rsi  = random.randint(30,70)
        sign = "+" if chg >= 0 else ""
        col  = "var(--green)" if chg >= 0 else "var(--red)"
        name = data.get("name", sym)
        st.markdown(
            f'<div class="scan-row">'
            f'<div>'
            f'<div class="scan-sym">{sym} <span style="font-size:.65rem;color:var(--dim);font-weight:400;">{name}</span></div>'
            f'<div style="font-size:.65rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;margin-top:2px;">RSI {rsi} &nbsp;|&nbsp; Vol: {vol}</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div class="scan-signal {cls}">{sig}</div>'
            f'<div style="font-size:.68rem;color:{col};font-family:\'JetBrains Mono\',monospace;margin-top:4px;">{sign}{chg:.2f}%</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

def pbar(pct, col):
    return f'<div class="prog"><div class="prog-fill" style="width:{pct:.1f}%;background:{col};box-shadow:0 0 4px {col};"></div></div>'




# ─── AI SUPPORT CHATBOT — Groq via Streamlit sidebar ─────────
if "chat_support_msgs" not in st.session_state:
    st.session_state.chat_support_msgs = []
if "chatbot_open" not in st.session_state:
    st.session_state.chatbot_open = False

# Floating chat widget via components — pure HTML/JS/CSS
# Groq API called directly from JS using the key from secrets
_groq_key = st.secrets.get("GROQ_API_KEY","")
st.markdown(f"""
<style>
#ak-fab{{position:fixed;bottom:28px;right:28px;z-index:99998;width:56px;height:56px;
  border-radius:50%;background:linear-gradient(135deg,#00D4FF,#00B87A);
  border:none;cursor:pointer;font-size:1.4rem;display:flex;align-items:center;
  justify-content:center;box-shadow:0 4px 28px rgba(0,212,255,.45);
  transition:transform .2s,box-shadow .2s;}}
#ak-fab:hover{{transform:scale(1.1);box-shadow:0 8px 36px rgba(0,212,255,.6);}}
#ak-fab.open{{background:linear-gradient(135deg,#444,#222);}}
#ak-win{{position:fixed;bottom:98px;right:28px;z-index:99997;width:380px;height:540px;
  background:#090909;border:1px solid #1c1c1c;border-radius:6px;display:none;
  flex-direction:column;overflow:hidden;
  box-shadow:0 24px 64px rgba(0,0,0,.85),0 0 0 1px rgba(0,212,255,.07);
  font-family:Rajdhani,sans-serif;}}
#ak-win.open{{display:flex;}}
#ak-hd{{background:#050505;border-bottom:1px solid #181818;padding:.9rem 1rem;
  display:flex;align-items:center;gap:.75rem;flex-shrink:0;}}
.ak-pulse{{width:7px;height:7px;background:#00B87A;border-radius:50%;
  box-shadow:0 0 8px #00B87A;animation:akP 2s infinite;}}
@keyframes akP{{0%,100%{{opacity:1;}}50%{{opacity:.2;}}}}
#ak-hd-t{{font-family:"Bebas Neue",sans-serif;font-size:1rem;letter-spacing:3px;color:#d8d8d8;}}
#ak-hd-s{{font-size:.5rem;color:#2a2a2a;letter-spacing:2px;text-transform:uppercase;margin-top:2px;}}
#ak-msgs{{flex:1;overflow-y:auto;padding:.9rem;display:flex;flex-direction:column;
  gap:.65rem;scrollbar-width:thin;scrollbar-color:#1e1e1e transparent;}}
#ak-msgs::-webkit-scrollbar{{width:3px;}}
#ak-msgs::-webkit-scrollbar-thumb{{background:#1e1e1e;}}
.ak-m{{max-width:85%;padding:.65rem .9rem;font-size:.76rem;line-height:1.6;
  border-radius:3px;word-break:break-word;}}
.ak-m.b{{background:#111;border:1px solid #1e1e1e;border-left:2px solid #00D4FF;
  color:#d0d0d0;align-self:flex-start;}}
.ak-m.u{{background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.2);
  color:#d0d0d0;align-self:flex-end;text-align:right;}}
#ak-qs{{padding:.5rem .8rem;display:flex;flex-wrap:wrap;gap:4px;
  border-top:1px solid #111;flex-shrink:0;}}
.ak-q{{background:#0d0d0d;border:1px solid #1c1c1c;color:#3a3a3a;font-size:.54rem;
  letter-spacing:1.5px;padding:3px 9px;cursor:pointer;border-radius:2px;
  transition:all .15s;font-family:Rajdhani,sans-serif;text-transform:uppercase;}}
.ak-q:hover{{border-color:rgba(0,212,255,.4);color:#00D4FF;}}
#ak-ir{{display:flex;gap:5px;padding:.65rem .8rem;border-top:1px solid #181818;
  flex-shrink:0;background:#050505;}}
#ak-inp{{flex:1;background:#0d0d0d;border:1px solid #1c1c1c;color:#d8d8d8;
  font-size:.73rem;padding:.5rem .8rem;outline:none;font-family:Rajdhani,sans-serif;
  border-radius:2px;}}
#ak-inp:focus{{border-color:rgba(0,212,255,.35);}}
#ak-inp::placeholder{{color:#252525;}}
#ak-send{{background:linear-gradient(135deg,#00D4FF,#00B87A);border:none;color:#000;
  font-size:.62rem;font-weight:700;padding:.5rem 1rem;cursor:pointer;letter-spacing:1.5px;
  font-family:Rajdhani,sans-serif;border-radius:2px;white-space:nowrap;}}
#ak-send:disabled{{opacity:.4;cursor:not-allowed;}}
</style>

<button id="ak-fab" onclick="akT()">&#x1F4AC;</button>

<div id="ak-win">
  <div id="ak-hd">
    <div class="ak-pulse"></div>
    <div>
      <div id="ak-hd-t">AK SUPPORT</div>
      <div id="ak-hd-s">AI Assistant &middot; Powered by Groq</div>
    </div>
    <div style="margin-left:auto;cursor:pointer;color:#333;font-size:.9rem;padding:4px 8px;" onclick="akT()">&#x2715;</div>
  </div>
  <div id="ak-msgs">
    <div class="ak-m b">Hey &#x1F44B; I&apos;m your <strong>AKFunded</strong> AI assistant.<br><br>Ask me anything about challenges, payouts, rules, or getting funded!</div>
  </div>
  <div id="ak-qs">
    <button class="ak-q" onclick="akQ('How do payouts work?')">Payouts</button>
    <button class="ak-q" onclick="akQ('What are the trading rules?')">Rules</button>
    <button class="ak-q" onclick="akQ('Tips to pass the challenge')">Pass Tips</button>
    <button class="ak-q" onclick="akQ('What plans are available?')">Plans</button>
    <button class="ak-q" onclick="akQ('Is news trading allowed?')">News OK?</button>
    <button class="ak-q" onclick="akQ('What instruments can I trade?')">Instruments</button>
  </div>
  <div id="ak-ir">
    <input id="ak-inp" placeholder="Ask anything..." onkeydown="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();akS();}}"/>
    <button id="ak-send" onclick="akS()">SEND</button>
  </div>
</div>

<script>
(function(){{
  const GROQ_KEY = "{_groq_key}";
  const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
  const SYSTEM = "You are AKFunded\'s helpful AI support assistant. AKFunded is a prop trading firm. Plans: Instant Funded (70-75% split, no evaluation), One-Step (8% target, 80% split), Two-Step (8%+5% targets, 90% split). Accounts $5K-$100K. Payouts within 24hr. News trading allowed. No time limit. Instruments: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT. Daily loss limit 3-5%, max drawdown 6-10%. Answer concisely in 2-4 sentences. Be warm and encouraging.";
  const history = [];
  let busy = false;

  function addMsg(text, cls){{
    const d = document.getElementById("ak-msgs");
    const el = document.createElement("div");
    el.className = "ak-m " + cls;
    el.innerHTML = text;
    d.appendChild(el);
    d.scrollTop = d.scrollHeight;
    return el;
  }}

  window.akT = function(){{
    const w = document.getElementById("ak-win");
    const b = document.getElementById("ak-fab");
    const isOpen = w.classList.toggle("open");
    b.classList.toggle("open");
    b.innerHTML = isOpen ? "&#x2715;" : "&#x1F4AC;";
    if(isOpen) setTimeout(()=>document.getElementById("ak-inp").focus(), 120);
  }};

  window.akQ = function(q){{
    document.getElementById("ak-inp").value = q;
    akS();
  }};

  async function akS(){{
    if(busy) return;
    const inp = document.getElementById("ak-inp");
    const txt = inp.value.trim();
    if(!txt) return;
    inp.value = "";
    addMsg(txt, "u");
    history.push({{role:"user", content:txt}});
    busy = true;
    document.getElementById("ak-send").disabled = true;
    const typing = addMsg("<span style=\"color:#2a2a2a;font-style:italic;\">Thinking&hellip;</span>", "b");

    try{{
      const res = await fetch(GROQ_URL, {{
        method: "POST",
        headers: {{
          "Content-Type": "application/json",
          "Authorization": "Bearer " + GROQ_KEY
        }},
        body: JSON.stringify({{
          model: "llama-3.3-70b-versatile",
          max_tokens: 300,
          temperature: 0.7,
          messages: [{{role:"system",content:SYSTEM}}, ...history.slice(-8)]
        }})
      }});
      const data = await res.json();
      const reply = data?.choices?.[0]?.message?.content || "Sorry, I couldn\'t get a response. Please try again.";
      typing.remove();
      addMsg(reply, "b");
      history.push({{role:"assistant", content:reply}});
    }} catch(e){{
      typing.remove();
      addMsg("Connection error. Please check your internet and try again.", "b");
    }}
    busy = false;
    document.getElementById("ak-send").disabled = false;
    document.getElementById("ak-inp").focus();
  }}

  window.akS = akS;
}})();
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    # ── SPLASH INTRO SCREEN — injected into parent page (true fullscreen) ──
    splash_logo = LOGO_URL
    st.markdown(f"""
<script>
(function(){{
  // Only show once per session
  if(sessionStorage.getItem('akfunded_splashed')) return;
  sessionStorage.setItem('akfunded_splashed','1');

  const logo = "{splash_logo}";

  // Inject Google Fonts
  const link = document.createElement('link');
  link.rel='stylesheet';
  link.href='https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@300;400;600;700&display=swap';
  document.head.appendChild(link);

  // Inject styles
  const style = document.createElement('style');
  style.textContent = `
    #ak-splash {{
      position:fixed; top:0; left:0; width:100vw; height:100vh;
      background:#050505; z-index:999999;
      display:flex; flex-direction:column;
      align-items:center; justify-content:center;
      overflow:hidden;
      transition: opacity 0.9s ease, transform 0.9s ease;
    }}
    #ak-splash.fade-out {{ opacity:0; transform:scale(1.05); pointer-events:none; }}

    #ak-bg {{ position:absolute; top:0; left:0; width:100%; height:100%; z-index:0; }}

    .ak-corner {{
      position:absolute; width:44px; height:44px; z-index:2;
      opacity:0; animation: ak-fadeIn 0.5s ease forwards 0.3s;
    }}
    .ak-corner-tl {{ top:24px; left:24px; border-top:1px solid rgba(0,212,255,0.4); border-left:1px solid rgba(0,212,255,0.4); }}
    .ak-corner-tr {{ top:24px; right:24px; border-top:1px solid rgba(0,212,255,0.4); border-right:1px solid rgba(0,212,255,0.4); }}
    .ak-corner-bl {{ bottom:24px; left:24px; border-bottom:1px solid rgba(0,212,255,0.4); border-left:1px solid rgba(0,212,255,0.4); }}
    .ak-corner-br {{ bottom:24px; right:24px; border-bottom:1px solid rgba(0,212,255,0.4); border-right:1px solid rgba(0,212,255,0.4); }}

    .ak-scanline {{
      position:absolute; left:0; right:0; height:1px; z-index:2;
      background:linear-gradient(90deg,transparent,rgba(0,212,255,0.2),transparent);
      animation: ak-scan 3s ease-in-out infinite 0.8s;
    }}
    @keyframes ak-scan {{
      0%   {{ top:0%; opacity:0; }}
      5%   {{ opacity:1; }}
      95%  {{ opacity:1; }}
      100% {{ top:100%; opacity:0; }}
    }}

    .ak-inner {{
      position:relative; z-index:3;
      display:flex; flex-direction:column;
      align-items:center; text-align:center;
    }}

    .ak-logo-wrap {{
      position:relative; width:150px; height:150px;
      display:flex; align-items:center; justify-content:center;
      margin-bottom:2.2rem;
      animation: ak-logoIn 1.2s cubic-bezier(0.16,1,0.3,1) forwards;
      opacity:0;
    }}
    @keyframes ak-logoIn {{
      0%   {{ opacity:0; transform:scale(0.2) rotateY(180deg); }}
      60%  {{ opacity:1; transform:scale(1.1) rotateY(-6deg); }}
      100% {{ opacity:1; transform:scale(1) rotateY(0deg); }}
    }}
    .ak-orbit1 {{
      position:absolute; width:136px; height:136px; border-radius:50%;
      border:1px solid rgba(0,212,255,0.45);
      box-shadow:0 0 14px rgba(0,212,255,0.15);
      animation:ak-spin 3s linear infinite;
    }}
    .ak-orbit1::before {{
      content:''; position:absolute; top:-4px; left:50%;
      width:8px; height:8px; background:#00D4FF; border-radius:50%;
      box-shadow:0 0 12px #00D4FF, 0 0 24px rgba(0,212,255,0.5);
      transform:translateX(-50%);
    }}
    .ak-orbit2 {{
      position:absolute; width:112px; height:112px; border-radius:50%;
      border:1px solid rgba(0,184,122,0.3);
      animation:ak-spin 5s linear infinite reverse;
    }}
    .ak-orbit2::before {{
      content:''; position:absolute; bottom:-3px; left:50%;
      width:6px; height:6px; background:#00B87A; border-radius:50%;
      box-shadow:0 0 8px #00B87A;
      transform:translateX(-50%);
    }}
    @keyframes ak-spin {{ from{{transform:rotate(0deg);}} to{{transform:rotate(360deg);}} }}

    .ak-logo-img {{
      width:78px; height:78px; object-fit:contain; position:relative; z-index:2;
      filter:drop-shadow(0 0 24px rgba(0,212,255,0.6));
    }}

    .ak-welcome {{
      font-family:'Rajdhani',sans-serif;
      font-size:.7rem; letter-spacing:6px; color:#00D4FF;
      text-transform:uppercase; font-weight:600;
      opacity:0; transform:translateY(14px);
      animation:ak-up 0.6s ease forwards 1s;
      margin-bottom:.5rem;
    }}
    .ak-brand {{
      font-family:'Bebas Neue',sans-serif;
      font-size:clamp(4rem,9vw,7.5rem);
      letter-spacing:10px; line-height:1;
      opacity:0; transform:translateY(18px);
      animation:ak-up 0.7s ease forwards 1.2s;
    }}
    .ak-brand-ak {{ color:#00D4FF; text-shadow:0 0 50px rgba(0,212,255,0.6), 0 0 100px rgba(0,212,255,0.2); }}
    .ak-brand-funded {{ color:#ffffff; }}
    .ak-tagline {{
      font-family:'Rajdhani',sans-serif;
      font-size:.8rem; letter-spacing:4px; color:#2e2e2e;
      text-transform:uppercase; font-weight:400;
      opacity:0; transform:translateY(12px);
      animation:ak-up 0.6s ease forwards 1.5s;
      margin-top:.9rem;
    }}

    .ak-bar-wrap {{
      width:240px; height:1px; background:rgba(255,255,255,0.06);
      margin-top:2.8rem; overflow:hidden;
      opacity:0; animation:ak-fadeIn 0.4s ease forwards 1.8s;
    }}
    .ak-bar {{
      height:100%; width:0%;
      background:linear-gradient(90deg,#00D4FF,#00B87A);
      box-shadow:0 0 10px #00D4FF;
      animation:ak-load 1.8s ease forwards 1.9s;
    }}
    @keyframes ak-load {{ 0%{{width:0%;}} 100%{{width:100%;}} }}

    .ak-status {{
      font-family:'Rajdhani',sans-serif;
      font-size:.52rem; letter-spacing:3px; color:#252525;
      text-transform:uppercase; margin-top:.7rem;
      opacity:0; animation:ak-fadeIn 0.4s ease forwards 2s;
    }}

    @keyframes ak-up {{
      from {{ opacity:0; transform:translateY(14px); }}
      to   {{ opacity:1; transform:translateY(0); }}
    }}
    @keyframes ak-fadeIn {{
      from {{ opacity:0; }} to {{ opacity:1; }}
    }}
  `;
  document.head.appendChild(style);

  // Build splash DOM
  const splash = document.createElement('div');
  splash.id = 'ak-splash';
  splash.innerHTML = `
    <canvas id="ak-bg"></canvas>
    <div class="ak-corner ak-corner-tl"></div>
    <div class="ak-corner ak-corner-tr"></div>
    <div class="ak-corner ak-corner-bl"></div>
    <div class="ak-corner ak-corner-br"></div>
    <div class="ak-scanline"></div>
    <div class="ak-inner">
      <div class="ak-logo-wrap">
        <div class="ak-orbit1"></div>
        <div class="ak-orbit2"></div>
        <img class="ak-logo-img" src="${{logo}}" onerror="this.style.display='none'" />
      </div>
      <div class="ak-welcome">Welcome to</div>
      <div class="ak-brand">
        <span class="ak-brand-ak">AK</span><span class="ak-brand-funded">FUNDED</span>
      </div>
      <div class="ak-tagline">Trade Crypto. Get Funded. — Get Funded</div>
      <div class="ak-bar-wrap"><div class="ak-bar"></div></div>
      <div class="ak-status" id="ak-status">Initializing platform...</div>
    </div>
  `;
  document.body.appendChild(splash);

  // Particle canvas
  const canvas = document.getElementById('ak-bg');
  const ctx = canvas.getContext('2d');
  function resize() {{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; }}
  resize();
  window.addEventListener('resize', resize);

  const pts = Array.from({{length:100}}, ()=>{{
    const a=Math.random()*Math.PI*2;
    const d=50+Math.random()*Math.max(window.innerWidth,window.innerHeight)*0.72;
    return {{
      x:window.innerWidth/2, y:window.innerHeight/2,
      tx:window.innerWidth/2+Math.cos(a)*d,
      ty:window.innerHeight/2+Math.sin(a)*d,
      prog:0, speed:0.003+Math.random()*0.006,
      col:Math.random()>.6?'#00D4FF':Math.random()>.5?'#00B87A':'#D4A843',
      sz:Math.random()*1.8+0.4,
    }};
  }});

  let fr=0;
  function draw(){{
    const W=canvas.width, H=canvas.height;
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#050505'; ctx.fillRect(0,0,W,H);
    // center glow
    const g=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.min(W,H)*0.4);
    g.addColorStop(0,'rgba(0,212,255,0.06)'); g.addColorStop(1,'transparent');
    ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
    // grid
    ctx.strokeStyle='rgba(0,212,255,0.04)'; ctx.lineWidth=0.5;
    const gs=80;
    for(let x=0;x<W;x+=gs){{ ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke(); }}
    for(let y=0;y<H;y+=gs){{ ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke(); }}
    // particles
    pts.forEach(p=>{{
      if(fr>20) p.prog=Math.min(1,p.prog+p.speed);
      const cx=p.x+(p.tx-p.x)*p.prog, cy=p.y+(p.ty-p.y)*p.prog;
      const al=p.prog*0.7;
      ctx.globalAlpha=al;
      ctx.beginPath(); ctx.arc(cx,cy,p.sz,0,Math.PI*2);
      ctx.fillStyle=p.col; ctx.fill();
      if(al>.3){{ ctx.beginPath();ctx.arc(cx,cy,p.sz*3.5,0,Math.PI*2);ctx.fillStyle=p.col+'18';ctx.fill(); }}
    }});
    ctx.globalAlpha=1;
    fr++;
    if(document.getElementById('ak-splash')) requestAnimationFrame(draw);
  }}
  draw();

  // Status cycling
  const statuses=['Initializing platform...','Loading market data...','Connecting to trading engine...','Almost ready...'];
  let si=0;
  const st2=setInterval(()=>{{
    si++; if(si<statuses.length) document.getElementById('ak-status').textContent=statuses[si];
    else clearInterval(st2);
  }},600);

  // Dismiss after 3.8s
  setTimeout(()=>{{
    splash.style.transition='opacity 0.9s ease, transform 0.9s ease';
    splash.style.opacity='0';
    splash.style.transform='scale(1.05)';
    setTimeout(()=>{{ if(splash.parentNode) splash.parentNode.removeChild(splash); }}, 950);
  }}, 3800);
}})();
</script>
""", unsafe_allow_html=True)

    nav()
    render_live_ticker()

    hero_logo = LOGO_URL
    st.components.v1.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;600;700&display=swap');
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:#020108;overflow:hidden;}}
  #hero{{
    position:relative;
    width:100%;
    height:600px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    overflow:hidden;
    background:#020108;
  }}
  #bgCanvas{{
    position:absolute;
    top:0;left:0;
    width:100%;height:100%;
    z-index:0;
  }}
  .hero-content{{
    position:relative;
    z-index:2;
    text-align:center;
    display:flex;
    flex-direction:column;
    align-items:center;
  }}
  .hero-logo{{
    height:68px;width:68px;
    object-fit:contain;
    margin-bottom:1.6rem;
    filter:drop-shadow(0 0 24px rgba(249,0,255,.5));
    animation:floatLogo 4s ease-in-out infinite;
  }}
  @keyframes floatLogo{{
    0%,100%{{transform:translateY(0);}}
    50%{{transform:translateY(-8px);}}
  }}
  .eyebrow{{
    display:inline-flex;
    align-items:center;
    gap:.6rem;
    border:1px solid rgba(212,175,55,.3);
    color:#D4AF37;
    font-size:.65rem;
    letter-spacing:4px;
    padding:6px 20px;
    border-radius:2px;
    margin-bottom:2.5rem;
    text-transform:uppercase;
    background:rgba(212,175,55,.05);
    font-family:'Orbitron',sans-serif;
    font-weight:600;
  }}
  .eyebrow-dot{{
    width:6px;height:6px;
    background:#F3E5AB;
    border-radius:50%;
    display:inline-block;
    animation:blink 2s infinite;
    box-shadow:0 0 10px #F3E5AB;
  }}
  @keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:.2;}}}}
  .hero-h1{{
    font-family:'Orbitron',sans-serif;
    font-weight:900;
    font-size:clamp(3.5rem,7vw,7.5rem);
    line-height:1;
    letter-spacing:2px;
    color:#EAF0FF;
    margin:0 0 1.5rem;
    text-shadow:0 0 40px rgba(243,229,171,.2);
  }}
  .hero-h1 em{{
    color:#F3E5AB;
    font-style:normal;
    text-shadow:0 0 40px rgba(243,229,171,.6), 0 0 80px rgba(243,229,171,.3);
  }}
  .hero-sub{{
    font-size:1.1rem;
    color:#687A9E;
    max-width:500px;
    line-height:1.8;
    font-weight:500;
    letter-spacing:1px;
    font-family:'Rajdhani',sans-serif;
  }}
</style>
</head>
<body>
<div id="hero">
  <canvas id="bgCanvas"></canvas>
  <div class="hero-content">
    <div style="background:rgba(212,175,55,0.08); padding:1rem; border-radius:12px; display:inline-block; margin-bottom:1.5rem; border:1px solid rgba(212,175,55,0.3); box-shadow:0 0 30px rgba(212,175,55,0.2);">
      <img class="hero-logo" src="{hero_logo}" style="margin-bottom:0;" onerror="this.style.display='none'" />
    </div>
    <div class="eyebrow"><span class="eyebrow-dot"></span> Crypto &middot; Bitcoin &middot; Ethereum &middot; Prop Trading</div>
    <div class="hero-h1">TRADE CRYPTO.<br>GET FUNDED.<br><em>KEEP UP TO 90%.</em></div>
    <p class="hero-sub">Prove your consistency on Bitcoin, Ethereum and top crypto markets.<br>Pass the challenge. Earn a funded account. Keep up to 90% of your profits.</p>
  </div>
</div>

<script>
(function(){{
  const canvas = document.getElementById('bgCanvas');
  const ctx    = canvas.getContext('2d');
  let W, H;

  function resize(){{
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }}
  resize();
  window.addEventListener('resize', resize);

  // ── 3D MOUSE PARALLAX TILT ──
  const heroContent = document.querySelector('.hero-content');
  const hero = document.getElementById('hero');
  
  hero.addEventListener('mousemove', e => {{
    const rect = hero.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width/2;
    const y = e.clientY - rect.top - rect.height/2;
    heroContent.style.transform = `perspective(1200px) rotateX(${{-y/40}}deg) rotateY(${{x/40}}deg) scale3d(1.05, 1.05, 1.05)`;
    heroContent.style.transition = 'transform 0.1s ease-out';
  }});
  
  hero.addEventListener('mouseleave', () => {{
    heroContent.style.transform = `perspective(1200px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
    heroContent.style.transition = 'transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)';
  }});

  // ── PARTICLES ──────────────────────────────────────────────
  const PARTICLE_COUNT = 180;
  const particles = Array.from({{length: PARTICLE_COUNT}}, () => ({{
    x: Math.random() * 1600,
    y: Math.random() * 600,
    z: Math.random() * 1200 + 100,
    vx: (Math.random() - 0.5) * 1.5,
    vy: (Math.random() - 0.5) * 1.0,
    vz: -1.0 - Math.random() * 2.0,
    color: Math.random() > 0.6 ? '#00F3FF' : Math.random() > 0.5 ? '#00FF85' : '#F900FF',
    size: Math.random() * 2 + 0.5,
  }}));

  // ── GRID LINES (perspective) ──────────────────────────────
  const GRID_ROWS = 14, GRID_COLS = 16;
  const GRID_Z_NEAR = 60, GRID_Z_FAR = 1400;
  const GRID_W = 2800, GRID_H_WORLD = 600;
  let gridOffset = 0;

  // ── FLOATING RINGS ────────────────────────────────────────
  const rings = [
    {{ x: 0.18, y: 0.38, r: 120, rot: 0,   rotV: 0.02,   tiltX: 0.55, tiltY: 0.3,  color: '#00F3FF', alpha: 0.2 }},
    {{ x: 0.82, y: 0.45, r: 90,  rot: 1.2, rotV: -0.015, tiltX: 0.4,  tiltY: 0.6,  color: '#00FF85', alpha: 0.15 }},
    {{ x: 0.5,  y: 0.15, r: 60,  rot: 0.5, rotV: 0.03,   tiltX: 0.7,  tiltY: 0.2,  color: '#F900FF', alpha: 0.2 }},
    {{ x: 0.12, y: 0.72, r: 54,  rot: 2.1, rotV: -0.02,  tiltX: 0.3,  tiltY: 0.65, color: '#00F3FF', alpha: 0.15 }},
    {{ x: 0.88, y: 0.78, r: 75,  rot: 1.8, rotV: 0.018,  tiltX: 0.5,  tiltY: 0.4,  color: '#A200FF', alpha: 0.15 }},
  ];

  // ── DATA STREAM LINES ─────────────────────────────────────
  const streams = Array.from({{length: 25}}, () => ({{
    x: Math.random() * 1600,
    y: 0,
    len: 60 + Math.random() * 100,
    speed: 3 + Math.random() * 4,
    alpha: 0.1 + Math.random() * 0.15,
    color: Math.random() > 0.5 ? '#00F3FF' : '#F900FF',
  }}));

  // ── FLOATING PRICE TAGS ───────────────────────────────────
  const tags = [
    {{ sym:'BTCUSDT', price:'69,450.20', chg:'+1.42%', up:true,  x:0.08, y:0.22, vy:-0.18, rz: -0.05 }},
    {{ sym:'ETHUSDT', price:'3,780.40',  chg:'+2.12%', up:true,  x:0.80, y:0.28, vy: 0.15, rz:  0.03 }},
    {{ sym:'SOLUSDT', price:'168.20',    chg:'+5.08%', up:true,  x:0.88, y:0.60, vy:-0.14, rz:  0.04 }},
    {{ sym:'XRPUSDT', price:'0.52',      chg:'-1.20%', up:false, x:0.04, y:0.65, vy: 0.16, rz: -0.02 }},
  ];
  tags.forEach(t => {{ t.fy = t.y * 600; t.oy = t.fy; }});

  let frame = 0;

  function drawRing(ring){{
    const rx = ring.x * W, ry = ring.fy !== undefined ? ring.fy : ring.y * H;
    ctx.save();
    ctx.translate(rx, ry);
    ctx.rotate(ring.rot);
    ctx.scale(1, ring.tiltX);
    ctx.beginPath();
    ctx.ellipse(0, 0, ring.r, ring.r * ring.tiltY, 0, 0, Math.PI * 2);
    ctx.strokeStyle = ring.color;
    ctx.globalAlpha = ring.alpha;
    ctx.lineWidth = 1;
    ctx.stroke();
    // Inner ring
    ctx.beginPath();
    ctx.ellipse(0, 0, ring.r * 0.6, ring.r * 0.6 * ring.tiltY, 0, 0, Math.PI * 2);
    ctx.globalAlpha = ring.alpha * 0.5;
    ctx.stroke();
    ctx.restore();
  }}

  function drawPerspectiveGrid(){{
    const vanishX = W / 2, vanishY = H * 0.52;
    const floorY  = H + 20;
    ctx.globalAlpha = 1;

    // Horizontal lines (moving toward viewer)
    for(let r = 0; r <= GRID_ROWS; r++){{
      const t   = (r / GRID_ROWS + gridOffset) % 1;
      const ease = t * t;
      const y   = vanishY + (floorY - vanishY) * ease;
      const xL  = vanishX - (W * 0.7) * ease;
      const xR  = vanishX + (W * 0.7) * ease;
      const a   = ease * 0.13;
      ctx.beginPath();
      ctx.moveTo(xL, y); ctx.lineTo(xR, y);
      ctx.strokeStyle = `rgba(0,212,255,${{a.toFixed(3)}})`;
      ctx.lineWidth   = 0.5;
      ctx.stroke();
    }}
    // Vertical lines (radiating from vanishing point)
    for(let c = 0; c <= GRID_COLS; c++){{
      const frac = c / GRID_COLS;
      const xFar = vanishX;
      const xNear = W * frac * 1.15 - W * 0.075;
      const g = ctx.createLinearGradient(xFar, vanishY, xNear, floorY);
      g.addColorStop(0, 'rgba(0,212,255,0)');
      g.addColorStop(1, 'rgba(0,212,255,0.07)');
      ctx.beginPath();
      ctx.moveTo(xFar, vanishY); ctx.lineTo(xNear, floorY);
      ctx.strokeStyle = g;
      ctx.lineWidth   = 0.5;
      ctx.stroke();
    }}
    gridOffset += 0.0025;
    if(gridOffset >= 1) gridOffset = 0;
  }}

  function drawParticles(){{
    const fovX = W / 2, fovY = H / 2;
    particles.forEach(p => {{
      p.x += p.vx; p.y += p.vy; p.z += p.vz;
      if(p.z < 10){{
        p.z = 1200; p.x = Math.random() * 1600; p.y = Math.random() * 600;
      }}
      const scale = 600 / p.z;
      const sx = fovX + (p.x - 800) * scale;
      const sy = fovY + (p.y - 300) * scale;
      const r  = p.size * scale;
      const a  = Math.min(1, (1200 - p.z) / 1000) * 0.7;
      if(sx < -10 || sx > W + 10 || sy < -10 || sy > H + 10) return;
      ctx.globalAlpha = a;
      ctx.beginPath();
      ctx.arc(sx, sy, Math.max(r, 0.3), 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();
      // Glow
      if(a > 0.3){{
        ctx.beginPath();
        ctx.arc(sx, sy, Math.max(r * 3, 1), 0, Math.PI * 2);
        ctx.fillStyle = p.color + '22';
        ctx.fill();
      }}
    }});
    ctx.globalAlpha = 1;
  }}

  function drawStreams(){{
    streams.forEach(s => {{
      s.y += s.speed;
      if(s.y > H + s.len) {{ s.y = -s.len; s.x = Math.random() * W; }}
      const g = ctx.createLinearGradient(s.x, s.y - s.len, s.x, s.y);
      g.addColorStop(0, 'transparent');
      g.addColorStop(1, s.color);
      ctx.globalAlpha = s.alpha;
      ctx.strokeStyle = g;
      ctx.lineWidth = 0.8;
      ctx.beginPath();
      ctx.moveTo(s.x, s.y - s.len);
      ctx.lineTo(s.x, s.y);
      ctx.stroke();
    }});
    ctx.globalAlpha = 1;
  }}

  function drawFloatingTags(){{
    tags.forEach(t => {{
      t.fy += t.vy;
      if(t.fy < -40) t.fy = H + 20;
      if(t.fy > H + 20) t.fy = -40;
      const tx = t.x * W, ty = t.fy;
      ctx.save();
      ctx.translate(tx + 54, ty + 20); // Center of tag
      ctx.rotate(t.rz);
      ctx.translate(-54, -20);
      
      ctx.globalAlpha = 0.65;
      ctx.fillStyle = 'rgba(12,10,25,0.8)';
      ctx.strokeStyle = t.up ? 'rgba(0,255,133,0.5)' : 'rgba(255,0,60,0.5)';
      ctx.lineWidth = 1.2;
      const bw = 114, bh = 44;
      ctx.beginPath();
      ctx.rect(0, 0, bw, bh);
      ctx.fill(); ctx.stroke();
      // Left accent bar
      ctx.fillStyle = t.up ? '#00FF85' : '#FF003C';
      ctx.fillRect(0, 0, 3, bh);
      // Symbol
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = '#EAF0FF';
      ctx.font = 'bold 10px Orbitron';
      ctx.fillText(t.sym, 10, 15);
      // Price
      ctx.fillStyle = '#00F3FF';
      ctx.font = 'bold 13px Rajdhani';
      ctx.fillText(t.price, 10, 30);
      // Change
      ctx.fillStyle = t.up ? '#00FF85' : '#FF003C';
      ctx.font = '9px Orbitron';
      ctx.fillText(t.chg, 10, 40);
      
      ctx.restore();
    }});
  }}

  function drawCentralGlow(){{
    const gx = W / 2, gy = H * 0.45;
    const g1 = ctx.createRadialGradient(gx, gy, 0, gx, gy, W * 0.55);
    g1.addColorStop(0, 'rgba(0,243,255,0.06)');
    g1.addColorStop(0.3,'rgba(249,0,255,0.03)');
    g1.addColorStop(1, 'transparent');
    ctx.globalAlpha = 1;
    ctx.fillStyle = g1;
    ctx.fillRect(0, 0, W, H);

    // Subtle center cross-light
    const g2 = ctx.createRadialGradient(gx, gy, 0, gx, gy, 180);
    g2.addColorStop(0, 'rgba(0,212,255,0.06)');
    g2.addColorStop(1, 'transparent');
    ctx.fillStyle = g2;
    ctx.beginPath();
    ctx.arc(gx, gy, 180, 0, Math.PI * 2);
    ctx.fill();
  }}

  function animate(){{
    ctx.clearRect(0, 0, W, H);

    // Base fill
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, W, H);

    drawCentralGlow();
    drawPerspectiveGrid();
    drawStreams();
    drawParticles();
    rings.forEach(r => {{
      r.rot += r.rotV;
      r.fy = (r.fy || r.y * 600);
      drawRing(r);
    }});
    drawFloatingTags();

    frame++;
    requestAnimationFrame(animate);
  }}
  animate();
}})();
</script>
</body>
</html>
""", height=610, scrolling=False)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("Start Challenge", use_container_width=True): goto("plans")

    # ── GLOBAL TRADING NETWORK — upgraded with GLB + new stats ──
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;">GLOBAL TRADING NETWORK</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>', unsafe_allow_html=True)
    st.components.v1.html(f"""
<style>
  #gn-wrap {{ width:100%;display:flex;align-items:center;justify-content:center;gap:2.5rem;padding:1.5rem 0 2.5rem;background:transparent; }}
  #gn-center {{ position:relative;width:420px;height:420px;flex-shrink:0; }}
  #gn-canvas {{ position:absolute;top:0;left:0;width:100%;height:100%; }}
  #gn-glb {{ position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:260px;height:260px;pointer-events:none; }}
  .gn-stats {{ display:flex;flex-direction:column;gap:1rem; }}
  .gs {{ background:#0a0a0a;border:1px solid #1a1a1a;border-left:3px solid #00D4FF;padding:1rem 1.5rem;min-width:220px;position:relative;overflow:hidden; }}
  .gs::after {{ content:"";position:absolute;top:0;right:0;bottom:0;width:2px;background:linear-gradient(180deg,transparent,rgba(0,212,255,.15),transparent); }}
  .gs-val {{ font-family:"Courier New",monospace;font-size:1.7rem;font-weight:700;color:#00D4FF;letter-spacing:2px;line-height:1; }}
  .gs-val.gr {{ color:#00B87A; }}
  .gs-val.go {{ color:#D4A843; }}
  .gs-val.gp {{ color:#7B6EF6; }}
  .gs-lbl {{ font-size:.55rem;color:#404040;letter-spacing:3px;text-transform:uppercase;margin-top:5px; }}
  .gs-sub {{ font-size:.5rem;color:#2a2a2a;letter-spacing:1.5px;margin-top:2px; }}
  /* counter animation */
  .gs-val[data-target] {{ opacity:0;animation:gsIn .6s ease forwards; }}
  @keyframes gsIn {{ from{{opacity:0;transform:translateY(8px);}} to{{opacity:1;transform:translateY(0);}} }}
</style>

<div id="gn-wrap">
  <div id="gn-center">
    <canvas id="gn-canvas"></canvas>
  </div>
  <div class="gn-stats">
    <div class="gs"><div class="gs-val" id="cnt-traders">0</div><div class="gs-lbl">Traders Worldwide</div><div class="gs-sub">Active funded accounts</div></div>
    <div class="gs"><div class="gs-val gr" id="cnt-payouts">$0</div><div class="gs-lbl">Total Payouts Processed</div><div class="gs-sub">And growing every day</div></div>
    <div class="gs"><div class="gs-val go" id="cnt-split">0%</div><div class="gs-lbl">Max Profit Split</div><div class="gs-sub">Two-Step plan</div></div>
    <div class="gs"><div class="gs-val gp" id="cnt-payout">0hr</div><div class="gs-lbl">Average Payout Time</div><div class="gs-sub">Fastest in industry</div></div>
  </div>
</div>

<script>
(function(){{
  // ── Counter animation ──
  function animCount(id, target, prefix, suffix, duration){{ 
    const el=document.getElementById(id); if(!el) return;
    let start=null;
    function step(ts){{
      if(!start) start=ts;
      const prog=Math.min((ts-start)/duration,1);
      const ease=1-Math.pow(1-prog,3);
      const val=Math.round(ease*target);
      el.textContent=prefix+(val>=1000?(val/1000).toFixed(1)+"K":val)+suffix;
      if(prog<1) requestAnimationFrame(step);
    }}
    setTimeout(()=>{{ el.style.opacity=1; requestAnimationFrame(step); }},300);
  }}
  animCount("cnt-traders",10500,"","+",1800);
  animCount("cnt-payouts",6500,"$","",2000);
  setTimeout(()=>document.getElementById("cnt-payouts").textContent="$6.5M+",2400);
  setTimeout(()=>{{ document.getElementById("cnt-split").textContent="90%"; document.getElementById("cnt-split").style.opacity=1; }},600);
  setTimeout(()=>{{ document.getElementById("cnt-payout").textContent="24hr"; document.getElementById("cnt-payout").style.opacity=1; }},900);

  // ── Globe canvas (node sphere) ──
  const cv=document.getElementById("gn-canvas");
  cv.width=420; cv.height=420;
  const ctx=cv.getContext("2d");
  const cx=210,cy=210,R=165;
  let angle=0;
  const nodes=Array.from({{length:80}},()=>{{
    const theta=Math.random()*Math.PI*2;
    const phi=Math.acos(2*Math.random()-1);
    return {{theta,phi,
      color:Math.random()>.5?"#00D4FF":Math.random()>.5?"#00B87A":"#D4A843",
      size:Math.random()*2+.8}};
  }});
  const lines=Array.from({{length:25}},()=>({{i:Math.floor(Math.random()*nodes.length),j:Math.floor(Math.random()*nodes.length)}}));

  function project(theta,phi,rot){{
    const x=R*Math.sin(phi)*Math.cos(theta+rot);
    const y=R*Math.cos(phi);
    const z=R*Math.sin(phi)*Math.sin(theta+rot);
    const sc=(z+R*1.4)/(R*2.4);
    return {{sx:cx+x*sc*1.05,sy:cy-y*sc*1.05,z,sc}};
  }}

  function drawGlobe(){{
    ctx.clearRect(0,0,420,420);
    // outer glow
    const gr=ctx.createRadialGradient(cx,cy,R*.2,cx,cy,R*1.2);
    gr.addColorStop(0,"rgba(0,212,255,0.03)"); gr.addColorStop(1,"transparent");
    ctx.fillStyle=gr; ctx.beginPath(); ctx.arc(cx,cy,R*1.2,0,Math.PI*2); ctx.fill();
    // grid
    ctx.strokeStyle="rgba(0,212,255,0.055)"; ctx.lineWidth=0.5;
    for(let lat=-80;lat<=80;lat+=20){{
      const phi=(90-lat)*Math.PI/180;
      ctx.beginPath();
      for(let lon=0;lon<=360;lon+=4){{
        const theta=lon*Math.PI/180;
        const p=project(theta,phi,angle);
        lon===0?ctx.moveTo(p.sx,p.sy):ctx.lineTo(p.sx,p.sy);
      }} ctx.stroke();
    }}
    for(let lon=0;lon<360;lon+=30){{
      const theta=lon*Math.PI/180;
      ctx.beginPath();
      for(let lat=0;lat<=180;lat+=4){{
        const phi=lat*Math.PI/180;
        const p=project(theta,phi,angle);
        lat===0?ctx.moveTo(p.sx,p.sy):ctx.lineTo(p.sx,p.sy);
      }} ctx.stroke();
    }}
    // connections
    lines.forEach(({{i,j}})=>{{
      const a=project(nodes[i].theta,nodes[i].phi,angle);
      const b=project(nodes[j].theta,nodes[j].phi,angle);
      if(a.z>-R*.3&&b.z>-R*.3){{
        ctx.beginPath(); ctx.moveTo(a.sx,a.sy); ctx.lineTo(b.sx,b.sy);
        ctx.strokeStyle="rgba(0,212,255,0.1)"; ctx.lineWidth=0.6; ctx.stroke();
      }}
    }});
    // nodes
    nodes.forEach(n=>{{
      const p=project(n.theta,n.phi,angle);
      if(p.z<-R*.3) return;
      const al=(p.z+R)/(R*2);
      ctx.globalAlpha=al*.85;
      ctx.beginPath(); ctx.arc(p.sx,p.sy,n.size*p.sc,0,Math.PI*2);
      ctx.fillStyle=n.color; ctx.fill();
      if(al>.6){{
        ctx.beginPath(); ctx.arc(p.sx,p.sy,n.size*p.sc*3,0,Math.PI*2);
        ctx.fillStyle=n.color+"18"; ctx.fill();
      }}
      ctx.globalAlpha=1;
    }});
    ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2);
    ctx.strokeStyle="rgba(0,212,255,0.08)"; ctx.lineWidth=1; ctx.stroke();
    angle+=0.002;
    requestAnimationFrame(drawGlobe);
  }}
  drawGlobe();

}})();
</script>
""", height=450)



    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;">CHOOSE YOUR PROGRAM</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.markdown(
            '<div style="background:linear-gradient(135deg,rgba(212,168,67,.08),rgba(212,168,67,.02));border:1px solid rgba(212,168,67,.3);padding:2rem;position:relative;">'
            '<div style="position:absolute;top:.8rem;right:.8rem;background:var(--gold);color:#000;font-size:.52rem;font-weight:700;padding:2px 10px;letter-spacing:1.5px;">INSTANT</div>'
            '<div style="font-size:.58rem;color:var(--gold);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;">INSTANT FUNDED</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(212,168,67,.1);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Daily Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">3%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">6%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Challenge</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--green);">NONE</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Split</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--gold);">70-75%</div></div>'
            '</div>'
            '<div style="font-size:.65rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.4rem;color:var(--gold);letter-spacing:2px;">$299</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get Instant Funded", use_container_width=True, key="h_inst"):
            st.session_state["selected_phase"] = "instant"; goto("plans")

    with col2:
        st.markdown(
            '<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.25);padding:2rem;position:relative;">'
            '<div style="font-size:.58rem;color:var(--cyan);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;">ONE-STEP</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Target</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--green);">8%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">10%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Daily Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">5%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Split</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--cyan);">80%</div></div>'
            '</div>'
            '<div style="font-size:.65rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.4rem;color:var(--text);letter-spacing:2px;">$79</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get One-Step", use_container_width=True, key="h_1p"):
            st.session_state["selected_phase"] = "one"; goto("plans")

    with col3:
        st.markdown(
            '<div style="background:rgba(123,110,246,.05);border:1px solid rgba(123,110,246,.25);padding:2rem;position:relative;">'
            '<div style="position:absolute;top:.8rem;right:.8rem;background:var(--purple);color:#fff;font-size:.52rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;">BEST VALUE</div>'
            '<div style="font-size:.58rem;color:var(--purple);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;">TWO-STEP</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Phase 1</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--green);">8%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">10%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Daily Loss</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--red);">5%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Profit Split</div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.4rem;color:var(--purple);">90%</div></div>'
            '</div>'
            '<div style="font-size:.65rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.4rem;color:var(--text);letter-spacing:2px;">$49</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get Two-Step", use_container_width=True, key="h_2p"):
            st.session_state["selected_phase"] = "two"; goto("plans")

    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3rem 0 .5rem;">LIVE INSTRUMENTS</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>', unsafe_allow_html=True)
    render_market_heatmap()

    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;">HOW IT WORKS</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="steps-grid">'
        '<div class="step-card"><div class="step-num">01</div><div class="step-title">Choose a Plan</div><div class="step-desc">Instant Funded, One-Step, or Two-Step. Accounts from $5K to $100K.</div></div>'
        '<div class="step-card"><div class="step-num">02</div><div class="step-title">Pass the Evaluation</div><div class="step-desc">Hit the profit target while respecting strict drawdown rules.</div></div>'
        '<div class="step-card"><div class="step-num">03</div><div class="step-title">Get Funded</div><div class="step-desc">Complete verification and receive your funded account. 24-hour payouts.</div></div>'
        '<div class="step-card"><div class="step-num">04</div><div class="step-title">Scale Up</div><div class="step-desc">Keep up to 90% of profits. Scale to $2,000,000 with consistent performance.</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:2.5rem 0 .5rem;">FUNDED TRADERS</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="testi-grid">'
        '<div class="testi-card"><div class="testi-quote">Passed the $50K One-Step on Bitcoin in 4 days. The rules are clear and the platform is rock solid.</div><div class="testi-name">Rahul S.</div><div class="testi-meta">$50K Funded &nbsp;|&nbsp; +$4,000 payout &nbsp;|&nbsp; One-Step</div></div>'
        '<div class="testi-card"><div class="testi-quote">Two-Step gave me 90% profit split at an affordable entry. Already on my third funded account.</div><div class="testi-name">Priya M.</div><div class="testi-meta">$25K Funded &nbsp;|&nbsp; +$2,250 payout &nbsp;|&nbsp; Two-Step</div></div>'
        '<div class="testi-card"><div class="testi-quote">Instant Funded is worth every rupee. Got funded same day and started trading Ethereum immediately.</div><div class="testi-name">Kiran T.</div><div class="testi-meta">$25K Instant Funded &nbsp;|&nbsp; 3 accounts completed</div></div>'
        '</div>',
        unsafe_allow_html=True
    )



    # ── 3D SECTION 3: 3D Feature Cards with perspective tilt ──
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;letter-spacing:4px;color:var(--text);margin:3rem 0 .5rem;">PLATFORM FEATURES</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>', unsafe_allow_html=True)
    st.components.v1.html("""
<style>
  * { box-sizing:border-box; margin:0; padding:0; font-family:'Rajdhani',sans-serif; }
  body { background:transparent; }
  .feat-grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:2px;
    perspective:1000px;
  }
  .feat-card {
    background:#0d0d0d;
    border:1px solid #1e1e1e;
    padding:1.8rem 1.5rem;
    cursor:default;
    transition:transform .3s ease, box-shadow .3s ease, border-color .3s;
    transform-style:preserve-3d;
    position:relative;
    overflow:hidden;
  }
  .feat-card::before {
    content:'';
    position:absolute; top:0; left:0; right:0;
    height:2px;
    background:linear-gradient(90deg,var(--accent,#00D4FF),transparent);
    opacity:.6;
  }
  .feat-card::after {
    content:'';
    position:absolute;
    top:-60%; left:-60%;
    width:120%; height:120%;
    background:radial-gradient(ellipse at center, rgba(255,255,255,.04) 0%, transparent 70%);
    opacity:0;
    transition:opacity .3s;
    pointer-events:none;
  }
  .feat-card:hover::after { opacity:1; }
  .feat-card:hover {
    border-color:var(--accent,#00D4FF);
    box-shadow:0 0 30px rgba(0,212,255,.08), 0 20px 40px rgba(0,0,0,.4);
  }
  .feat-icon {
    font-size:2rem;
    margin-bottom:1rem;
    display:block;
    filter:drop-shadow(0 0 8px var(--accent,#00D4FF));
  }
  .feat-title {
    font-family:'Bebas Neue',sans-serif;
    font-size:1rem;
    letter-spacing:2.5px;
    color:#D8D8D8;
    margin-bottom:.6rem;
  }
  .feat-desc {
    font-size:.8rem;
    color:#505050;
    line-height:1.7;
    font-weight:400;
  }
  .feat-tag {
    display:inline-block;
    margin-top:.9rem;
    font-size:.52rem;
    letter-spacing:2px;
    padding:3px 10px;
    border:1px solid;
    font-weight:700;
    text-transform:uppercase;
    color:var(--accent,#00D4FF);
    border-color:var(--accent,#00D4FF);
    background:rgba(0,212,255,.06);
  }
  /* 3D canvas orb per card */
  .card-orb { position:absolute; bottom:-20px; right:-20px; opacity:.25; pointer-events:none; }
</style>
<div class="feat-grid" id="featGrid">
  <div class="feat-card" style="--accent:#00D4FF;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">⚡</span>
    <div class="feat-title">Real-Time Execution</div>
    <div class="feat-desc">Instant order fills on Forex, Bitcoin, Crude Oil and more. Sub-second latency with live spread simulation.</div>
    <span class="feat-tag">Live Data</span>
  </div>
  <div class="feat-card" style="--accent:#00B87A;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">📊</span>
    <div class="feat-title">Advanced Analytics</div>
    <div class="feat-desc">Deep trade journal with win rate, R-multiple, drawdown heatmaps and performance breakdown by session.</div>
    <span class="feat-tag">Pro Tools</span>
  </div>
  <div class="feat-card" style="--accent:#D4A843;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">🏆</span>
    <div class="feat-title">Instant Payouts</div>
    <div class="feat-desc">Pass your evaluation and receive payouts within 24 hours. No delays, no hidden conditions — just results.</div>
    <span class="feat-tag">24hr Payout</span>
  </div>
  <div class="feat-card" style="--accent:#7B6EF6;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">🛡️</span>
    <div class="feat-title">Risk Management Suite</div>
    <div class="feat-desc">Built-in risk calculator, position sizer, daily loss tracker and automatic breach alerts protect your account.</div>
    <span class="feat-tag">Smart Risk</span>
  </div>
  <div class="feat-card" style="--accent:#00D4FF;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">🤖</span>
    <div class="feat-title">AI Trading Coach</div>
    <div class="feat-desc">Ask our AI coach anything about strategy, market structure, or your own trade history. Available 24/7.</div>
    <span class="feat-tag">AI Powered</span>
  </div>
  <div class="feat-card" style="--accent:#00B87A;">
    <canvas class="card-orb" width="100" height="100"></canvas>
    <span class="feat-icon">🌍</span>
    <div class="feat-title">Global Leaderboard</div>
    <div class="feat-desc">Compete with 3,500+ traders worldwide. Real-time rankings updated every trading session.</div>
    <span class="feat-tag">Competitive</span>
  </div>
</div>
<script>
// 3D tilt on hover
document.querySelectorAll('.feat-card').forEach(card=>{
  card.addEventListener('mousemove',e=>{
    const rect=card.getBoundingClientRect();
    const x=(e.clientX-rect.left)/rect.width-0.5;
    const y=(e.clientY-rect.top)/rect.height-0.5;
    card.style.transform=`perspective(600px) rotateY(${x*14}deg) rotateX(${-y*14}deg) translateZ(8px)`;
  });
  card.addEventListener('mouseleave',()=>{
    card.style.transform='perspective(600px) rotateY(0deg) rotateX(0deg) translateZ(0px)';
  });
});

// Draw animated orb on each card canvas
document.querySelectorAll('.card-orb').forEach((cv,idx)=>{
  const ctx=cv.getContext('2d');
  const colors=['#00D4FF','#00B87A','#D4A843','#7B6EF6','#00D4FF','#00B87A'];
  const col=colors[idx%colors.length];
  let t=idx*0.5;
  function drawOrb(){
    ctx.clearRect(0,0,100,100);
    const x=50+Math.cos(t)*8, y=50+Math.sin(t)*8;
    const g=ctx.createRadialGradient(x,y,2,x,y,45);
    g.addColorStop(0,col+'cc'); g.addColorStop(1,'transparent');
    ctx.beginPath(); ctx.arc(x,y,45,0,Math.PI*2);
    ctx.fillStyle=g; ctx.fill();
    t+=0.02;
    requestAnimationFrame(drawOrb);
  }
  drawOrb();
});
</script>
""", height=460)



    # ── CHALLENGE CALCULATOR ─────────────────────────────────
    st.markdown(
        '<div style="font-family:Bebas Neue,sans-serif;font-size:1.2rem;letter-spacing:4px;'
        'color:var(--text);margin:3.5rem 0 .5rem;">PROFIT CHALLENGE CALCULATOR</div>'
        '<div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;'
        'opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>',
        unsafe_allow_html=True
    )
    cc1, cc2, cc3 = st.columns(3, gap="small")
    with cc1:
        calc_size = st.selectbox("Account Size", [5000,10000,25000,50000,100000],
                                  format_func=lambda x: f"${x:,}", key="calc_sz")
        calc_plan = st.selectbox("Plan",
                                  ["Two-Step (90%)", "One-Step (80%)", "Instant (75%)"],
                                  key="calc_plan")
    with cc2:
        calc_pct  = st.slider("Profit Target %", 1.0, 20.0, 8.0, 0.5, key="calc_pct")
        calc_days = st.slider("Trading Days", 1, 30, 10, key="calc_days")
    with cc3:
        split_map  = {"Two-Step (90%)": 0.90, "One-Step (80%)": 0.80, "Instant (75%)": 0.75}
        fee_map    = {"Two-Step (90%)": 49,   "One-Step (80%)": 79,   "Instant (75%)": 299}
        split      = split_map[calc_plan]
        gross_pnl  = calc_size * (calc_pct / 100)
        net_payout = gross_pnl * split
        daily_avg  = gross_pnl / max(calc_days, 1)
        fee        = fee_map[calc_plan]
        roi_fee    = (net_payout / fee) * 100
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid rgba(0,212,255,.15);'
            f'border-left:2px solid var(--cyan);padding:1.5rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);letter-spacing:2.5px;'
            f'text-transform:uppercase;margin-bottom:1rem;">Estimated Returns</div>'
            f'<div style="margin-bottom:.8rem;">'
            f'<div style="font-size:.55rem;color:var(--dim);">Gross Profit</div>'
            f'<div style="font-size:1.8rem;font-family:Bebas Neue,sans-serif;'
            f'color:var(--green);letter-spacing:2px;">${gross_pnl:,.0f}</div></div>'
            f'<div style="margin-bottom:.8rem;">'
            f'<div style="font-size:.55rem;color:var(--dim);">Your Payout ({int(split*100)}% split)</div>'
            f'<div style="font-size:1.8rem;font-family:Bebas Neue,sans-serif;'
            f'color:var(--cyan);letter-spacing:2px;">${net_payout:,.0f}</div></div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;'
            f'background:var(--border);margin-top:1rem;">'
            f'<div style="background:var(--s2);padding:.7rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);">Daily Avg</div>'
            f'<div style="font-size:1.2rem;font-family:Bebas Neue,sans-serif;'
            f'color:var(--gold);">${daily_avg:,.0f}</div></div>'
            f'<div style="background:var(--s2);padding:.7rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);">ROI on Fee</div>'
            f'<div style="font-size:1.2rem;font-family:Bebas Neue,sans-serif;'
            f'color:var(--green);">{roi_fee:.0f}%</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    # ── FAQ ──────────────────────────────────────────────────
    st.markdown(
        '<div style="font-family:Bebas Neue,sans-serif;font-size:1.2rem;letter-spacing:4px;'
        'color:var(--text);margin:3.5rem 0 .5rem;">FREQUENTLY ASKED QUESTIONS</div>'
        '<div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;'
        'opacity:.5;box-shadow:0 0 8px var(--cyan);"></div>',
        unsafe_allow_html=True
    )
    faqs = [
        ("How do payouts work?",
         "Once you pass your evaluation, submit a payout request. We process within 24 hours via bank transfer or crypto."),
        ("Can I trade news events?",
         "Yes. We allow trading during NFP, FOMC, CPI and all major news events. No trading restrictions."),
        ("What happens if I breach a rule?",
         "Your account is flagged immediately. You receive a breach email and can restart a new challenge anytime."),
        ("Is there a time limit to pass?",
         "No time limit. Trade at your own pace — just respect the daily and total loss rules."),
        ("Can I hold trades overnight?",
         "Yes, overnight and weekend holding is permitted on all plans."),
        ("What instruments can I trade?",
         "Forex majors/minors, Bitcoin, XAGUSD, WTI Crude Oil, Brent Crude, and Natural Gas."),
    ]
    faq_c = st.columns(2, gap="small")
    for idx_f, (fq, fa) in enumerate(faqs):
        with faq_c[idx_f % 2]:
            st.markdown(
                f'<div style="background:var(--s1);border:1px solid var(--border);'
                f'border-left:2px solid rgba(0,212,255,.3);padding:1.2rem 1.4rem;margin-bottom:2px;">'
                f'<div style="font-size:.8rem;font-weight:700;color:var(--text);margin-bottom:.5rem;">{fq}</div>'
                f'<div style="font-size:.75rem;color:var(--dim);line-height:1.7;">{fa}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    footer()

# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "auth":
    nav()
    st.markdown("<br>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.2,1])
    with col:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:4px;color:var(--text);margin-bottom:.3rem;">ACCESS AKFUNDED</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;"></div>', unsafe_allow_html=True)
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
    nav()
    name = st.session_state.user.get("name","Trader")
    sec(f"SELECT CHALLENGE", f"Testing phase — challenges activate instantly — {name}")

    st.markdown(
        '<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);border-left:2px solid var(--cyan);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.78rem;color:var(--dim);">'
        '<b style="color:var(--cyan);">TESTING PHASE</b> — All challenges activate instantly. No payment required. Trade Forex, Bitcoin, XAGUSD, Crude Oil &amp; Natural Gas.'
        '</div>',
        unsafe_allow_html=True
    )

    tab_inst, tab1, tab2 = st.tabs(["  Instant Funded  ","  One-Step Challenge  ","  Two-Step Challenge  "])

    def activate_challenge(plan, uid):
        try:
            ch = supabase.table("challenges").insert({
                "user_id":uid,"plan":plan["slug"],"capital":plan["capital"],
                "status":"active","started_at":datetime.utcnow().isoformat()
            }).execute()
            ch_id = ch.data[0]["id"]
            supabase.table("accounts").insert({
                "user_id":uid,"challenge_id":ch_id,"balance":plan["capital"],
                "initial_capital":plan["capital"],"daily_loss":0,"total_loss":0,"days_traded":0
            }).execute()
            return True, ch_id
        except Exception as e:
            return False, str(e)

    def render_plan_card(plan, phase_type):
        r   = RULES.get(plan["slug"], {})
        hot = plan["capital"] == 50000
        if phase_type == "instant":
            border,accent,pop = "rgba(212,168,67,.35)","var(--gold)",'<div style="position:absolute;top:.6rem;right:.6rem;background:var(--gold);color:#000;font-size:.5rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;">INSTANT</div>'
        elif phase_type == "1step":
            border  = "rgba(0,212,255,.4)" if hot else "rgba(0,212,255,.2)"
            accent  = "var(--cyan)"
            pop     = '<div style="position:absolute;top:.6rem;right:.6rem;background:rgba(0,212,255,.2);color:var(--cyan);border:1px solid rgba(0,212,255,.3);font-size:.5rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;">POPULAR</div>' if hot else ""
        else:
            border  = "rgba(123,110,246,.4)" if hot else "rgba(123,110,246,.2)"
            accent  = "var(--purple)"
            pop     = '<div style="position:absolute;top:.6rem;right:.6rem;background:rgba(123,110,246,.2);color:var(--purple);border:1px solid rgba(123,110,246,.3);font-size:.5rem;font-weight:700;padding:2px 8px;letter-spacing:1.5px;">BEST VALUE</div>' if hot else ""

        if phase_type == "instant":
            rules_html = (
                f'<li><span>Daily Loss Limit</span><b style="color:var(--red);">-{r.get("daily_loss",3)}%</b></li>'
                f'<li><span>Max Total Loss</span><b style="color:var(--red);">-{r.get("total_loss",6)}%</b></li>'
                f'<li><span>Evaluation</span><b style="color:var(--green);">None Required</b></li>'
                f'<li><span>Profit Split</span><b style="color:{accent};">{plan["split"]}%</b></li>'
                f'<li><span>Markets</span><b>Crypto</b></li>'
            )
        elif phase_type == "1step":
            rules_html = (
                f'<li><span>Profit Target</span><b style="color:var(--green);">+{r.get("target",8)}%</b></li>'
                f'<li><span>Max Daily Loss</span><b style="color:var(--red);">-{r.get("daily_loss",5)}%</b></li>'
                f'<li><span>Max Total Loss</span><b style="color:var(--red);">-{r.get("total_loss",10)}%</b></li>'
                f'<li><span>Min Trading Days</span><b>{r.get("min_days",5)} days</b></li>'
                f'<li><span>Profit Split</span><b style="color:{accent};">{plan["split"]}%</b></li>'
            )
        else:
            rules_html = (
                f'<li><span>Phase 1 Target</span><b style="color:var(--green);">+8%</b></li>'
                f'<li><span>Phase 2 Target</span><b style="color:var(--green);">+5%</b></li>'
                f'<li><span>Max Daily Loss</span><b style="color:var(--red);">-{r.get("daily_loss",5)}%</b></li>'
                f'<li><span>Max Total Loss</span><b style="color:var(--red);">-{r.get("total_loss",10)}%</b></li>'
                f'<li><span>Profit Split</span><b style="color:{accent};">{plan["split"]}%</b></li>'
            )

        st.markdown(
            f'<div style="background:var(--s1);border:1px solid {border};padding:1.5rem;position:relative;overflow:hidden;">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{accent},transparent);opacity:.4;"></div>'
            f'{pop}'
            f'<div style="font-size:.52rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.3rem;">Account Size</div>'
            f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.6rem;color:{accent};letter-spacing:2px;line-height:1;margin-bottom:1.2rem;">{plan["name"]}</div>'
            f'<ul class="plan-rules">{rules_html}</ul>'
            f'<div style="border-top:1px solid var(--border);padding-top:.8rem;">'
            f'<div style="font-size:.62rem;color:var(--dim);text-decoration:line-through;letter-spacing:1px;">${plan["price"]} value</div>'
            f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.6rem;color:var(--green);letter-spacing:2px;">FREE <span style="font-size:.8rem;color:var(--dim);font-family:\'Rajdhani\',sans-serif;">testing</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        if st.button(f"Activate {plan['name']}", key=f"buy_{plan['slug']}", use_container_width=True):
            uid = st.session_state.user["id"]
            ok, ch_id = activate_challenge(plan, uid)
            if ok:
                push_notification(uid,"⚡","Challenge Activated",f"{plan['name']} {phase_type.upper()} challenge is now active.")
                st.success(f"✅ {plan['name']} {phase_type.upper()} challenge activated!")
                time.sleep(1); goto("dashboard")
            else:
                st.error(f"Activation failed: {ch_id}")

    with tab_inst:
        st.markdown('<div style="background:linear-gradient(135deg,rgba(212,168,67,.06),rgba(212,168,67,.02));border:1px solid rgba(212,168,67,.2);border-left:2px solid var(--gold);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.78rem;color:var(--dim);"><b style="color:var(--gold);">INSTANT FUNDED</b> — No evaluation required. Strictest rules: <b style="color:var(--red);">3% daily loss</b> &middot; <b style="color:var(--red);">6% max loss</b> &middot; <b style="color:var(--gold);">70-75% profit split</b></div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_INSTANT):
            with cols[i]: render_plan_card(plan, "instant")

    with tab1:
        st.markdown('<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);border-left:2px solid var(--cyan);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.78rem;color:var(--dim);"><b style="color:var(--cyan);">ONE-STEP</b> — Single evaluation phase. <b style="color:var(--red);">5% daily loss</b> &middot; <b style="color:var(--red);">10% max loss</b> &middot; <b style="color:var(--cyan);">80% profit split</b></div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_1P):
            with cols[i]: render_plan_card(plan, "1step")

    with tab2:
        st.markdown('<div style="background:rgba(123,110,246,.05);border:1px solid rgba(123,110,246,.15);border-left:2px solid var(--purple);padding:.8rem 1.2rem;margin-bottom:1.5rem;font-size:.78rem;color:var(--dim);"><b style="color:var(--purple);">TWO-STEP</b> — Two evaluation phases, lowest entry price. <b style="color:var(--red);">5% daily loss</b> &middot; <b style="color:var(--red);">10% max loss</b> &middot; <b style="color:var(--purple);">90% profit split</b></div>', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_2P):
            with cols[i]: render_plan_card(plan, "2step")

    st.markdown('<br><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:3px;color:var(--dim);margin-bottom:1rem;">PROGRAM COMPARISON</div>', unsafe_allow_html=True)
    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;padding:.8rem 1.2rem;background:var(--s2);font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;font-weight:600;border-bottom:1px solid var(--border);"><span>Feature</span><span style="text-align:center;color:var(--gold);">Instant</span><span style="text-align:center;color:var(--cyan);">One-Step</span><span style="text-align:center;color:var(--purple);">Two-Step</span></div>', unsafe_allow_html=True)
    for feat,v0,v1,v2 in [
        ("Account Sizes","$5K–$100K","$5K–$100K","$5K–$100K"),
        ("Evaluation Required","None","1 Phase","2 Phases"),
        ("Daily Loss Limit","3%","5%","5%"),
        ("Max Total Loss","6%","10%","10%"),
        ("Profit Target","N/A","8%","8% + 5%"),
        ("Profit Split","70–75%","80%","90%"),
        ("Min Trading Days","None","5 days","4 days"),
        ("Time Limit","None","None","None"),
        ("Markets","Crypto","Crypto","Crypto"),
    ]:
        st.markdown(f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;padding:.65rem 1.2rem;border-bottom:1px solid var(--border);font-size:.78rem;align-items:center;"><span style="color:var(--dim);">{feat}</span><span style="text-align:center;color:var(--gold);">{v0}</span><span style="text-align:center;color:var(--cyan);">{v1}</span><span style="text-align:center;color:var(--purple);">{v2}</span></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.user: goto("auth")
    nav()
    render_live_ticker()
    uid   = st.session_state.user["id"]
    name  = st.session_state.user.get("name","Trader")
    email = st.session_state.user.get("email","")

    all_challenges = db_get_all_challenges(uid)
    
    if not all_challenges:
        st.markdown(
            f'<div style="text-align:center;padding:6rem 2rem;">'
            f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.5rem;letter-spacing:5px;color:var(--text);">Welcome, {name.upper()}</div>'
            f'<div style="font-size:.85rem;color:var(--dim);margin:.5rem 0 2rem;font-weight:300;letter-spacing:.5px;">No challenges found. Start your first challenge to begin trading.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("Start Challenge", use_container_width=True): goto("plans")
        footer(); st.stop()
        
    st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-weight:600;">Select Account</div>', unsafe_allow_html=True)
    
    options = []
    for ch in all_challenges:
        status = ch.get("status", "unknown").upper()
        emoji = "🟢" if status == "ACTIVE" else "🏆" if status == "PASSED" else "❌" if status == "FAILED" else "⏳"
        options.append(f"{emoji} {ch['plan'].upper()} — {status} (ID: {ch['id']})")
        
    c1, c2 = st.columns([3, 1])
    with c1:
        sel_idx = st.selectbox("Select Account", range(len(options)), format_func=lambda i: options[i], label_visibility="collapsed")
    with c2:
        if st.button("+ New Challenge", use_container_width=True): goto("plans")
        
    challenge = all_challenges[sel_idx]
    account = db_get_account(challenge["id"])
    
    if not account:
        st.error("Account details not found.")
        st.stop()
        
    is_active = challenge.get("status") == "active"


    balance = float(account.get("balance",0))
    initial = float(account.get("initial_capital",1))
    pnl     = balance - initial
    pnl_pct = (pnl/initial)*100
    days    = int(account.get("days_traded",0))
    r       = RULES.get(challenge["plan"], {})
    all_trades = db_get_trades(uid, challenge["id"], limit=500)
    wr,ap,bt,wt,tt = compute_stats(all_trades)
    win_streak, loss_streak = compute_streaks(all_trades)

    breached, breach_reason = check_and_breach(uid, challenge, account, email, name)
    if breached:
        st.markdown(
            f'<div class="breach-alert">'
            f'<div style="font-size:.62rem;color:var(--red);letter-spacing:3px;text-transform:uppercase;margin-bottom:.5rem;font-weight:700;">ACCOUNT BREACHED</div>'
            f'<div style="font-size:.85rem;color:#D8D8D8;">{breach_reason}</div>'
            f'<div style="font-size:.72rem;color:var(--dim);margin-top:.5rem;">A notification email has been sent. You can start a new challenge anytime.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("Start New Challenge", use_container_width=True): goto("plans")
        footer(); st.stop()

    pc = "g" if pnl>=0 else "r"
    ps = "+" if pnl>=0 else ""
    tc = "g" if pnl_pct>=r.get("target",8) else "o" if pnl_pct > 0 else "r"
    phase_type = r.get("phase","1step")
    if phase_type == "instant":   phase_badge = "INSTANT FUNDED"
    elif phase_type == "1step":   phase_badge = "ONE-STEP"
    else:                         phase_badge = "TWO-STEP"
    
    ch_status = challenge.get("status", "unknown").upper()
    status_col = "var(--green)" if ch_status == "ACTIVE" else "var(--gold)" if ch_status == "PASSED" else "var(--red)"
    status_emoji = "&#x25CF;" if ch_status == "ACTIVE" else "🏆" if ch_status == "PASSED" else "❌"

    st.markdown(
        f'<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1.5rem;">'
        f'<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;letter-spacing:4px;color:var(--text);line-height:1;">Trading Dashboard</div>'
        f'<div style="font-size:.72rem;color:var(--dim);margin-top:.3rem;letter-spacing:.5px;">{name} &nbsp;|&nbsp; {challenge["plan"].upper()} &nbsp;|&nbsp; Day {days}</div>'
        f'<div style="width:30px;height:1px;background:var(--cyan);margin-top:.6rem;opacity:.5;"></div></div>'
        f'<div style="display:flex;gap:.5rem;align-items:center;">'
        f'<div style="border:1px solid rgba(0,212,255,.2);padding:4px 14px;font-size:.58rem;color:var(--cyan);letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">{phase_badge}</div>'
        f'<div style="border:1px solid {status_col};padding:4px 14px;font-size:.58rem;color:{status_col};letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">{status_emoji} {ch_status}</div>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="metric-row" style="margin-bottom:1px;">'
        f'<div class="m-card"><div class="m-label">Account Balance</div><div class="m-val c">${balance:,.2f}</div><div class="m-sub">Base: ${initial:,.0f}</div></div>'
        f'<div class="m-card"><div class="m-label">Total P&L</div><div class="m-val {pc}">{ps}${pnl:,.2f}</div><div class="m-sub">{ps}{pnl_pct:.2f}% return</div></div>'
        f'<div class="m-card"><div class="m-label">Profit Target</div><div class="m-val {tc}">{("+"+str(r.get("target",0))+"%") if r.get("target",0)>0 else "N/A"}</div><div class="m-sub">{ps}{pnl_pct:.2f}% achieved</div></div>'
        f'<div class="m-card"><div class="m-label">Days Traded</div><div class="m-val w">{days}{(" / "+str(r.get("min_days",0))) if r.get("min_days",0)>0 else ""}</div><div class="m-sub">{"Min "+str(r.get("min_days",0))+" required" if r.get("min_days",0)>0 else "No min days"}</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""
    st.markdown(
        f'<div class="stats-row">'
        f'<div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>'
        f'<div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>'
        f'<div class="stat-box"><div class="sv {apc}">{aps}${ap:,.2f}</div><div class="sl">Avg P&L</div></div>'
        f'<div class="stat-box"><div class="sv g">{win_streak}</div><div class="sl">Win Streak</div></div>'
        f'<div class="stat-box"><div class="sv r">{loss_streak}</div><div class="sl">Loss Streak</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    target = r.get("target",8)
    profit_prog = min((pnl_pct/target)*100,100) if target > 0 else 100
    dl_limit = initial*r.get("daily_loss",5)/100; tl_limit = initial*r.get("total_loss",10)/100
    dl_used  = min(abs(account.get("daily_loss",0))/dl_limit*100,100) if dl_limit else 0
    tl_used  = min(abs(account.get("total_loss",0))/tl_limit*100,100) if tl_limit else 0
    dl_cls = "bad" if dl_used>75 else "ok"; tl_cls = "bad" if tl_used>75 else "ok"

    target_row = ""
    if target > 0:
        target_row = (
            f'<div class="r-row"><span class="r-name">Profit Target +{target}%</span>'
            f'<span class="r-val ok">{pnl_pct:.2f}% / +{target}% {"— Target Met" if profit_prog>=100 else ""}</span></div>'
            + pbar(profit_prog, 'var(--green)' if profit_prog>=100 else 'var(--cyan)')
        )

    st.markdown(
        f'<div class="rules-box" style="margin-top:1px;">'
        f'<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1.2rem;font-weight:600;">Rules Monitor</div>'
        f'{target_row}'
        f'<div class="r-row"><span class="r-name">Max Daily Loss -{r.get("daily_loss",5)}%</span><span class="r-val {dl_cls}">{dl_used:.1f}% of limit used {"⚠" if dl_used>75 else ""}</span></div>'
        f'{pbar(dl_used,"var(--red)" if dl_used>75 else "var(--gold)")}'
        f'<div class="r-row"><span class="r-name">Max Total Loss -{r.get("total_loss",10)}%</span><span class="r-val {tl_cls}">{tl_used:.1f}% of limit used {"⚠" if tl_used>75 else ""}</span></div>'
        f'{pbar(tl_used,"var(--red)" if tl_used>75 else "var(--gold)")}'
        f'</div>',
        unsafe_allow_html=True
    )

    def reset_trade_inputs():
        for k in ["tentry", "texit", "tsl"]:
            if k in st.session_state:
                del st.session_state[k]

    col_chart, col_trade = st.columns([2,1], gap="medium")
    with col_chart:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Live Chart — TradingView</div>', unsafe_allow_html=True)
        mkt      = st.selectbox("Market", list(SYMBOLS.keys()), key="mkt", on_change=reset_trade_inputs)
        sym_list = SYMBOLS[mkt]
        sym_pick = st.selectbox("Symbol", sym_list, key="csym", on_change=reset_trade_inputs)
        tv_sym   = TV_SYMBOL_MAP.get(sym_pick, f"BINANCE:{sym_pick}")
        st.components.v1.html(
            f'<div style="height:400px;width:100%;"><div id="tvc" style="height:100%;width:100%;"></div>'
            f'<script src="https://s3.tradingview.com/tv.js"></script>'
            f'<script>new TradingView.widget({{width:"100%",height:400,symbol:"{tv_sym}",interval:"15",'
            f'timezone:"UTC",theme:"dark",style:"1",locale:"en",toolbar_bg:"#0d0d0d",'
            f'enable_publishing:false,container_id:"tvc",backgroundColor:"#050505",'
            f'gridColor:"rgba(0,212,255,0.05)"}});</script></div>',
            height=410
        )

    with col_trade:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Execute Trade</div>', unsafe_allow_html=True)
        t_sym   = sym_pick
        live_px = get_live_price(t_sym)
        t_dir   = st.selectbox("Direction", ["BUY","SELL"], key="ttype")
        decimal = 5 if get_all_market_data().get(t_sym,{}).get("price",1) < 10 else 2
        t_entry = st.number_input("Entry Price", min_value=0.00001, value=float(live_px), format=f"%.{decimal}f", key=f"tentry_{t_sym}")
        t_qty   = st.number_input("Lot Size / Units", min_value=0.01, value=0.10, step=0.01, format="%.2f", key=f"tqty_{t_sym}")
        t_exit  = st.number_input("Exit Price", min_value=0.00001, value=float(round(live_px*1.015,decimal)), format=f"%.{decimal}f", key=f"texit_{t_sym}")
        t_sl    = st.number_input("Stop Loss", min_value=0.00001, value=float(round(live_px*0.985,decimal)), format=f"%.{decimal}f", key=f"tsl_{t_sym}")

        lot_mult   = 100000 if get_all_market_data().get(t_sym,{}).get("price",1) < 100 else 1
        est        = (t_exit-t_entry)*t_qty*lot_mult if t_dir=="BUY" else (t_entry-t_exit)*t_qty*lot_mult
        risk_trade = abs(t_entry-t_sl)*t_qty*lot_mult
        ec         = "var(--green)" if est>=0 else "var(--red)"
        es         = "+" if est>=0 else ""
        roi        = (est/initial)*100 if initial>0 else 0
        rr         = abs(est)/risk_trade if risk_trade>0 else 0

        st.markdown(
            f'<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid {ec};padding:1rem;margin:.8rem 0;">'
            f'<div style="font-size:.55rem;color:var(--dim);letter-spacing:2.5px;margin-bottom:4px;text-transform:uppercase;">Estimated P&L</div>'
            f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.2rem;color:{ec};letter-spacing:2px;line-height:1;">{es}${est:,.2f}</div>'
            f'<div style="font-size:.68rem;color:{ec};margin-top:4px;font-family:\'JetBrains Mono\',monospace;">{es}{roi:.3f}% acct &nbsp;|&nbsp; R:R 1:{rr:.1f}</div>'
            f'<div style="font-size:.65rem;color:var(--red);margin-top:4px;font-family:\'JetBrains Mono\',monospace;">Risk: ${risk_trade:,.2f}</div>'
            f'</div>'
            f'<div style="background:var(--s2);border:1px solid var(--border);padding:.6rem 1rem;margin-bottom:.8rem;display:flex;justify-content:space-between;align-items:center;">'
            f'<div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">Live Price</div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1rem;color:var(--cyan);">{live_px:.{decimal}f}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if not is_active:
            st.button("Execute Trade (Account Inactive)", use_container_width=True, disabled=True)
        elif st.button("Execute Trade", use_container_width=True, key="exec"):
            # Exact moment live price
            real_entry_price = get_live_price(t_sym)
            
            # Recalculate P&L based on exact moment price
            actual_est = (t_exit - real_entry_price) * t_qty * lot_mult if t_dir == "BUY" else (real_entry_price - t_exit) * t_qty * lot_mult
            
            ch_id   = challenge["id"]
            new_bal = balance + actual_est
            new_tl  = min(0.0, new_bal-initial)
            new_days = days+1
            new_daily = float(account.get("daily_loss",0)) + (actual_est if actual_est < 0 else 0)
            daily_loss_pct = abs(new_daily)/initial*100 if new_daily < 0 else 0
            total_loss_pct = abs(new_tl)/initial*100 if new_tl < 0 else 0
            try:
                supabase.table("trades").insert({
                    "user_id":uid,"challenge_id":ch_id,"symbol":t_sym,"type":t_dir,
                    "entry_price":real_entry_price,"exit_price":t_exit,"quantity":t_qty,
                    "pnl":actual_est,"closed_at":datetime.utcnow().isoformat()
                }).execute()
                supabase.table("accounts").update({
                    "balance":new_bal,"total_loss":new_tl,"daily_loss":new_daily,
                    "days_traded":new_days,"updated_at":datetime.utcnow().isoformat()
                }).eq("challenge_id",ch_id).execute()
                new_pct = ((new_bal-initial)/initial)*100
                if total_loss_pct >= r.get("total_loss",10):
                    supabase.table("challenges").update({"status":"failed"}).eq("id",ch_id).execute()
                    reason = f"Max total loss of {r.get('total_loss',10)}% breached."
                    send_breach_email(email,name,reason,challenge["plan"],int(initial))
                    push_notification(uid,"⚠","Account Breached","Max total loss reached.")
                    st.error("Account breached — max total loss reached.")
                elif daily_loss_pct >= r.get("daily_loss",5):
                    supabase.table("challenges").update({"status":"failed"}).eq("id",ch_id).execute()
                    reason = f"Max daily loss of {r.get('daily_loss',5)}% breached."
                    send_breach_email(email,name,reason,challenge["plan"],int(initial))
                    push_notification(uid,"⚠","Account Breached","Daily loss limit breached.")
                    st.error("Account breached — daily loss limit hit.")
                elif target > 0 and new_pct >= target and new_days >= r.get("min_days",0):
                    supabase.table("challenges").update({"status":"passed"}).eq("id",ch_id).execute()
                    push_notification(uid,"🏆","Challenge Passed!",f"Profit target of +{target}% achieved.")
                    send_passed_email(email, name, target, challenge["plan"], int(initial))
                    st.components.v1.html("""
                    <script>
                    const w = window.parent; const d = w.document;
                    if(!d.getElementById('g-confetti-style')){
                        const s = d.createElement('style'); s.id = 'g-confetti-style';
                        s.innerHTML = `@keyframes gFall{0%{transform:translateY(-10vh) rotateZ(0deg) rotateX(0deg);opacity:1;}100%{transform:translateY(110vh) rotateZ(720deg) rotateX(360deg);opacity:0;}} .g-confetti{position:fixed;z-index:999999;width:12px;height:24px;background:linear-gradient(135deg,#D4AF37,#FFDF00);box-shadow:0 0 10px rgba(212,175,55,0.6);pointer-events:none;} @keyframes passAnim{0%{opacity:0;transform:translate(-50%,-50%) scale(0.5);} 15%{opacity:1;transform:translate(-50%,-50%) scale(1.1);} 25%{transform:translate(-50%,-50%) scale(1);} 80%{opacity:1;transform:translate(-50%,-50%) scale(1);} 100%{opacity:0;transform:translate(-50%,-50%) scale(1.3);}}`;
                        d.head.appendChild(s);
                    }
                    for(let i=0; i<150; i++) {
                        const c = d.createElement('div'); c.className = 'g-confetti';
                        c.style.left = Math.random() * 100 + 'vw';
                        c.style.animation = 'gFall ' + (Math.random() * 2 + 2) + 's linear forwards';
                        c.style.animationDelay = Math.random() * 1 + 's';
                        d.body.appendChild(c); setTimeout(()=>c.remove(), 4000);
                    }
                    const text = d.createElement('div');
                    text.innerHTML = '<h1 style="color:#D4AF37;text-shadow:0 0 40px #D4AF37, 0 0 80px #D4AF37;font-size:clamp(4rem,10vw,8rem);font-family:Orbitron,sans-serif;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:999999;animation:passAnim 3.5s forwards;text-align:center;line-height:1;margin:0;">CHALLENGE<br>PASSED!</h1>';
                    d.body.appendChild(text); setTimeout(()=>text.remove(), 4000);
                    </script>
                    """, height=0, width=0)
                    st.success("Challenge passed! Certificate available.")
                else:
                    push_notification(uid,"⚡","Trade Executed",f"{t_dir} {t_sym} — P&L: {es}${actual_est:,.2f}")
                    if actual_est>=0: st.success(f"Trade executed. P&L: {es}${actual_est:,.2f}")
                    else: st.warning(f"Trade executed. P&L: ${actual_est:,.2f}")
            except Exception as e:
                st.error(f"Trade execution error: {e}")
            time.sleep(1); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Recent Trades</div>', unsafe_allow_html=True)
    trades = db_get_trades(uid, challenge["id"], limit=20)
    if trades:
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div class="t-header"><span>Symbol</span><span>Type</span><span>Entry</span><span>Exit</span><span>Lots</span><span>P&L</span></div>', unsafe_allow_html=True)
        for t in trades:
            p=t.get("pnl",0); pc3="var(--green)" if p>=0 else "var(--red)"; ps3="+" if p>=0 else ""
            tag='<span class="tag-b">BUY</span>' if t.get("type")=="BUY" else '<span class="tag-s">SELL</span>'
            dt=t.get("closed_at","")[:10]; sym=t.get("symbol","")
            dec = 5 if get_all_market_data().get(sym,{}).get("price",1) < 10 else 2
            st.markdown(
                f'<div class="t-row">'
                f'<span style="font-weight:700;">{sym} <span style="font-size:.62rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">{dt}</span></span>'
                f'{tag}'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;">{t.get("entry_price",0):.{dec}f}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:.72rem;">{t.get("exit_price",0):.{dec}f}</span>'
                f'<span style="font-family:\'JetBrains Mono\',monospace;">{t.get("quantity",0):.2f}</span>'
                f'<span style="color:{pc3};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps3}${p:,.2f}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:2.5rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;letter-spacing:.5px;">No trades yet. Execute your first trade above.</div>', unsafe_allow_html=True)


    # ── P&L HEATMAP CALENDAR ────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
        'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">P&L Calendar — Last 30 Days</div>',
        unsafe_allow_html=True
    )
    from datetime import date as _dt_date
    _today = _dt_date.today()
    _trade_by_day = {}
    for _t in all_trades:
        _d = _t.get("closed_at","")[:10]
        if _d:
            _trade_by_day[_d] = _trade_by_day.get(_d, 0) + _t.get("pnl", 0)
    _days_30 = [_today - timedelta(days=_i) for _i in range(29, -1, -1)]
    _cal_cells = ""
    for _day in _days_30:
        _ds = _day.strftime("%Y-%m-%d")
        _p  = _trade_by_day.get(_ds, None)
        _lbl = _day.strftime("%d")
        if _p is None:
            _bg = "#0d0d0d"; _bord = "#1e1e1e"
            _txt = '<span style="color:#2a2a2a;font-size:.52rem;">—</span>'
        elif _p >= 0:
            _iv = min(_p / max(initial * 0.02, 1), 1.0)
            _g  = int(100 + _iv * 84)
            _bg = "rgba(0," + str(_g) + ",80," + str(round(0.08 + _iv * 0.22, 2)) + ")"
            _bord = "rgba(0,184,122,0.3)"
            _txt = '<span style="color:#00B87A;font-size:.52rem;">+$' + f'{_p:,.0f}' + '</span>'
        else:
            _iv = min(abs(_p) / max(initial * 0.02, 1), 1.0)
            _bg = "rgba(224,58,82," + str(round(0.08 + _iv * 0.22, 2)) + ")"
            _bord = "rgba(224,58,82,0.3)"
            _txt = '<span style="color:#E03A52;font-size:.52rem;">$' + f'{_p:,.0f}' + '</span>'
        _cal_cells += (
            '<div style="background:' + _bg + ';border:1px solid ' + _bord + ';'
            'padding:.5rem .3rem;text-align:center;min-height:52px;">'
            '<div style="font-size:.44rem;color:#3a3a3a;margin-bottom:3px;">' + _lbl + '</div>'
            + _txt + '</div>'
        )
    st.markdown(
        '<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:1px;'
        'background:var(--border);margin-bottom:1.5rem;">' + _cal_cells + '</div>',
        unsafe_allow_html=True
    )

    # ── TRADE BREAKDOWN ──────────────────────────────────────
    _hm1, _hm2 = st.columns(2, gap="small")
    with _hm1:
        st.markdown(
            '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
            'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Symbol Breakdown</div>',
            unsafe_allow_html=True
        )
        _sym_pnl = {}
        for _t2 in all_trades:
            _s2 = _t2.get("symbol","?")
            _sym_pnl[_s2] = _sym_pnl.get(_s2, 0) + _t2.get("pnl", 0)
        _sorted_syms = sorted(_sym_pnl.items(), key=lambda x: abs(x[1]), reverse=True)[:6]
        _max_abs = max((abs(_v) for _, _v in _sorted_syms), default=1)
        for _sn, _sp in _sorted_syms:
            _bw  = abs(_sp) / _max_abs * 100
            _sc  = "var(--green)" if _sp >= 0 else "var(--red)"
            _ss  = "+" if _sp >= 0 else ""
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:.8rem;margin-bottom:6px;">'
                f'<div style="font-weight:700;font-size:.75rem;width:72px;color:var(--text);">{_sn}</div>'
                f'<div style="flex:1;height:6px;background:var(--border3);border-radius:1px;">'
                f'<div style="width:{_bw:.1f}%;height:100%;background:{_sc};border-radius:1px;"></div></div>'
                f'<div style="font-size:.7rem;color:{_sc};width:72px;text-align:right;'
                f'font-family:JetBrains Mono,monospace;">{_ss}${_sp:,.2f}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    with _hm2:
        st.markdown(
            '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
            'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Best vs Worst Trades</div>',
            unsafe_allow_html=True
        )
        if all_trades:
            _sorted_t = sorted(all_trades, key=lambda x: x.get("pnl", 0))
            for _label, _tlist, _col in [
                ("BEST",  _sorted_t[-3:][::-1], "var(--green)"),
                ("WORST", _sorted_t[:3],         "var(--red)")
            ]:
                st.markdown(
                    f'<div style="font-size:.52rem;color:{_col};letter-spacing:2px;'
                    f'text-transform:uppercase;margin:.5rem 0 4px;">{_label}</div>',
                    unsafe_allow_html=True
                )
                for _t3 in _tlist:
                    _p3 = _t3.get("pnl", 0)
                    _ps3 = "+" if _p3 >= 0 else ""
                    _pc3 = "var(--green)" if _p3 >= 0 else "var(--red)"
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;background:var(--s1);'
                        f'border:1px solid var(--border);border-left:2px solid {_pc3};'
                        f'padding:.5rem 1rem;margin-bottom:1px;">'
                        f'<span style="font-size:.72rem;font-weight:700;">{_t3.get("symbol","?")} '
                        f'<span style="color:var(--dim);font-weight:400;">{_t3.get("type","")}</span></span>'
                        f'<span style="color:{_pc3};font-size:.72rem;font-family:JetBrains Mono,monospace;'
                        f'font-weight:700;">{_ps3}${_p3:,.2f}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown('<div style="color:var(--dim);font-size:.78rem;padding:1rem;">No trades yet.</div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tc1,tc2,tc3,tc4,tc5,tc6,tc7 = st.columns(7)
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
    with tc7:
        if st.button("Daily XP",     use_container_width=True, key="qt_dc"):   goto("daily_challenge")
    footer()

# ══════════════════════════════════════════════════════════════
# CRYPTO MARKETS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "markets":
    if not st.session_state.user: goto("auth")
    nav()
    render_live_ticker()
    sec("Live Markets","Crypto · Bitcoin · Ethereum — Signals, order book and watchlist")

    # ── AI TRADING SIGNAL ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    signal = random.choice(["STRONG BUY", "BUY", "WAIT", "NO TRADE", "SELL", "STRONG SELL"])
    sig_col = {"STRONG BUY":"var(--green)", "BUY":"var(--green)", "WAIT":"var(--gold)", "NO TRADE":"var(--dim)", "SELL":"var(--red)", "STRONG SELL":"var(--red)"}[signal]
    
    st.markdown(f'''
    <div style="background:var(--s1);border:1px solid var(--border);padding:1.5rem;text-align:center;margin-bottom:2rem;border-radius:4px;box-shadow:0 10px 30px rgba(0,0,0,0.5);position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{sig_col},transparent);opacity:0.8;"></div>
        <div style="font-size:.65rem;color:var(--dim);letter-spacing:4px;text-transform:uppercase;margin-bottom:.8rem;">Algorithmic Market Bias</div>
        <div style="font-family:\\'Bebas Neue\\',sans-serif;font-size:3.5rem;color:{sig_col};letter-spacing:4px;line-height:1;text-shadow:0 0 30px {sig_col}60;">{signal}</div>
        <div style="font-size:.6rem;color:var(--dim2);margin-top:1rem;letter-spacing:1px;text-transform:uppercase;">Scanning liquidity pools and macro order blocks...</div>
    </div>
    ''', unsafe_allow_html=True)

    # ── TRADINGVIEW CHART ────────────────────────────────────
    _stc.html("""
    <div class="tradingview-widget-container" style="height:100%;width:100%">
      <div id="tradingview_mkt" style="height:600px;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true,
        "symbol": "BINANCE:BTCUSDT",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "backgroundColor": "#030303",
        "gridColor": "#1e1e1e",
        "hide_top_toolbar": false,
        "hide_legend": false,
        "save_image": false,
        "container_id": "tradingview_mkt"
      });
      </script>
    </div>
    """, height=620)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PORTFOLIO & ANALYTICS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page in ["portfolio", "analytics"]:
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]
    
    challenge = db_get_active_challenge(uid)
    ch_id = challenge["id"] if challenge else 0
    all_trades = db_get_trades(uid, ch_id, limit=500)
    wr, ap, bt, wt, tt = compute_stats(all_trades)
    
    passed_challenges = supabase.table("challenges").select("id").eq("user_id", uid).eq("status", "passed").execute().data
    passed = len(passed_challenges)

    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    sec("Portfolio & Trading DNA", "Detailed analysis of your trading habits and performance.")

    # ── TRADING DNA ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
        'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Trading DNA</div>',
        unsafe_allow_html=True
    )
    _dna1, _dna2, _dna3 = st.columns(3, gap="small")
    _sym_count = {}
    for _t4 in all_trades:
        _sym_count[_t4.get("symbol","?")] = _sym_count.get(_t4.get("symbol","?"), 0) + 1
    _fav_sym = max(_sym_count, key=_sym_count.get) if _sym_count else "N/A"
    _buys    = sum(1 for _t4 in all_trades if _t4.get("type") == "BUY")
    _sells   = sum(1 for _t4 in all_trades if _t4.get("type") == "SELL")
    _tot_dir = max(_buys + _sells, 1)
    _buy_pct  = _buys  / _tot_dir * 100
    _sell_pct = _sells / _tot_dir * 100
    _best_t  = max(all_trades, key=lambda x: x.get("pnl",0)) if all_trades else {}
    _worst_t = min(all_trades, key=lambda x: x.get("pnl",0)) if all_trades else {}
    _score   = min(int(wr*0.5 + (ap/5 if ap>0 else 0) + passed*8), 100)

    with _dna1:
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);padding:1.2rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;'
            f'text-transform:uppercase;margin-bottom:.8rem;">Direction Bias</div>'
            f'<div style="display:flex;height:8px;gap:2px;margin-bottom:.6rem;">'
            f'<div style="width:{_buy_pct:.0f}%;background:var(--green);"></div>'
            f'<div style="flex:1;background:var(--red);"></div></div>'
            f'<div style="display:flex;justify-content:space-between;font-size:.65rem;">'
            f'<span style="color:var(--green);">BUY {_buy_pct:.0f}%</span>'
            f'<span style="color:var(--red);">SELL {_sell_pct:.0f}%</span></div>'
            f'<div style="margin-top:1rem;font-size:.52rem;color:var(--dim);'
            f'text-transform:uppercase;letter-spacing:2px;">Favourite Instrument</div>'
            f'<div style="font-family:Bebas Neue,sans-serif;font-size:1.5rem;'
            f'color:var(--cyan);letter-spacing:3px;">{_fav_sym}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with _dna2:
        _score_col = "var(--green)" if _score >= 50 else "var(--red)"
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);padding:1.2rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;'
            f'text-transform:uppercase;margin-bottom:.8rem;">Performance Score</div>'
            f'<div style="font-family:Bebas Neue,sans-serif;font-size:3.2rem;'
            f'color:{_score_col};letter-spacing:2px;line-height:1;">{_score}</div>'
            f'<div style="font-size:.52rem;color:var(--dim);margin-top:.2rem;">/ 100 overall score</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:1rem;">'
            f'<div style="background:var(--s2);padding:.5rem;text-align:center;">'
            f'<div style="font-size:.5rem;color:var(--dim);">Win Rate</div>'
            f'<div style="font-size:.9rem;color:var(--green);font-weight:700;">{wr:.0f}%</div></div>'
            f'<div style="background:var(--s2);padding:.5rem;text-align:center;">'
            f'<div style="font-size:.5rem;color:var(--dim);">Challenges Passed</div>'
            f'<div style="font-size:.9rem;color:var(--cyan);font-weight:700;">{passed}</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with _dna3:
        _bp = _best_t.get("pnl",0);  _bsym = _best_t.get("symbol","—")
        _wp = _worst_t.get("pnl",0); _wsym = _worst_t.get("symbol","—")
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid var(--border);padding:1.2rem;">'
            f'<div style="font-size:.52rem;color:var(--dim);letter-spacing:2px;'
            f'text-transform:uppercase;margin-bottom:.8rem;">Milestone Trades</div>'
            f'<div style="border-left:2px solid var(--green);padding-left:.8rem;margin-bottom:.9rem;">'
            f'<div style="font-size:.5rem;color:var(--dim);text-transform:uppercase;">Best Trade</div>'
            f'<div style="font-weight:700;color:var(--text);font-size:.8rem;">{_bsym}</div>'
            f'<div style="color:var(--green);font-family:JetBrains Mono,monospace;font-weight:700;">+${_bp:,.2f}</div></div>'
            f'<div style="border-left:2px solid var(--red);padding-left:.8rem;">'
            f'<div style="font-size:.5rem;color:var(--dim);text-transform:uppercase;">Worst Trade</div>'
            f'<div style="font-weight:700;color:var(--text);font-size:.8rem;">{_wsym}</div>'
            f'<div style="color:var(--red);font-family:JetBrains Mono,monospace;font-weight:700;">${_wp:,.2f}</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )


    footer()

# ══════════════════════════════════════════════════════════════
# JOURNAL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "journal":
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]
    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    sec("Trading Journal", "Log your thoughts, emotions, and trade rationale.")
    
    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);padding:1.5rem;margin-bottom:2rem;border-left:2px solid var(--gold);">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.65rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">New Entry</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: j_sym = st.text_input("Asset / Symbol", placeholder="e.g. BTCUSDT", key="jsym")
    with c2: j_mood = st.selectbox("Psychology / Mood", ["Focused", "Anxious", "Confident", "Revenge Trading", "Tired", "Euphoric"], key="jmood")
    
    j_text = st.text_area("Entry details", placeholder="Why did you take this trade? What is your macro bias? Did you stick to your rules?", height=120, key="jtext")
    
    if st.button("Save Entry", key="jsave"):
        if j_text.strip() == "":
            st.error("Please enter some text for your journal.")
        else:
            db_add_journal_entry(uid, j_text, j_mood, j_sym)
            st.success("Entry saved successfully!")
            time.sleep(1); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    entries = db_get_journal(uid)
    if not entries:
        st.markdown('<div style="text-align:center;color:var(--dim);font-size:.8rem;padding:2rem;">No journal entries found. Start writing above!</div>', unsafe_allow_html=True)
    else:
        for e in entries:
            dt = e.get("created_at", "")[:10]
            mood = e.get("mood", "Neutral")
            mood_col = "var(--green)" if mood in ["Focused", "Confident"] else "var(--red)" if mood in ["Revenge Trading", "Anxious"] else "var(--gold)"
            sym = e.get("symbol", "") or "General"
            txt = e.get("entry_text", "")
            
            st.markdown(f'''
            <div style="background:var(--s0);border:1px solid var(--border);padding:1.2rem;margin-bottom:1rem;position:relative;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem;border-bottom:1px solid var(--border);padding-bottom:.5rem;">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--cyan);">{sym.upper()}</div>
                    <div style="font-size:.65rem;color:var(--dim);letter-spacing:1px;">{dt}</div>
                </div>
                <div style="font-size:.85rem;color:var(--text);line-height:1.6;margin-bottom:1rem;">{txt}</div>
                <div style="display:inline-block;padding:3px 10px;border:1px solid {mood_col}40;color:{mood_col};font-size:.55rem;letter-spacing:1px;text-transform:uppercase;background:{mood_col}10;">{mood}</div>
            </div>
            ''', unsafe_allow_html=True)
            
    footer()

# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user: goto("auth")
    nav()
    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    sec("Trade History", "Complete log of all executed trades across all challenges.")
    st.markdown('<div style="color:var(--dim);text-align:center;padding:3rem;background:var(--s1);border:1px solid var(--border);border-radius:4px;">Trade history table is currently being synchronized. View recent trades on the Dashboard.</div>', unsafe_allow_html=True)
    footer()


# ══════════════════════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "leaderboard":
    nav()
    sec("Global Leaderboard", "Top traders ranked by total profit percentage.")
    lb = db_get_leaderboard()
    
    if not lb:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--dim);border:1px solid var(--border);background:var(--s1);border-radius:4px;">No leaderboard data available yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="display:grid;grid-template-columns:50px 3fr 2fr 2fr 2fr;padding:1rem;background:var(--s2);font-size:.65rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;border-bottom:1px solid var(--border);"><span>Rank</span><span>Trader</span><span>Plan</span><span>Status</span><span style="text-align:right;">Profit %</span></div>', unsafe_allow_html=True)
        
        for i, row in enumerate(lb):
            rank = i + 1
            rank_html = f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;color:var(--gold);">{rank}</div>' if rank <= 3 else f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.2rem;color:var(--dim);">{rank}</div>'
            name = row.get("name", "Unknown")
            country = row.get("country", "")
            if country: name += f' <span style="font-size:.7rem;color:var(--dim);">({country})</span>'
            
            plan = row.get("plan", "").upper()
            status = row.get("status", "ACTIVE").upper()
            prof_pct = row.get("profit_pct", 0)
            
            prof_col = "var(--green)" if prof_pct >= 0 else "var(--red)"
            status_emoji = "🟢" if status == "ACTIVE" else "🏆" if status == "PASSED" else "❌"
            
            st.markdown(
                f'<div style="display:grid;grid-template-columns:50px 3fr 2fr 2fr 2fr;padding:1rem;border-bottom:1px solid var(--border);align-items:center;background:var(--s1);transition:background .2s;">'
                f'{rank_html}'
                f'<div style="font-weight:600;color:var(--text);font-size:.9rem;">{name}</div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;color:var(--cyan);">{plan}</div>'
                f'<div style="font-size:.7rem;color:var(--dim);letter-spacing:1px;">{status_emoji} {status}</div>'
                f'<div style="text-align:right;font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;color:{prof_col};font-weight:700;">+{prof_pct:.2f}%</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PROFILE / ME
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]
    name = st.session_state.user.get("name", "Trader")
    email = st.session_state.user.get("email", "")
    
    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    sec("Trader Profile", "Manage your account and platform settings")
    
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);padding:2rem;border-radius:4px;margin-bottom:1.5rem;">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.5rem;color:var(--text);letter-spacing:2px;line-height:1;">{name}</div>'
        f'<div style="font-size:.9rem;color:var(--gold);margin-top:8px;font-family:\'JetBrains Mono\',monospace;">{email}</div>'
        f'<div style="font-size:.7rem;color:var(--dim);margin-top:8px;">ID: {uid}</div>'
        f'</div>', unsafe_allow_html=True
    )
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Sign Out",use_container_width=True,key="profile_logout"):
            supabase.auth.sign_out()
            st.session_state.user=None
            st.session_state.notifications=[]
            goto("home")
    with c2:
        if st.button("Send Test Email",use_container_width=True,key="test_email"):
            ok=send_email_html(email,"AKFunded — Email Test",f'<div style="font-family:Arial,sans-serif;background:#030303;color:#D8D8D8;padding:2rem;max-width:500px;"><h2 style="color:#D4AF37;">AKFUNDED</h2><p>Email working correctly, {name}.</p></div>')
            if ok: st.success(f"Test email sent to {email}.")
            else: st.error("Configure SMTP_EMAIL and SMTP_PASSWORD in secrets.")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "notifications":
    if not st.session_state.user: goto("auth")
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
        st.markdown('<div style="text-align:center;padding:4rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No notifications yet.</div>', unsafe_allow_html=True)
    else:
        for n in notifs:
            uc="unread" if n.get("unread") else ""
            new_badge='<span class="notif-badge">NEW</span>' if n.get("unread") else ""
            st.markdown(f'<div class="notif-item {uc}"><div class="notif-body"><div class="notif-title">{n.get("title","Notification")}{new_badge}</div><div class="notif-msg">{n.get("msg","")}</div><div class="notif-time">{n.get("time","")}</div></div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":
    if not st.session_state.user: goto("auth")
    if st.session_state.user.get("email","") != st.secrets.get("ADMIN_EMAIL","admin@akfunded.com"):
        st.error("Access denied."); st.stop()
    nav()
    sec("Admin Panel","Platform overview — all traders and challenges")
    all_data=db_get_all_accounts()
    total_traders=len(set(r["user_id"] for r in all_data)); total_ch=len(all_data)
    total_passed=sum(1 for r in all_data if r["status"]=="passed")
    total_active=sum(1 for r in all_data if r["status"]=="active")
    total_failed=sum(1 for r in all_data if r["status"]=="failed")
    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border);"><div class="stat-box"><div class="sv w">{total_traders}</div><div class="sl">Traders</div></div><div class="stat-box"><div class="sv w">{total_ch}</div><div class="sl">Challenges</div></div><div class="stat-box"><div class="sv c">{total_active}</div><div class="sl">Active</div></div><div class="stat-box"><div class="sv g">{total_passed}</div><div class="sl">Passed</div></div><div class="stat-box"><div class="sv r">{total_failed}</div><div class="sl">Failed</div></div></div>', unsafe_allow_html=True)
    search=st.text_input("Search",placeholder="Filter by name or email...",key="admin_search")
    status_filter=st.selectbox("Status",["All","active","passed","failed"],key="admin_status")
    filtered=all_data
    if search: filtered=[r for r in filtered if search.lower() in r["name"].lower() or search.lower() in r["email"].lower()]
    if status_filter!="All": filtered=[r for r in filtered if r["status"]==status_filter]
    st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div class="admin-row header"><span>Trader</span><span>Plan</span><span>Balance</span><span>P&L %</span><span>Days</span><span>Status</span></div>', unsafe_allow_html=True)
    for r in filtered[:50]:
        pc="var(--green)" if r["pnl_pct"]>=0 else "var(--red)"; ps="+" if r["pnl_pct"]>=0 else ""
        cap_str=f"${r['capital']//1000}K"
        st.markdown(f'<div class="admin-row"><div><div style="font-weight:700;color:var(--text);">{r["name"]}</div><div style="font-size:.65rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">{r["email"]}</div></div><div style="color:var(--cyan);font-size:.75rem;">{r["plan"].upper()} ({cap_str})</div><div style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">${r["balance"]:,.2f}</div><div style="color:{pc};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps}{r["pnl_pct"]:.2f}%</div><div style="color:var(--text);">{r["days_traded"]}</div><div class="admin-status {r["status"]}">{r["status"].upper()}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()


# ══════════════════════════════════════════════════════════════
# DAILY CHALLENGE & XP (Gamification)
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "daily_challenge":
    if not st.session_state.user: goto("auth")
    nav()
    _uid_g  = st.session_state.user["id"]
    _name_g = st.session_state.user.get("name","Trader")
    _ch_g   = db_get_active_challenge(_uid_g)
    _acc_g  = db_get_account(_ch_g["id"]) if _ch_g else None
    _at_g   = db_get_trades(_uid_g, _ch_g["id"] if _ch_g else None, limit=500) if _ch_g else []
    _wr_g, _ap_g, _bt_g, _wt_g, _tt_g = compute_stats(_at_g)
    _init_g = float(_acc_g.get("initial_capital",1)) if _acc_g else 100000

    _xp    = _tt_g * 10 + int(_wr_g) * 2 + (_wt_g * 3)
    _level = _xp // 100 + 1
    _xp_in = _xp % 100

    sec("Daily Challenge & XP", "Complete tasks. Earn XP. Level up.")

    # XP Bar
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid var(--border);padding:1.5rem;margin-bottom:1.5rem;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.8rem;">'
        f'<div>'
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:1.4rem;letter-spacing:4px;color:var(--cyan);">LEVEL {_level}</div>'
        f'<div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">{_name_g.upper()} — {_xp} XP total</div>'
        f'</div>'
        f'<div style="text-align:right;">'
        f'<div style="font-size:.52rem;color:var(--dim);text-transform:uppercase;">Next Level</div>'
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:var(--gold);">{100 - _xp_in} XP away</div>'
        f'</div></div>'
        f'<div style="height:6px;background:var(--border3);border-radius:2px;overflow:hidden;">'
        f'<div style="width:{_xp_in}%;height:100%;background:linear-gradient(90deg,var(--cyan),var(--green));'
        f'box-shadow:0 0 10px rgba(0,212,255,.4);border-radius:2px;"></div></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:.5rem;color:var(--dim);margin-top:.4rem;">'
        f'<span>Level {_level}</span><span>{_xp_in}/100 XP</span><span>Level {_level+1}</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    # Daily Tasks
    st.markdown(
        '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
        'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Daily Challenges</div>',
        unsafe_allow_html=True
    )
    _dl_loss = abs(_acc_g.get("daily_loss", 0)) if _acc_g else 0
    _tasks = [
        ("⚡", "Execute 1 Trade",    "+10 XP", _tt_g >= 1,    "var(--cyan)"),
        ("🎯", "Positive P&L",       "+20 XP", _ap_g > 0,     "var(--green)"),
        ("🔥", "Win 2 in a Row",     "+15 XP", _wr_g >= 60,   "var(--gold)"),
        ("📊", "Trade 2 Symbols",    "+10 XP", len(set(_t.get("symbol","") for _t in _at_g)) >= 2, "var(--purple)"),
        ("💎", "Loss Under 1%",      "+25 XP", _dl_loss < _init_g * 0.01, "var(--cyan)"),
    ]
    _tcols = st.columns(5, gap="small")
    for _ti, (_tic, _ttask, _trew, _tdone, _tcol) in enumerate(_tasks):
        with _tcols[_ti]:
            _tbord = _tcol if _tdone else "var(--border)"
            _tbg   = "rgba(0,212,255,0.05)" if _tdone else "var(--s1)"
            _tcheck = (
                '<div style="font-size:.52rem;color:var(--green);letter-spacing:1px;margin-top:5px;">✓ COMPLETE</div>'
                if _tdone else
                '<div style="font-size:.52rem;color:var(--dim);letter-spacing:1px;margin-top:5px;">PENDING</div>'
            )
            st.markdown(
                f'<div style="background:{_tbg};border:1px solid {_tbord};padding:1.2rem .8rem;'
                f'text-align:center;height:100%;">'
                f'<div style="font-size:1.8rem;margin-bottom:.5rem;">{_tic}</div>'
                f'<div style="font-size:.65rem;font-weight:700;color:var(--text);line-height:1.3;margin-bottom:.3rem;">{_ttask}</div>'
                f'<div style="font-family:Bebas Neue,sans-serif;font-size:1rem;color:{_tcol};">{_trew}</div>'
                f'{_tcheck}</div>',
                unsafe_allow_html=True
            )

    # XP History table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;'
        'text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">XP Breakdown</div>',
        unsafe_allow_html=True
    )
    _xp_rows = [
        ("Trades Executed",    _tt_g,              "× 10 XP each",  _tt_g * 10),
        ("Win Rate Bonus",     f"{_wr_g:.0f}%",    "× 2 XP per %",  int(_wr_g) * 2),
        ("Winning Trades",     _wt_g,              "× 3 XP each",   _wt_g * 3),
    ]
    st.markdown(
        '<div style="background:var(--s1);border:1px solid var(--border);">',
        unsafe_allow_html=True
    )
    for _xr_label, _xr_val, _xr_formula, _xr_pts in _xp_rows:
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'padding:.8rem 1.2rem;border-bottom:1px solid var(--border);">'
            f'<span style="font-size:.78rem;color:var(--text);">{_xr_label}</span>'
            f'<span style="font-size:.72rem;color:var(--dim);font-family:JetBrains Mono,monospace;">'
            f'{_xr_val} {_xr_formula}</span>'
            f'<span style="font-family:Bebas Neue,sans-serif;font-size:1rem;color:var(--gold);">'
            f'+{_xr_pts} XP</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    st.markdown(
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:.8rem 1.2rem;background:rgba(0,212,255,0.04);">'
        f'<span style="font-size:.78rem;font-weight:700;color:var(--text);">TOTAL XP</span>'
        f'<span style="font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:var(--cyan);">'
        f'{_xp} XP — Level {_level}</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )
    footer()

# ══════════════════════════════════════════════════════════════
# AI CHAT
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "ai_chat":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]; name=st.session_state.user.get("name","Trader")
    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    trades=db_get_trades(uid,challenge["id"] if challenge else None,limit=10)
    balance=account.get("balance",0) if account else 0; initial=account.get("initial_capital",1) if account else 1
    pnl_pct=((balance-initial)/initial*100) if initial else 0; plan=challenge.get("plan","") if challenge else ""
    r=RULES.get(plan,{}); phase=r.get("phase","1step")
    SYSTEM=(
        f"You are a professional AI trading coach for AKFunded, a forex prop trading simulator. "
        f"Trader: {name}, {plan.upper()} ({phase}) challenge. P&L: {pnl_pct:.1f}%. Balance: ${balance:,.2f}. "
        f"Instruments: Forex pairs, Metals (Bitcoin, XAGUSD), Crude Oil (Ethereum, UKOIL). "
        f"Rules: {r.get('daily_loss',5)}% daily loss limit, {r.get('total_loss',10)}% max loss, {r.get('target',8)}% target. "
        f"Recent trades: {[t.get('symbol','')+' '+t.get('type','')+' $'+str(round(t.get('pnl',0),2)) for t in trades[:5]]}. "
        f"Give concise professional forex/metals trading advice. Keep replies under 130 words."
    )
    sec("AI Trading Coach","Powered by Groq — LLaMA 3.3 70B")
    st.markdown('<div class="chat-container"><div class="chat-header"><div class="chat-ai-dot"></div><div><div style="font-weight:700;font-size:.85rem;color:var(--text);">AK Trading Coach</div><div style="font-size:.65rem;color:var(--green);letter-spacing:1px;">Online — Crypto Specialist</div></div></div></div>', unsafe_allow_html=True)
    chat=st.session_state.chat_history
    if not chat:
        st.markdown(f'<div class="chat-messages"><div class="chat-msg"><div class="chat-avatar ai">AI</div><div class="chat-bubble ai">Hello {name}. I specialise in Crypto trading. Ask me about Bitcoin setups, risk management, or how to pass your challenge efficiently.</div></div></div>', unsafe_allow_html=True)
    else:
        msgs_html=""
        for m in chat[-10:]:
            role=m["role"]; txt=m["content"]; cls="user" if role=="user" else "ai"
            av=name[0].upper() if role=="user" else "AI"
            msgs_html+=f'<div class="chat-msg {cls}"><div class="chat-avatar {cls}">{av}</div><div class="chat-bubble {cls}">{txt}</div></div>'
        st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)
    quick=["Bitcoin setup","EURUSD analysis","Risk management","Recovering drawdown","How to pass faster"]
    qcols=st.columns(len(quick))
    for i,q in enumerate(quick):
        with qcols[i]:
            if st.button(q,key=f"qp_{i}",use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Processing..."): resp=call_ai(st.session_state.chat_history,SYSTEM)
                st.session_state.chat_history.append({"role":"assistant","content":resp}); st.rerun()
    user_input=st.text_input("Message",placeholder="Ask about Bitcoin, Ethereum, or altcoins...",key="chat_input",label_visibility="collapsed")
    c1,c2=st.columns([5,1])
    with c2: send=st.button("Send",use_container_width=True,key="chat_send")
    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner("Processing..."): resp=call_ai(st.session_state.chat_history,SYSTEM)
        st.session_state.chat_history.append({"role":"assistant","content":resp}); st.rerun()
    if st.button("Clear",key="clear_chat"):
        st.session_state.chat_history=[]; st.rerun()
    footer()

# ══════════════════════════════════════════════════════════════
# RISK CALCULATOR
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "risk_calc":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]
    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    balance=float(account.get("balance",10000)) if account else 10000.0
    sec("Risk Calculator","Crypto position sizing, pip value and challenge limits")
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Position Size Calculator</div>', unsafe_allow_html=True)
        acc_size=st.number_input("Account Balance ($)",value=balance,min_value=1000.0,step=1000.0,key="rc_bal")
        risk_pct=st.slider("Risk per trade (%)",0.1,3.0,1.0,0.1,key="rc_risk")
        sym_sel=st.selectbox("Symbol",[s for g in SYMBOLS.values() for s in g],key="rc_sym")
        entry_p=st.number_input("Entry Price",value=float(get_all_market_data().get(sym_sel,{}).get("price",1.0)),min_value=0.00001,format="%.5f",key="rc_entry")
        stop_loss=st.number_input("Stop Loss",value=float(round(get_all_market_data().get(sym_sel,{}).get("price",1.0)*0.995,5)),min_value=0.00001,format="%.5f",key="rc_sl")
        target_p=st.number_input("Take Profit",value=float(round(get_all_market_data().get(sym_sel,{}).get("price",1.0)*1.015,5)),min_value=0.00001,format="%.5f",key="rc_tp")
        risk_amt=acc_size*risk_pct/100; sl_dist=abs(entry_p-stop_loss); tp_dist=abs(target_p-entry_p)
        pip_val=10 if "JPY" not in sym_sel and "XAG" not in sym_sel and "OIL" not in sym_sel else 1
        lots=round(risk_amt/(sl_dist*pip_val*1000),2) if sl_dist>0 else 0
        reward_amt=lots*tp_dist*pip_val*1000; rr_ratio=tp_dist/sl_dist if sl_dist>0 else 0
        rc="var(--green)" if rr_ratio>=2 else ("var(--gold)" if rr_ratio>=1 else "var(--red)")
        st.markdown(
            f'<div class="risk-card" style="margin-top:1rem;">'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);">'
            f'<div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Lot Size</div><div class="risk-val" style="color:var(--cyan);">{lots}</div><div style="font-size:.65rem;color:var(--dim);">standard lots</div></div>'
            f'<div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Risk Amount</div><div class="risk-val" style="color:var(--red);">${risk_amt:,.2f}</div><div style="font-size:.65rem;color:var(--dim);">{risk_pct}% of account</div></div>'
            f'<div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">Reward</div><div class="risk-val" style="color:var(--green);">${reward_amt:,.2f}</div><div style="font-size:.65rem;color:var(--dim);">if TP hit</div></div>'
            f'<div class="risk-result"><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;text-transform:uppercase;">R:R Ratio</div><div class="risk-val" style="color:{rc};">1:{rr_ratio:.1f}</div><div style="font-size:.65rem;color:var(--dim);">{"Good" if rr_ratio>=2 else "Marginal" if rr_ratio>=1 else "Poor"}</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Challenge Risk Limits</div>', unsafe_allow_html=True)
        if challenge and account:
            r=RULES.get(challenge["plan"],{}); init=float(account.get("initial_capital",1))
            daily_lim=init*r.get("daily_loss",5)/100; total_lim=init*r.get("total_loss",10)/100
            daily_rem=daily_lim-abs(account.get("daily_loss",0)); total_rem=total_lim-abs(account.get("total_loss",0))
            st.markdown(
                f'<div class="risk-card">'
                f'<div style="margin-bottom:1.2rem;"><div class="m-label">Daily Loss Remaining</div>'
                f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:{"var(--green)" if daily_rem>daily_lim*0.5 else "var(--red)"};">${daily_rem:,.2f}</div>'
                f'<div style="font-size:.65rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">of ${daily_lim:,.2f} ({r.get("daily_loss",5)}%)</div></div>'
                f'<div style="margin-bottom:1.2rem;"><div class="m-label">Total Loss Remaining</div>'
                f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:{"var(--green)" if total_rem>total_lim*0.5 else "var(--red)"};">${total_rem:,.2f}</div>'
                f'<div style="font-size:.65rem;color:var(--dim);font-family:\'JetBrains Mono\',monospace;">of ${total_lim:,.2f} ({r.get("total_loss",10)}%)</div></div>'
                f'<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--green);padding:1rem;margin-top:1px;">'
                f'<div class="m-label">Recommended Max Risk / Trade</div>'
                f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:var(--green);">${min(daily_rem*0.25,total_rem*0.1):,.2f}</div>'
                f'<div style="font-size:.65rem;color:var(--dim);">Protects daily &amp; total loss limits</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div style="color:var(--dim);padding:2rem;text-align:center;background:var(--s1);border:1px solid var(--border);font-size:.8rem;">Activate a challenge to see your limits.</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# CERTIFICATE  ← KEY FIX: email uses table-based HTML, PDF download added
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "certificate":
    if not st.session_state.user: goto("auth")
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name", "Trader")
    sec("Achievement Certificate", "Official AKFunded funded trader certificate")

    all_ch    = db_get_all_challenges(uid)
    passed_ch = [c for c in all_ch if c.get("status") == "passed"]

    if not passed_ch:
        st.markdown(
            '<div style="text-align:center;padding:5rem;background:var(--s1);border:1px solid var(--border);">'
            '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:4px;color:var(--dim);margin-bottom:.5rem;">No Certificate Yet</div>'
            '<div style="font-size:.8rem;color:var(--dim);font-weight:300;">Pass a challenge to earn your funded trader certificate.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        _, c, _ = st.columns([2, 1, 2])
        with c:
            if st.button("Activate Challenge", use_container_width=True): goto("plans")
    else:
        if len(passed_ch) > 1:
            ch_options = [f"{c['plan'].upper()} — {c.get('started_at','')[:10]}" for c in passed_ch]
            selected   = st.selectbox("Select Challenge", ch_options, key="cert_sel")
            ch         = passed_ch[ch_options.index(selected)]
        else:
            ch = passed_ch[0]

        acc      = db_get_account(ch["id"]) or {}
        cap      = ch.get("capital", 0)
        bal      = acc.get("balance", cap)
        pnl_pct  = (bal - cap) / cap * 100 if cap else 0
        days     = acc.get("days_traded", 0)
        date_str = ch.get("started_at", "")[:10]

        # ── On-screen certificate (browser flex/grid — looks great) ──
        cert_html = build_certificate_html(name, ch["plan"], cap, pnl_pct, days, date_str, ch["id"])
        st.markdown(f'<div style="overflow-x:auto;padding:1rem 0;">{cert_html}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        # ── Email Certificate — uses Gmail-safe table HTML ──
        with col1:
            if st.button("Email Certificate", use_container_width=True, key="email_cert"):
                email_addr = st.session_state.user.get("email", "")
                # Use table-based email version, NOT the flex/grid browser version
                email_html = build_certificate_email_html(name, ch["plan"], cap, pnl_pct, days, date_str)
                ok = send_email_html(email_addr, "AKFunded — Certificate of Achievement", email_html)
                if ok:
                    st.success(f"Certificate emailed to {email_addr}.")
                else:
                    st.info("Configure SMTP_EMAIL and SMTP_PASSWORD in secrets to send emails.")

        # ── Download PDF ──
        with col2:
            with st.spinner("Generating PDF..."):
                pdf_bytes = build_certificate_pdf(name, ch["plan"], cap, pnl_pct, days, date_str)
            if pdf_bytes:
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name=f"AKFunded_Certificate_{name.replace(' ','_')}_{date_str}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="dl_cert_pdf"
                )
            else:
                st.info("Install reportlab to enable PDF: pip install reportlab")

        # ── Copy share text ──
        with col3:
            if st.button("Copy Share Text", use_container_width=True, key="share_cert"):
                cap_str = f"${cap // 1000}K"
                share = (
                    f"I passed the AKFunded {ch['plan'].upper()} Challenge ({cap_str}) "
                    f"with +{pnl_pct:.1f}% profit in {days} trading days! "
                    f"Trading Crypto. @akfunded #AKFunded #PropTrading #Crypto"
                )
                st.code(share, language=None)

        # ── Instagram ──
        with col4:
            if st.button("Share on Instagram", use_container_width=True, key="ig_cert"):
                st.markdown(
                    f'<a href="{IG_URL}" target="_blank" style="color:var(--cyan);">Open @akfunded on Instagram</a>',
                    unsafe_allow_html=True
                )

        st.markdown(
            '<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid rgba(0,184,122,.4);padding:1rem 1.4rem;margin-top:1rem;">'
            '<div style="font-size:.72rem;color:var(--dim);line-height:1.7;">'
            'Tag <b style="color:var(--cyan);">@akfunded</b> on Instagram when you share your achievement. '
            'The emailed certificate is formatted for Gmail &amp; Outlook. Download the PDF for the best print quality.'
            '</div></div>',
            unsafe_allow_html=True
        )
    footer()

# ══════════════════════════════════════════════════════════════
# PAYOUTS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "payouts":
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]
    challenge = db_get_active_challenge(uid)
    account = db_get_account(challenge["id"]) if challenge else None

    st.markdown('<div style="margin-top:2rem;"></div>', unsafe_allow_html=True)
    sec("Request Withdrawal", "Withdraw your profits to your crypto wallet or bank account.")

    can_withdraw = False
    if challenge and account:
        r = RULES.get(challenge["plan"], {})
        phase_type = r.get("phase", "")
        if phase_type == "instant" or challenge.get("status") == "funded":
            balance = float(account.get("balance", 0))
            initial = float(account.get("initial_capital", 1))
            if balance > initial:
                can_withdraw = True

    if can_withdraw:
        profit = float(account.get("balance", 0)) - float(account.get("initial_capital", 1))
        st.markdown(f'<div style="background:var(--s1);border:1px solid var(--border);padding:1.5rem;border-radius:4px;margin-bottom:2rem;">'
                    f'<div style="font-size:.65rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">Available Profit to Withdraw</div>'
                    f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:3rem;color:var(--gold);line-height:1;margin-top:8px;">${profit:,.2f}</div>'
                    f'</div>', unsafe_allow_html=True)
        
        st.markdown("### Select Withdrawal Method")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                '<div class="card" style="text-align:center;padding:2rem;">'
                '<div style="font-size:2rem;margin-bottom:1rem;">🏛️</div>'
                '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:2px;color:var(--text);">Rise Wallet</div>'
                '<div style="font-size:.7rem;color:var(--gold);letter-spacing:1px;margin-top:8px;font-weight:700;">COMING SOON</div>'
                '</div>', unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                '<div class="card" style="text-align:center;padding:2rem;">'
                '<div style="font-size:2rem;margin-bottom:1rem;">🔗</div>'
                '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.5rem;letter-spacing:2px;color:var(--text);">Crypto (USDT/USDC)</div>'
                '<div style="font-size:.7rem;color:var(--gold);letter-spacing:1px;margin-top:8px;font-weight:700;">COMING SOON</div>'
                '</div>', unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<div style="background:var(--s1);border:1px solid var(--border);padding:2rem;text-align:center;">'
            '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.8rem;color:var(--text);letter-spacing:2px;margin-bottom:10px;">Not Eligible for Withdrawal</div>'
            '<div style="font-size:.85rem;color:var(--dim);">You need an active Instant Funding account or a Passed 2-Step Funded account in profit to request a withdrawal.</div>'
            '</div>', unsafe_allow_html=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# REFERRAL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "referral":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]; name=st.session_state.user.get("name","Trader"); email=st.session_state.user.get("email","")
    sec("Refer & Earn","Invite traders — earn rewards when they join")
    ref=db_get_referral(uid)
    if not ref:
        code=generate_referral_code(name); db_create_referral(uid,code)
        ref=db_get_referral(uid) or {"code":code,"uses":0}
    code=ref.get("code",""); uses=ref.get("uses",0); earnings=uses*500
    share_url=f"{PLATFORM_URL}/?ref={code}"
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid rgba(0,212,255,.15);border-left:2px solid var(--cyan);padding:2rem;margin-bottom:1.5rem;">'
        f'<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Your Referral Code</div>'
        f'<div class="ref-code-box"><div class="ref-code">{code}</div><div style="font-size:.65rem;color:var(--dim);">Unique code</div></div>'
        f'<div class="ref-stats">'
        f'<div class="stat-box"><div class="sv c">{uses}</div><div class="sl">Referrals</div></div>'
        f'<div class="stat-box"><div class="sv g">&#8377;{earnings}</div><div class="sl">Earned</div></div>'
        f'<div class="stat-box"><div class="sv w">&#8377;500</div><div class="sl">Per Referral</div></div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
    st.code(share_url, language=None)
    c1,c2=st.columns(2)
    with c1:
        wa=f"https://wa.me/?text=Join%20AKFunded%20-%20Forex%20Prop%20Trading%20Simulator.%20Use%20code%20{code}.%20{share_url}"
        st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%;background:rgba(0,212,255,.1);color:var(--cyan);font-weight:700;border:1px solid rgba(0,212,255,.3);padding:.55rem;font-family:\'Rajdhani\',sans-serif;cursor:pointer;letter-spacing:2px;font-size:.78rem;text-transform:uppercase;">Share on WhatsApp</button></a>', unsafe_allow_html=True)
    with c2:
        if st.button("Email Invite",use_container_width=True,key="email_invite"):
            html_invite=(
                f'<div style="font-family:Arial,sans-serif;max-width:580px;background:#050505;color:#D8D8D8;padding:2rem;">'
                f'<h2 style="color:#00D4FF;letter-spacing:4px;">AKFUNDED</h2>'
                f'<p>{name} has invited you to AKFunded — Crypto Prop Trading.</p>'
                f'<div style="background:#0d0d0d;border-left:2px solid #00D4FF;padding:1rem;margin:1rem 0;">'
                f'<div style="font-size:1.4rem;font-weight:700;color:#00D4FF;letter-spacing:4px;">{code}</div>'
                f'</div>'
                f'<p><a href="{share_url}" style="color:#00D4FF;">Join here — akfunded.streamlit.app</a></p>'
                f'</div>'
            )
            ok=send_email_html(email,f"{name} invited you to AKFunded",html_invite)
            if ok: st.success("Invite sent.")
            else: st.info("Configure SMTP settings.")
    footer()
