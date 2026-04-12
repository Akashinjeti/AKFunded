import streamlit as st
from supabase import create_client
import time, random, string, smtplib, base64, io
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
@import url('https://fonts.googleapis.com/css2?family=Alex+Brush&family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Exo+2:ital,wght@0,100;0,300;0,400;0,600;0,700;1,300&family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@300;400;500;600;700&display=swap');

:root {
  --gold:#FFB627;
  --gold-dim:#5c3d00;
  --gold-glow:rgba(255,182,39,.2);
  --black:#02030a;
  --s0:#030410;
  --s1:#060818;
  --s2:#080b1e;
  --s3:#0b0f28;
  --border:#12183a;
  --border2:#1a2248;
  --border3:#222e5c;
  --text:#c8d4f0;
  --dim:#3a4870;
  --dim2:#2a3560;
  --green:#00ff9d;
  --green-dim:rgba(0,255,157,.1);
  --red:#ff2d6b;
  --red-dim:rgba(255,45,107,.1);
  --purple:#bf5fff;
  --blue:#4d9eff;
  --cyan:#00e5ff;
  --cyan-dim:rgba(0,229,255,.08);
  --neon:#39FF14;
  --accent:#7c3aed;
  --accent2:#2563eb;
}

html, body {
  background:#02030a!important;
  font-family:'Exo 2',sans-serif;
}
[class*="css"],.main,.stApp,.stApp>div,section.main,
div[data-testid="stAppViewContainer"],div[data-testid="stHeader"],
div[data-testid="stToolbar"],div[data-testid="stDecoration"],
div[data-testid="stBottom"],.appview-container,.reportview-container,
.main .block-container,iframe {
  background-color:#02030a!important;background:#02030a!important;
}
* { font-family:'Exo 2',sans-serif; color:var(--text); }
#MainMenu,footer,header { visibility:hidden!important;display:none!important; }
.block-container { padding:1rem 2.5rem 3rem!important;max-width:1440px!important; }
::-webkit-scrollbar { width:2px; }
::-webkit-scrollbar-thumb { background:var(--accent); border-radius:2px; }

body::before {
  content:'';
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(124,58,237,.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 90%, rgba(37,99,235,.06) 0%, transparent 60%);
  pointer-events:none;
  z-index:0;
}
body::after {
  content:'';
  position:fixed;
  top:0;left:0;right:0;bottom:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 60px,rgba(0,229,255,.012) 60px,rgba(0,229,255,.012) 61px),
    repeating-linear-gradient(90deg,transparent,transparent 60px,rgba(0,229,255,.012) 60px,rgba(0,229,255,.012) 61px);
  pointer-events:none;
  z-index:0;
}

.ak-nav {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:1rem 0;
  border-bottom:1px solid var(--border);
  margin-bottom:2rem;
  position:relative;
  background:linear-gradient(90deg,rgba(124,58,237,.05),transparent);
}
.ak-nav::before {
  content:'';
  position:absolute;
  bottom:-1px;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,var(--accent),var(--cyan),transparent);
  opacity:.6;
}
.ak-logo {
  font-family:'Orbitron',monospace;
  font-size:1.6rem;
  letter-spacing:4px;
  display:inline-flex;
  align-items:baseline;
  gap:2px;
  font-weight:900;
}
.ak-part { color:var(--cyan); text-shadow:0 0 20px rgba(0,229,255,.5),0 0 40px rgba(0,229,255,.2); }
.funded-part { color:#fff; letter-spacing:2px; }
.ak-beta {
  background:linear-gradient(135deg,var(--accent),var(--cyan));
  color:#fff;
  font-size:.42rem;
  font-weight:700;
  padding:2px 6px;
  border-radius:3px;
  letter-spacing:2px;
  vertical-align:super;
  margin-left:5px;
  font-family:'Orbitron',monospace;
}
.ak-tagline {
  font-size:.58rem;
  color:var(--dim);
  letter-spacing:4px;
  text-transform:uppercase;
  margin-top:3px;
  font-family:'Share Tech Mono',monospace;
}

.ticker-wrap {
  overflow:hidden;
  background:var(--s1);
  border-top:1px solid rgba(0,229,255,.12);
  border-bottom:1px solid rgba(0,229,255,.12);
  padding:.4rem 0;
  margin-bottom:2rem;
  position:relative;
}
.ticker-wrap::before {
  content:'◈ LIVE';
  position:absolute;
  left:0;
  top:50%;
  transform:translateY(-50%);
  background:linear-gradient(135deg,var(--accent),var(--cyan));
  color:#fff;
  font-size:.48rem;
  font-weight:700;
  padding:3px 12px;
  letter-spacing:2px;
  z-index:2;
  font-family:'Orbitron',monospace;
}
.ticker-inner {
  display:flex;
  gap:3.5rem;
  animation:ticker 45s linear infinite;
  white-space:nowrap;
  padding-left:80px;
}
@keyframes ticker { 0%{transform:translateX(0);} 100%{transform:translateX(-50%);} }
.ticker-item { display:inline-flex;align-items:center;gap:.6rem;font-size:.7rem; }
.ticker-sep { color:rgba(0,229,255,.25); }
.ticker-sym { font-weight:700;color:var(--text);font-family:'Orbitron',monospace;letter-spacing:1px;font-size:.6rem; }
.ticker-price { font-family:'Share Tech Mono',monospace;color:var(--dim);font-size:.68rem; }
.ticker-chg { font-family:'Share Tech Mono',monospace;font-size:.68rem;font-weight:700; }
.ticker-chg.up { color:var(--green); }
.ticker-chg.dn { color:var(--red); }

.hero-v2 {
  position:relative;
  text-align:center;
  padding:5rem 2rem 4rem;
  overflow:hidden;
}
.eyebrow {
  display:inline-flex;
  align-items:center;
  gap:.6rem;
  border:1px solid rgba(0,229,255,.2);
  color:var(--cyan);
  font-size:.55rem;
  letter-spacing:4px;
  padding:6px 20px;
  border-radius:2px;
  margin-bottom:2rem;
  text-transform:uppercase;
  background:rgba(0,229,255,.04);
  font-family:'Orbitron',monospace;
  font-weight:600;
  box-shadow:0 0 20px rgba(0,229,255,.08),inset 0 0 20px rgba(0,229,255,.03);
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
  font-family:'Orbitron',monospace;
  font-size:clamp(2.8rem,7vw,7rem);
  line-height:.95;
  letter-spacing:4px;
  margin:0 0 1.5rem;
  color:#fff;
  font-weight:900;
  text-shadow:0 0 60px rgba(124,58,237,.3);
}
.hero-v2 h1 em { 
  color:var(--cyan);
  font-style:normal;
  text-shadow:0 0 40px rgba(0,229,255,.5),0 0 80px rgba(0,229,255,.2);
  display:block;
}
.hero-v2 .sub {
  font-size:.95rem;
  color:var(--dim);
  max-width:500px;
  margin:0 auto 2.5rem;
  line-height:1.9;
  font-weight:300;
  letter-spacing:.5px;
  font-family:'Exo 2',sans-serif;
}

.hstats {
  display:flex;
  justify-content:center;
  gap:0;
  border:1px solid var(--border);
  margin-bottom:4rem;
  border-radius:4px;
  overflow:hidden;
  background:var(--s1);
}
.hstat {
  flex:1;
  padding:1.4rem 2rem;
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
  background:linear-gradient(90deg,transparent,var(--cyan),transparent);
  opacity:.4;
}
.hstat:last-child { border-right:none; }
.hstat .n {
  font-family:'Orbitron',monospace;
  font-size:1.6rem;
  color:var(--cyan);
  letter-spacing:2px;
  display:block;
  margin-bottom:.25rem;
  font-weight:700;
  text-shadow:0 0 20px rgba(0,229,255,.3);
}
.hstat .l {
  font-size:.52rem;
  color:var(--dim);
  letter-spacing:3px;
  text-transform:uppercase;
  font-family:'Share Tech Mono',monospace;
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
  background:linear-gradient(180deg,var(--cyan),var(--accent));
  opacity:.5;
}
.m-card::after {
  content:'';
  position:absolute;
  top:0;left:0;right:0;
  height:1px;
  background:linear-gradient(90deg,var(--cyan),var(--accent),transparent);
  opacity:.3;
}
.m-label {
  font-size:.5rem;
  color:var(--dim);
  letter-spacing:3px;
  text-transform:uppercase;
  margin-bottom:.6rem;
  font-weight:600;
  font-family:'Share Tech Mono',monospace;
}
.m-val {
  font-family:'Orbitron',monospace;
  font-size:1.6rem;
  letter-spacing:2px;
  line-height:1;
  font-weight:700;
}
.m-val.g { color:var(--green); text-shadow:0 0 15px rgba(0,255,157,.3); }
.m-val.r { color:var(--red); text-shadow:0 0 15px rgba(255,45,107,.3); }
.m-val.o { color:var(--gold); }
.m-val.c { color:var(--cyan); text-shadow:0 0 15px rgba(0,229,255,.3); }
.m-val.w { color:var(--text); }
.m-sub { font-size:.6rem;color:var(--dim);margin-top:.5rem;font-family:'Share Tech Mono',monospace; }

.stats-row { display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border); }
.stat-box { background:var(--s1);padding:1.1rem 1rem;text-align:center;position:relative;overflow:hidden; }
.stat-box::after { content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:.3; }
.stat-box .sv { font-family:'Orbitron',monospace;font-size:1.3rem;letter-spacing:2px;line-height:1;font-weight:700; }
.stat-box .sl { font-size:.48rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-top:.4rem;font-family:'Share Tech Mono',monospace; }
.sv.g { color:var(--green); text-shadow:0 0 10px rgba(0,255,157,.3); }
.sv.r { color:var(--red); }
.sv.o { color:var(--gold); }
.sv.c { color:var(--cyan); text-shadow:0 0 10px rgba(0,229,255,.3); }
.sv.w { color:var(--text); }

.rules-box {
  background:var(--s1);
  border:1px solid var(--border);
  border-radius:0;
  padding:1.6rem;
  margin-bottom:1.5rem;
  position:relative;
  overflow:hidden;
}
.rules-box::before { content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan),transparent);opacity:.4; }
.r-row { display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem; }
.r-name { font-size:.72rem;color:var(--dim);letter-spacing:.5px;font-family:'Exo 2',sans-serif; }
.r-val { font-family:'Share Tech Mono',monospace;font-size:.72rem;font-weight:600; }
.r-val.ok { color:var(--green); }
.r-val.bad { color:var(--red); }
.prog { height:2px;background:var(--border3);margin-bottom:1.2rem;border-radius:1px; }
.prog-fill { height:100%;border-radius:1px; }

