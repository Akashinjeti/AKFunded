import streamlit as st
from supabase import create_client
import time, random, string, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="AKFunded — Prove Your Edge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── SUPABASE (service role — all filtering done in Python) ────
@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_KEY"]   # use service role key
    )

supabase = get_supabase()

# ─── STYLES ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
:root{--gold:#F0B429;--gold-dim:#7a5c0a;--black:#070707;--s1:#111;--s2:#181818;--border:#222;--border2:#2a2a2a;--text:#E8E8E8;--dim:#666;--green:#00C896;--red:#FF4560;}

/* ── LIGHT MODE OVERRIDE ── */
body.light-mode, body.light-mode [class*="css"],
body.light-mode .stApp, body.light-mode .main,
body.light-mode div[data-testid="stAppViewContainer"],
body.light-mode .appview-container {
  background-color:#F5F5F0!important; background:#F5F5F0!important;
}
body.light-mode * { color:#111!important; }
body.light-mode .ak-nav { border-color:#ddd!important; background:#fff!important; }
body.light-mode .m-card, body.light-mode .stat-box, body.light-mode .rules-box,
body.light-mode .journal-entry, body.light-mode .ch-card, body.light-mode .lb-item,
body.light-mode .plan-card { background:#fff!important; border-color:#e0e0e0!important; }
body.light-mode .stButton>button { background:var(--gold)!important; color:#000!important; }
html,body{background-color:#070707!important;}
[class*="css"],.main,.stApp,.stApp>div,section.main,div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"],div[data-testid="stToolbar"],div[data-testid="stDecoration"],
div[data-testid="stBottom"],.appview-container,.reportview-container,.main .block-container,
iframe{background-color:#070707!important;background:#070707!important;}
*{font-family:'DM Sans',sans-serif;color:var(--text);}
#MainMenu,footer,header{visibility:hidden!important;display:none!important;}
.block-container{padding:1rem 2.5rem 3rem!important;max-width:1380px!important;}
::-webkit-scrollbar{width:3px;}::-webkit-scrollbar-thumb{background:var(--gold-dim);}

/* NAV */
.ak-nav{display:flex;align-items:center;justify-content:space-between;padding:1.4rem 0;border-bottom:1px solid var(--border);margin-bottom:2rem;}
.ak-logo{font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:5px;display:inline-flex;align-items:baseline;}
.ak-part{color:#F0B429;-webkit-text-fill-color:#F0B429;}
.funded-part{color:#fff;-webkit-text-fill-color:#fff;}
.ak-beta{background:var(--gold);color:#000;font-size:.55rem;font-weight:800;padding:2px 7px;border-radius:20px;letter-spacing:1.5px;vertical-align:super;margin-left:6px;font-family:'DM Sans',sans-serif;}
.ak-powered{font-size:.68rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;}
.ak-powered b{color:var(--gold);-webkit-text-fill-color:var(--gold);}

/* HERO */
.hero{text-align:center;padding:5rem 0 3.5rem;position:relative;}
.hero::before{content:'';position:absolute;top:-40%;left:50%;transform:translateX(-50%);width:700px;height:700px;background:radial-gradient(circle,rgba(240,180,41,.09) 0%,transparent 65%);pointer-events:none;}
.hero-chip{display:inline-block;border:1px solid var(--gold-dim);color:var(--gold);-webkit-text-fill-color:var(--gold);font-size:.65rem;letter-spacing:3px;padding:5px 18px;border-radius:20px;margin-bottom:1.8rem;text-transform:uppercase;background:rgba(240,180,41,.05);}
.hero h1{font-family:'Bebas Neue',sans-serif;font-size:clamp(4rem,9vw,9rem);line-height:.93;letter-spacing:5px;margin:0 0 1.2rem;color:#fff;-webkit-text-fill-color:#fff;}
.hero h1 em{font-style:normal;color:var(--gold);-webkit-text-fill-color:var(--gold);}
.hero-sub{font-size:1.05rem;color:#777;-webkit-text-fill-color:#777;max-width:480px;margin:0 auto 2.5rem;line-height:1.75;}

/* STATS BAR */
.hstats{display:flex;justify-content:center;gap:4rem;padding:1.8rem 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);margin-bottom:3rem;}
.hstat .n{font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:var(--gold);-webkit-text-fill-color:var(--gold);letter-spacing:2px;display:block;}
.hstat .l{font-size:.65rem;color:#666;-webkit-text-fill-color:#666;letter-spacing:2px;text-transform:uppercase;}

/* PLAN CARDS */
.plans-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-bottom:3rem;}
.plan-card{background:var(--s1);border:1px solid var(--border);border-radius:18px;padding:2rem 1.8rem;position:relative;overflow:hidden;transition:all .25s;}
.plan-card:hover{border-color:var(--gold-dim);transform:translateY(-5px);}
.plan-card.hot{border-color:var(--gold);background:linear-gradient(160deg,#130f00,var(--s1));}
.plan-card.hot::before{content:'MOST POPULAR';position:absolute;top:1rem;right:-2rem;background:var(--gold);color:#000;font-size:.55rem;font-weight:800;padding:3px 3rem;letter-spacing:1.5px;transform:rotate(35deg);}
.plan-name{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:3px;color:var(--dim);margin-bottom:.4rem;}
.plan-capital{font-family:'Bebas Neue',sans-serif;font-size:3.2rem;color:var(--gold);-webkit-text-fill-color:var(--gold);letter-spacing:2px;line-height:1;margin-bottom:1.5rem;}
.plan-rules{list-style:none;padding:0;margin:0 0 1.5rem;}
.plan-rules li{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid var(--border2);font-size:.82rem;color:var(--dim);}
.plan-rules li b{color:var(--text);font-weight:500;}
.plan-price{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:2px;}
.plan-price small{font-family:'DM Sans',sans-serif;font-size:.7rem;color:var(--dim);font-weight:300;letter-spacing:0;}

/* METRIC CARDS */
.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;}
.m-card{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;}
.m-label{font-size:.65rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:.4rem;}
.m-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:2px;line-height:1;}
.m-val.g{color:var(--green);-webkit-text-fill-color:var(--green);}
.m-val.r{color:var(--red);-webkit-text-fill-color:var(--red);}
.m-val.o{color:var(--gold);-webkit-text-fill-color:var(--gold);}
.m-val.w{color:var(--text);-webkit-text-fill-color:var(--text);}
.m-sub{font-size:.7rem;color:var(--dim);margin-top:4px;}

/* STATS ROW (5 col) */
.stats-row{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;margin-bottom:1.5rem;}
.stat-box{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;text-align:center;}
.stat-box .sv{font-family:'Bebas Neue',sans-serif;font-size:1.7rem;letter-spacing:2px;line-height:1;}
.stat-box .sl{font-size:.62rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;}
.sv.g{color:var(--green);-webkit-text-fill-color:var(--green);}
.sv.r{color:var(--red);-webkit-text-fill-color:var(--red);}
.sv.o{color:var(--gold);-webkit-text-fill-color:var(--gold);}
.sv.w{color:var(--text);-webkit-text-fill-color:var(--text);}

/* RULES */
.rules-box{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1.4rem;margin-bottom:1.5rem;}
.r-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;}
.r-name{font-size:.82rem;color:var(--dim);}
.r-val{font-family:'JetBrains Mono',monospace;font-size:.82rem;}
.r-val.ok{color:var(--green);} .r-val.bad{color:var(--red);}
.prog{height:3px;background:var(--border);border-radius:3px;overflow:hidden;margin-bottom:1rem;}
.prog-fill{height:100%;border-radius:3px;}

/* TRADE TABLE */
.t-header,.t-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.2fr;padding:.7rem 1rem;font-size:.82rem;align-items:center;}
.t-header{color:var(--dim);font-size:.65rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);}
.t-row{border-bottom:1px solid var(--border2);}
.t-row:last-child{border-bottom:none;}
.tag-b{background:rgba(0,200,150,.12);color:var(--green);padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:700;}
.tag-s{background:rgba(255,69,96,.12);color:var(--red);padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:700;}

/* LEADERBOARD */
.lb-item{display:flex;align-items:center;gap:1rem;background:var(--s1);border:1px solid var(--border);border-radius:10px;padding:.9rem 1.2rem;margin-bottom:.5rem;}
.lb-rank{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--dim);width:36px;text-align:center;}
.lb-rank.top{color:var(--gold);-webkit-text-fill-color:var(--gold);}
.lb-info{flex:1;}
.lb-name{font-weight:600;font-size:.92rem;}
.lb-country{font-size:.72rem;color:var(--dim);}
.lb-pnl{font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);font-size:1rem;}
.lb-badge{font-size:.58rem;padding:2px 8px;border-radius:20px;font-weight:700;letter-spacing:1px;}
.funded-b{background:rgba(240,180,41,.15);color:var(--gold);}
.active-b{background:rgba(0,200,150,.1);color:var(--green);}

/* JOURNAL */
.journal-entry{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:.7rem;}
.je-date{font-size:.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.3rem;}
.je-note{font-size:.88rem;color:var(--text);line-height:1.6;}
.je-tags{display:flex;gap:.5rem;margin-top:.6rem;flex-wrap:wrap;}
.je-tag{font-size:.62rem;padding:2px 8px;border-radius:20px;background:rgba(240,180,41,.1);color:var(--gold);font-weight:600;}
.je-tag.win{background:rgba(0,200,150,.1);color:var(--green);}
.je-tag.loss{background:rgba(255,69,96,.1);color:var(--red);}

/* CHALLENGE HISTORY */
.ch-card{background:var(--s1);border:1px solid var(--border);border-radius:14px;padding:1.4rem 1.6rem;margin-bottom:.8rem;display:grid;grid-template-columns:1fr 1fr 1fr 1fr auto;align-items:center;gap:1rem;}
.ch-plan{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:2px;color:var(--gold);-webkit-text-fill-color:var(--gold);}
.ch-status{padding:4px 12px;border-radius:20px;font-size:.65rem;font-weight:700;letter-spacing:1px;text-align:center;}
.ch-status.passed{background:rgba(0,200,150,.12);color:var(--green);}
.ch-status.failed{background:rgba(255,69,96,.12);color:var(--red);}
.ch-status.active{background:rgba(240,180,41,.12);color:var(--gold);}

/* NOTIFICATIONS */
.notif-item{display:flex;align-items:flex-start;gap:1rem;background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;margin-bottom:.6rem;transition:border-color .2s;}
.notif-item.unread{border-left:3px solid var(--gold);}
.notif-icon{font-size:1.4rem;flex-shrink:0;}
.notif-body{flex:1;}
.notif-title{font-weight:600;font-size:.88rem;color:var(--text);margin-bottom:2px;}
.notif-msg{font-size:.78rem;color:var(--dim);line-height:1.5;}
.notif-time{font-size:.65rem;color:#444;letter-spacing:1px;margin-top:4px;}
.notif-badge{background:var(--gold);color:#000;font-size:.55rem;font-weight:800;padding:2px 6px;border-radius:20px;margin-left:6px;vertical-align:middle;}

/* PROFILE */
.profile-hero{background:linear-gradient(135deg,#130f00,var(--s1));border:1px solid var(--gold-dim);border-radius:18px;padding:2rem;margin-bottom:1.5rem;display:flex;gap:2rem;align-items:center;}
.profile-avatar{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,var(--gold),#c88a00);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#000;flex-shrink:0;}
.profile-name{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:3px;color:#E8E8E8;line-height:1;}
.profile-email{font-size:.8rem;color:var(--dim);margin-top:4px;}
.profile-country{font-size:.75rem;color:var(--gold);margin-top:6px;letter-spacing:1px;}
.funded-badge{display:inline-block;background:linear-gradient(135deg,var(--gold),#c88a00);color:#000;font-family:'Bebas Neue',sans-serif;font-size:.9rem;letter-spacing:2px;padding:4px 16px;border-radius:20px;margin-top:8px;}

/* ADMIN */
.admin-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr auto;align-items:center;gap:1rem;padding:.8rem 1rem;border-bottom:1px solid var(--border2);font-size:.82rem;}
.admin-row.header{color:var(--dim);font-size:.65rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);}
.admin-status{padding:3px 10px;border-radius:20px;font-size:.62rem;font-weight:700;letter-spacing:1px;text-align:center;}
.admin-status.active{background:rgba(240,180,41,.12);color:var(--gold);}
.admin-status.passed{background:rgba(0,200,150,.12);color:var(--green);}
.admin-status.failed{background:rgba(255,69,96,.12);color:var(--red);}

/* TOGGLE THEME BTN */
.theme-btn{background:transparent;border:1px solid var(--border);color:var(--dim);font-size:.75rem;padding:4px 12px;border-radius:20px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;}
.theme-btn:hover{border-color:var(--gold);color:var(--gold);}

/* ── WEEK 4 FEATURES ── */

/* LANDING HERO V2 */
.hero-v2{position:relative;text-align:center;padding:6rem 2rem 4rem;overflow:hidden;}
.hero-v2::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(240,180,41,.12),transparent);
  pointer-events:none;}
.hero-v2 .eyebrow{display:inline-flex;align-items:center;gap:.5rem;border:1px solid var(--gold-dim);
  color:var(--gold);font-size:.65rem;letter-spacing:3px;padding:5px 16px;border-radius:20px;
  margin-bottom:2rem;text-transform:uppercase;background:rgba(240,180,41,.05);}
.hero-v2 h1{font-family:'Bebas Neue',sans-serif;font-size:clamp(4rem,10vw,10rem);
  line-height:.9;letter-spacing:6px;margin:0 0 1.5rem;color:#fff;-webkit-text-fill-color:#fff;}
.hero-v2 h1 em{color:var(--gold);-webkit-text-fill-color:var(--gold);font-style:normal;}
.hero-v2 .sub{font-size:1.15rem;color:#666;max-width:520px;margin:0 auto 3rem;line-height:1.8;}
.hero-cta{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:4rem;}
.cta-primary{background:var(--gold);color:#000;font-family:'Bebas Neue',sans-serif;
  font-size:1.1rem;letter-spacing:3px;padding:14px 40px;border-radius:10px;
  border:none;cursor:pointer;transition:all .2s;}
.cta-primary:hover{opacity:.85;transform:translateY(-2px);}
.cta-secondary{background:transparent;color:var(--text);font-family:'Bebas Neue',sans-serif;
  font-size:1.1rem;letter-spacing:3px;padding:14px 40px;border-radius:10px;
  border:1px solid var(--border);cursor:pointer;transition:all .2s;}
.cta-secondary:hover{border-color:var(--gold-dim);}

/* HOW IT WORKS */
.steps-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;margin:3rem 0;}
.step-card{background:var(--s1);border:1px solid var(--border);border-radius:16px;
  padding:1.8rem 1.5rem;text-align:center;position:relative;}
.step-num{font-family:'Bebas Neue',sans-serif;font-size:3rem;color:var(--gold);
  -webkit-text-fill-color:var(--gold);line-height:1;margin-bottom:.5rem;}
.step-title{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:2px;
  color:#E8E8E8;margin-bottom:.5rem;}
.step-desc{font-size:.82rem;color:#555;line-height:1.6;}

/* TESTIMONIALS */
.testi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin:2rem 0;}
.testi-card{background:var(--s1);border:1px solid var(--border);border-radius:16px;padding:1.5rem;}
.testi-quote{font-size:.9rem;color:#E8E8E8;line-height:1.7;margin-bottom:1rem;font-style:italic;}
.testi-name{font-weight:700;font-size:.82rem;color:var(--gold);}
.testi-meta{font-size:.72rem;color:#555;}

/* CERTIFICATE */
.cert-container{background:linear-gradient(135deg,#0a0800,#111,#0a0800);
  border:2px solid var(--gold-dim);border-radius:20px;padding:3rem;
  text-align:center;position:relative;overflow:hidden;max-width:700px;margin:0 auto;}
.cert-container::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;
  background:repeating-linear-gradient(45deg,transparent,transparent 40px,rgba(240,180,41,.02) 40px,rgba(240,180,41,.02) 41px);
  pointer-events:none;}
.cert-title{font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:6px;
  background:linear-gradient(135deg,#F0B429,#fff5a0,#F0B429);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.5rem;}
.cert-sub{font-size:.75rem;color:#555;letter-spacing:3px;text-transform:uppercase;margin-bottom:2rem;}
.cert-name{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#E8E8E8;letter-spacing:3px;margin:1rem 0;}
.cert-detail{font-size:.85rem;color:#666;margin:.3rem 0;}
.cert-badge{font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:3px;
  background:var(--gold);color:#000;padding:8px 24px;border-radius:30px;
  display:inline-block;margin:1.5rem 0;}
.cert-seal{font-size:4rem;margin:1rem 0;}
.cert-footer{font-size:.7rem;color:#333;letter-spacing:2px;text-transform:uppercase;margin-top:1.5rem;
  border-top:1px solid #222;padding-top:1rem;}

/* AI CHAT */
.chat-container{background:var(--s1);border:1px solid var(--border);border-radius:16px;
  overflow:hidden;margin-bottom:1rem;}
.chat-header{padding:1rem 1.4rem;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:.8rem;}
.chat-ai-dot{width:8px;height:8px;background:var(--green);border-radius:50%;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.4;}}
.chat-messages{padding:1.2rem;max-height:380px;overflow-y:auto;}
.chat-msg{margin-bottom:1rem;display:flex;gap:.8rem;align-items:flex-start;}
.chat-msg.user{flex-direction:row-reverse;}
.chat-bubble{padding:.7rem 1rem;border-radius:12px;font-size:.85rem;line-height:1.6;max-width:75%;}
.chat-bubble.ai{background:var(--s2);border:1px solid var(--border);color:var(--text);}
.chat-bubble.user{background:var(--gold);color:#000;font-weight:500;}
.chat-avatar{width:28px;height:28px;border-radius:50%;font-size:.75rem;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.chat-avatar.ai{background:var(--s2);border:1px solid var(--border);}
.chat-avatar.user{background:var(--gold);color:#000;font-weight:700;}

/* RISK CALCULATOR */
.risk-card{background:var(--s1);border:1px solid var(--border);border-radius:14px;padding:1.5rem;}
.risk-result{background:var(--s2);border-radius:10px;padding:1.2rem;text-align:center;margin-top:1rem;}
.risk-val{font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:2px;}

/* REFERRAL */
.ref-code-box{background:var(--s2);border:1px solid var(--gold-dim);border-radius:10px;
  padding:1rem 1.4rem;display:flex;align-items:center;justify-content:space-between;
  margin:1rem 0;}
.ref-code{font-family:'JetBrains Mono',monospace;font-size:1.4rem;color:var(--gold);
  font-weight:700;letter-spacing:4px;}
.ref-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0;}

/* FOOTER */
.ak-footer{text-align:center;padding:2rem 0 1rem;border-top:1px solid var(--border);margin-top:4rem;color:var(--dim);font-size:.72rem;letter-spacing:1px;}
.ak-footer b{color:var(--gold);-webkit-text-fill-color:var(--gold);}

/* STREAMLIT */
.stButton>button{background:var(--gold)!important;color:#000!important;font-weight:700!important;border:none!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;letter-spacing:1px!important;}
.stButton>button:hover{opacity:.8!important;}
.stButton>button p{color:#000!important;-webkit-text-fill-color:#000!important;}
div[data-testid="stTabs"] [data-baseweb="tab-list"]{background:var(--s1)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:3px!important;gap:3px!important;}
div[data-testid="stTabs"] [data-baseweb="tab"]{color:var(--dim)!important;font-family:'DM Sans',sans-serif!important;}
div[data-testid="stTabs"] [aria-selected="true"]{background:var(--gold)!important;color:#000!important;border-radius:8px!important;}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],div[data-testid="stTabs"] [data-baseweb="tab-border"]{display:none!important;}
.stSelectbox>div>div,.stNumberInput>div>div>input,.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--s2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
label[data-testid="stWidgetLabel"]{color:var(--dim)!important;font-size:.78rem!important;letter-spacing:1px!important;}
div[data-testid="stVerticalBlock"],div[data-testid="stHorizontalBlock"],
div[data-testid="column"],div[data-testid="stMarkdownContainer"],
div.element-container,div.stMarkdown{background:transparent!important;}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────
LOGO_URL = "https://i.imgur.com/placeholder.png"  # replace with your hosted logo URL

# One-Phase rules
RULES_1P = {
    "10k":  {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5,  "profit_split":80},
    "25k":  {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5,  "profit_split":80},
    "50k":  {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5,  "profit_split":80},
    "100k": {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5,  "profit_split":80},
    "200k": {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5,  "profit_split":80},
}
# Two-Phase rules (Phase 1 / Phase 2)
RULES_2P = {
    "10k":  {"target1":8,  "target2":5, "daily_loss":5, "total_loss":10, "min_days":4, "profit_split":90},
    "25k":  {"target1":8,  "target2":5, "daily_loss":5, "total_loss":10, "min_days":4, "profit_split":90},
    "50k":  {"target1":8,  "target2":5, "daily_loss":5, "total_loss":10, "min_days":4, "profit_split":90},
    "100k": {"target1":8,  "target2":5, "daily_loss":5, "total_loss":10, "min_days":4, "profit_split":90},
    "200k": {"target1":8,  "target2":5, "daily_loss":5, "total_loss":10, "min_days":4, "profit_split":90},
}

# Legacy rules for dashboard compatibility
RULES = {
    # Instant Funded — no challenge, strictest rules
    "instant_5k":   {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_10k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_25k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_50k":  {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    "instant_100k": {"target":0,"daily_loss":3,"total_loss":6, "min_days":0,"phase":"instant"},
    # One-Phase — 8% target, 5% daily, 10% max
    "1phase_5k":    {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "1phase_10k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "1phase_25k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "1phase_50k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "1phase_100k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    # Two-Phase — phase1 8%, phase2 5%, 5% daily, 10% max
    "2phase_5k":    {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"two"},
    "2phase_10k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"two"},
    "2phase_25k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"two"},
    "2phase_50k":   {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"two"},
    "2phase_100k":  {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"two"},
    # Legacy
    "starter":      {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "pro":          {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
    "elite":        {"target":8,"daily_loss":5,"total_loss":10,"min_days":4,"phase":"one"},
}

# One-Phase plans (USD pricing matching IF)
PLANS_IF = [
    {"name":"$5,000",   "capital":5000,   "price":139,  "slug":"instant_5k",   "split":80,"phase":"instant"},
    {"name":"$10,000",  "capital":10000,  "price":249,  "slug":"instant_10k",  "split":80,"phase":"instant"},
    {"name":"$25,000",  "capital":25000,  "price":449,  "slug":"instant_25k",  "split":80,"phase":"instant"},
    {"name":"$50,000",  "capital":50000,  "price":749,  "slug":"instant_50k",  "split":80,"phase":"instant"},
    {"name":"$100,000", "capital":100000, "price":1249, "slug":"instant_100k", "split":80,"phase":"instant"},
]
PLANS_1P = [
    {"name":"$5,000",   "capital":5000,   "price":49,  "slug":"1phase_5k",   "split":85,"phase":"one"},
    {"name":"$10,000",  "capital":10000,  "price":89,  "slug":"1phase_10k",  "split":85,"phase":"one"},
    {"name":"$25,000",  "capital":25000,  "price":169, "slug":"1phase_25k",  "split":85,"phase":"one"},
    {"name":"$50,000",  "capital":50000,  "price":249, "slug":"1phase_50k",  "split":85,"phase":"one"},
    {"name":"$100,000", "capital":100000, "price":399, "slug":"1phase_100k", "split":85,"phase":"one"},
]
PLANS_2P = [
    {"name":"$5,000",   "capital":5000,   "price":35,  "slug":"2phase_5k",   "split":90,"phase":"two"},
    {"name":"$10,000",  "capital":10000,  "price":59,  "slug":"2phase_10k",  "split":90,"phase":"two"},
    {"name":"$25,000",  "capital":25000,  "price":119, "slug":"2phase_25k",  "split":90,"phase":"two"},
    {"name":"$50,000",  "capital":50000,  "price":189, "slug":"2phase_50k",  "split":90,"phase":"two"},
    {"name":"$100,000", "capital":100000, "price":299, "slug":"2phase_100k", "split":90,"phase":"two"},
]
PLANS = PLANS_1P
SYMBOLS = {
    "Forex Majors":  ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","USDCHF","NZDUSD","EURGBP"],
    "Forex Minors":  ["EURJPY","GBPJPY","CADJPY","EURCAD","GBPAUD","AUDCAD","CHFJPY","EURCHF"],
    "Metals":        ["XAUUSD","XAGUSD","XPTUSD","XPDUSD"],
    "Energy":        ["USOIL","UKOIL","NATGAS","GASOLINE"],
    "Indices":       ["US30","NAS100","SPX500","GER40","UK100","JPN225"],
}
TV_PREFIX = {
    "Forex Majors":"FX:","Forex Minors":"FX:",
    "Metals":"TVC:","Energy":"PEPPERSTONE:","Indices":"OANDA:"
}
TV_SYMBOL_MAP = {
    "XAUUSD":"TVC:GOLD","XAGUSD":"TVC:SILVER","XPTUSD":"TVC:PLATINUM","XPDUSD":"TVC:PALLADIUM",
    "USOIL":"TVC:USOIL","UKOIL":"TVC:UKOIL","NATGAS":"TVC:NATURALGAS","GASOLINE":"TVC:GASOLINE",
    "US30":"OANDA:US30USD","NAS100":"OANDA:NAS100USD","SPX500":"OANDA:SPX500USD",
    "GER40":"OANDA:DE40EUR","UK100":"OANDA:UK100GBP","JPN225":"OANDA:JP225USD",
    "EURUSD":"FX:EURUSD","GBPUSD":"FX:GBPUSD","USDJPY":"FX:USDJPY","AUDUSD":"FX:AUDUSD",
    "USDCAD":"FX:USDCAD","USDCHF":"FX:USDCHF","NZDUSD":"FX:NZDUSD","EURGBP":"FX:EURGBP",
    "EURJPY":"FX:EURJPY","GBPJPY":"FX:GBPJPY","CADJPY":"FX:CADJPY","EURCAD":"FX:EURCAD",
    "GBPAUD":"FX:GBPAUD","AUDCAD":"FX:AUDCAD","CHFJPY":"FX:CHFJPY","EURCHF":"FX:EURCHF",
}

# ─── SESSION STATE ──────────────────────────────────────────────
for k,v in [("user",None),("page","home"),("theme","dark"),("notifications",[]),("chat_history",[])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── THEME INJECT ───────────────────────────────────────────────
if st.session_state.theme == "light":
    st.markdown('<script>document.body.classList.add("light-mode")</script>', unsafe_allow_html=True)

# ─── PYTHON DATA HELPERS (no RLS needed) ───────────────────────
def db_get_profile(uid):
    try:
        r = supabase.table("profiles").select("*").eq("id", uid).execute()
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
        r = supabase.table("challenges").select("*").eq("user_id", uid).eq("status","active").execute()
        return r.data[0] if r.data else None
    except: return None

def db_get_account(challenge_id):
    try:
        r = supabase.table("accounts").select("*").eq("challenge_id", challenge_id).execute()
        return r.data[0] if r.data else None
    except: return None

def db_get_trades(uid, challenge_id=None, limit=25):
    try:
        q = supabase.table("trades").select("*").eq("user_id", uid)
        if challenge_id:
            q = q.eq("challenge_id", challenge_id)
        return q.order("closed_at", desc=True).limit(limit).execute().data or []
    except: return []

def db_get_all_challenges(uid):
    try:
        return supabase.table("challenges").select("*").eq("user_id", uid).order("started_at", desc=True).execute().data or []
    except: return []

def db_get_journal(uid):
    try:
        return supabase.table("journal_entries").select("*").eq("user_id", uid).order("created_at", desc=True).limit(30).execute().data or []
    except: return []

def db_get_leaderboard():
    try:
        # Python-side leaderboard: get all passed/active accounts with user info
        challenges = supabase.table("challenges").select("*").in_("status",["passed","active"]).execute().data or []
        result = []
        for ch in challenges:
            acc = db_get_account(ch["id"])
            if not acc: continue
            prof = db_get_profile(ch["user_id"])
            if not prof: continue
            cap = acc.get("initial_capital",1)
            bal = acc.get("balance", cap)
            pnl_pct = round((bal - cap) / cap * 100, 2) if cap else 0
            result.append({
                "name": prof.get("name","Trader"),
                "country": prof.get("country",""),
                "profit_pct": pnl_pct,
                "plan": ch.get("plan",""),
                "status": ch.get("status","active"),
                "days_traded": acc.get("days_traded",0),
            })
        return sorted(result, key=lambda x: x["profit_pct"], reverse=True)[:20]
    except: return []

def db_get_all_users():
    """Admin only — get all profiles"""
    try:
        return supabase.table("profiles").select("*").execute().data or []
    except: return []

def db_get_all_accounts():
    """Admin only — get all accounts with challenge info"""
    try:
        challenges = supabase.table("challenges").select("*").execute().data or []
        result = []
        for ch in challenges:
            acc = db_get_account(ch["id"])
            prof = db_get_profile(ch["user_id"])
            if not acc or not prof: continue
            cap = acc.get("initial_capital", 1)
            bal = acc.get("balance", cap)
            result.append({
                "name":        prof.get("name","?"),
                "email":       prof.get("email","?"),
                "plan":        ch.get("plan","?"),
                "status":      ch.get("status","active"),
                "capital":     cap,
                "balance":     bal,
                "pnl_pct":     round((bal-cap)/cap*100,2) if cap else 0,
                "days_traded": acc.get("days_traded",0),
                "started_at":  ch.get("started_at","")[:10],
                "challenge_id":ch.get("id",""),
                "user_id":     ch.get("user_id",""),
            })
        return sorted(result, key=lambda x: x["started_at"], reverse=True)
    except: return []

def push_notification(uid, icon, title, msg):
    """Add a notification to session state"""
    notifs = st.session_state.get("notifications", [])
    notifs.insert(0, {
        "uid": uid, "icon": icon, "title": title,
        "msg": msg, "time": datetime.utcnow().strftime("%H:%M"),
        "unread": True
    })
    st.session_state.notifications = notifs[:20]  # keep last 20

def db_update_profile(uid, name, country, bio=""):
    try:
        supabase.table("profiles").update({
            "name": name, "country": country, "bio": bio
        }).eq("id", uid).execute()
        return True
    except: return False

# ── WEEK 4 HELPERS ──────────────────────────────────────────────

def generate_referral_code(name):
    """Generate a unique referral code from name"""
    prefix = name[:3].upper().replace(" ","")
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{suffix}"

def db_get_referral(uid):
    try:
        r = supabase.table("referrals").select("*").eq("user_id", uid).execute()
        return r.data[0] if r.data else None
    except: return None

def db_create_referral(uid, code):
    try:
        supabase.table("referrals").insert({
            "user_id": uid, "code": code,
            "uses": 0, "created_at": datetime.utcnow().isoformat()
        }).execute()
        return True
    except: return False

def db_get_referral_by_code(code):
    try:
        r = supabase.table("referrals").select("*").eq("code", code).execute()
        return r.data[0] if r.data else None
    except: return None

def send_email_notification(to_email, subject, body_html):
    """Send real email via Gmail SMTP"""
    try:
        smtp_email = st.secrets.get("SMTP_EMAIL","")
        smtp_pass  = st.secrets.get("SMTP_PASSWORD","")
        if not smtp_email or not smtp_pass:
            return False
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"AKFunded ⚡ <{smtp_email}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(body_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(smtp_email, smtp_pass)
            s.sendmail(smtp_email, to_email, msg.as_string())
        return True
    except: return False

def call_ai(messages, system_prompt):
    """Call Groq API - LLaMA 3.3 70B for AI trading assistant"""
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {st.secrets.get('GROQ_API_KEY','')}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama-3.3-70b-versatile",
            "max_tokens": 1000,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages
            ]
        }
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=body, headers=headers, timeout=30
        )
        data = r.json()
        return data["choices"][0]["message"]["content"] if data.get("choices") else "Sorry, I couldn't process that."
    except Exception as e:
        return f"AI unavailable right now. ({e})"

def render_certificate(name, plan, capital, pnl_pct, days, date_str):
    cap_str = f"₹{capital//100000}L" if capital>=100000 else f"₹{capital//1000}K"
    return f"""
    <div class="cert-container">
      <div class="cert-seal">🏆</div>
      <div class="cert-title">CERTIFICATE OF ACHIEVEMENT</div>
      <div class="cert-sub">AKFunded Prop Trading Challenge</div>
      <div style="font-size:.82rem;color:#555;margin-bottom:.5rem;">This certifies that</div>
      <div class="cert-name">{name.upper()}</div>
      <div style="font-size:.85rem;color:#666;margin-bottom:1.5rem;">
        has successfully completed the
      </div>
      <div class="cert-badge">⚡ {plan.upper()} CHALLENGE — {cap_str}</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin:1.5rem 0;">
        <div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--green);">+{pnl_pct:.2f}%</div>
          <div style="font-size:.65rem;color:#444;letter-spacing:2px;text-transform:uppercase;">Profit Achieved</div>
        </div>
        <div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--gold);">{days}</div>
          <div style="font-size:.65rem;color:#444;letter-spacing:2px;text-transform:uppercase;">Days Traded</div>
        </div>
        <div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#E8E8E8;">{date_str}</div>
          <div style="font-size:.65rem;color:#444;letter-spacing:2px;text-transform:uppercase;">Date Passed</div>
        </div>
      </div>
      <div class="cert-footer">
        AKFUNDED &nbsp;·&nbsp; Powered by Akash Injeti &nbsp;·&nbsp; akfunded.streamlit.app
      </div>
    </div>"""
    if not trades: return 0,0,0,0,0
    pnls = [t.get("pnl",0) for t in trades]
    wins = [p for p in pnls if p > 0]
    total = len(pnls)
    return (
        round(len(wins)/total*100,1) if total else 0,
        round(sum(pnls)/total,2) if total else 0,
        max(pnls) if pnls else 0,
        min(pnls) if pnls else 0,
        total
    )

def compute_stats(trades):
    if not trades: return 0,0,0,0,0
    pnls  = [t.get("pnl",0) for t in trades]
    wins  = [p for p in pnls if p > 0]
    total = len(pnls)
    return (
        round(len(wins)/total*100, 1) if total else 0,
        round(sum(pnls)/total, 2)     if total else 0,
        max(pnls) if pnls else 0,
        min(pnls) if pnls else 0,
        total
    )

def goto(page):
    st.session_state.page = page
    st.rerun()

# ─── UI COMPONENTS ─────────────────────────────────────────────
def nav():
    logged_in = st.session_state.user is not None

    st.markdown("""
    <div class="ak-nav">
      <div style="display:flex;align-items:center;gap:12px;">
        <img src="https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.png"
             onerror="this.style.display='none'"
             style="height:38px;width:38px;object-fit:contain;border-radius:6px;" />
        <span class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span></span>
        <span class="ak-beta">BETA</span>
      </div>
      <div class="ak-powered">Powered by <b>Akash Injeti</b></div>
    </div>""", unsafe_allow_html=True)

    if logged_in:
        is_admin = st.session_state.user.get("email","") == st.secrets.get("ADMIN_EMAIL","admin@akfunded.com")

        # CSS to prevent button text wrapping
        st.markdown("""
        <style>
        .stButton>button {
            white-space: nowrap !important;
            font-size: 0.72rem !important;
            padding: 0.4rem 0.6rem !important;
            letter-spacing: 0.5px !important;
        }
        </style>""", unsafe_allow_html=True)

        if is_admin:
            c0,c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1.2,.9,.9,.9,.9,1.2,.7,.7,.5])
            with c6:
                if st.button("🔔" + (f" {sum(1 for n in st.session_state.notifications if n.get('unread'))}" if any(n.get('unread') for n in st.session_state.notifications) else ""), key="nb"): goto("notifications")
            with c7:
                if st.button("⚙️ ADMIN", key="na"): goto("admin")
            with c8:
                if st.button("👤", key="npr"): goto("profile")
        else:
            c0,c1,c2,c3,c4,c5,c6,c7 = st.columns([1.5,.9,.9,.9,.9,1.2,.7,.5])
            with c6:
                unread = sum(1 for n in st.session_state.notifications if n.get("unread"))
                if st.button("🔔" + (f" {unread}" if unread else ""), key="nb"): goto("notifications")
            with c7:
                if st.button("👤", key="npr"): goto("profile")

        with c1:
            if st.button("DASHBOARD",   key="nd"): goto("dashboard")
        with c2:
            if st.button("PORTFOLIO",   key="np"): goto("portfolio")
        with c3:
            if st.button("JOURNAL",     key="nj"): goto("journal")
        with c4:
            if st.button("HISTORY",     key="nh"): goto("history")
        with c5:
            if st.button("LEADERBOARD", key="nl"): goto("leaderboard")

    else:
        c1,c2,c3 = st.columns([5,1,1])
        with c2:
            if st.button("LEADERBOARD", key="nl2"): goto("leaderboard")
        with c3:
            if st.button("LOGIN", key="nl3"): goto("auth")

def footer():
    st.markdown("""
    <div class="ak-footer">
      <div style="display:flex;align-items:center;justify-content:center;gap:.8rem;margin-bottom:.8rem;">
        <img src="https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.png"
             onerror="this.style.display='none'"
             style="height:28px;width:28px;object-fit:contain;border-radius:4px;opacity:.7;" />
        <b>AKFUNDED</b>
      </div>
      Built & Designed by <b>Akash Injeti</b>
      &nbsp;·&nbsp; Simulate. Prove. Get Funded.
      &nbsp;·&nbsp; <span style="color:#444;">Risk Disclosure: AKFunded is a simulated trading platform. All accounts are demo accounts.</span>
    </div>""", unsafe_allow_html=True)

def sec(title, sub=""):
    st.markdown(f"""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;margin-bottom:.2rem;color:#E8E8E8;">{title}</div>
    {"<div style='color:#666;font-size:.85rem;margin-bottom:1.5rem;'>"+sub+"</div>" if sub else ""}
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HOME — PREMIUM PROP FIRM LANDING
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    nav()

    # ── HERO ──
    st.markdown("""
    <div class="hero-v2">
      <div style="display:flex;justify-content:center;margin-bottom:1.5rem;">
        <img src="https://raw.githubusercontent.com/Akashinjeti/akfunded/main/logo.png"
             onerror="this.style.display='none'"
             style="height:70px;width:70px;object-fit:contain;border-radius:12px;" />
      </div>
      <div class="eyebrow">⚡ The World's Premier Prop Trading Firm</div>
      <h1>TRADE OUR<br><em>CAPITAL.</em></h1>
      <p class="sub">Pass the challenge. Get funded up to $200,000.<br>Keep up to 90% of your profits. Join 3,500+ funded traders worldwide.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("🚀 START CHALLENGE", use_container_width=True): goto("plans")

    # ── LIVE STATS ──
    st.markdown("""
    <div class="hstats" style="margin-top:2rem;">
      <div class="hstat"><span class="n">$2M+</span><span class="l">Total Payouts</span></div>
      <div class="hstat"><span class="n">3,500+</span><span class="l">Funded Traders</span></div>
      <div class="hstat"><span class="n">180+</span><span class="l">Countries</span></div>
      <div class="hstat"><span class="n">90%</span><span class="l">Profit Split</span></div>
      <div class="hstat"><span class="n">24hr</span><span class="l">Payouts</span></div>
    </div>""", unsafe_allow_html=True)

    # ── CHALLENGE TYPES ──
    st.markdown("""
    <div style="text-align:center;margin:3rem 0 1.5rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:4px;color:#E8E8E8;">CHOOSE YOUR PROGRAM</div>
      <div style="color:#555;font-size:.88rem;">Two paths to getting funded — pick what suits your style</div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div style="background:var(--s1);border:2px solid var(--border);border-radius:18px;padding:2rem;height:100%;">
          <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:rgba(240,180,41,.1);border:1px solid var(--gold-dim);border-radius:10px;padding:.6rem 1rem;">
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;color:var(--gold);letter-spacing:2px;">ONE-PHASE</div>
            </div>
            <div style="font-size:.75rem;color:#555;letter-spacing:1px;">Faster path to funding</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Profit Target</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">8%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Max Drawdown</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">8%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Daily Loss</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">4%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Profit Split</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--gold);">80%</div>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:.5rem;margin-bottom:1.5rem;">
            <div style="font-size:.82rem;color:#666;">✅ 1 phase only — faster funding</div>
            <div style="font-size:.82rem;color:#666;">✅ $10K – $200K account sizes</div>
            <div style="font-size:.82rem;color:#666;">✅ Forex, Indices, Crypto, Commodities</div>
            <div style="font-size:.82rem;color:#666;">✅ MT5 / cTrader compatible</div>
            <div style="font-size:.82rem;color:#666;">✅ No time limit</div>
          </div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;color:#555;letter-spacing:2px;margin-bottom:.3rem;">STARTING FROM</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#E8E8E8;letter-spacing:2px;">$119</div>
        </div>""", unsafe_allow_html=True)
        if st.button("GET ONE-PHASE →", use_container_width=True, key="h_1p"):
            st.session_state["selected_phase"] = "one"
            goto("plans")

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(160deg,#0d0b1a,var(--s1));border:2px solid #6C5CE7;border-radius:18px;padding:2rem;height:100%;position:relative;overflow:hidden;">
          <div style="position:absolute;top:1rem;right:1rem;background:#6C5CE7;color:#fff;font-size:.6rem;font-weight:800;padding:3px 10px;border-radius:20px;letter-spacing:1.5px;">BEST VALUE</div>
          <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:rgba(108,92,231,.15);border:1px solid #6C5CE7;border-radius:10px;padding:.6rem 1rem;">
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;color:#6C5CE7;letter-spacing:2px;">TWO-PHASE</div>
            </div>
            <div style="font-size:.75rem;color:#555;letter-spacing:1px;">Higher split, lower cost</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Phase 1 Target</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">8%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Phase 2 Target</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--green);">5%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Max Drawdown</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--red);">10%</div>
            </div>
            <div style="background:var(--s2);border-radius:10px;padding:.8rem 1rem;">
              <div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Profit Split</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#6C5CE7;">90%</div>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:.5rem;margin-bottom:1.5rem;">
            <div style="font-size:.82rem;color:#666;">✅ 90% profit split (highest tier)</div>
            <div style="font-size:.82rem;color:#666;">✅ Cheaper entry fees</div>
            <div style="font-size:.82rem;color:#666;">✅ $10K – $200K account sizes</div>
            <div style="font-size:.82rem;color:#666;">✅ Scale up to $2,000,000</div>
            <div style="font-size:.82rem;color:#666;">✅ 24-hour payouts</div>
          </div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;color:#555;letter-spacing:2px;margin-bottom:.3rem;">STARTING FROM</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#E8E8E8;letter-spacing:2px;">$49</div>
        </div>""", unsafe_allow_html=True)
        if st.button("GET TWO-PHASE →", use_container_width=True, key="h_2p"):
            st.session_state["selected_phase"] = "two"
            goto("plans")

    # ── HOW IT WORKS ──
    st.markdown("""
    <div style="text-align:center;margin:3rem 0 1rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:4px;color:#E8E8E8;">HOW IT WORKS</div>
      <div style="color:#555;font-size:.88rem;">From signup to funded in as little as 1 day</div>
    </div>
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-num">01</div>
        <div class="step-title">CHOOSE A PLAN</div>
        <div class="step-desc">Pick One-Phase or Two-Phase. Select your account size from $10K to $200K. Pay once, no subscriptions.</div>
      </div>
      <div class="step-card">
        <div class="step-num">02</div>
        <div class="step-title">PASS THE CHALLENGE</div>
        <div class="step-desc">Hit the profit target while respecting drawdown limits. Trade any instrument — Forex, Crypto, Indices, Commodities.</div>
      </div>
      <div class="step-card">
        <div class="step-num">03</div>
        <div class="step-title">GET FUNDED</div>
        <div class="step-desc">Pass verification and receive your funded account. Real capital, real rules, real payouts within 24 hours.</div>
      </div>
      <div class="step-card">
        <div class="step-num">04</div>
        <div class="step-title">SCALE UP</div>
        <div class="step-desc">Keep up to 90% of profits. Scale your account up to $2,000,000 as you consistently perform.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── TESTIMONIALS ──
    st.markdown("""
    <div style="text-align:center;margin:3rem 0 1rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:4px;color:#E8E8E8;">FUNDED TRADERS</div>
      <div style="color:#555;font-size:.88rem;">Real traders. Real payouts. Real results.</div>
    </div>
    <div class="testi-grid">
      <div class="testi-card">
        <div class="testi-quote">"Passed the $100K One-Phase challenge in 6 days. Withdrawal processed within 24 hours. AKFunded is the real deal."</div>
        <div class="testi-name">Rahul S. 🇮🇳</div>
        <div class="testi-meta">$100K Funded · +$8,200 payout · One-Phase</div>
      </div>
      <div class="testi-card">
        <div class="testi-quote">"The Two-Phase program gave me 90% profit split. Best value in the prop firm space. Already on my second account."</div>
        <div class="testi-name">Priya M. 🇮🇳</div>
        <div class="testi-meta">$50K Funded · +$4,500 payout · Two-Phase</div>
      </div>
      <div class="testi-card">
        <div class="testi-quote">"Transparent rules, fast payouts, and real support. AKFunded treats traders like professionals, not just customers."</div>
        <div class="testi-name">Kiran T. 🇮🇳</div>
        <div class="testi-meta">$25K Funded · 3 challenges completed</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("⚡ START NOW", use_container_width=True, key="cta2"): goto("plans")

    footer()
# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "auth":
    nav()
    st.markdown("<br>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,1.1,1])
    with col:
        st.markdown("""
        <div style="background:var(--s1);border:1px solid var(--border);border-radius:18px;padding:2.5rem 2rem 1rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;color:#E8E8E8;">JOIN AKFUNDED</div>
          <div style="color:#666;font-size:.85rem;margin-bottom:1.8rem;">Sign in or create your trader profile</div>
        </div>""", unsafe_allow_html=True)

        t1,t2 = st.tabs(["  SIGN IN  ","  SIGN UP  "])

        with t1:
            email = st.text_input("Email", placeholder="you@email.com", key="si_e")
            pwd   = st.text_input("Password", type="password", placeholder="••••••••", key="si_p")
            if st.button("SIGN IN →", use_container_width=True, key="si_btn"):
                if not email or not pwd:
                    st.warning("Please enter your email and password.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        uid = res.user.id

                        # Auto-create profile if missing (handles old accounts)
                        prof = db_get_profile(uid)
                        if not prof:
                            db_save_profile(uid, email.split("@")[0], email, "India")
                            prof = db_get_profile(uid)

                        st.session_state.user = {
                            "id":    uid,
                            "email": res.user.email,
                            "name":  prof.get("name", email.split("@")[0]) if prof else email.split("@")[0]
                        }
                        st.success("✅ Welcome back!")
                        time.sleep(0.5)
                        goto("dashboard")
                    except Exception as e:
                        err = str(e)
                        if "Email not confirmed" in err:
                            st.error("📧 Please verify your email first — check your inbox.")
                        elif "Invalid login credentials" in err:
                            st.error("❌ Wrong email or password. Try again.")
                        else:
                            st.error(f"❌ {err}")

        with t2:
            name    = st.text_input("Full Name", placeholder="Akash Injeti", key="su_n")
            email2  = st.text_input("Email", placeholder="you@email.com", key="su_e")
            pwd2    = st.text_input("Password", type="password", placeholder="Min 6 characters", key="su_p")
            country = st.selectbox("Country", ["🇮🇳 India","🇺🇸 USA","🇬🇧 UK","🇦🇪 UAE","🇸🇬 Singapore","Other"])

            if st.button("CREATE ACCOUNT →", use_container_width=True, key="su_btn"):
                if not name or not email2 or not pwd2:
                    st.warning("Please fill in all fields.")
                elif len(pwd2) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": email2, "password": pwd2})
                        uid = res.user.id
                        c_str = country.split(" ",1)[-1]
                        db_save_profile(uid, name, email2, c_str)
                        st.session_state.user = {"id": uid, "email": email2, "name": name}
                        # Try to sign in immediately (works if email confirm is disabled)
                        try:
                            res2 = supabase.auth.sign_in_with_password({"email": email2, "password": pwd2})
                            st.success("✅ Account created! Taking you to plans...")
                            time.sleep(1)
                            goto("plans")
                        except:
                            st.success("✅ Account created! Check your email to verify, then sign in.")
                    except Exception as e:
                        err = str(e)
                        if "already registered" in err or "already exists" in err:
                            st.error("❌ Email already registered. Please sign in instead.")
                        else:
                            st.error(f"❌ {err}")

    footer()

# ══════════════════════════════════════════════════════════════
# PLANS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "plans":
    if not st.session_state.user: goto("auth")
    nav()
    name = st.session_state.user.get("name","Trader")

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:2rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:3px;color:#E8E8E8;">
        CHOOSE YOUR CHALLENGE, {name.upper()} 👋
      </div>
      <div style="color:#666;font-size:.88rem;margin-top:.3rem;">
        One-time fee · No subscription · Trade your way to funding
      </div>
    </div>""", unsafe_allow_html=True)

    # Phase selector
    default_tab = 1 if st.session_state.get("selected_phase") == "two" else 0
    tab1, tab2 = st.tabs(["  ⚡ ONE-PHASE CHALLENGE  ", "  🔥 TWO-PHASE CHALLENGE  "])

    def render_plan_card(plan, phase):
        r   = RULES.get(plan["slug"], RULES["1phase_10k"])
        hot = plan["capital"] == 100000
        border  = "var(--gold)" if hot else "var(--border)"
        bg      = "background:linear-gradient(160deg,#130f00,var(--s1));" if hot else ""
        badge   = '<div style="position:absolute;top:1rem;right:1rem;background:var(--gold);color:#000;font-size:.55rem;font-weight:800;padding:3px 10px;border-radius:20px;letter-spacing:1.5px;">POPULAR</div>' if hot else ""
        split_c = "#6C5CE7" if phase == 2 else "var(--gold)"

        if phase == 0:  # Instant Funded
            rules_html = f"""
            <li><span>Access</span><b style="color:var(--cyan);">Immediate</b></li>
            <li><span>Daily Loss Limit</span><b style="color:var(--red);">-{r['daily_loss']}%</b></li>
            <li><span>Max Drawdown</span><b style="color:var(--red);">-{r['total_loss']}%</b></li>
            <li><span>Challenge Required</span><b style="color:var(--green);">None</b></li>
            <li><span>Profit Split</span><b style="color:{sc};">{split}%</b></li>
            <li><span>Leverage</span><b>1:100</b></li>"""
        elif phase == 1:
            rules_html = f"""
            <li><span>Profit Target</span><b style="color:var(--green);">+{r['target']}%</b></li>
            <li><span>Max Daily Loss</span><b style="color:var(--red);">-{r['daily_loss']}%</b></li>
            <li><span>Max Drawdown</span><b style="color:var(--red);">-{r['total_loss']}%</b></li>
            <li><span>Min Trading Days</span><b>{r['min_days']} days</b></li>
            <li><span>Profit Split</span><b style="color:{split_c};">80%</b></li>
            <li><span>Leverage</span><b>1:100</b></li>"""
        else:
            rules_html = f"""
            <li><span>Phase 1 Target</span><b style="color:var(--green);">+8%</b></li>
            <li><span>Phase 2 Target</span><b style="color:var(--green);">+5%</b></li>
            <li><span>Max Daily Loss</span><b style="color:var(--red);">-{r['daily_loss']}%</b></li>
            <li><span>Max Drawdown</span><b style="color:var(--red);">-{r['total_loss']}%</b></li>
            <li><span>Profit Split</span><b style="color:{split_c};">90%</b></li>
            <li><span>Leverage</span><b>1:100</b></li>"""

        st.markdown(f"""
        <div style="background:var(--s1);{bg}border:2px solid {border};border-radius:18px;
                    padding:1.8rem;position:relative;overflow:hidden;">
          {badge}
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:3px;
                      color:#555;margin-bottom:.3rem;">ACCOUNT SIZE</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:var(--gold);
                      letter-spacing:2px;line-height:1;margin-bottom:1.2rem;">{plan['name']}</div>
          <ul class="plan-rules" style="margin-bottom:1.2rem;">
            {rules_html}
          </ul>
          <div style="border-top:1px solid var(--border);padding-top:1rem;">
            <div style="font-size:.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">One-time fee</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#E8E8E8;letter-spacing:2px;">
              ${plan['price']}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.button(f"START ${plan['price']} CHALLENGE", key=f"buy_{plan['slug']}", use_container_width=True):
            rz = st.secrets.get("RAZORPAY_KEY_ID","rzp_test_placeholder")
            # Convert USD to INR approx for Razorpay (1 USD ≈ 84 INR)
            inr_amount = plan['price'] * 84 * 100
            st.markdown(f"""
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <script>
              var rzp=new Razorpay({{
                key:"{rz}", amount:{inr_amount}, currency:"INR",
                name:"AKFunded", description:"{plan['name']} {['One','Two'][phase-1]}-Phase Challenge",
                prefill:{{email:"{st.session_state.user.get('email','')}"}},
                theme:{{color:"#F0B429"}},
                handler:function(r){{alert("✅ Payment successful! Challenge activated.");}}
              }});rzp.open();
            </script>""", unsafe_allow_html=True)
            uid  = st.session_state.user["id"]
            ch   = supabase.table("challenges").insert({
                "user_id":uid, "plan":plan["slug"],
                "capital":plan["capital"], "status":"active"
            }).execute()
            ch_id = ch.data[0]["id"]
            supabase.table("accounts").insert({
                "user_id":uid, "challenge_id":ch_id,
                "balance":plan["capital"], "initial_capital":plan["capital"],
                "daily_loss":0, "total_loss":0, "days_traded":0
            }).execute()
            st.success(f"✅ {plan['name']} {['One','Two'][phase-1]}-Phase Challenge activated!")
            st.session_state.pop("selected_phase", None)
            time.sleep(1)
            goto("dashboard")

    with tab_if:
        st.markdown('''<div style="background:rgba(0,200,224,.04);border:1px solid rgba(0,200,224,.25);border-left:2px solid var(--cyan);padding:1rem 1.4rem;margin-bottom:1.5rem;">
          <div style="font-size:.72rem;color:var(--cyan);font-weight:700;letter-spacing:.5px;margin-bottom:.3rem;">⚡ No Challenge Required — Funded Immediately</div>
          <div style="font-size:.75rem;color:var(--dim);line-height:1.7;">Pay once and receive your funded account instantly. Stricter rules apply: 3% daily loss, 6% max drawdown. Higher fees compensate for immediate capital access with no evaluation phase.</div>
        </div>''', unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_IF):
            with cols[i]: render_plan_card(plan, 0)

    with tab1:
        st.markdown("""
        <div style="background:rgba(240,180,41,.05);border:1px solid var(--gold-dim);border-radius:12px;
                    padding:1rem 1.5rem;margin:.5rem 0 1.5rem;display:flex;gap:2rem;flex-wrap:wrap;">
          <span style="font-size:.82rem;color:#888;">✅ Single phase &nbsp;·&nbsp; ✅ Faster funding &nbsp;·&nbsp;
          ✅ 80% profit split &nbsp;·&nbsp; ✅ No time limit &nbsp;·&nbsp; ✅ 24hr payouts</span>
        </div>""", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_1P):
            with cols[i]:
                render_plan_card(plan, 1)

    with tab2:
        st.markdown("""
        <div style="background:rgba(108,92,231,.05);border:1px solid #6C5CE7;border-radius:12px;
                    padding:1rem 1.5rem;margin:.5rem 0 1.5rem;display:flex;gap:2rem;flex-wrap:wrap;">
          <span style="font-size:.82rem;color:#888;">✅ 90% profit split &nbsp;·&nbsp; ✅ Lower fees &nbsp;·&nbsp;
          ✅ Two verification phases &nbsp;·&nbsp; ✅ Scale to $2M &nbsp;·&nbsp; ✅ 24hr payouts</span>
        </div>""", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, plan in enumerate(PLANS_2P):
            with cols[i]:
                render_plan_card(plan, 2)

    # Compare table
    st.markdown("""
    <br>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:3px;color:#555;margin-bottom:1rem;">
      COMPARE PROGRAMS
    </div>
    <div style="background:var(--s1);border:1px solid var(--border);border-radius:14px;overflow:hidden;">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:.8rem 1.2rem;
                  background:var(--s2);font-size:.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">
        <span>FEATURE</span><span style="text-align:center;">ONE-PHASE</span><span style="text-align:center;">TWO-PHASE</span>
      </div>""", unsafe_allow_html=True)

    rows = [
        ("Entry Fee", "$119 – $799", "$49 – $449"),
        ("Profit Target", "8%", "8% + 5%"),
        ("Max Drawdown", "8%", "10%"),
        ("Profit Split", "80%", "90%"),
        ("Phases", "1", "2"),
        ("Time Limit", "None", "None"),
        ("Payout Speed", "24 hours", "24 hours"),
        ("Scale Up To", "$2,000,000", "$2,000,000"),
        ("Platforms", "MT5, cTrader", "MT5, cTrader"),
    ]
    for feat, v1, v2 in rows:
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:.7rem 1.2rem;
                    border-top:1px solid var(--border2);font-size:.82rem;">
          <span style="color:#888;">{feat}</span>
          <span style="text-align:center;color:#E8E8E8;font-weight:500;">{v1}</span>
          <span style="text-align:center;color:#6C5CE7;font-weight:500;">{v2}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.user: goto("auth")
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")

    challenge = db_get_active_challenge(uid)
    account   = db_get_account(challenge["id"]) if challenge else None

    if not challenge or not account:
        st.markdown(f"""
        <div style="text-align:center;padding:5rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:4px;color:#E8E8E8;">WELCOME, {name.upper()} 👋</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:3px;color:#444;margin:.5rem 0;">NO ACTIVE CHALLENGE</div>
          <div style="color:#555;margin-bottom:2.5rem;">Buy a challenge plan to start trading with simulated capital</div>
        </div>""", unsafe_allow_html=True)
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("🚀 BUY A CHALLENGE", use_container_width=True): goto("plans")
        footer(); st.stop()

    balance  = float(account.get("balance", 0))
    initial  = float(account.get("initial_capital", 1))
    pnl      = balance - initial
    pnl_pct  = (pnl / initial) * 100
    days     = int(account.get("days_traded", 0))
    r        = RULES.get(challenge["plan"], RULES["pro"])
    all_trades = db_get_trades(uid, challenge["id"], limit=500)
    wr,ap,bt,wt,tt = compute_stats(all_trades)

    pc="g" if pnl>=0 else "r"; ps="+" if pnl>=0 else ""
    tc="g" if pnl_pct>=r["target"] else "o"
    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">
      <div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:3px;color:#E8E8E8;">TRADING DASHBOARD</div>
        <div style="color:#666;font-size:.85rem;">Welcome back, <b style="color:#E8E8E8;">{name}</b></div>
      </div>
      <div style="display:flex;gap:.8rem;align-items:center;">
        <div style="background:linear-gradient(135deg,#F0B429,#c88a00);color:#000;font-weight:800;font-size:.72rem;padding:7px 18px;border-radius:20px;letter-spacing:1.5px;">
          ⚡ {challenge['plan'].upper()} CHALLENGE
        </div>
        <div style="background:var(--s1);border:1px solid var(--border);color:#666;font-size:.7rem;padding:7px 14px;border-radius:20px;letter-spacing:1px;">
          Day {days} of {r['min_days']}
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
      <div class="m-card"><div class="m-label">Account Balance</div><div class="m-val o">₹{balance:,.0f}</div><div class="m-sub">Started: ₹{initial:,.0f}</div></div>
      <div class="m-card"><div class="m-label">Total P&L</div><div class="m-val {pc}">{ps}₹{pnl:,.0f}</div><div class="m-sub">{ps}{pnl_pct:.2f}% return</div></div>
      <div class="m-card"><div class="m-label">Profit Target</div><div class="m-val {tc}">+{r['target']}%</div><div class="m-sub">{ps}{pnl_pct:.2f}% achieved</div></div>
      <div class="m-card"><div class="m-label">Days Traded</div><div class="m-val w">{days} <span style="font-size:1rem;color:#444;">/ {r['min_days']}</span></div><div class="m-sub">Min {r['min_days']} days required</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
      <div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>
      <div class="stat-box"><div class="sv {apc}">{aps}₹{ap:,.0f}</div><div class="sl">Avg P&L</div></div>
      <div class="stat-box"><div class="sv g">+₹{bt:,.0f}</div><div class="sl">Best Trade</div></div>
      <div class="stat-box"><div class="sv r">₹{wt:,.0f}</div><div class="sl">Worst Trade</div></div>
    </div>""", unsafe_allow_html=True)

    profit_prog = min((pnl_pct/r["target"])*100, 100) if r["target"] else 0
    dl_limit = initial*r["daily_loss"]/100
    tl_limit = initial*r["total_loss"]/100
    dl_used  = min(abs(account.get("daily_loss",0))/dl_limit*100, 100) if dl_limit else 0
    tl_used  = min(abs(account.get("total_loss",0))/tl_limit*100, 100) if tl_limit else 0
    def pbar(pct,col): return f'<div class="prog"><div class="prog-fill" style="width:{pct:.1f}%;background:{col};"></div></div>'
    dl_cls = "bad" if dl_used>75 else "ok"
    tl_cls = "bad" if tl_used>75 else "ok"

    st.markdown(f"""
    <div class="rules-box">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:1.2rem;">CHALLENGE RULES TRACKER</div>
      <div class="r-row"><span class="r-name">🎯 Profit Target +{r['target']}%</span><span class="r-val ok">{pnl_pct:.2f}% / +{r['target']}% {'✅' if profit_prog>=100 else ''}</span></div>
      {pbar(profit_prog, 'var(--green)' if profit_prog>=100 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">📉 Max Daily Loss -{r['daily_loss']}%</span><span class="r-val {dl_cls}">{dl_used:.1f}% of limit used</span></div>
      {pbar(dl_used, 'var(--red)' if dl_used>75 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">🚫 Max Total Loss -{r['total_loss']}%</span><span class="r-val {tl_cls}">{tl_used:.1f}% of limit used</span></div>
      {pbar(tl_used, 'var(--red)' if tl_used>75 else 'var(--gold)')}
    </div>""", unsafe_allow_html=True)

    col_chart, col_trade = st.columns([2, 1], gap="medium")
    with col_chart:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.5rem;">📊 LIVE CHART — TRADINGVIEW</div>', unsafe_allow_html=True)
        mkt      = st.selectbox("Market", list(SYMBOLS.keys()), key="mkt")
        sym_list = SYMBOLS[mkt]
        sym_pick = st.selectbox("Symbol", sym_list, key="csym")
        tv_sym   = TV_SYMBOL_MAP.get(sym_pick, TV_PREFIX.get(mkt,"FX:") + sym_pick)
        st.components.v1.html(f"""
        <div style="height:400px;width:100%;border-radius:12px;overflow:hidden;">
          <div id="tvc" style="height:100%;width:100%;"></div>
          <script src="https://s3.tradingview.com/tv.js"></script>
          <script>new TradingView.widget({{width:"100%",height:400,symbol:"{tv_sym}",interval:"15",timezone:"Asia/Kolkata",theme:"dark",style:"1",locale:"en",toolbar_bg:"#111",enable_publishing:false,container_id:"tvc",backgroundColor:"#070707",gridColor:"rgba(34,34,34,0.6)"}});</script>
        </div>""", height=410)

    with col_trade:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.5rem;">⚡ PLACE TRADE</div>', unsafe_allow_html=True)
        t_sym   = st.selectbox("Symbol", sym_list, key="tsym")
        t_dir   = st.selectbox("Direction", ["BUY 📈","SELL 📉"], key="ttype")
        t_entry = st.number_input("Entry Price (₹)", min_value=0.01, value=100.0, step=0.5, key="tentry")
        t_qty   = st.number_input("Quantity / Lots", min_value=1, value=10, step=1, key="tqty")
        t_exit  = st.number_input("Exit Price (₹)", min_value=0.01, value=105.0, step=0.5, key="texit")
        ttype   = "BUY" if "BUY" in t_dir else "SELL"
        est     = (t_exit-t_entry)*t_qty if ttype=="BUY" else (t_entry-t_exit)*t_qty
        ec      = "var(--green)" if est>=0 else "var(--red)"
        es      = "+" if est>=0 else ""
        roi     = (est/(t_entry*t_qty))*100 if (t_entry*t_qty)>0 else 0
        st.markdown(f"""
        <div style="background:var(--s2);border:1px solid {ec};border-radius:10px;padding:1rem;margin:.8rem 0;text-align:center;">
          <div style="font-size:.6rem;color:#555;letter-spacing:2px;margin-bottom:2px;">ESTIMATED P&L</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;color:{ec};letter-spacing:2px;line-height:1;">{es}₹{est:,.0f}</div>
          <div style="font-size:.72rem;color:{ec};margin-top:2px;">{es}{roi:.2f}% ROI</div>
        </div>""", unsafe_allow_html=True)
        if st.button("⚡ EXECUTE TRADE", use_container_width=True, key="exec"):
            ch_id=challenge["id"]; new_bal=balance+est; new_tl=min(0.0,new_bal-initial); new_days=days+1
            supabase.table("trades").insert({"user_id":uid,"challenge_id":ch_id,"symbol":t_sym,"type":ttype,"entry_price":t_entry,"exit_price":t_exit,"quantity":t_qty,"pnl":est,"closed_at":datetime.utcnow().isoformat()}).execute()
            supabase.table("accounts").update({"balance":new_bal,"total_loss":new_tl,"days_traded":new_days,"updated_at":datetime.utcnow().isoformat()}).eq("challenge_id",ch_id).execute()
            new_pct=((new_bal-initial)/initial)*100
            if new_pct>=r["target"] and new_days>=r["min_days"]:
                supabase.table("challenges").update({"status":"passed"}).eq("id",ch_id).execute()
                push_notification(uid,"🏆","CHALLENGE PASSED!",f"You hit +{r['target']}% profit target on your {challenge['plan'].upper()} challenge. Funded badge unlocked!")
                st.balloons(); st.success("🏆 CHALLENGE PASSED! Funded badge unlocked! 🎉")
            elif new_pct<=-r["total_loss"]:
                supabase.table("challenges").update({"status":"failed"}).eq("id",ch_id).execute()
                push_notification(uid,"❌","Challenge Failed",f"Max total loss of -{r['total_loss']}% hit on your {challenge['plan'].upper()} challenge.")
                st.error("❌ Challenge FAILED — max total loss hit.")
            else:
                push_notification(uid,"⚡","Trade Executed",f"{ttype} {t_sym} — P&L: {es}₹{est:,.0f}")
                st.success(f"✅ Trade done! P&L: {es}₹{est:,.0f}") if est>=0 else st.warning(f"⚠️ Trade done! P&L: ₹{est:,.0f}")
            time.sleep(1); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.6rem;">📋 RECENT TRADES</div>', unsafe_allow_html=True)
    trades = db_get_trades(uid, challenge["id"], limit=20)
    if trades:
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);border-radius:12px;overflow:hidden;">', unsafe_allow_html=True)
        st.markdown('<div class="t-header"><span>SYMBOL</span><span>TYPE</span><span>ENTRY</span><span>EXIT</span><span>QTY</span><span>P&L</span></div>', unsafe_allow_html=True)
        for t in trades:
            p=t.get("pnl",0); pc3="var(--green)" if p>=0 else "var(--red)"; ps3="+" if p>=0 else ""
            tag='<span class="tag-b">BUY</span>' if t.get("type")=="BUY" else '<span class="tag-s">SELL</span>'
            st.markdown(f'<div class="t-row"><span style="font-weight:600;">{t.get("symbol","")}</span>{tag}<span>₹{t.get("entry_price",0):,.1f}</span><span>₹{t.get("exit_price",0):,.1f}</span><span>{t.get("quantity",0)}</span><span style="color:{pc3};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps3}₹{p:,.0f}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:2.5rem;color:#444;background:var(--s1);border:1px solid var(--border);border-radius:12px;">No trades yet — place your first trade above! 📈</div>', unsafe_allow_html=True)

    # ── QUICK TOOLS ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">⚡ QUICK TOOLS</div>', unsafe_allow_html=True)
    tc1,tc2,tc3,tc4 = st.columns(4)
    with tc1:
        if st.button("🤖 AI Coach",       use_container_width=True, key="qt_ai"):   goto("ai_chat")
    with tc2:
        if st.button("🧮 Risk Calc",      use_container_width=True, key="qt_rc"):   goto("risk_calc")
    with tc3:
        if st.button("🏆 Certificate",    use_container_width=True, key="qt_cert"): goto("certificate")
    with tc4:
        if st.button("🎁 Refer & Earn",   use_container_width=True, key="qt_ref"):  goto("referral")

    footer()

# ══════════════════════════════════════════════════════════════
# PORTFOLIO
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "portfolio":
    if not st.session_state.user: goto("auth")
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")
    sec("PORTFOLIO OVERVIEW", f"{name}'s performance across all challenges")

    all_trades     = db_get_trades(uid, limit=500)
    all_challenges = db_get_all_challenges(uid)
    wr,ap,bt,wt,tt = compute_stats(all_trades)
    passed = sum(1 for c in all_challenges if c.get("status")=="passed")
    failed = sum(1 for c in all_challenges if c.get("status")=="failed")

    wrc="g" if wr>=50 else "r"; apc="g" if ap>=0 else "r"; aps="+" if ap>=0 else ""
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
      <div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>
      <div class="stat-box"><div class="sv {apc}">{aps}₹{ap:,.0f}</div><div class="sl">Avg P&L</div></div>
      <div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed ✅</div></div>
      <div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed ❌</div></div>
    </div>""", unsafe_allow_html=True)

    # Active challenge
    challenge = db_get_active_challenge(uid)
    account   = db_get_account(challenge["id"]) if challenge else None
    if challenge and account:
        bal=account["balance"]; init=account["initial_capital"]
        p=bal-init; pp=(p/init)*100; r=RULES.get(challenge["plan"],RULES["pro"])
        pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
        st.markdown(f"""
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">ACTIVE CHALLENGE</div>
        <div style="background:linear-gradient(135deg,#130f00,var(--s1));border:2px solid var(--gold);border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;">
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;">
            <div><div style="font-size:.62rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Plan</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--gold);">{challenge['plan'].upper()}</div></div>
            <div><div style="font-size:.62rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Balance</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#E8E8E8;">₹{bal:,.0f}</div></div>
            <div><div style="font-size:.62rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">P&L</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:{pc};">{ps}₹{p:,.0f}</div></div>
            <div><div style="font-size:.62rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Progress</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:{'var(--green)' if pp>=r['target'] else 'var(--gold)'};">{ps}{pp:.1f}% / +{r['target']}%</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # P&L by symbol
    if all_trades:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">P&L BY SYMBOL</div>', unsafe_allow_html=True)
        sym_pnl = {}
        for t in all_trades:
            s=t.get("symbol","?"); sym_pnl[s]=sym_pnl.get(s,0)+t.get("pnl",0)
        top5 = sorted(sym_pnl.items(), key=lambda x:x[1], reverse=True)[:5]
        cols = st.columns(len(top5)) if top5 else st.columns(1)
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
    nav()
    uid = st.session_state.user["id"]
    challenge = db_get_active_challenge(uid)
    sec("📓 TRADE JOURNAL","Log your thoughts, setups and lessons after each trade")

    with st.expander("✍️ ADD NEW ENTRY", expanded=True):
        ca,cb = st.columns(2)
        with ca:
            j_sym = st.selectbox("Symbol", [s for g in SYMBOLS.values() for s in g], key="jsym")
            j_out = st.selectbox("Outcome", ["WIN 🟢","LOSS 🔴","BREAKEVEN ⚪"], key="jout")
        with cb:
            j_setup = st.text_input("Setup / Pattern", placeholder="e.g. Breakout retest", key="jsetup")
            j_emo   = st.selectbox("Emotional State", ["Calm 😌","Confident 💪","Anxious 😰","Greedy 🤑","Fearful 😨","FOMO 🚀"], key="jemo")
        j_note = st.text_area("Journal Note", placeholder="What did you see? Why did you enter? What would you do differently?", height=100, key="jnote")
        if st.button("💾 SAVE ENTRY", use_container_width=True, key="jsave"):
            if j_note.strip():
                outcome_clean = j_out.split(" ")[0].lower()
                try:
                    supabase.table("journal_entries").insert({
                        "user_id":uid,
                        "challenge_id":challenge["id"] if challenge else None,
                        "symbol":j_sym, "outcome":outcome_clean,
                        "setup":j_setup, "emotion":j_emo.split(" ")[0],
                        "note":j_note, "created_at":datetime.utcnow().isoformat()
                    }).execute()
                    st.success("✅ Journal entry saved!")
                    time.sleep(1); st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")
            else:
                st.warning("Please write a note before saving.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">PAST ENTRIES</div>', unsafe_allow_html=True)
    entries = db_get_journal(uid)
    if entries:
        for e in entries:
            out=e.get("outcome",""); tc="win" if out=="win" else ("loss" if out=="loss" else "")
            tl="WIN ✅" if out=="win" else ("LOSS ❌" if out=="loss" else "BREAKEVEN")
            dt=e.get("created_at","")[:10]
            setup_tag = f'<span class="je-tag">{e["setup"]}</span>' if e.get("setup") else ""
            st.markdown(f"""
            <div class="journal-entry">
              <div class="je-date">{dt} &nbsp;·&nbsp; {e.get('symbol','')} &nbsp;·&nbsp; {e.get('emotion','')}</div>
              <div class="je-note">{e.get('note','')}</div>
              <div class="je-tags"><span class="je-tag {tc}">{tl}</span>{setup_tag}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem;color:#444;background:var(--s1);border:1px solid var(--border);border-radius:12px;">No journal entries yet — log your first trade above! 📓</div>', unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]
    sec("📋 CHALLENGE HISTORY","All your past and active challenge attempts")

    all_ch = db_get_all_challenges(uid)
    if not all_ch:
        st.markdown('<div style="text-align:center;padding:4rem;color:#444;background:var(--s1);border:1px solid var(--border);border-radius:12px;">No challenges yet!</div>', unsafe_allow_html=True)
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("BUY A PLAN →", use_container_width=True): goto("plans")
    else:
        total=len(all_ch); passed=sum(1 for c in all_ch if c.get("status")=="passed")
        failed=sum(1 for c in all_ch if c.get("status")=="failed"); active=sum(1 for c in all_ch if c.get("status")=="active")
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;">
          <div class="stat-box"><div class="sv w">{total}</div><div class="sl">Total</div></div>
          <div class="stat-box"><div class="sv g">{passed}</div><div class="sl">Passed ✅</div></div>
          <div class="stat-box"><div class="sv r">{failed}</div><div class="sl">Failed ❌</div></div>
          <div class="stat-box"><div class="sv o">{active}</div><div class="sl">Active ⚡</div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin:.5rem 0 1rem;">ALL ATTEMPTS</div>', unsafe_allow_html=True)
        for ch in all_ch:
            acc=db_get_account(ch["id"]) or {}
            cap=ch.get("capital",0); bal=acc.get("balance",cap)
            p=bal-cap; pp=(p/cap*100) if cap else 0
            status=ch.get("status","active"); d=acc.get("days_traded",0)
            cap_str=f"₹{cap//100000}L" if cap>=100000 else f"₹{cap//1000}K"
            date_str=ch.get("started_at","")[:10]
            pc="var(--green)" if p>=0 else "var(--red)"; ps="+" if p>=0 else ""
            st.markdown(f"""
            <div class="ch-card">
              <div><div class="ch-plan">{ch.get('plan','').upper()}</div><div style="font-size:.78rem;color:#555;">{cap_str} &nbsp;·&nbsp; {date_str}</div></div>
              <div style="font-size:.85rem;">Balance: <b style="color:#E8E8E8;">₹{bal:,.0f}</b></div>
              <div style="font-size:.85rem;color:{pc};">P&L: <b>{ps}₹{p:,.0f} ({ps}{pp:.1f}%)</b></div>
              <div style="font-size:.85rem;color:#555;">Days: <b style="color:#E8E8E8;">{d}</b></div>
              <div class="ch-status {status}">{status.upper()}</div>
            </div>""", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# LEADERBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "leaderboard":
    nav()
    sec("🏆 LEADERBOARD","Top traders ranked by profit % — updated live")

    data = db_get_leaderboard()
    if not data:
        data=[
            {"name":"Rahul S.","country":"India","profit_pct":18.4,"status":"passed","plan":"elite"},
            {"name":"Priya M.","country":"India","profit_pct":15.2,"status":"passed","plan":"pro"},
            {"name":"Kiran T.","country":"India","profit_pct":12.7,"status":"active","plan":"pro"},
            {"name":"Arun K.","country":"India","profit_pct":11.1,"status":"passed","plan":"starter"},
            {"name":"Sneha R.","country":"India","profit_pct":9.8, "status":"active","plan":"pro"},
        ]
    medals=["🥇","🥈","🥉"]
    for i,t in enumerate(data):
        rank=i+1; medal=medals[i] if i<3 else f"#{rank}"
        rc="top" if rank<=3 else ""
        funded=t.get("status")=="passed"
        bc="funded-b" if funded else "active-b"; bt="FUNDED" if funded else "ACTIVE"
        profit=t.get("profit_pct",0)
        st.markdown(f"""
        <div class="lb-item">
          <div class="lb-rank {rc}">{medal}</div>
          <div class="lb-info"><div class="lb-name">{t.get('name','Trader')}</div><div class="lb-country">{t.get('country','')}</div></div>
          <div class="lb-pnl">+{profit:.2f}%</div>
          <div class="lb-badge {bc}">{bt}</div>
        </div>""", unsafe_allow_html=True)
    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: PROFILE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    if not st.session_state.user: goto("auth")
    nav()
    uid   = st.session_state.user["id"]
    email = st.session_state.user.get("email","")

    # Load full profile
    prof          = db_get_profile(uid) or {}
    name          = prof.get("name", email.split("@")[0])
    country       = prof.get("country","India")
    bio           = prof.get("bio","")
    all_challenges= db_get_all_challenges(uid)
    all_trades    = db_get_trades(uid, limit=500)
    wr,ap,bt,wt,tt= compute_stats(all_trades)
    passed        = sum(1 for c in all_challenges if c.get("status")=="passed")
    failed        = sum(1 for c in all_challenges if c.get("status")=="failed")
    funded_badge  = passed > 0
    initials      = "".join([w[0].upper() for w in name.split()[:2]])

    sec("👤 MY PROFILE","Your trader identity and career stats")

    # Hero card
    badge_html = '<div class="funded-badge">⚡ FUNDED TRADER</div>' if funded_badge else ""
    st.markdown(f"""
    <div class="profile-hero">
      <div class="profile-avatar">{initials}</div>
      <div>
        <div class="profile-name">{name.upper()}</div>
        <div class="profile-email">{email}</div>
        <div class="profile-country">🌍 {country}</div>
        {badge_html}
      </div>
      <div style="margin-left:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;text-align:center;">
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--gold);">{tt}</div><div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Trades</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{'var(--green)' if wr>=50 else 'var(--red)'};">{wr:.0f}%</div><div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Win Rate</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--green);">{passed}</div><div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Passed</div></div>
        <div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--red);">{failed}</div><div style="font-size:.62rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;">Failed</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Edit profile form
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">EDIT PROFILE</div>', unsafe_allow_html=True)
    with st.form("edit_profile"):
        c1, c2 = st.columns(2)
        with c1:
            new_name    = st.text_input("Full Name", value=name, key="pf_name")
            new_country = st.text_input("Country", value=country, key="pf_country")
        with c2:
            new_bio = st.text_area("Bio / Tagline", value=bio, placeholder="e.g. Nifty scalper. Risk manager first.", height=100, key="pf_bio")
        submitted = st.form_submit_button("💾 SAVE PROFILE", use_container_width=True)
        if submitted:
            if db_update_profile(uid, new_name, new_country, new_bio):
                st.session_state.user["name"] = new_name
                push_notification(uid,"✅","Profile Updated","Your profile has been saved successfully.")
                st.success("✅ Profile saved!")
                time.sleep(1); st.rerun()
            else:
                st.error("❌ Save failed — make sure the 'bio' column exists in your profiles table.")

    # Security section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1.1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">ACCOUNT</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="m-card">
          <div class="m-label">Email</div>
          <div style="font-size:.9rem;color:#E8E8E8;margin-top:4px;">{email}</div>
          <div class="m-sub">Supabase Auth account</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="m-card">
          <div class="m-label">Member Since</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--gold);">
            {all_challenges[-1].get('started_at','')[:7] if all_challenges else 'NEW'}
          </div>
          <div class="m-sub">First challenge date</div>
        </div>""", unsafe_allow_html=True)

    if st.button("🚪 LOGOUT", key="profile_logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.notifications = []
        goto("home")

    # ── TEST EMAIL ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">📧 EMAIL TEST</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#555;font-size:.8rem;margin-bottom:.5rem;">Send a test email to <b style="color:#E8E8E8;">{email}</b> to verify SMTP is configured correctly.</div>', unsafe_allow_html=True)
    if st.button("📧 SEND TEST EMAIL", key="test_email"):
        ok = send_email_notification(
            email,
            "✅ AKFunded Email Test",
            f"""<div style="font-family:Arial,sans-serif;background:#070707;color:#E8E8E8;padding:2rem;border-radius:12px;max-width:500px;">
              <h2 style="color:#F0B429;letter-spacing:3px;">AKFUNDED ⚡</h2>
              <h3>Email is working! ✅</h3>
              <p style="color:#666;">Hey {name}, your SMTP is configured correctly.<br>You'll receive challenge certificates and notifications here.</p>
              <p style="font-size:.75rem;color:#333;">Powered by Akash Injeti · akfunded.streamlit.app</p>
            </div>"""
        )
        if ok:
            st.success(f"✅ Test email sent to {email}! Check your inbox.")
        else:
            st.error("❌ Failed — double check SMTP_EMAIL and SMTP_PASSWORD in secrets.")

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "notifications":
    if not st.session_state.user: goto("auth")
    nav()
    uid = st.session_state.user["id"]

    sec("🔔 NOTIFICATIONS","Trade alerts, challenge updates and system messages")

    notifs = [n for n in st.session_state.notifications if n.get("uid") == uid]

    col_a, col_b = st.columns([4,1])
    with col_b:
        if st.button("✅ Mark All Read", key="mark_read"):
            for n in st.session_state.notifications:
                n["unread"] = False
            st.rerun()

    if not notifs:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#444;background:var(--s1);border:1px solid var(--border);border-radius:12px;">
          <div style="font-size:2rem;margin-bottom:.5rem;">🔔</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:2px;color:#555;">NO NOTIFICATIONS YET</div>
          <div style="font-size:.82rem;color:#444;margin-top:.5rem;">Notifications appear when you trade, pass or fail a challenge</div>
        </div>""", unsafe_allow_html=True)
    else:
        for n in notifs:
            unread_class = "unread" if n.get("unread") else ""
            st.markdown(f"""
            <div class="notif-item {unread_class}">
              <div class="notif-icon">{n.get('icon','📢')}</div>
              <div class="notif-body">
                <div class="notif-title">{n.get('title','Notification')}
                  {'<span class="notif-badge">NEW</span>' if n.get('unread') else ''}
                </div>
                <div class="notif-msg">{n.get('msg','')}</div>
                <div class="notif-time">{n.get('time','')}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":
    if not st.session_state.user: goto("auth")
    # Check admin
    is_admin = st.session_state.user.get("email","") == st.secrets.get("ADMIN_EMAIL","admin@akfunded.com")
    if not is_admin:
        st.error("❌ Access denied. Admin only.")
        st.stop()
    nav()

    sec("⚙️ ADMIN PANEL","Full platform overview — all traders and challenges")

    all_data = db_get_all_accounts()

    # Summary stats
    total_traders  = len(set(r["user_id"] for r in all_data))
    total_ch       = len(all_data)
    total_passed   = sum(1 for r in all_data if r["status"]=="passed")
    total_active   = sum(1 for r in all_data if r["status"]=="active")
    total_failed   = sum(1 for r in all_data if r["status"]=="failed")
    total_capital  = sum(r["capital"] for r in all_data)

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1rem;margin-bottom:1.5rem;">
      <div class="stat-box"><div class="sv w">{total_traders}</div><div class="sl">Traders</div></div>
      <div class="stat-box"><div class="sv w">{total_ch}</div><div class="sl">Challenges</div></div>
      <div class="stat-box"><div class="sv o">{total_active}</div><div class="sl">Active</div></div>
      <div class="stat-box"><div class="sv g">{total_passed}</div><div class="sl">Passed</div></div>
      <div class="stat-box"><div class="sv r">{total_failed}</div><div class="sl">Failed</div></div>
      <div class="stat-box"><div class="sv o">₹{total_capital//1000}K</div><div class="sl">Total Capital</div></div>
    </div>""", unsafe_allow_html=True)

    # Search/filter
    search = st.text_input("🔍 Search by name or email", placeholder="Type to filter...", key="admin_search")
    status_filter = st.selectbox("Filter by status", ["All","active","passed","failed"], key="admin_status")

    filtered = all_data
    if search:
        filtered = [r for r in filtered if search.lower() in r["name"].lower() or search.lower() in r["email"].lower()]
    if status_filter != "All":
        filtered = [r for r in filtered if r["status"] == status_filter]

    st.markdown(f'<div style="color:#555;font-size:.78rem;margin-bottom:.8rem;">{len(filtered)} results</div>', unsafe_allow_html=True)

    # Table
    st.markdown("""
    <div style="background:var(--s1);border:1px solid var(--border);border-radius:12px;overflow:hidden;">
      <div class="admin-row header">
        <span>TRADER</span><span>PLAN</span><span>BALANCE</span><span>P&L %</span><span>DAYS</span><span>STATUS</span>
      </div>""", unsafe_allow_html=True)

    for r in filtered[:50]:
        pc = "var(--green)" if r["pnl_pct"] >= 0 else "var(--red)"
        ps = "+" if r["pnl_pct"] >= 0 else ""
        cap_str = f"₹{r['capital']//100000}L" if r['capital']>=100000 else f"₹{r['capital']//1000}K"
        st.markdown(f"""
        <div class="admin-row">
          <div>
            <div style="font-weight:600;color:#E8E8E8;">{r['name']}</div>
            <div style="font-size:.7rem;color:#555;">{r['email']}</div>
          </div>
          <div style="color:var(--gold);font-weight:600;">{r['plan'].upper()} <span style="color:#555;font-size:.72rem;">({cap_str})</span></div>
          <div style="font-family:'JetBrains Mono',monospace;">₹{r['balance']:,.0f}</div>
          <div style="color:{pc};font-family:'JetBrains Mono',monospace;font-weight:700;">{ps}{r['pnl_pct']:.2f}%</div>
          <div style="color:#E8E8E8;">{r['days_traded']}</div>
          <div class="admin-status {r['status']}">{r['status'].upper()}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if len(filtered) > 50:
        st.markdown(f'<div style="color:#555;font-size:.75rem;margin-top:.5rem;text-align:center;">Showing first 50 of {len(filtered)} results</div>', unsafe_allow_html=True)

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: AI TRADING ASSISTANT
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "ai_chat":
    if not st.session_state.user: goto("auth")
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")

    # Load context
    challenge = db_get_active_challenge(uid)
    account   = db_get_account(challenge["id"]) if challenge else None
    trades    = db_get_trades(uid, challenge["id"] if challenge else None, limit=10)

    balance  = account.get("balance",0) if account else 0
    initial  = account.get("initial_capital",1) if account else 1
    pnl_pct  = ((balance-initial)/initial*100) if initial else 0
    plan     = challenge.get("plan","") if challenge else ""

    SYSTEM = f"""You are an expert AI trading coach for AKFunded, India's premier prop trading simulator.
The trader you're helping is {name}, currently on the {plan.upper()} challenge.
Their current P&L: {pnl_pct:.1f}%. Balance: ₹{balance:,.0f}.
Recent trades: {[t.get('symbol','') + ' ' + t.get('type','') + ' P&L ₹' + str(t.get('pnl',0)) for t in trades[:5]]}.

You give concise, practical trading advice. Focus on:
- Risk management and position sizing
- Reading the challenge rules wisely
- Emotional discipline and trade psychology
- Technical analysis tips for Indian markets (Nifty, BankNifty)
- When to trade and when to stay out
Keep replies under 150 words. Be direct and encouraging."""

    sec("🤖 AI TRADING ASSISTANT", f"Your personal trading coach — powered by Groq & LLaMA 3.3 70B")

    # Chat UI
    st.markdown("""
    <div class="chat-container">
      <div class="chat-header">
        <div class="chat-ai-dot"></div>
        <div>
          <div style="font-weight:600;font-size:.88rem;color:#E8E8E8;">AK Trading Coach</div>
          <div style="font-size:.7rem;color:var(--green);">Online — Powered by LLaMA 3.3 70B via Groq</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Display chat history
    chat = st.session_state.chat_history
    if not chat:
        st.markdown(f"""
        <div class="chat-messages">
          <div class="chat-msg">
            <div class="chat-avatar ai">🤖</div>
            <div class="chat-bubble ai">Hey {name}! 👋 I'm your AKFunded trading coach. I can see your current challenge data. Ask me anything — risk management, trade setups, how to handle drawdowns, or tips to pass your challenge faster!</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        msgs_html = ""
        for m in chat[-10:]:
            role  = m["role"]
            txt   = m["content"]
            cls   = "user" if role=="user" else "ai"
            av    = name[0].upper() if role=="user" else "🤖"
            msgs_html += f'<div class="chat-msg {cls}"><div class="chat-avatar {cls}">{av}</div><div class="chat-bubble {cls}">{txt}</div></div>'
        st.markdown(f'<div class="chat-messages">{msgs_html}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown('<div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.8rem;">', unsafe_allow_html=True)
    quick = ["How do I manage risk?","Should I trade today?","How to pass faster?","I'm in drawdown, help!","Best Nifty setup?"]
    qcols = st.columns(len(quick))
    for i,q in enumerate(quick):
        with qcols[i]:
            if st.button(q, key=f"qp_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Thinking..."):
                    resp = call_ai(st.session_state.chat_history, SYSTEM)
                st.session_state.chat_history.append({"role":"assistant","content":resp})
                st.rerun()

    # Input
    user_input = st.text_input("Ask your trading coach...", placeholder="e.g. I lost 3% today, what should I do?", key="chat_input", label_visibility="collapsed")
    c1,c2 = st.columns([5,1])
    with c2:
        send = st.button("SEND ➤", use_container_width=True, key="chat_send")
    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner("Coach is typing..."):
            resp = call_ai(st.session_state.chat_history, SYSTEM)
        st.session_state.chat_history.append({"role":"assistant","content":resp})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: RISK CALCULATOR
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "risk_calc":
    if not st.session_state.user: goto("auth")
    nav()
    uid      = st.session_state.user["id"]
    challenge= db_get_active_challenge(uid)
    account  = db_get_account(challenge["id"]) if challenge else None
    balance  = float(account.get("balance",100000)) if account else 100000.0

    sec("🧮 RISK CALCULATOR","Calculate position size, risk and reward before placing any trade")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">POSITION SIZE CALCULATOR</div>', unsafe_allow_html=True)
        with st.container():
            acc_size   = st.number_input("Account Balance (₹)", value=balance, min_value=1000.0, step=1000.0, key="rc_bal")
            risk_pct   = st.slider("Risk per trade (%)", 0.1, 5.0, 1.0, 0.1, key="rc_risk")
            entry_p    = st.number_input("Entry Price (₹)", value=100.0, min_value=0.01, step=0.5, key="rc_entry")
            stop_loss  = st.number_input("Stop Loss Price (₹)", value=97.0, min_value=0.01, step=0.5, key="rc_sl")
            target_p   = st.number_input("Target Price (₹)", value=106.0, min_value=0.01, step=0.5, key="rc_tp")

            risk_amt   = acc_size * risk_pct / 100
            sl_dist    = abs(entry_p - stop_loss)
            tp_dist    = abs(target_p - entry_p)
            qty        = int(risk_amt / sl_dist) if sl_dist > 0 else 0
            reward_amt = qty * tp_dist
            rr_ratio   = tp_dist / sl_dist if sl_dist > 0 else 0
            margin     = qty * entry_p

            rc = "var(--green)" if rr_ratio >= 2 else ("var(--gold)" if rr_ratio >= 1 else "var(--red)")
            st.markdown(f"""
            <div class="risk-card" style="margin-top:1rem;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div class="risk-result">
                  <div style="font-size:.62rem;color:#555;letter-spacing:2px;margin-bottom:4px;">POSITION SIZE</div>
                  <div class="risk-val" style="color:var(--gold);">{qty:,}</div>
                  <div style="font-size:.7rem;color:#555;">shares / lots</div>
                </div>
                <div class="risk-result">
                  <div style="font-size:.62rem;color:#555;letter-spacing:2px;margin-bottom:4px;">RISK AMOUNT</div>
                  <div class="risk-val" style="color:var(--red);">₹{risk_amt:,.0f}</div>
                  <div style="font-size:.7rem;color:#555;">{risk_pct}% of account</div>
                </div>
                <div class="risk-result">
                  <div style="font-size:.62rem;color:#555;letter-spacing:2px;margin-bottom:4px;">REWARD</div>
                  <div class="risk-val" style="color:var(--green);">₹{reward_amt:,.0f}</div>
                  <div style="font-size:.7rem;color:#555;">if target hit</div>
                </div>
                <div class="risk-result">
                  <div style="font-size:.62rem;color:#555;letter-spacing:2px;margin-bottom:4px;">R:R RATIO</div>
                  <div class="risk-val" style="color:{rc};">1:{rr_ratio:.1f}</div>
                  <div style="font-size:.7rem;color:#555;">{'✅ Good' if rr_ratio>=2 else '⚠️ Low' if rr_ratio>=1 else '❌ Poor'}</div>
                </div>
              </div>
              <div style="margin-top:1rem;padding:.8rem;background:var(--s2);border-radius:8px;font-size:.78rem;color:#666;">
                💰 Capital required: <b style="color:#E8E8E8;">₹{margin:,.0f}</b> &nbsp;·&nbsp;
                SL distance: <b style="color:var(--red);">₹{sl_dist:.2f}</b> &nbsp;·&nbsp;
                TP distance: <b style="color:var(--green);">₹{tp_dist:.2f}</b>
              </div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">CHALLENGE RISK LIMITS</div>', unsafe_allow_html=True)
        if challenge and account:
            r        = RULES.get(challenge["plan"], RULES["pro"])
            init     = float(account.get("initial_capital", 1))
            daily_lim= init * r["daily_loss"] / 100
            total_lim= init * r["total_loss"] / 100
            daily_rem= daily_lim - abs(account.get("daily_loss",0))
            total_rem= total_lim - abs(account.get("total_loss",0))
            trades_needed = max(0, r["min_days"] - account.get("days_traded",0))

            st.markdown(f"""
            <div class="risk-card">
              <div style="margin-bottom:1rem;">
                <div style="font-size:.65rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Daily Loss Remaining</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{'var(--green)' if daily_rem>daily_lim*0.5 else 'var(--red)'};">₹{daily_rem:,.0f}</div>
                <div style="font-size:.72rem;color:#555;">of ₹{daily_lim:,.0f} daily limit</div>
              </div>
              <div style="margin-bottom:1rem;">
                <div style="font-size:.65rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">Max Total Loss Remaining</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{'var(--green)' if total_rem>total_lim*0.5 else 'var(--red)'};">₹{total_rem:,.0f}</div>
                <div style="font-size:.72rem;color:#555;">of ₹{total_lim:,.0f} total limit</div>
              </div>
              <div>
                <div style="font-size:.65rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">More Trading Days Needed</div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--gold);">{trades_needed}</div>
                <div style="font-size:.72rem;color:#555;">days before you can pass</div>
              </div>
            </div>""", unsafe_allow_html=True)

            # Safe trade size
            safe_risk = min(daily_rem * 0.25, total_rem * 0.1)
            st.markdown(f"""
            <div style="background:rgba(0,200,150,.07);border:1px solid rgba(0,200,150,.2);border-radius:10px;padding:1rem;margin-top:1rem;">
              <div style="font-size:.7rem;color:var(--green);letter-spacing:2px;margin-bottom:4px;">💡 SAFE RISK PER TRADE TODAY</div>
              <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:var(--green);">₹{safe_risk:,.0f}</div>
              <div style="font-size:.72rem;color:#555;">Max recommended to protect daily & total limits</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#444;padding:2rem;text-align:center;background:var(--s1);border:1px solid var(--border);border-radius:12px;">Buy a challenge to see your risk limits here</div>', unsafe_allow_html=True)

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: CERTIFICATE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "certificate":
    if not st.session_state.user: goto("auth")
    nav()
    uid  = st.session_state.user["id"]
    name = st.session_state.user.get("name","Trader")
    sec("🏆 MY CERTIFICATE","Your funded trader achievement certificate")

    # Get passed challenges
    all_ch = db_get_all_challenges(uid)
    passed_ch = [c for c in all_ch if c.get("status") == "passed"]

    if not passed_ch:
        st.markdown("""
        <div style="text-align:center;padding:4rem;background:var(--s1);border:1px solid var(--border);border-radius:16px;">
          <div style="font-size:3rem;margin-bottom:1rem;">🎯</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:3px;color:#444;">NO CERTIFICATE YET</div>
          <div style="color:#555;margin-top:.5rem;">Pass a challenge to earn your funded trader certificate</div>
        </div>""", unsafe_allow_html=True)
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("BUY A CHALLENGE →", use_container_width=True): goto("plans")
    else:
        if len(passed_ch) > 1:
            ch_options = [f"{c['plan'].upper()} — {c.get('started_at','')[:10]}" for c in passed_ch]
            selected   = st.selectbox("Select Challenge", ch_options, key="cert_sel")
            ch = passed_ch[ch_options.index(selected)]
        else:
            ch = passed_ch[0]

        acc = db_get_account(ch["id"]) or {}
        cap = ch.get("capital", 0)
        bal = acc.get("balance", cap)
        pnl_pct = (bal - cap) / cap * 100 if cap else 0
        days = acc.get("days_traded", 0)
        date_str = ch.get("started_at","")[:10]

        cert_html = render_certificate(name, ch["plan"], cap, pnl_pct, days, date_str)
        st.markdown(cert_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            # Email certificate
            if st.button("📧 EMAIL MY CERTIFICATE", use_container_width=True, key="email_cert"):
                email = st.session_state.user.get("email","")
                cap_str = f"₹{cap//100000}L" if cap>=100000 else f"₹{cap//1000}K"
                html_body = f"""
                <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#070707;color:#E8E8E8;padding:2rem;border-radius:12px;">
                  <h1 style="font-size:2rem;letter-spacing:4px;color:#F0B429;text-align:center;">AKFUNDED ⚡</h1>
                  <h2 style="text-align:center;color:#E8E8E8;">🏆 Congratulations, {name}!</h2>
                  <p style="text-align:center;color:#666;">You have successfully passed the <b style="color:#F0B429;">{ch['plan'].upper()} Challenge ({cap_str})</b></p>
                  <div style="background:#111;border:1px solid #222;border-radius:12px;padding:1.5rem;margin:1.5rem 0;text-align:center;">
                    <div style="font-size:2rem;color:#00C896;font-weight:700;">+{pnl_pct:.2f}%</div>
                    <div style="color:#666;font-size:.85rem;">Profit Achieved in {days} trading days</div>
                  </div>
                  <p style="text-align:center;color:#666;">You are now a <b style="color:#F0B429;">FUNDED TRADER</b> on AKFunded.</p>
                  <p style="text-align:center;font-size:.78rem;color:#333;">Powered by Akash Injeti &nbsp;·&nbsp; akfunded.streamlit.app</p>
                </div>"""
                ok = send_email_notification(email, "🏆 Your AKFunded Certificate!", html_body)
                if ok:
                    st.success(f"✅ Certificate emailed to {email}")
                else:
                    st.info("📧 Email not configured — add SMTP_EMAIL & SMTP_PASSWORD to secrets to enable.")
        with col2:
            if st.button("📋 COPY SHARE TEXT", use_container_width=True, key="share_cert"):
                cap_str = f"₹{cap//100000}L" if cap>=100000 else f"₹{cap//1000}K"
                share = f"🏆 I just passed the AKFunded {ch['plan'].upper()} Challenge ({cap_str}) with +{pnl_pct:.1f}% profit in {days} days! 📈 #AKFunded #PropTrading #Funded"
                st.code(share)

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: REFERRAL SYSTEM
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "referral":
    if not st.session_state.user: goto("auth")
    nav()
    uid   = st.session_state.user["id"]
    name  = st.session_state.user.get("name","Trader")
    email = st.session_state.user.get("email","")
    sec("🎁 REFER & EARN","Invite traders, earn rewards when they buy a challenge")

    # Get or create referral code
    ref = db_get_referral(uid)
    if not ref:
        code = generate_referral_code(name)
        db_create_referral(uid, code)
        ref  = db_get_referral(uid) or {"code": code, "uses": 0}

    code = ref.get("code","")
    uses = ref.get("uses", 0)
    earnings = uses * 50  # ₹50 reward per referral

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#130f00,var(--s1));border:1px solid var(--gold-dim);border-radius:18px;padding:2rem;margin-bottom:1.5rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.5rem;">YOUR REFERRAL CODE</div>
      <div class="ref-code-box">
        <div class="ref-code">{code}</div>
        <div style="font-size:.72rem;color:#555;">Share this code</div>
      </div>
      <div class="ref-stats">
        <div class="stat-box"><div class="sv o">{uses}</div><div class="sl">Referrals</div></div>
        <div class="stat-box"><div class="sv g">₹{earnings}</div><div class="sl">Earned</div></div>
        <div class="stat-box"><div class="sv w">₹50</div><div class="sl">Per Referral</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Share options
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">SHARE YOUR LINK</div>', unsafe_allow_html=True)

    share_url  = f"https://akfunded.streamlit.app/?ref={code}"
    share_text = f"🚀 Join AKFunded — India's Prop Trading Simulator! Use my code {code} and prove your trading edge. Start from just ₹199. {share_url}"

    st.code(share_url, language=None)

    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("📋 COPY LINK", use_container_width=True, key="copy_link"):
            st.code(share_url)
            st.success("✅ Copy the link above!")
    with c2:
        wa_link = f"https://wa.me/?text={share_text.replace(' ','%20')}"
        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%;background:var(--gold);color:#000;font-weight:700;border:none;border-radius:8px;padding:0.55rem;font-family:DM Sans,sans-serif;cursor:pointer;letter-spacing:1px;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)
    with c3:
        if st.button("📧 EMAIL INVITE", use_container_width=True, key="email_invite"):
            html_invite = f"""
            <div style="font-family:Arial,sans-serif;max-width:600px;background:#070707;color:#E8E8E8;padding:2rem;border-radius:12px;">
              <h1 style="color:#F0B429;letter-spacing:4px;">AKFUNDED ⚡</h1>
              <h2>Hey! {name} invites you to trade 🚀</h2>
              <p style="color:#666;">Join AKFunded — India's premier prop trading simulator. Trade simulated capital, pass the challenge, earn your funded badge.</p>
              <div style="background:#111;border-radius:8px;padding:1rem;text-align:center;margin:1rem 0;">
                <div style="font-size:1.5rem;font-weight:700;color:#F0B429;letter-spacing:4px;">{code}</div>
                <div style="color:#555;font-size:.82rem;">Use this referral code</div>
              </div>
              <p style="color:#666;">Start from just ₹199. <a href="{share_url}" style="color:#F0B429;">Click here to join</a></p>
            </div>"""
            ok = send_email_notification(email, f"{name} invited you to AKFunded! 🚀", html_invite)
            if ok:
                st.success("✅ Invite sent!")
            else:
                st.info("📧 Configure SMTP_EMAIL & SMTP_PASSWORD in secrets to send emails.")

    # How referral works
    st.markdown("""
    <br>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.8rem;">HOW IT WORKS</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
      <div class="stat-box" style="text-align:left;padding:1.2rem;">
        <div style="font-size:1.5rem;margin-bottom:.5rem;">🔗</div>
        <div style="font-weight:600;margin-bottom:.3rem;color:#E8E8E8;">Share Your Code</div>
        <div style="font-size:.78rem;color:#555;">Send your unique referral code to friends who trade</div>
      </div>
      <div class="stat-box" style="text-align:left;padding:1.2rem;">
        <div style="font-size:1.5rem;margin-bottom:.5rem;">💳</div>
        <div style="font-weight:600;margin-bottom:.3rem;color:#E8E8E8;">They Buy a Plan</div>
        <div style="font-size:.78rem;color:#555;">When they purchase any challenge using your code</div>
      </div>
      <div class="stat-box" style="text-align:left;padding:1.2rem;">
        <div style="font-size:1.5rem;margin-bottom:.5rem;">💰</div>
        <div style="font-weight:600;margin-bottom:.3rem;color:#E8E8E8;">You Earn ₹50</div>
        <div style="font-size:.78rem;color:#555;">₹50 reward credited per successful referral</div>
      </div>
    </div>""", unsafe_allow_html=True)

    footer()