.t-header,.t-row {
  display:grid;
  grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.2fr;
  padding:.65rem 1rem;
  font-size:.72rem;
  align-items:center;
}
.t-header {
  color:var(--dim);
  font-size:.5rem;
  letter-spacing:3px;
  text-transform:uppercase;
  border-bottom:1px solid var(--border);
  font-weight:600;
  font-family:'Share Tech Mono',monospace;
}
.t-row { border-bottom:1px solid var(--border); }
.t-row:hover { background:var(--s2); }
.t-row:last-child { border-bottom:none; }
.tag-b { background:rgba(0,255,157,.08);color:var(--green);padding:2px 8px;border-radius:2px;font-size:.58rem;font-weight:700;letter-spacing:1px;border:1px solid rgba(0,255,157,.2); }
.tag-s { background:rgba(255,45,107,.08);color:var(--red);padding:2px 8px;border-radius:2px;font-size:.58rem;font-weight:700;letter-spacing:1px;border:1px solid rgba(255,45,107,.2); }

.lb-item {
  display:flex;
  align-items:center;
  gap:1.2rem;
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid transparent;
  padding:1rem 1.4rem;
  margin-bottom:2px;
  transition:all .2s;
}
.lb-item:hover { border-left-color:var(--cyan);background:var(--s2);transform:translateX(2px); }
.lb-rank { font-family:'Orbitron',monospace;font-size:1.1rem;color:var(--dim);width:36px;text-align:center;font-weight:700; }
.lb-rank.top { color:var(--cyan); text-shadow:0 0 15px rgba(0,229,255,.5); }
.lb-info { flex:1; }
.lb-name { font-weight:600;font-size:.88rem;letter-spacing:.3px; }
.lb-country { font-size:.65rem;color:var(--dim);margin-top:2px;font-family:'Share Tech Mono',monospace; }
.lb-pnl { font-family:'Share Tech Mono',monospace;font-weight:700;color:var(--green);font-size:.9rem; }
.lb-badge { font-size:.5rem;padding:2px 8px;border-radius:2px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;font-family:'Orbitron',monospace; }
.funded-b { background:rgba(0,229,255,.08);color:var(--cyan);border:1px solid rgba(0,229,255,.2); }
.active-b { background:rgba(0,255,157,.06);color:var(--green);border:1px solid rgba(0,255,157,.15); }

.journal-entry {
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid var(--border3);
  padding:1.2rem 1.5rem;
  margin-bottom:2px;
  transition:border-left-color .2s;
}
.journal-entry:hover { border-left-color:var(--accent); }
.je-date { font-size:.52rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.4rem;font-family:'Share Tech Mono',monospace; }
.je-note { font-size:.85rem;color:var(--text);line-height:1.7;font-weight:300; }
.je-tags { display:flex;gap:.4rem;margin-top:.7rem;flex-wrap:wrap; }
.je-tag { font-size:.52rem;padding:2px 8px;border-radius:2px;background:rgba(0,229,255,.06);color:var(--cyan);font-weight:700;letter-spacing:1px;font-family:'Share Tech Mono',monospace; }
.je-tag.win { background:rgba(0,255,157,.08);color:var(--green);border:1px solid rgba(0,255,157,.15); }
.je-tag.loss { background:rgba(255,45,107,.08);color:var(--red);border:1px solid rgba(255,45,107,.15); }

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
.ch-plan { font-family:'Orbitron',monospace;font-size:.9rem;letter-spacing:2px;color:var(--cyan);font-weight:700; }
.ch-status { padding:3px 12px;border-radius:2px;font-size:.52rem;font-weight:700;letter-spacing:2px;text-align:center;text-transform:uppercase;font-family:'Orbitron',monospace; }
.ch-status.passed { background:rgba(0,255,157,.08);color:var(--green);border:1px solid rgba(0,255,157,.2); }
.ch-status.failed { background:rgba(255,45,107,.08);color:var(--red);border:1px solid rgba(255,45,107,.2); }
.ch-status.active { background:rgba(0,229,255,.06);color:var(--cyan);border:1px solid rgba(0,229,255,.15); }

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
.notif-item.unread { border-left:2px solid var(--accent); }
.notif-icon { font-size:1rem;flex-shrink:0;margin-top:2px;opacity:.7; }
.notif-body { flex:1; }
.notif-title { font-weight:600;font-size:.85rem;color:var(--text);margin-bottom:3px; }
.notif-msg { font-size:.72rem;color:var(--dim);line-height:1.5; }
.notif-time { font-size:.58rem;color:var(--dim2);letter-spacing:1px;margin-top:5px;font-family:'Share Tech Mono',monospace; }
.notif-badge { background:linear-gradient(135deg,var(--accent),var(--cyan));color:#fff;font-size:.48rem;font-weight:800;padding:1px 6px;border-radius:2px;margin-left:6px;vertical-align:middle;letter-spacing:1px; }

.profile-hero {
  background:var(--s1);
  border:1px solid var(--border);
  padding:2rem 2.5rem;
  margin-bottom:1.5rem;
  display:flex;
  gap:2.5rem;
  align-items:center;
  position:relative;
  overflow:hidden;
}
.profile-hero::before { content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan),transparent);opacity:.4; }
.profile-avatar {
  width:72px;height:72px;
  border:1px solid rgba(0,229,255,.3);
  display:flex;
  align-items:center;
  justify-content:center;
  font-family:'Orbitron',monospace;
  font-size:1.6rem;
  color:var(--cyan);
  flex-shrink:0;
  background:var(--s2);
  box-shadow:0 0 30px rgba(124,58,237,.2),inset 0 0 20px rgba(0,229,255,.05);
  font-weight:700;
}
.profile-name { font-family:'Orbitron',monospace;font-size:1.4rem;letter-spacing:3px;color:var(--text);line-height:1;font-weight:700; }
.profile-email { font-size:.68rem;color:var(--dim);margin-top:5px;font-family:'Share Tech Mono',monospace; }
.funded-badge-inline {
  display:inline-block;
  background:transparent;
  border:1px solid rgba(0,229,255,.25);
  color:var(--cyan);
  font-size:.52rem;
  letter-spacing:2.5px;
  padding:3px 12px;
  margin-top:8px;
  font-weight:700;
  text-transform:uppercase;
  font-family:'Orbitron',monospace;
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
.admin-row.header { color:var(--dim);font-size:.5rem;letter-spacing:2.5px;text-transform:uppercase;font-family:'Share Tech Mono',monospace; }
.admin-status { padding:2px 10px;border-radius:2px;font-size:.5rem;font-weight:700;letter-spacing:1.5px;text-align:center;text-transform:uppercase;font-family:'Orbitron',monospace; }
.admin-status.active { background:rgba(0,229,255,.06);color:var(--cyan); }
.admin-status.passed { background:rgba(0,255,157,.08);color:var(--green); }
.admin-status.failed { background:rgba(255,45,107,.08);color:var(--red); }

.plan-rules { list-style:none;padding:0;margin:0 0 1.2rem; }
.plan-rules li {
  display:flex;
  justify-content:space-between;
  padding:.45rem 0;
  border-bottom:1px solid var(--border);
  font-size:.76rem;
  color:var(--dim);
}
.plan-rules li b { color:var(--text);font-weight:500; }

.chat-container { background:var(--s1);border:1px solid var(--border);overflow:hidden;margin-bottom:1rem; }
.chat-header { padding:1rem 1.4rem;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:.8rem; }
.chat-ai-dot { width:6px;height:6px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;box-shadow:0 0 10px var(--green); }
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.3;}}
.chat-messages { padding:1.2rem;max-height:380px;overflow-y:auto; }
.chat-msg { margin-bottom:1rem;display:flex;gap:.8rem;align-items:flex-start; }
.chat-msg.user { flex-direction:row-reverse; }
.chat-bubble { padding:.7rem 1rem;font-size:.82rem;line-height:1.6;max-width:78%; }
.chat-bubble.ai { background:var(--s2);border:1px solid var(--border);color:var(--text); }
.chat-bubble.user { background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;font-weight:500; }
.chat-avatar { width:28px;height:28px;font-size:.65rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:var(--s2);border:1px solid var(--border);font-weight:700;font-family:'Orbitron',monospace; }
.chat-avatar.user { background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff; }

.risk-card { background:var(--s1);border:1px solid var(--border);padding:1.5rem; }
.risk-result { background:var(--s2);border:1px solid var(--border);padding:1.1rem;text-align:center;margin-top:1rem; }
.risk-val { font-family:'Orbitron',monospace;font-size:1.8rem;letter-spacing:2px;font-weight:700; }

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
.ref-code { font-family:'Share Tech Mono',monospace;font-size:1.4rem;color:var(--cyan);font-weight:700;letter-spacing:5px; }
.ref-stats { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:1rem 0;background:var(--border); }

.heatmap-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:1rem;background:var(--border); }
.hmap-cell { padding:.8rem .5rem;text-align:center;cursor:default;transition:opacity .2s; }
.hmap-cell:hover { opacity:.85; }
.hmap-sym { font-size:.62rem;font-weight:700;color:var(--text);letter-spacing:1px;font-family:'Orbitron',monospace; }
.hmap-chg { font-size:.72rem;font-family:'Share Tech Mono',monospace;margin-top:3px; }

.scan-row {
  display:flex;
  align-items:center;
  justify-content:space-between;
  background:var(--s1);
  border:1px solid var(--border);
  border-left:2px solid transparent;
  padding:.85rem 1.2rem;
  margin-bottom:2px;
  transition:all .15s;
}
.scan-row:hover { border-left-color:var(--accent);background:var(--s2); }
.scan-sym { font-weight:700;font-size:.82rem;letter-spacing:.5px;font-family:'Orbitron',monospace; }
.scan-signal { font-size:.5rem;font-weight:700;letter-spacing:2px;padding:3px 10px;border-radius:2px;text-transform:uppercase;font-family:'Orbitron',monospace; }
.scan-signal.bull { background:rgba(0,255,157,.08);color:var(--green);border:1px solid rgba(0,255,157,.2); }
.scan-signal.bear { background:rgba(255,45,107,.08);color:var(--red);border:1px solid rgba(255,45,107,.2); }
.scan-signal.neut { background:rgba(0,229,255,.06);color:var(--cyan);border:1px solid rgba(0,229,255,.15); }

.wl-row { display:flex;align-items:center;justify-content:space-between;padding:.7rem .5rem;border-bottom:1px solid var(--border); }
.wl-row:last-child { border-bottom:none; }

.ob-row { display:grid;grid-template-columns:1fr 1fr 1fr;padding:.3rem .8rem;font-size:.7rem;font-family:'Share Tech Mono',monospace; }
.ob-bid { color:var(--green); }
.ob-ask { color:var(--red); }
.ob-vol { color:var(--dim);text-align:right; }

.steps-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin:3rem 0;background:var(--border); }
.step-card { background:var(--s1);padding:2rem 1.5rem;position:relative;overflow:hidden; }
.step-card::before { content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan),transparent);opacity:.3; }
.step-card::after { content:'';position:absolute;bottom:0;right:0;width:60px;height:60px;background:radial-gradient(circle,rgba(124,58,237,.1),transparent);pointer-events:none; }
.step-num { font-family:'Orbitron',monospace;font-size:2.2rem;color:var(--accent);line-height:1;margin-bottom:.6rem;letter-spacing:2px;opacity:.6;font-weight:900; }
.step-title { font-family:'Orbitron',monospace;font-size:.72rem;letter-spacing:2.5px;color:var(--text);margin-bottom:.6rem;font-weight:700; }
.step-desc { font-size:.8rem;color:var(--dim);line-height:1.7;font-weight:300; }

.testi-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:1px;margin:2rem 0;background:var(--border); }
.testi-card { background:var(--s1);padding:1.8rem;position:relative;overflow:hidden; }
.testi-card::before { content:'"';position:absolute;top:-.5rem;left:1rem;font-size:5rem;color:var(--accent);opacity:.08;font-family:'Orbitron',monospace;line-height:1; }
.testi-quote { font-size:.84rem;color:var(--text);line-height:1.8;margin-bottom:1.2rem;font-weight:300;border-left:2px solid var(--accent);padding-left:1rem;opacity:.9; }
.testi-name { font-weight:700;font-size:.78rem;color:var(--cyan);letter-spacing:.5px;font-family:'Orbitron',monospace; }
.testi-meta { font-size:.65rem;color:var(--dim);margin-top:3px;font-family:'Share Tech Mono',monospace; }

.ak-footer {
  text-align:center;
  padding:2.5rem 0 1.5rem;
  border-top:1px solid var(--border);
  margin-top:5rem;
  color:var(--dim);
  font-size:.65rem;
  letter-spacing:1px;
  position:relative;
}
.ak-footer::before {
  content:'';
  position:absolute;
  top:-1px;
  left:50%;
  transform:translateX(-50%);
  width:200px;height:1px;
  background:linear-gradient(90deg,transparent,var(--accent),var(--cyan),transparent);
  opacity:.5;
}
.ak-footer b { color:var(--cyan); }

.breach-alert {
  background:rgba(255,45,107,.06);
  border:1px solid rgba(255,45,107,.25);
  border-left:3px solid var(--red);
  padding:1.2rem 1.6rem;
  margin-bottom:1rem;
}

.stButton>button {
  background:var(--s2)!important;
  color:var(--cyan)!important;
  font-weight:600!important;
  border:1px solid rgba(0,229,255,.25)!important;
  border-radius:2px!important;
  font-family:'Orbitron',monospace!important;
  letter-spacing:1.5px!important;
  white-space:nowrap!important;
  text-transform:uppercase!important;
  font-size:.62rem!important;
  transition:all .2s!important;
}
.stButton>button:hover {
  background:rgba(124,58,237,.15)!important;
  border-color:var(--accent)!important;
  color:var(--text)!important;
  box-shadow:0 0 20px rgba(124,58,237,.2)!important;
}
.stButton>button p { color:var(--cyan)!important; }
.stButton>button[kind="primary"],
.stButton>button[data-testid*="primary"] {
  background:linear-gradient(135deg,var(--accent),var(--accent2))!important;
  color:#fff!important;
  border-color:transparent!important;
  box-shadow:0 0 20px rgba(124,58,237,.3)!important;
}
.stButton>button[kind="primary"] p { color:#fff!important; }
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background:var(--s1)!important;
  border:1px solid var(--border)!important;
  border-radius:2px!important;
  padding:3px!important;
  gap:3px!important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] { color:var(--dim)!important;font-family:'Orbitron',monospace!important;font-size:.55rem!important;letter-spacing:1.5px!important; }
div[data-testid="stTabs"] [aria-selected="true"] { background:rgba(124,58,237,.15)!important;color:var(--cyan)!important;border-radius:2px!important;border:1px solid rgba(0,229,255,.2)!important; }
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
  font-family:'Exo 2',sans-serif!important;
}
.stSelectbox>div>div:focus-within,
.stNumberInput>div>div>input:focus,
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus {
  border-color:rgba(124,58,237,.5)!important;
  box-shadow:0 0 15px rgba(124,58,237,.15)!important;
}
label[data-testid="stWidgetLabel"] { color:var(--dim)!important;font-size:.55rem!important;letter-spacing:2px!important;text-transform:uppercase!important;font-family:'Share Tech Mono',monospace!important; }
div[data-testid="stVerticalBlock"],div[data-testid="stHorizontalBlock"],
div[data-testid="column"],div[data-testid="stMarkdownContainer"],
div.element-container,div.stMarkdown { background:transparent!important; }
.stSlider [data-baseweb="slider"] [data-testid="stSliderThumb"] { background:var(--accent)!important; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────
LOGO_URL     = "https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.PNG"
IG_HANDLE    = "@akfunded"
IG_URL       = "https://www.instagram.com/akfunded"
PLATFORM_URL = "https://akfunded.streamlit.app"

SYMBOLS = {
    "Forex Majors":  ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCHF","NZDUSD","USDCAD"],
    "Forex Minors":  ["EURGBP","EURJPY","GBPJPY","AUDCAD","CADJPY","EURNZD"],
    "Metals":        ["XAUUSD","XAGUSD"],
    "Commodities":   ["USOIL","UKOIL","NATGAS"],
}
TV_SYMBOL_MAP = {
    "XAUUSD":"TVC:GOLD","XAGUSD":"TVC:SILVER",
    "USOIL":"TVC:USOIL","UKOIL":"TVC:UKOIL","NATGAS":"TVC:NATURALGAS",
    "EURUSD":"FX:EURUSD","GBPUSD":"FX:GBPUSD","USDJPY":"FX:USDJPY",
    "AUDUSD":"FX:AUDUSD","USDCHF":"FX:USDCHF","NZDUSD":"FX:NZDUSD","USDCAD":"FX:USDCAD",
    "EURGBP":"FX:EURGBP","EURJPY":"FX:EURJPY","GBPJPY":"FX:GBPJPY",
    "AUDCAD":"FX:AUDCAD","CADJPY":"FX:CADJPY","EURNZD":"FX:EURNZD",
}

MARKET_DATA = {
    "XAUUSD": {"price":2345.80,"change":+0.42,"vol":"High","name":"Gold / USD"},
    "XAGUSD": {"price":29.15,  "change":-0.18,"vol":"Medium","name":"Silver / USD"},
    "EURUSD": {"price":1.0842, "change":-0.12,"vol":"High","name":"Euro / USD"},
    "GBPUSD": {"price":1.2680, "change":+0.08,"vol":"High","name":"GBP / USD"},
    "USDJPY": {"price":151.42, "change":+0.31,"vol":"High","name":"USD / JPY"},
    "AUDUSD": {"price":0.6540, "change":-0.22,"vol":"Medium","name":"AUD / USD"},
    "USDCHF": {"price":0.8921, "change":+0.05,"vol":"Medium","name":"USD / CHF"},
    "USOIL":  {"price":82.45,  "change":+1.20,"vol":"High","name":"WTI Crude Oil"},
    "UKOIL":  {"price":87.30,  "change":+0.95,"vol":"High","name":"Brent Crude"},
    "NATGAS": {"price":2.18,   "change":-0.85,"vol":"Medium","name":"Natural Gas"},
    "NZDUSD": {"price":0.6015, "change":-0.15,"vol":"Low","name":"NZD / USD"},
    "USDCAD": {"price":1.3620, "change":+0.10,"vol":"Medium","name":"USD / CAD"},
}

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
for k, v in [
    ("user",None),("page","home"),("notifications",[]),
    ("chat_history",[]),("watchlist",["XAUUSD","EURUSD","GBPUSD","USOIL"]),
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
    return send_email_html(to_email, "AKFunded — Account Breached", html)

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

def get_simulated_price(symbol):
    base_price = MARKET_DATA.get(symbol,{}).get("price",1.0)
    return round(base_price * (1 + random.uniform(-0.002, 0.002)), 5 if base_price < 10 else 2)

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
        f'border:1px solid {accent_bord};font-family:Orbitron,monospace;'
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
        '<div style="font-family:\'Orbitron\',monospace;font-size:1.5rem;letter-spacing:6px;color:#00D4FF;line-height:1;">AKFUNDED</div>'
        '<div style="font-size:0.48rem;color:#3a6a5a;letter-spacing:3px;text-transform:uppercase;">Prop Trading Platform</div>'
        '</div></div>'

        f'<div style="display:flex;align-items:center;gap:14px;width:100%;margin-bottom:14px;">'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,{accent_bord});"></div>'
        f'<div style="width:5px;height:5px;background:{accent};border-radius:50%;box-shadow:0 0 8px {accent};flex-shrink:0;"></div>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,{accent_bord},transparent);"></div>'
        '</div>'

        '<div style="font-size:0.52rem;color:#3a6a4a;letter-spacing:4px;text-transform:uppercase;margin-bottom:6px;font-weight:600;">OFFICIAL CERTIFICATE</div>'
        f'<div style="font-family:\'Orbitron\',monospace;font-size:3.6rem;letter-spacing:10px;color:{accent};line-height:1;margin-bottom:1px;text-shadow:0 0 40px {accent_glow};">CERTIFICATE</div>'
        '<div style="font-size:0.8rem;letter-spacing:8px;color:#2a5a3a;margin-bottom:10px;font-weight:700;text-transform:uppercase;">OF RECOGNITION</div>'

        f'<div style="display:flex;align-items:center;gap:14px;width:100%;margin-bottom:10px;">'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,{accent_bord});"></div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:3px;text-transform:uppercase;white-space:nowrap;">This certificate is proudly presented to</div>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,{accent_bord},transparent);"></div>'
        '</div>'

        '<div style="text-align:center;margin-bottom:6px;">'
        f'<div style="font-family:\'Orbitron\',monospace;font-size:2.9rem;color:#EFEFEF;line-height:1.1;letter-spacing:6px;">{name.upper()}</div>'
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
        f'<div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;letter-spacing:2px;color:{accent};line-height:1;margin-bottom:3px;">+{pnl_pct:.2f}%</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Profit Achieved</div>'
        '</div>'
        f'<div style="padding:12px 16px;border-right:1px solid {accent_bord};text-align:center;">'
        f'<div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;letter-spacing:2px;color:#D4A843;line-height:1;margin-bottom:3px;">{days}</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Trading Days</div>'
        '</div>'
        f'<div style="padding:12px 16px;text-align:center;">'
        f'<div style="font-family:\'Orbitron\',monospace;font-size:1.45rem;letter-spacing:2px;color:#D8D8D8;line-height:1;margin-bottom:3px;">{date_str}</div>'
        '<div style="font-size:0.48rem;color:#3a6a4a;letter-spacing:2.5px;text-transform:uppercase;">Date Issued</div>'
        '</div>'
        '</div>'
        '</div>'

        f'<div style="position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;padding:16px 90px 26px;border-top:1px solid {accent_bord};">'
        '<div style="text-align:center;">'
        f'<div style="font-family:\'Alex Brush\',cursive;font-size:2.4rem;color:{accent};line-height:1.1;letter-spacing:1px;">Akash Injeti</div>'
        f'<div style="width:130px;height:1px;background:{accent_bord};margin:5px auto;"></div>'
        '<div style="font-size:0.5rem;color:#3a6a4a;letter-spacing:1.5px;text-transform:uppercase;">Akash Injeti</div>'
        '<div style="font-size:0.48rem;color:#2a5a3a;letter-spacing:1px;text-transform:uppercase;">Founder, AKFunded</div>'
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
            <p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:22px;
              color:#00B87A;">Akash Injeti</p>
            <table cellpadding="0" cellspacing="0" border="0">
              <tr><td width="140" height="1"
                style="background:#1a3a1a;font-size:1px;line-height:1px;padding-top:6px;">&nbsp;</td></tr>
            </table>
            <p style="margin:6px 0 2px;font-family:Arial,Helvetica,sans-serif;font-size:7px;
              color:#3a6a4a;letter-spacing:1.5px;text-transform:uppercase;">AKASH INJETI</p>
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
    st.rerun()

# ─── UI HELPERS ────────────────────────────────────────────────
def nav():
    logged_in = st.session_state.user is not None
    st.markdown(
        '<div class="ak-nav">'
        f'<div style="display:flex;align-items:center;gap:14px;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\'none\'" style="height:34px;width:34px;object-fit:contain;filter:drop-shadow(0 0 10px rgba(124,58,237,.5));" />'
        '<div>'
        '<div class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span><span class="ak-beta">BETA</span></div>'
        '<div class="ak-tagline">// PROVE YOUR EDGE — GET FUNDED</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )
    if logged_in:
        is_admin = st.session_state.user.get("email","") == st.secrets.get("ADMIN_EMAIL","admin@akfunded.com")
        if is_admin:
            c0,c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns([1.2,.8,.8,.8,.8,.8,1,.7,.7,.4])
            with c7:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("Alerts"+(f" ({unread})" if unread else ""),key="nb"): goto("notifications")
            with c8:
                if st.button("Admin",key="na"): goto("admin")
            with c9:
                if st.button("Me",key="npr"): goto("profile")
        else:
            c0,c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1.2,.8,.8,.8,.8,.8,1,.7,.4])
            with c7:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("Alerts"+(f" ({unread})" if unread else ""),key="nb"): goto("notifications")
            with c8:
                if st.button("Me",key="npr"): goto("profile")
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
        f'<div style="display:flex;align-items:center;justify-content:center;gap:1.5rem;margin-bottom:1rem;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\'none\'" style="height:20px;width:20px;object-fit:contain;opacity:.4;" />'
        '<span style="font-size:.72rem;letter-spacing:4px;color:#1e1e1e;font-weight:700;">AKFUNDED</span>'
        '<span style="color:#1e1e1e;">|</span>'
        f'<a href="{IG_URL}" target="_blank" style="color:#2a2a2a;text-decoration:none;font-size:.68rem;letter-spacing:1.5px;">Instagram: <b style="color:#3a3a3a;">{IG_HANDLE}</b></a>'
        '</div>'
        '<div style="color:#1e1e1e;">Built by <b>Akash Injeti</b> &nbsp;&middot;&nbsp; Simulate. Prove. Get Funded. &nbsp;&middot;&nbsp; All accounts are simulated.</div>'
        '</div>',
        unsafe_allow_html=True
    )

def sec(title, sub=""):
    sub_html = f'<div style="color:var(--dim);font-size:.78rem;margin-top:.4rem;letter-spacing:.5px;font-weight:300;">{sub}</div>' if sub else ""
    st.markdown(
        '<div style="margin-bottom:1.5rem;">'
        f'<div style="font-family:\'Orbitron\',monospace;font-size:1.3rem;letter-spacing:4px;color:var(--text);line-height:1;font-weight:700;">{title}</div>'
        f'{sub_html}'
        '<div style="width:40px;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));margin-top:.6rem;box-shadow:0 0 8px rgba(124,58,237,.5);"></div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_live_ticker():
    items = ""
    for sym, data in MARKET_DATA.items():
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
    for sym, data in MARKET_DATA.items():
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
            f'<div style="font-size:.65rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;margin-top:2px;">RSI {rsi} &nbsp;|&nbsp; Vol: {vol}</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div class="scan-signal {cls}">{sig}</div>'
            f'<div style="font-size:.68rem;color:{col};font-family:\'Share Tech Mono\',monospace;margin-top:4px;">{sign}{chg:.2f}%</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

def pbar(pct, col):
    return f'<div class="prog"><div class="prog-fill" style="width:{pct:.1f}%;background:{col};box-shadow:0 0 4px {col};"></div></div>'

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    # ─── FULL-SCREEN 3D GLOBE INTRO ────────────────────────────
    st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:#02030a;overflow:hidden;font-family:'Orbitron',monospace;}
  #intro{
    position:fixed;top:0;left:0;width:100vw;height:100vh;
    background:#02030a;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    z-index:9999;
    transition:opacity 1s ease;
  }
  #intro.fade-out{opacity:0;pointer-events:none;}
  canvas{display:block;}
  #globe-wrap{
    position:relative;width:420px;height:420px;
    margin-bottom:2.5rem;
  }
  #globe-canvas{
    border-radius:50%;
    box-shadow:0 0 80px rgba(124,58,237,.4),0 0 160px rgba(0,229,255,.15);
  }
  .ring{
    position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
    border-radius:50%;
    border:1px solid rgba(0,229,255,.15);
    animation:pulse-ring 3s infinite ease-out;
  }
  .ring:nth-child(1){width:480px;height:480px;animation-delay:0s;}
  .ring:nth-child(2){width:540px;height:540px;animation-delay:.8s;}
  .ring:nth-child(3){width:600px;height:600px;animation-delay:1.6s;}
  @keyframes pulse-ring{
    0%{opacity:.4;transform:translate(-50%,-50%) scale(.9);}
    100%{opacity:0;transform:translate(-50%,-50%) scale(1.1);}
  }
  #tagline{
    text-align:center;
    animation:reveal 1.2s ease 0.3s both;
  }
  @keyframes reveal{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
  #top-line{
    font-size:.65rem;letter-spacing:8px;text-transform:uppercase;
    color:rgba(0,229,255,.5);margin-bottom:1rem;
    font-family:'Share Tech Mono',monospace;
  }
  #main-line{
    font-size:clamp(1.8rem,4vw,3.5rem);
    font-weight:900;
    letter-spacing:3px;
    line-height:1.1;
    background:linear-gradient(135deg,#fff 0%,#c8d4f0 40%,#00e5ff 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    margin-bottom:.6rem;
  }
  #sub-line{
    font-size:.75rem;
    color:rgba(124,58,237,.8);
    letter-spacing:4px;
    text-transform:uppercase;
    font-family:'Share Tech Mono',monospace;
  }
  #enter-btn{
    margin-top:2.5rem;
    padding:1rem 3rem;
    background:transparent;
    border:1px solid rgba(0,229,255,.4);
    color:#00e5ff;
    font-family:'Orbitron',monospace;
    font-size:.7rem;
    letter-spacing:4px;
    text-transform:uppercase;
    cursor:pointer;
    position:relative;
    overflow:hidden;
    transition:all .3s;
    animation:reveal 1s ease 1.8s both;
  }
  #enter-btn::before{
    content:'';position:absolute;inset:0;
    background:linear-gradient(135deg,rgba(124,58,237,.2),rgba(0,229,255,.1));
    opacity:0;transition:opacity .3s;
  }
  #enter-btn:hover{
    border-color:var(--c,#00e5ff);
    box-shadow:0 0 30px rgba(0,229,255,.3),inset 0 0 30px rgba(124,58,237,.1);
    transform:translateY(-2px);
  }
  #enter-btn:hover::before{opacity:1;}
  #particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;}
  #globe-wrap{z-index:2;}
  #tagline{z-index:2;}
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap');
</style>
</head>
<body>
<div id="intro">
  <canvas id="particles" width="0" height="0"></canvas>
  <div id="globe-wrap">
    <div class="ring"></div><div class="ring"></div><div class="ring"></div>
    <canvas id="globe-canvas" width="420" height="420"></canvas>
  </div>
  <div id="tagline">
    <div id="top-line">// AKFUNDED TERMINAL v1.0</div>
    <div id="main-line">WELCOME TO<br>THE REAL WORLD</div>
    <div id="sub-line">TRADE OUR CAPITAL &nbsp;&bull;&nbsp; KEEP YOUR PROFITS</div>
    <button id="enter-btn" onclick="enterPlatform()">ENTER THE MATRIX &nbsp;&#x25B6;</button>
  </div>
</div>

<script>
// ── PARTICLE CANVAS ──────────────────────────────────────────
const pc = document.getElementById('particles');
pc.width = window.innerWidth; pc.height = window.innerHeight;
const px = pc.getContext('2d');
const particles = Array.from({length:80},()=>({
  x:Math.random()*pc.width, y:Math.random()*pc.height,
  vx:(Math.random()-.5)*.3, vy:(Math.random()-.5)*.3,
  r:Math.random()*1.5+.5,
  c:`rgba(${Math.random()>.5?'0,229,255':'124,58,237'},${Math.random()*.4+.1})`
}));
function animParticles(){
  px.clearRect(0,0,pc.width,pc.height);
  particles.forEach(p=>{
    p.x+=p.vx; p.y+=p.vy;
    if(p.x<0||p.x>pc.width) p.vx*=-1;
    if(p.y<0||p.y>pc.height) p.vy*=-1;
    px.beginPath(); px.arc(p.x,p.y,p.r,0,Math.PI*2);
    px.fillStyle=p.c; px.fill();
  });
  requestAnimationFrame(animParticles);
}
animParticles();

// ── 3D GLOBE ──────────────────────────────────────────────────
const gc = document.getElementById('globe-canvas');
const g = gc.getContext('2d');
const W=420, R=200, CX=W/2, CY=W/2;
let rot=0;
const DOTS = [];
// Generate dots on sphere using Fibonacci lattice
const N=600;
const golden = Math.PI*(3-Math.sqrt(5));
for(let i=0;i<N;i++){
  const y2 = 1-(i/(N-1))*2;
  const radius = Math.sqrt(1-y2*y2);
  const theta = golden*i;
  const x2=Math.cos(theta)*radius, z2=Math.sin(theta)*radius;
  DOTS.push([x2,y2,z2]);
}
// Lat/lon lines
const LINES=[];
for(let lat=-80;lat<=80;lat+=20){
  const r2=Math.cos(lat*Math.PI/180);
  const y2=Math.sin(lat*Math.PI/180);
  const pts=[];
  for(let lon=0;lon<=360;lon+=4){
    pts.push([r2*Math.cos(lon*Math.PI/180),y2,r2*Math.sin(lon*Math.PI/180)]);
  }
  LINES.push(pts);
}
for(let lon=0;lon<360;lon+=30){
  const pts=[];
  for(let lat=-90;lat<=90;lat+=3){
    const r2=Math.cos(lat*Math.PI/180);
    const y2=Math.sin(lat*Math.PI/180);
    pts.push([r2*Math.cos(lon*Math.PI/180),y2,r2*Math.sin(lon*Math.PI/180)]);
  }
  LINES.push(pts);
}

function proj(x,y,z,rx,ry){
  // rotate Y
  const cosY=Math.cos(ry), sinY=Math.sin(ry);
  const x2=x*cosY+z*sinY, z2=-x*sinY+z*cosY;
  // rotate X
  const cosX=Math.cos(rx), sinX=Math.sin(rx);
  const y3=y*cosX-z2*sinX, z3=y*sinX+z2*cosX;
  return {sx:CX+x2*R, sy:CY+y3*R, z:z3};
}

function drawGlobe(){
  g.clearRect(0,0,W,W);
  // Background glow
  const grd=g.createRadialGradient(CX,CY,0,CX,CY,R);
  grd.addColorStop(0,'rgba(124,58,237,.08)');
  grd.addColorStop(.5,'rgba(37,99,235,.04)');
  grd.addColorStop(1,'transparent');
  g.beginPath(); g.arc(CX,CY,R,0,Math.PI*2);
  g.fillStyle=grd; g.fill();

  const rx=0.25, ry=rot;

  // Draw grid lines
  LINES.forEach(pts=>{
    let first=true;
    g.beginPath();
    pts.forEach(([x,y,z])=>{
      const {sx,sy,z:pz}=proj(x,y,z,rx,ry);
      if(pz<0){first=true;return;}
      if(first){g.moveTo(sx,sy);first=false;}
      else g.lineTo(sx,sy);
    });
    g.strokeStyle='rgba(0,229,255,.06)'; g.lineWidth=.5; g.stroke();
  });

  // Draw dots
  const front=[],back=[];
  DOTS.forEach(([x,y,z])=>{
    const {sx,sy,z:pz}=proj(x,y,z,rx,ry);
    (pz>=0?front:back).push({sx,sy,pz});
  });
  back.forEach(({sx,sy})=>{
    g.beginPath(); g.arc(sx,sy,1,0,Math.PI*2);
    g.fillStyle='rgba(124,58,237,.12)'; g.fill();
  });
  front.forEach(({sx,sy,pz})=>{
    const br=Math.pow(pz,1.5);
    g.beginPath(); g.arc(sx,sy,1.4,0,Math.PI*2);
    g.fillStyle=`rgba(0,229,255,${0.15+br*.55})`; g.fill();
  });

  // Globe rim glow
  const rim=g.createRadialGradient(CX,CY,R*.75,CX,CY,R);
  rim.addColorStop(0,'transparent');
  rim.addColorStop(.8,'rgba(0,229,255,.04)');
  rim.addColorStop(1,'rgba(0,229,255,.18)');
  g.beginPath(); g.arc(CX,CY,R,0,Math.PI*2);
  g.fillStyle=rim; g.fill();

  rot+=0.004;
  requestAnimationFrame(drawGlobe);
}
drawGlobe();

// ── ENTER ──────────────────────────────────────────────────────
function enterPlatform(){
  const intro=document.getElementById('intro');
  intro.style.transition='opacity .8s ease';
  intro.style.opacity='0';
  setTimeout(()=>{ intro.style.display='none'; window.parent.postMessage({type:'akfunded_enter'},'*'); },800);
}
// Auto-enter after 8 seconds if user doesn't click
setTimeout(enterPlatform, 8000);
</script>
</body>
</html>
""", height=700, scrolling=False)

    # After globe intro, show dashboard link to skip
    _,cc,_ = st.columns([2,1.5,2])
    with cc:
        if st.button("⚡  Skip Intro — Enter Platform", use_container_width=True, key="skip_intro"):
            if st.session_state.user:
                goto("dashboard")
            else:
                goto("auth")

    st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
    nav()
    render_live_ticker()

    st.markdown(
        '<div class="hero-v2">'
        f'<div style="margin-bottom:1.5rem;">'
        f'<img src="{LOGO_URL}" onerror="this.style.display=\'none\'" style="height:56px;width:56px;object-fit:contain;filter:drop-shadow(0 0 20px rgba(124,58,237,.6));" />'
        f'</div>'
        '<div class="eyebrow"><span class="eyebrow-dot"></span> Forex &nbsp;&bull;&nbsp; Metals &nbsp;&bull;&nbsp; Commodities &nbsp;&bull;&nbsp; Prop Trading</div>'
        '<h1>TRADE OUR<br><em>CAPITAL.</em></h1>'
        '<p class="sub">Pass the evaluation. Get funded up to $100,000.<br>Keep up to 90% of your profits. Trade XAUUSD, Forex &amp; Crude Oil.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("ENTER CHALLENGE", use_container_width=True): goto("plans")

    st.markdown(
        '<div class="hstats" style="margin-top:2rem;">'
        '<div class="hstat"><span class="n">$2M+</span><span class="l">Total Payouts</span></div>'
        '<div class="hstat"><span class="n">3,500+</span><span class="l">Funded Traders</span></div>'
        '<div class="hstat"><span class="n">180+</span><span class="l">Countries</span></div>'
        '<div class="hstat"><span class="n">90%</span><span class="l">Profit Split</span></div>'
        '<div class="hstat"><span class="n">24hr</span><span class="l">Payouts</span></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(f'<div style="font-family:\'Orbitron\',monospace;font-size:.85rem;letter-spacing:4px;color:var(--text);margin:3rem 0 .5rem;font-weight:700;">// LIVE INSTRUMENTS</div><div style="width:30px;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));margin-bottom:1.5rem;box-shadow:0 0 8px rgba(124,58,237,.5);"></div>', unsafe_allow_html=True)
    render_market_heatmap()

    st.markdown(f'<div style="font-family:\'Orbitron\',monospace;font-size:.85rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;font-weight:700;">// CHOOSE YOUR PROGRAM</div><div style="width:30px;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));margin-bottom:1.5rem;box-shadow:0 0 8px rgba(124,58,237,.5);"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.markdown(
            '<div style="background:linear-gradient(135deg,rgba(255,182,39,.06),rgba(255,182,39,.02));border:1px solid rgba(255,182,39,.25);padding:2rem;position:relative;overflow:hidden;">'
            '<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--gold),transparent);opacity:.5;"></div>'
            '<div style="position:absolute;top:.7rem;right:.7rem;background:var(--gold);color:#000;font-size:.45rem;font-weight:700;padding:2px 8px;letter-spacing:2px;font-family:\'Orbitron\',monospace;">INSTANT</div>'
            '<div style="font-size:.5rem;color:var(--gold);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;font-family:\'Orbitron\',monospace;">INSTANT FUNDED</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(255,182,39,.08);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Daily Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">3%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Max Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">6%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Challenge</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--green);font-weight:700;">NONE</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Profit Split</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--gold);font-weight:700;">70-75%</div></div>'
            '</div>'
            '<div style="font-size:.55rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;font-family:\'Share Tech Mono\',monospace;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Orbitron\',monospace;font-size:2rem;color:var(--gold);letter-spacing:2px;font-weight:700;">$299</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get Instant Funded", use_container_width=True, key="h_inst"):
            st.session_state["selected_phase"] = "instant"; goto("plans")

    with col2:
        st.markdown(
            '<div style="background:rgba(0,229,255,.04);border:1px solid rgba(0,229,255,.2);padding:2rem;position:relative;overflow:hidden;">'
            '<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--cyan),transparent);opacity:.5;"></div>'
            '<div style="font-size:.5rem;color:var(--cyan);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;font-family:\'Orbitron\',monospace;">ONE-STEP</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Profit Target</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--green);font-weight:700;">8%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Max Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">10%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Daily Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">5%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Profit Split</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--cyan);font-weight:700;">80%</div></div>'
            '</div>'
            '<div style="font-size:.55rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;font-family:\'Share Tech Mono\',monospace;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Orbitron\',monospace;font-size:2rem;color:var(--text);letter-spacing:2px;font-weight:700;">$79</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get One-Step", use_container_width=True, key="h_1p"):
            st.session_state["selected_phase"] = "one"; goto("plans")

    with col3:
        st.markdown(
            '<div style="background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.25);padding:2rem;position:relative;overflow:hidden;">'
            '<div style="position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));opacity:.4;"></div>'
            '<div style="position:absolute;top:.7rem;right:.7rem;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;font-size:.45rem;font-weight:700;padding:2px 8px;letter-spacing:2px;font-family:\'Orbitron\',monospace;">BEST VALUE</div>'
            '<div style="font-size:.5rem;color:var(--purple);letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem;font-family:\'Orbitron\',monospace;">TWO-STEP</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--border);margin-bottom:1.5rem;">'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Phase 1</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--green);font-weight:700;">8%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Max Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">10%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Daily Loss</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--red);font-weight:700;">5%</div></div>'
            '<div style="background:var(--s2);padding:.8rem;"><div style="font-size:.45rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;font-family:\'Share Tech Mono\',monospace;">Profit Split</div><div style="font-family:\'Orbitron\',monospace;font-size:1.2rem;color:var(--purple);font-weight:700;">90%</div></div>'
            '</div>'
            '<div style="font-size:.55rem;color:var(--dim);margin-bottom:.3rem;letter-spacing:1px;font-family:\'Share Tech Mono\',monospace;">ONE-TIME FEE FROM</div>'
            '<div style="font-family:\'Orbitron\',monospace;font-size:2rem;color:var(--text);letter-spacing:2px;font-weight:700;">$49</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Get Two-Step", use_container_width=True, key="h_2p"):
            st.session_state["selected_phase"] = "two"; goto("plans")

    st.markdown(f'<div style="font-family:\'Orbitron\',monospace;font-size:.85rem;letter-spacing:4px;color:var(--text);margin:3.5rem 0 .5rem;font-weight:700;">// HOW IT WORKS</div><div style="width:30px;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));margin-bottom:1.5rem;box-shadow:0 0 8px rgba(124,58,237,.5);"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="steps-grid">'
        '<div class="step-card"><div class="step-num">01</div><div class="step-title">Choose a Plan</div><div class="step-desc">Instant Funded, One-Step, or Two-Step. Accounts from $5K to $100K.</div></div>'
        '<div class="step-card"><div class="step-num">02</div><div class="step-title">Pass the Evaluation</div><div class="step-desc">Hit the profit target while respecting strict drawdown rules.</div></div>'
        '<div class="step-card"><div class="step-num">03</div><div class="step-title">Get Funded</div><div class="step-desc">Complete verification and receive your funded account. 24-hour payouts.</div></div>'
        '<div class="step-card"><div class="step-num">04</div><div class="step-title">Scale Up</div><div class="step-desc">Keep up to 90% of profits. Scale to $2,000,000 with consistent performance.</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(f'<div style="font-family:\'Orbitron\',monospace;font-size:.85rem;letter-spacing:4px;color:var(--text);margin:2.5rem 0 .5rem;font-weight:700;">// FUNDED TRADERS</div><div style="width:30px;height:1px;background:linear-gradient(90deg,var(--accent),var(--cyan));margin-bottom:1.5rem;box-shadow:0 0 8px rgba(124,58,237,.5);"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="testi-grid">'
        '<div class="testi-card"><div class="testi-quote">Passed the $50K One-Step on XAUUSD in 4 days. The rules are clear and the platform is rock solid.</div><div class="testi-name">Rahul S.</div><div class="testi-meta">$50K Funded &nbsp;|&nbsp; +$4,000 payout &nbsp;|&nbsp; One-Step</div></div>'
        '<div class="testi-card"><div class="testi-quote">Two-Step gave me 90% profit split at an affordable entry. Already on my third funded account.</div><div class="testi-name">Priya M.</div><div class="testi-meta">$25K Funded &nbsp;|&nbsp; +$2,250 payout &nbsp;|&nbsp; Two-Step</div></div>'
        '<div class="testi-card"><div class="testi-quote">Instant Funded is worth every rupee. Got funded same day and started trading USOIL immediately.</div><div class="testi-name">Kiran T.</div><div class="testi-meta">$25K Instant Funded &nbsp;|&nbsp; 3 accounts completed</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("LAUNCH NOW", use_container_width=True, key="cta2"): goto("plans")
    st.markdown("</div>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "auth":
    nav()
    st.markdown("<br>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.2,1])
    with col:
        st.markdown('<div style="font-family:\'Orbitron\',monospace;font-size:1.5rem;letter-spacing:4px;color:var(--text);margin-bottom:.3rem;">ACCESS AKFUNDED</div><div style="width:30px;height:1px;background:var(--cyan);margin-bottom:1.5rem;opacity:.5;"></div>', unsafe_allow_html=True)
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
        '<b style="color:var(--cyan);">TESTING PHASE</b> — All challenges activate instantly. No payment required. Trade Forex, XAUUSD, XAGUSD, Crude Oil &amp; Natural Gas.'
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
                f'<li><span>Markets</span><b>Forex, XAU, Oil</b></li>'
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
            f'<div style="font-family:\'Orbitron\',monospace;font-size:2.6rem;color:{accent};letter-spacing:2px;line-height:1;margin-bottom:1.2rem;">{plan["name"]}</div>'
            f'<ul class="plan-rules">{rules_html}</ul>'
            f'<div style="border-top:1px solid var(--border);padding-top:.8rem;">'
            f'<div style="font-size:.62rem;color:var(--dim);text-decoration:line-through;letter-spacing:1px;">${plan["price"]} value</div>'
            f'<div style="font-family:\'Orbitron\',monospace;font-size:1.6rem;color:var(--green);letter-spacing:2px;">FREE <span style="font-size:.8rem;color:var(--dim);font-family:\'Exo 2\',sans-serif;">testing</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
        if st.button(f"Activate {plan['name']}", key=f"buy_{plan['slug']}", use_container_width=True):
            uid = st.session_state.user["id"]
            existing = db_get_active_challenge(uid)
            if existing:
                st.warning("You already have an active challenge. Complete or view it in your dashboard.")
            else:
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

    st.markdown('<br><div style="font-family:\'Orbitron\',monospace;font-size:1rem;letter-spacing:3px;color:var(--dim);margin-bottom:1rem;">PROGRAM COMPARISON</div>', unsafe_allow_html=True)
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
        ("Markets","Forex, XAU, Oil","Forex, XAU, Oil","Forex, XAU, Oil"),
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

    challenge = db_get_active_challenge(uid)
    account   = db_get_account(challenge["id"]) if challenge else None

    if not challenge or not account:
        st.markdown(
            f'<div style="text-align:center;padding:6rem 2rem;">'
            f'<div style="font-family:\'Orbitron\',monospace;font-size:2.5rem;letter-spacing:5px;color:var(--text);">Welcome, {name.upper()}</div>'
            f'<div style="font-size:.85rem;color:var(--dim);margin:.5rem 0 2rem;font-weight:300;letter-spacing:.5px;">No active challenge. Activate one to start trading.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("Activate Challenge", use_container_width=True): goto("plans")
        footer(); st.stop()

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

    st.markdown(
        f'<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1.5rem;">'
        f'<div><div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;letter-spacing:4px;color:var(--text);line-height:1;">Trading Dashboard</div>'
        f'<div style="font-size:.72rem;color:var(--dim);margin-top:.3rem;letter-spacing:.5px;">{name} &nbsp;|&nbsp; {challenge["plan"].upper()} &nbsp;|&nbsp; Day {days}</div>'
        f'<div style="width:30px;height:1px;background:var(--cyan);margin-top:.6rem;opacity:.5;"></div></div>'
        f'<div style="display:flex;gap:.5rem;align-items:center;">'
        f'<div style="border:1px solid rgba(0,212,255,.2);padding:4px 14px;font-size:.58rem;color:var(--cyan);letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">{phase_badge}</div>'
        f'<div style="border:1px solid rgba(0,184,122,.2);padding:4px 14px;font-size:.58rem;color:var(--green);letter-spacing:2.5px;text-transform:uppercase;font-weight:700;">&#x25CF; ACTIVE</div>'
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

    col_chart, col_trade = st.columns([2,1], gap="medium")
    with col_chart:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Live Chart — TradingView</div>', unsafe_allow_html=True)
        mkt      = st.selectbox("Market", list(SYMBOLS.keys()), key="mkt")
        sym_list = SYMBOLS[mkt]
        sym_pick = st.selectbox("Symbol", sym_list, key="csym")
        tv_sym   = TV_SYMBOL_MAP.get(sym_pick, f"FX:{sym_pick}")
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
        t_sym   = st.selectbox("Symbol", [s for g in SYMBOLS.values() for s in g], key="tsym")
        live_px = get_simulated_price(t_sym)
        t_dir   = st.selectbox("Direction", ["BUY","SELL"], key="ttype")
        decimal = 5 if MARKET_DATA.get(t_sym,{}).get("price",1) < 10 else 2
        t_entry = st.number_input("Entry Price", min_value=0.00001, value=float(live_px), format=f"%.{decimal}f", key="tentry")
        t_qty   = st.number_input("Lot Size / Units", min_value=0.01, value=0.10, step=0.01, format="%.2f", key="tqty")
        t_exit  = st.number_input("Exit Price", min_value=0.00001, value=float(round(live_px*1.015,decimal)), format=f"%.{decimal}f", key="texit")
        t_sl    = st.number_input("Stop Loss", min_value=0.00001, value=float(round(live_px*0.985,decimal)), format=f"%.{decimal}f", key="tsl")

        lot_mult   = 100000 if MARKET_DATA.get(t_sym,{}).get("price",1) < 100 else 1
        est        = (t_exit-t_entry)*t_qty*lot_mult if t_dir=="BUY" else (t_entry-t_exit)*t_qty*lot_mult
        risk_trade = abs(t_entry-t_sl)*t_qty*lot_mult
        ec         = "var(--green)" if est>=0 else "var(--red)"
        es         = "+" if est>=0 else ""
        roi        = (est/initial)*100 if initial>0 else 0
        rr         = abs(est)/risk_trade if risk_trade>0 else 0

        st.markdown(
            f'<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid {ec};padding:1rem;margin:.8rem 0;">'
            f'<div style="font-size:.55rem;color:var(--dim);letter-spacing:2.5px;margin-bottom:4px;text-transform:uppercase;">Estimated P&L</div>'
            f'<div style="font-family:\'Orbitron\',monospace;font-size:2.2rem;color:{ec};letter-spacing:2px;line-height:1;">{es}${est:,.2f}</div>'
            f'<div style="font-size:.68rem;color:{ec};margin-top:4px;font-family:\'Share Tech Mono\',monospace;">{es}{roi:.3f}% acct &nbsp;|&nbsp; R:R 1:{rr:.1f}</div>'
            f'<div style="font-size:.65rem;color:var(--red);margin-top:4px;font-family:\'Share Tech Mono\',monospace;">Risk: ${risk_trade:,.2f}</div>'
            f'</div>'
            f'<div style="background:var(--s2);border:1px solid var(--border);padding:.6rem 1rem;margin-bottom:.8rem;display:flex;justify-content:space-between;align-items:center;">'
            f'<div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;">Live Price</div>'
            f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:1rem;color:var(--cyan);">{live_px:.{decimal}f}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        if st.button("Execute Trade", use_container_width=True, key="exec"):
            ch_id   = challenge["id"]
            new_bal = balance + est
            new_tl  = min(0.0, new_bal-initial)
            new_days = days+1
            new_daily = float(account.get("daily_loss",0)) + (est if est < 0 else 0)
            daily_loss_pct = abs(new_daily)/initial*100 if new_daily < 0 else 0
            total_loss_pct = abs(new_tl)/initial*100 if new_tl < 0 else 0
            try:
                supabase.table("trades").insert({
                    "user_id":uid,"challenge_id":ch_id,"symbol":t_sym,"type":t_dir,
                    "entry_price":t_entry,"exit_price":t_exit,"quantity":t_qty,
                    "pnl":est,"closed_at":datetime.utcnow().isoformat()
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
                    st.balloons(); st.success("Challenge passed! Certificate available.")
                else:
                    push_notification(uid,"⚡","Trade Executed",f"{t_dir} {t_sym} — P&L: {es}${est:,.2f}")
                    if est>=0: st.success(f"Trade executed. P&L: {es}${est:,.2f}")
                    else: st.warning(f"Trade executed. P&L: ${est:,.2f}")
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
            dec = 5 if MARKET_DATA.get(sym,{}).get("price",1) < 10 else 2
            st.markdown(
                f'<div class="t-row">'
                f'<span style="font-weight:700;">{sym} <span style="font-size:.62rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;">{dt}</span></span>'
                f'{tag}'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:.72rem;">{t.get("entry_price",0):.{dec}f}</span>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;font-size:.72rem;">{t.get("exit_price",0):.{dec}f}</span>'
                f'<span style="font-family:\'Share Tech Mono\',monospace;">{t.get("quantity",0):.2f}</span>'
                f'<span style="color:{pc3};font-family:\'Share Tech Mono\',monospace;font-weight:700;">{ps3}${p:,.2f}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:2.5rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;letter-spacing:.5px;">No trades yet. Execute your first trade above.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
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
    nav()
    render_live_ticker()
    sec("Live Markets","Forex · Metals · Crude Oil — Signals, order book and watchlist")

    tab_hm, tab_sc, tab_ob, tab_wl = st.tabs(["  Heatmap  ","  Signal Scanner  ","  Order Book  ","  Watchlist  "])

    with tab_hm:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Market Heatmap</div>', unsafe_allow_html=True)
        render_market_heatmap()
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);"><div style="display:grid;grid-template-columns:1.5fr 1.2fr 1fr 1fr 1fr 1fr;padding:.8rem 1.2rem;background:var(--s2);font-size:.58rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;font-weight:600;border-bottom:1px solid var(--border);"><span>Symbol</span><span>Name</span><span>Price</span><span>Change</span><span>Volume</span><span>Signal</span></div>', unsafe_allow_html=True)
        for sym, data in MARKET_DATA.items():
            chg=data["change"]; col="var(--green)" if chg>=0 else "var(--red)"; sign="+" if chg>=0 else ""
            sig="BUY" if chg>0.5 else ("SELL" if chg<-0.5 else "HOLD")
            sc="bull" if sig=="BUY" else ("bear" if sig=="SELL" else "neut")
            dec = 5 if data["price"] < 10 else 2
            st.markdown(f'<div style="display:grid;grid-template-columns:1.5fr 1.2fr 1fr 1fr 1fr 1fr;padding:.65rem 1.2rem;border-top:1px solid var(--border);align-items:center;"><span style="font-weight:700;color:var(--text);">{sym}</span><span style="font-size:.72rem;color:var(--dim);">{data.get("name","")}</span><span style="font-family:\'Share Tech Mono\',monospace;font-size:.75rem;">{data["price"]:.{dec}f}</span><span style="color:{col};font-weight:700;font-family:\'Share Tech Mono\',monospace;font-size:.75rem;">{sign}{chg:.2f}%</span><span style="font-size:.72rem;color:var(--dim);">{data["vol"]}</span><span class="scan-signal {sc}" style="width:fit-content;">{sig}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_sc:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">Signal Scanner</div>', unsafe_allow_html=True)
        render_signal_scanner()

    with tab_ob:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;font-weight:600;">Simulated Order Book</div>', unsafe_allow_html=True)
        ob_sym = st.selectbox("Symbol", list(MARKET_DATA.keys()), key="ob_sym")
        base   = MARKET_DATA[ob_sym]["price"]
        dec    = 5 if base < 10 else 2
        col_bid, col_ask = st.columns(2)
        with col_bid:
            st.markdown('<div style="font-size:.65rem;color:var(--green);letter-spacing:2px;font-weight:700;margin-bottom:.5rem;">BIDS</div><div style="background:var(--s1);border:1px solid var(--border);"><div class="ob-row" style="color:var(--dim);font-size:.58rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);font-weight:600;"><span>Price</span><span>Size</span><span>Total</span></div>', unsafe_allow_html=True)
            for i in range(8):
                px=round(base-(i+1)*base*0.0003,dec); sz=random.randint(1,500)
                st.markdown(f'<div class="ob-row"><span class="ob-bid">{px:.{dec}f}</span><span style="color:var(--text);">{sz}</span><span class="ob-vol">${px*sz:,.0f}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_ask:
            st.markdown('<div style="font-size:.65rem;color:var(--red);letter-spacing:2px;font-weight:700;margin-bottom:.5rem;">ASKS</div><div style="background:var(--s1);border:1px solid var(--border);"><div class="ob-row" style="color:var(--dim);font-size:.58rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);font-weight:600;"><span>Price</span><span>Size</span><span>Total</span></div>', unsafe_allow_html=True)
            for i in range(8):
                px=round(base+(i+1)*base*0.0003,dec); sz=random.randint(1,500)
                st.markdown(f'<div class="ob-row"><span class="ob-ask">{px:.{dec}f}</span><span style="color:var(--text);">{sz}</span><span class="ob-vol">${px*sz:,.0f}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

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
            data=MARKET_DATA.get(sym,{"price":1.0,"change":0.0,"vol":"N/A","name":sym})
            chg=data["change"]; col="var(--green)" if chg>=0 else "var(--red)"; sign="+" if chg>=0 else ""
            dec = 5 if data["price"] < 10 else 2
            st.markdown(f'<div class="wl-row"><div><div style="font-weight:700;color:var(--text);">{sym}</div><div style="font-size:.65rem;color:var(--dim);">{data.get("name","")} &middot; {data["vol"]}</div></div><div style="font-family:\'Share Tech Mono\',monospace;color:var(--text);font-size:.82rem;">{data["price"]:.{dec}f}</div><div style="font-weight:700;color:{col};font-family:\'Share Tech Mono\',monospace;font-size:.78rem;">{sign}{chg:.2f}%</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# ANALYTICS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "analytics":
    if not st.session_state.user: goto("auth")
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
    wins=[t for t in all_trades if t.get("pnl",0)>0]; losses=[t for t in all_trades if t.get("pnl",0)<0]
    gross_profit=sum(t.get("pnl",0) for t in wins); gross_loss=abs(sum(t.get("pnl",0) for t in losses))
    pf=round(gross_profit/gross_loss,2) if gross_loss>0 else 99.0
    avg_win=round(gross_profit/len(wins),2) if wins else 0; avg_loss=round(gross_loss/len(losses),2) if losses else 0
    expectancy=round(wr/100*avg_win-(1-wr/100)*avg_loss,2)
    st.markdown(
        f'<div class="metric-row">'
        f'<div class="m-card"><div class="m-label">Profit Factor</div><div class="m-val {"g" if pf>=1.5 else "r"}">{pf}x</div><div class="m-sub">{"Strong edge" if pf>=1.5 else "Needs work"}</div></div>'
        f'<div class="m-card"><div class="m-label">Expectancy / Trade</div><div class="m-val {"g" if expectancy>0 else "r"}">{"+" if expectancy>0 else ""}${expectancy:,.2f}</div><div class="m-sub">Expected P&L per trade</div></div>'
        f'<div class="m-card"><div class="m-label">Avg Win</div><div class="m-val g">+${avg_win:,.2f}</div><div class="m-sub">{len(wins)} winning trades</div></div>'
        f'<div class="m-card"><div class="m-label">Avg Loss</div><div class="m-val r">-${avg_loss:,.2f}</div><div class="m-sub">{len(losses)} losing trades</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )
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
        st.markdown(f'<div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;padding:.65rem 1.2rem;border-top:1px solid var(--border);align-items:center;"><span style="font-weight:700;color:var(--text);">{sym}</span><span style="color:{pc};font-family:\'Share Tech Mono\',monospace;font-size:.75rem;">{ps2}${total:,.2f}</span><span style="color:var(--text);">{cnt}</span><span style="color:{wrc2};font-weight:700;">{wr2:.0f}%</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PORTFOLIO
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "portfolio":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]
    sec("Portfolio Overview","Performance across all challenges")
    all_trades=db_get_trades(uid,limit=500); all_challenges=db_get_all_challenges(uid)
    wr,ap,bt,wt,tt=compute_stats(all_trades)
    passed=sum(1 for c in all_challenges if c.get("status")=="passed")
    failed=sum(1 for c in all_challenges if c.get("status")=="failed")
    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""
    st.markdown(
        f'<div class="stats-row">'
        f'<div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>'
        f'<div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>'
        f'<div class="stat-box"><div class="sv {apc}">{aps}${ap:,.2f}</div><div class="sl">Avg P&L</div></div>'
        f'<div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed</div></div>'
        f'<div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )
    challenge=db_get_active_challenge(uid); account=db_get_account(challenge["id"]) if challenge else None
    if challenge and account:
        bal=account["balance"]; init=account["initial_capital"]; p=bal-init; pp=(p/init)*100
        r=RULES.get(challenge["plan"],{}); pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
        st.markdown(
            f'<div style="background:var(--s1);border:1px solid rgba(0,212,255,.2);border-left:2px solid var(--cyan);padding:1.8rem 2rem;margin-bottom:1.5rem;">'
            f'<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:1rem;">Active Challenge</div>'
            f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;">'
            f'<div><div class="m-label">Plan</div><div style="font-family:\'Orbitron\',monospace;font-size:1.4rem;color:var(--cyan);">{challenge["plan"].upper()}</div></div>'
            f'<div><div class="m-label">Balance</div><div style="font-family:\'Orbitron\',monospace;font-size:1.4rem;color:var(--text);">${bal:,.2f}</div></div>'
            f'<div><div class="m-label">P&L</div><div style="font-family:\'Orbitron\',monospace;font-size:1.4rem;color:{pc};">{ps}${p:,.2f}</div></div>'
            f'<div><div class="m-label">Progress</div><div style="font-family:\'Orbitron\',monospace;font-size:1.4rem;color:var(--cyan);">{ps}{pp:.1f}%</div></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
    footer()

# ══════════════════════════════════════════════════════════════
# JOURNAL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "journal":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]; challenge=db_get_active_challenge(uid)
    sec("Trade Journal","Document your setups, outcomes and mindset")
    with st.expander("Add New Entry", expanded=True):
        ca,cb = st.columns(2)
        with ca:
            all_s=[s for g in SYMBOLS.values() for s in g]
            j_sym=st.selectbox("Symbol",all_s,key="jsym")
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
    entries=db_get_journal(uid)
    if entries:
        for e in entries:
            out=e.get("outcome",""); tc="win" if out=="win" else ("loss" if out=="loss" else "")
            dt=e.get("created_at","")[:10]
            setup_tag=f'<span class="je-tag">{e["setup"]}</span>' if e.get("setup") else ""
            st.markdown(f'<div class="journal-entry"><div class="je-date">{dt} &nbsp;|&nbsp; {e.get("symbol","")} &nbsp;|&nbsp; {e.get("emotion","")}</div><div class="je-note">{e.get("note","")}</div><div class="je-tags"><span class="je-tag {tc}">{out.upper()}</span>{setup_tag}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No entries yet.</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user: goto("auth")
    nav()
    uid=st.session_state.user["id"]
    sec("Challenge History","All past and active challenge attempts")
    all_ch=db_get_all_challenges(uid)
    if not all_ch:
        st.markdown('<div style="text-align:center;padding:4rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);font-size:.8rem;">No challenges yet.</div>', unsafe_allow_html=True)
        _,c,_=st.columns([2,1,2])
        with c:
            if st.button("Activate Plan",use_container_width=True): goto("plans")
    else:
        total=len(all_ch); passed=sum(1 for c in all_ch if c.get("status")=="passed")
        failed=sum(1 for c in all_ch if c.get("status")=="failed"); active=sum(1 for c in all_ch if c.get("status")=="active")
        st.markdown(f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-bottom:1.5rem;background:var(--border);"><div class="stat-box"><div class="sv w">{total}</div><div class="sl">Total</div></div><div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed</div></div><div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed</div></div><div class="stat-box"><div class="sv c">{active}</div><div class="sl">Active</div></div></div>', unsafe_allow_html=True)
        for ch in all_ch:
            acc=db_get_account(ch["id"]) or {}; cap=ch.get("capital",0); bal=acc.get("balance",cap)
            p=bal-cap; pp=(p/cap*100) if cap else 0; status=ch.get("status","active"); d=acc.get("days_traded",0)
            r=RULES.get(ch.get("plan",""),{}); phase=r.get("phase","1step")
            cap_str=f"${cap//1000}K"; date_str=ch.get("started_at","")[:10]
            pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
            st.markdown(f'<div class="ch-card"><div><div class="ch-plan">{ch.get("plan","").upper()}</div><div style="font-size:.68rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;">{cap_str} &nbsp;|&nbsp; {date_str} &nbsp;|&nbsp; {phase.upper()}</div></div><div style="font-size:.8rem;">Balance: <b style="color:var(--text);">${bal:,.2f}</b></div><div style="font-size:.8rem;color:{pc};">P&L: <b>{ps}${p:,.2f} ({ps}{pp:.1f}%)</b></div><div style="font-size:.8rem;color:var(--dim);">Days: <b style="color:var(--text);">{d}</b></div><div class="ch-status {status}">{status.upper()}</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "leaderboard":
    nav()
    sec("Leaderboard","Top traders ranked by profit")
    data=db_get_leaderboard()
    if not data:
        data=[
            {"name":"Rahul S.","country":"India","profit_pct":18.4,"status":"passed","plan":"1phase_50k"},
            {"name":"Priya M.","country":"India","profit_pct":15.2,"status":"passed","plan":"2phase_25k"},
            {"name":"Kiran T.","country":"India","profit_pct":12.7,"status":"active","plan":"instant_25k"},
            {"name":"Arun K.","country":"UAE",  "profit_pct":11.1,"status":"passed","plan":"1phase_100k"},
            {"name":"Sneha R.","country":"India","profit_pct":9.8, "status":"active","plan":"2phase_50k"},
        ]
    medals=["01","02","03"]
    for i,t in enumerate(data):
        rank=i+1; medal=medals[i] if i<3 else f"{rank:02d}"
        rc="top" if rank<=3 else ""; funded=t.get("status")=="passed"
        bc="funded-b" if funded else "active-b"; bt2="Funded" if funded else "Active"
        profit=t.get("profit_pct",0)
        r=RULES.get(t.get("plan",""),{}); phase=r.get("phase","1step")
        st.markdown(f'<div class="lb-item"><div class="lb-rank {rc}">{medal}</div><div class="lb-info"><div class="lb-name">{t.get("name","Trader")}</div><div class="lb-country">{t.get("country","")} &nbsp;|&nbsp; {t.get("plan","").upper()} &nbsp;|&nbsp; {phase.upper()}</div></div><div class="lb-pnl">+{profit:.2f}%</div><div class="lb-badge {bc}">{bt2}</div></div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PROFILE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    if not st.session_state.user: goto("auth")
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
    badge_html='<div class="funded-badge-inline">&#10003; Funded Trader</div>' if funded_badge else ""
    st.markdown(
        f'<div class="profile-hero">'
        f'<div class="profile-avatar">{initials}</div>'
        f'<div><div class="profile-name">{name.upper()}</div>'
        f'<div class="profile-email">{email}</div>'
        f'<div style="font-size:.68rem;color:var(--dim);margin-top:4px;letter-spacing:.5px;">{country}</div>'
        f'{badge_html}</div>'
        f'<div style="margin-left:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;text-align:center;">'
        f'<div><div style="font-family:\'Orbitron\',monospace;font-size:1.6rem;color:var(--cyan);">{tt}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Trades</div></div>'
        f'<div><div style="font-family:\'Orbitron\',monospace;font-size:1.6rem;color:{"var(--green)" if wr>=50 else "var(--red)"};">{wr:.0f}%</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Win Rate</div></div>'
        f'<div><div style="font-family:\'Orbitron\',monospace;font-size:1.6rem;color:var(--green);">{passed}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Passed</div></div>'
        f'<div><div style="font-family:\'Orbitron\',monospace;font-size:1.6rem;color:var(--red);">{failed}</div><div style="font-size:.55rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-top:4px;">Failed</div></div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
    with st.form("edit_profile"):
        c1,c2=st.columns(2)
        with c1:
            new_name=st.text_input("Full Name",value=name,key="pf_name")
            new_country=st.text_input("Country",value=country,key="pf_country")
        with c2:
            new_bio=st.text_area("Bio",value=bio,placeholder="e.g. XAUUSD scalper.",height=100,key="pf_bio")
        if st.form_submit_button("Save Profile",use_container_width=True):
            if db_update_profile(uid,new_name,new_country,new_bio):
                st.session_state.user["name"]=new_name
                st.success("Profile saved."); time.sleep(1); st.rerun()
            else: st.error("Save failed.")
    c1,c2=st.columns(2)
    with c1:
        if st.button("Sign Out",use_container_width=True,key="profile_logout"):
            supabase.auth.sign_out(); st.session_state.user=None; st.session_state.notifications=[]; goto("home")
    with c2:
        if st.button("Send Test Email",use_container_width=True,key="test_email"):
            ok=send_email_html(email,"AKFunded — Email Test",f'<div style="font-family:Arial,sans-serif;background:#050505;color:#D8D8D8;padding:2rem;max-width:500px;"><h2 style="color:#00D4FF;">AKFUNDED</h2><p>Email working correctly, {name}.</p></div>')
            if ok: st.success(f"Test email sent to {email}.")
            else: st.error("Configure SMTP_EMAIL and SMTP_PASSWORD in secrets.")
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
        st.markdown(f'<div class="admin-row"><div><div style="font-weight:700;color:var(--text);">{r["name"]}</div><div style="font-size:.65rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;">{r["email"]}</div></div><div style="color:var(--cyan);font-size:.75rem;">{r["plan"].upper()} ({cap_str})</div><div style="font-family:\'Share Tech Mono\',monospace;font-size:.75rem;">${r["balance"]:,.2f}</div><div style="color:{pc};font-family:\'Share Tech Mono\',monospace;font-weight:700;">{ps}{r["pnl_pct"]:.2f}%</div><div style="color:var(--text);">{r["days_traded"]}</div><div class="admin-status {r["status"]}">{r["status"].upper()}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
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
        f"Instruments: Forex pairs, Metals (XAUUSD, XAGUSD), Crude Oil (USOIL, UKOIL). "
        f"Rules: {r.get('daily_loss',5)}% daily loss limit, {r.get('total_loss',10)}% max loss, {r.get('target',8)}% target. "
        f"Recent trades: {[t.get('symbol','')+' '+t.get('type','')+' $'+str(round(t.get('pnl',0),2)) for t in trades[:5]]}. "
        f"Give concise professional forex/metals trading advice. Keep replies under 130 words."
    )
    sec("AI Trading Coach","Powered by Groq — LLaMA 3.3 70B")
    st.markdown('<div class="chat-container"><div class="chat-header"><div class="chat-ai-dot"></div><div><div style="font-weight:700;font-size:.85rem;color:var(--text);">AK Trading Coach</div><div style="font-size:.65rem;color:var(--green);letter-spacing:1px;">Online — Forex &amp; Metals Specialist</div></div></div></div>', unsafe_allow_html=True)
    chat=st.session_state.chat_history
    if not chat:
        st.markdown(f'<div class="chat-messages"><div class="chat-msg"><div class="chat-avatar ai">AI</div><div class="chat-bubble ai">Hello {name}. I specialise in Forex and metals trading. Ask me about XAUUSD setups, risk management, or how to pass your challenge efficiently.</div></div></div>', unsafe_allow_html=True)
    else:
        msgs_html=""
        for m in chat[-10:]:
            role=m["role"]; txt=m["content"]; cls="user" if role=="user" else "ai"
            av=name[0].upper() if role=="user" else "AI"
            msgs_html+=f'<div class="chat-msg {cls}"><div class="chat-avatar {cls}">{av}</div><div class="chat-bubble {cls}">{txt}</div></div>'
        st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)
    quick=["XAUUSD setup","EURUSD analysis","Risk management","Recovering drawdown","How to pass faster"]
    qcols=st.columns(len(quick))
    for i,q in enumerate(quick):
        with qcols[i]:
            if st.button(q,key=f"qp_{i}",use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Processing..."): resp=call_ai(st.session_state.chat_history,SYSTEM)
                st.session_state.chat_history.append({"role":"assistant","content":resp}); st.rerun()
    user_input=st.text_input("Message",placeholder="Ask about Forex, XAU, or crude oil...",key="chat_input",label_visibility="collapsed")
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
    sec("Risk Calculator","Forex position sizing, pip value and challenge limits")
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Position Size Calculator</div>', unsafe_allow_html=True)
        acc_size=st.number_input("Account Balance ($)",value=balance,min_value=1000.0,step=1000.0,key="rc_bal")
        risk_pct=st.slider("Risk per trade (%)",0.1,3.0,1.0,0.1,key="rc_risk")
        sym_sel=st.selectbox("Symbol",[s for g in SYMBOLS.values() for s in g],key="rc_sym")
        entry_p=st.number_input("Entry Price",value=float(MARKET_DATA.get(sym_sel,{}).get("price",1.0)),min_value=0.00001,format="%.5f",key="rc_entry")
        stop_loss=st.number_input("Stop Loss",value=float(round(MARKET_DATA.get(sym_sel,{}).get("price",1.0)*0.995,5)),min_value=0.00001,format="%.5f",key="rc_sl")
        target_p=st.number_input("Take Profit",value=float(round(MARKET_DATA.get(sym_sel,{}).get("price",1.0)*1.015,5)),min_value=0.00001,format="%.5f",key="rc_tp")
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
                f'<div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;color:{"var(--green)" if daily_rem>daily_lim*0.5 else "var(--red)"};">${daily_rem:,.2f}</div>'
                f'<div style="font-size:.65rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;">of ${daily_lim:,.2f} ({r.get("daily_loss",5)}%)</div></div>'
                f'<div style="margin-bottom:1.2rem;"><div class="m-label">Total Loss Remaining</div>'
                f'<div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;color:{"var(--green)" if total_rem>total_lim*0.5 else "var(--red)"};">${total_rem:,.2f}</div>'
                f'<div style="font-size:.65rem;color:var(--dim);font-family:\'Share Tech Mono\',monospace;">of ${total_lim:,.2f} ({r.get("total_loss",10)}%)</div></div>'
                f'<div style="background:var(--s2);border:1px solid var(--border);border-left:2px solid var(--green);padding:1rem;margin-top:1px;">'
                f'<div class="m-label">Recommended Max Risk / Trade</div>'
                f'<div style="font-family:\'Orbitron\',monospace;font-size:1.8rem;color:var(--green);">${min(daily_rem*0.25,total_rem*0.1):,.2f}</div>'
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
            '<div style="font-family:\'Orbitron\',monospace;font-size:1.5rem;letter-spacing:4px;color:var(--dim);margin-bottom:.5rem;">No Certificate Yet</div>'
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
                    f"Trading Forex & XAUUSD. @akfunded #AKFunded #PropTrading #Forex"
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
    code=ref.get("code",""); uses=ref.get("uses",0); earnings=uses*50
    share_url=f"{PLATFORM_URL}/?ref={code}"
    st.markdown(
        f'<div style="background:var(--s1);border:1px solid rgba(0,212,255,.15);border-left:2px solid var(--cyan);padding:2rem;margin-bottom:1.5rem;">'
        f'<div style="font-size:.58rem;color:var(--dim);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:.8rem;font-weight:600;">Your Referral Code</div>'
        f'<div class="ref-code-box"><div class="ref-code">{code}</div><div style="font-size:.65rem;color:var(--dim);">Unique code</div></div>'
        f'<div class="ref-stats">'
        f'<div class="stat-box"><div class="sv c">{uses}</div><div class="sl">Referrals</div></div>'
        f'<div class="stat-box"><div class="sv g">&#8377;{earnings}</div><div class="sl">Earned</div></div>'
        f'<div class="stat-box"><div class="sv w">&#8377;50</div><div class="sl">Per Referral</div></div>'
        f'</div></div>',
        unsafe_allow_html=True
    )
    st.code(share_url, language=None)
    c1,c2=st.columns(2)
    with c1:
        wa=f"https://wa.me/?text=Join%20AKFunded%20-%20Forex%20Prop%20Trading%20Simulator.%20Use%20code%20{code}.%20{share_url}"
        st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%;background:rgba(0,212,255,.1);color:var(--cyan);font-weight:700;border:1px solid rgba(0,212,255,.3);padding:.55rem;font-family:\'Exo 2\',sans-serif;cursor:pointer;letter-spacing:2px;font-size:.78rem;text-transform:uppercase;">Share on WhatsApp</button></a>', unsafe_allow_html=True)
    with c2:
        if st.button("Email Invite",use_container_width=True,key="email_invite"):
            html_invite=(
                f'<div style="font-family:Arial,sans-serif;max-width:580px;background:#050505;color:#D8D8D8;padding:2rem;">'
                f'<h2 style="color:#00D4FF;letter-spacing:4px;">AKFUNDED</h2>'
                f'<p>{name} has invited you to AKFunded — Forex Prop Trading.</p>'
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
