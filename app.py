import streamlit as st
from supabase import create_client
import time
from datetime import datetime

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
RULES = {
    "starter": {"target":8,  "daily_loss":4, "total_loss":8,  "min_days":5},
    "pro":     {"target":10, "daily_loss":5, "total_loss":10, "min_days":5},
    "elite":   {"target":10, "daily_loss":5, "total_loss":10, "min_days":7},
}
PLANS = [
    {"name":"STARTER","capital":50000, "price":199,"slug":"starter"},
    {"name":"PRO",    "capital":100000,"price":399,"slug":"pro"},
    {"name":"ELITE",  "capital":500000,"price":799,"slug":"elite"},
]
SYMBOLS = {
    "🇮🇳 NSE Indices": ["NIFTY","BANKNIFTY","FINNIFTY","MIDCPNIFTY"],
    "🇮🇳 NSE Stocks":  ["RELIANCE","TCS","INFY","HDFCBANK","TATAMOTORS","WIPRO","SBIN","ICICIBANK","BAJFINANCE","ADANIENT"],
    "₿ Crypto":        ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT"],
    "💱 Forex":        ["EURUSD","GBPUSD","USDJPY","USDINR","AUDUSD"],
    "🥇 Commodities":  ["GOLD","SILVER","CRUDEOIL","NATURALGAS"],
}
TV_PREFIX = {
    "🇮🇳 NSE Indices":"NSE:", "🇮🇳 NSE Stocks":"NSE:",
    "₿ Crypto":"BINANCE:", "💱 Forex":"FX:", "🥇 Commodities":"TVC:"
}

# ─── SESSION STATE ──────────────────────────────────────────────
for k,v in [("user",None),("page","home")]:
    if k not in st.session_state:
        st.session_state[k] = v

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

def compute_stats(trades):
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

def goto(page):
    st.session_state.page = page
    st.rerun()

# ─── UI COMPONENTS ─────────────────────────────────────────────
def nav():
    logged_in = st.session_state.user is not None
    st.markdown("""
    <div class="ak-nav">
      <div style="display:flex;align-items:center;">
        <span class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span></span>
        <span class="ak-beta">BETA</span>
      </div>
      <div class="ak-powered">Powered by <b>Akash Injeti</b></div>
    </div>""", unsafe_allow_html=True)

    if logged_in:
        c1,c2,c3,c4,c5,c6,c7 = st.columns([2,.9,.9,.9,.9,.9,.9])
        with c2:
            if st.button("DASHBOARD",   key="nd"): goto("dashboard")
        with c3:
            if st.button("PORTFOLIO",   key="np"): goto("portfolio")
        with c4:
            if st.button("JOURNAL",     key="nj"): goto("journal")
        with c5:
            if st.button("HISTORY",     key="nh"): goto("history")
        with c6:
            if st.button("LEADERBOARD", key="nl"): goto("leaderboard")
        with c7:
            if st.button("LOGOUT",      key="nx"):
                supabase.auth.sign_out()
                st.session_state.user = None
                goto("home")
    else:
        c1,c2,c3 = st.columns([4,1,1])
        with c2:
            if st.button("LEADERBOARD", key="nl2"): goto("leaderboard")
        with c3:
            if st.button("LOGIN",       key="nl3"): goto("auth")

def footer():
    st.markdown("""
    <div class="ak-footer">
      <b>AKFUNDED</b> &nbsp;·&nbsp; Built & Designed by <b>Akash Injeti</b>
      &nbsp;·&nbsp; Simulate. Prove. Get Funded. &nbsp;·&nbsp; ⚡
    </div>""", unsafe_allow_html=True)

def sec(title, sub=""):
    st.markdown(f"""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;margin-bottom:.2rem;color:#E8E8E8;">{title}</div>
    {"<div style='color:#666;font-size:.85rem;margin-bottom:1.5rem;'>"+sub+"</div>" if sub else ""}
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    nav()
    st.markdown("""
    <div class="hero">
      <div class="hero-chip">⚡ India's Prop Trading Simulator</div>
      <h1>PROVE YOUR <em>EDGE.</em><br>GET FUNDED.</h1>
      <p class="hero-sub">Trade simulated capital. Pass the challenge. Earn your funded badge. Built for serious Indian traders.</p>
    </div>
    <div class="hstats">
      <div class="hstat"><span class="n">₹50L+</span><span class="l">Capital Simulated</span></div>
      <div class="hstat"><span class="n">340+</span><span class="l">Active Traders</span></div>
      <div class="hstat"><span class="n">87</span><span class="l">Funded Badges</span></div>
      <div class="hstat"><span class="n">4.9★</span><span class="l">Trader Rating</span></div>
    </div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:3px;margin-bottom:.3rem;color:#E8E8E8;">CHALLENGE PLANS</div>
    <div style="color:#666;font-size:.85rem;margin-bottom:1.5rem;">One-time fee. Prove your skills. Unlock your funded badge.</div>
    <div class="plans-grid">
      <div class="plan-card">
        <div class="plan-name">STARTER</div><div class="plan-capital">₹50K</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+8%</b></li><li><span>Max Daily Loss</span><b>-4%</b></li>
          <li><span>Max Total Loss</span><b>-8%</b></li><li><span>Min Days</span><b>5</b></li>
        </ul>
        <div class="plan-price">₹199 <small>/ one-time</small></div>
      </div>
      <div class="plan-card hot">
        <div class="plan-name">PRO</div><div class="plan-capital">₹1L</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+10%</b></li><li><span>Max Daily Loss</span><b>-5%</b></li>
          <li><span>Max Total Loss</span><b>-10%</b></li><li><span>Min Days</span><b>5</b></li>
        </ul>
        <div class="plan-price">₹399 <small>/ one-time</small></div>
      </div>
      <div class="plan-card">
        <div class="plan-name">ELITE</div><div class="plan-capital">₹5L</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+10%</b></li><li><span>Max Daily Loss</span><b>-5%</b></li>
          <li><span>Max Total Loss</span><b>-10%</b></li><li><span>Min Days</span><b>7</b></li>
        </ul>
        <div class="plan-price">₹799 <small>/ one-time</small></div>
      </div>
    </div>""", unsafe_allow_html=True)
    _,c,_ = st.columns([2,1,2])
    with c:
        if st.button("🚀 START TRADING", use_container_width=True): goto("auth")
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
        <div style="background:var(--s1);border:1px solid var(--border);border-radius:18px;padding:2.5rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;">JOIN AKFUNDED</div>
          <div style="color:var(--dim);font-size:.85rem;margin-bottom:1.8rem;">Create your trader profile to begin</div>
        </div>""", unsafe_allow_html=True)
        t1,t2 = st.tabs(["  SIGN IN  ","  SIGN UP  "])
        with t1:
            email = st.text_input("Email", placeholder="you@email.com", key="si_e")
            pwd   = st.text_input("Password", type="password", placeholder="••••••••", key="si_p")
            if st.button("SIGN IN →", use_container_width=True, key="si_btn"):
                try:
                    res = supabase.auth.sign_in_with_password({"email":email,"password":pwd})
                    uid = res.user.id
                    prof = db_get_profile(uid)
                    st.session_state.user = {
                        "id": uid, "email": res.user.email,
                        "name": prof.get("name", email.split("@")[0]) if prof else email.split("@")[0]
                    }
                    goto("dashboard")
                except Exception as e:
                    st.error(f"❌ {e}")
        with t2:
            name    = st.text_input("Full Name", placeholder="Akash Injeti", key="su_n")
            email2  = st.text_input("Email", placeholder="you@email.com", key="su_e")
            pwd2    = st.text_input("Password", type="password", placeholder="Min 6 chars", key="su_p")
            country = st.selectbox("Country", ["🇮🇳 India","🇺🇸 USA","🇬🇧 UK","🇦🇪 UAE","🇸🇬 Singapore","Other"])
            if st.button("CREATE ACCOUNT →", use_container_width=True, key="su_btn"):
                try:
                    res = supabase.auth.sign_up({"email":email2,"password":pwd2})
                    uid = res.user.id
                    c_str = country.split(" ",1)[-1]
                    db_save_profile(uid, name, email2, c_str)
                    st.session_state.user = {"id":uid,"email":email2,"name":name}
                    st.success("✅ Account created! Check email to verify, then buy a plan.")
                    time.sleep(1)
                    goto("plans")
                except Exception as e:
                    st.error(f"❌ {e}")
    footer()

# ══════════════════════════════════════════════════════════════
# PLANS
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "plans":
    if not st.session_state.user: goto("auth")
    nav()
    name = st.session_state.user.get("name","Trader")
    sec(f"WELCOME, {name.upper()} 👋", "Select a challenge to start trading with simulated capital")

    cols = st.columns(3)
    for i,plan in enumerate(PLANS):
        with cols[i]:
            r = RULES[plan["slug"]]
            cap_str = f"₹{plan['capital']//100000}L" if plan['capital']>=100000 else f"₹{plan['capital']//1000}K"
            hot = plan["slug"] == "pro"
            border = "var(--gold)" if hot else "var(--border)"
            bg = "background:linear-gradient(160deg,#130f00,var(--s1));" if hot else ""
            st.markdown(f"""
            <div style="background:var(--s1);{bg}border:2px solid {border};border-radius:18px;padding:2rem;text-align:center;">
              <div class="plan-name">{plan['name']}</div>
              <div class="plan-capital">{cap_str}</div>
              <ul class="plan-rules" style="text-align:left;">
                <li><span>Profit Target</span><b>+{r['target']}%</b></li>
                <li><span>Max Daily Loss</span><b>-{r['daily_loss']}%</b></li>
                <li><span>Max Total Loss</span><b>-{r['total_loss']}%</b></li>
                <li><span>Min Days</span><b>{r['min_days']}</b></li>
              </ul>
              <div class="plan-price">₹{plan['price']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"BUY {plan['name']}", key=f"buy_{plan['slug']}", use_container_width=True):
                rz = st.secrets.get("RAZORPAY_KEY_ID","rzp_test_placeholder")
                st.markdown(f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                  var rzp=new Razorpay({{key:"{rz}",amount:{plan['price']*100},currency:"INR",
                  name:"AKFunded",description:"{plan['name']} Challenge",
                  prefill:{{email:"{st.session_state.user.get('email','')}"}},
                  theme:{{color:"#F0B429"}},
                  handler:function(r){{alert("✅ Payment successful!");}} }});rzp.open();
                </script>""", unsafe_allow_html=True)
                uid = st.session_state.user["id"]
                ch = supabase.table("challenges").insert({
                    "user_id":uid,"plan":plan["slug"],
                    "capital":plan["capital"],"status":"active"
                }).execute()
                ch_id = ch.data[0]["id"]
                supabase.table("accounts").insert({
                    "user_id":uid,"challenge_id":ch_id,
                    "balance":plan["capital"],"initial_capital":plan["capital"],
                    "daily_loss":0,"total_loss":0,"days_traded":0
                }).execute()
                st.success(f"✅ {plan['name']} activated! {cap_str} ready to trade.")
                time.sleep(1)
                goto("dashboard")
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
        st.markdown("""<div style="text-align:center;padding:5rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:#444;">NO ACTIVE CHALLENGE</div>
          <div style="color:#555;margin:.5rem 0 2rem;">Buy a challenge plan to begin trading</div>
        </div>""", unsafe_allow_html=True)
        _,c,_ = st.columns([2,1,2])
        with c:
            if st.button("BUY A CHALLENGE →", use_container_width=True): goto("plans")
        footer(); st.stop()

    balance  = account["balance"]
    initial  = account["initial_capital"]
    pnl      = balance - initial
    pnl_pct  = (pnl/initial)*100
    days     = account["days_traded"]
    r        = RULES.get(challenge["plan"], RULES["pro"])

    # Header
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;">
      <div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;">TRADING DASHBOARD</div>
        <div style="color:#666;font-size:.85rem;">Welcome back, {name}</div>
      </div>
      <div style="background:linear-gradient(135deg,#F0B429,#c88a00);color:#000;font-weight:800;font-size:.72rem;padding:7px 18px;border-radius:20px;letter-spacing:1.5px;">
        ⚡ {challenge['plan'].upper()} CHALLENGE
      </div>
    </div>""", unsafe_allow_html=True)

    # 4 metric cards
    pc = "g" if pnl>=0 else "r"
    ps = "+" if pnl>=0 else ""
    tc = "g" if pnl_pct>=r["target"] else "o"
    st.markdown(f"""
    <div class="metric-row">
      <div class="m-card"><div class="m-label">Account Balance</div><div class="m-val o">₹{balance:,.0f}</div><div class="m-sub">Initial: ₹{initial:,.0f}</div></div>
      <div class="m-card"><div class="m-label">Total P&L</div><div class="m-val {pc}">{ps}₹{pnl:,.0f}</div><div class="m-sub">{ps}{pnl_pct:.2f}%</div></div>
      <div class="m-card"><div class="m-label">Days Traded</div><div class="m-val w">{days}<span style="font-size:1rem;color:#555;"> / {r['min_days']}</span></div><div class="m-sub">Min required</div></div>
      <div class="m-card"><div class="m-label">Profit Target</div><div class="m-val {tc}">+{r['target']}%</div><div class="m-sub">{ps}{pnl_pct:.2f}% achieved</div></div>
    </div>""", unsafe_allow_html=True)

    # Trade stats row
    all_trades = db_get_trades(uid, challenge["id"], limit=500)
    wr,ap,bt,wt,tt = compute_stats(all_trades)
    wrc = "g" if wr>=50 else "r"
    apc = "g" if ap>=0 else "r"
    aps = "+" if ap>=0 else ""
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-box"><div class="sv w">{tt}</div><div class="sl">Total Trades</div></div>
      <div class="stat-box"><div class="sv {wrc}">{wr:.0f}%</div><div class="sl">Win Rate</div></div>
      <div class="stat-box"><div class="sv {apc}">{aps}₹{ap:,.0f}</div><div class="sl">Avg P&L</div></div>
      <div class="stat-box"><div class="sv g">+₹{bt:,.0f}</div><div class="sl">Best Trade</div></div>
      <div class="stat-box"><div class="sv r">₹{wt:,.0f}</div><div class="sl">Worst Trade</div></div>
    </div>""", unsafe_allow_html=True)

    # Rules progress
    profit_prog = min((pnl_pct/r["target"])*100,100) if r["target"] else 0
    dl_limit    = initial*r["daily_loss"]/100
    tl_limit    = initial*r["total_loss"]/100
    dl_used     = min(abs(account.get("daily_loss",0))/dl_limit*100,100) if dl_limit else 0
    tl_used     = min(abs(account.get("total_loss",0))/tl_limit*100,100) if tl_limit else 0
    def pbar(pct,col): return f'<div class="prog"><div class="prog-fill" style="width:{pct}%;background:{col};"></div></div>'
    st.markdown(f"""
    <div class="rules-box">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:1rem;">CHALLENGE RULES</div>
      <div class="r-row"><span class="r-name">🎯 Profit Target (+{r['target']}%)</span><span class="r-val {'ok' if profit_prog>=100 else 'ok'}">{pnl_pct:.2f}% / +{r['target']}%</span></div>
      {pbar(profit_prog,'var(--green)' if profit_prog>=100 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">🔴 Max Daily Loss (-{r['daily_loss']}%)</span><span class="r-val {'bad' if dl_used>80 else 'ok'}">{dl_used:.1f}% used</span></div>
      {pbar(dl_used,'var(--red)' if dl_used>80 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">🚫 Max Total Loss (-{r['total_loss']}%)</span><span class="r-val {'bad' if tl_used>80 else 'ok'}">{tl_used:.1f}% used</span></div>
      {pbar(tl_used,'var(--red)' if tl_used>80 else 'var(--gold)')}
    </div>""", unsafe_allow_html=True)

    # Chart + Trade form
    col_chart, col_trade = st.columns([2,1])
    with col_chart:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.5rem;">LIVE CHART — TRADINGVIEW</div>', unsafe_allow_html=True)
        mkt = st.selectbox("Market", list(SYMBOLS.keys()), key="mkt")
        sym_list = SYMBOLS[mkt]
        sym_pick = st.selectbox("Symbol", sym_list, key="csym")
        tv_sym   = TV_PREFIX[mkt] + sym_pick
        st.components.v1.html(f"""
        <div style="height:400px;width:100%;">
          <div id="tvc" style="height:100%;width:100%;"></div>
          <script src="https://s3.tradingview.com/tv.js"></script>
          <script>new TradingView.widget({{width:"100%",height:400,symbol:"{tv_sym}",
            interval:"15",timezone:"Asia/Kolkata",theme:"dark",style:"1",locale:"en",
            toolbar_bg:"#111",enable_publishing:false,container_id:"tvc",
            backgroundColor:"#070707",gridColor:"rgba(34,34,34,0.6)"}});</script>
        </div>""", height=410)

    with col_trade:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.5rem;">PLACE TRADE</div>', unsafe_allow_html=True)
        t_sym   = st.selectbox("Symbol", sym_list, key="tsym")
        t_type  = st.selectbox("Type", ["BUY","SELL"], key="ttype")
        t_entry = st.number_input("Entry Price", min_value=0.01, value=100.0, step=0.5, key="tentry")
        t_qty   = st.number_input("Quantity", min_value=1, value=10, step=1, key="tqty")
        t_exit  = st.number_input("Exit Price", min_value=0.01, value=105.0, step=0.5, key="texit")

        est = (t_exit-t_entry)*t_qty if t_type=="BUY" else (t_entry-t_exit)*t_qty
        ec  = "var(--green)" if est>=0 else "var(--red)"
        es  = "+" if est>=0 else ""
        st.markdown(f"""
        <div style="background:var(--s2);border:1px solid var(--border);border-radius:10px;padding:1rem;margin:.8rem 0;text-align:center;">
          <div style="font-size:.62rem;color:#555;letter-spacing:2px;margin-bottom:4px;">ESTIMATED P&L</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:{ec};letter-spacing:2px;">{es}₹{est:,.0f}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("⚡ EXECUTE TRADE", use_container_width=True, key="exec"):
            ch_id = challenge["id"]
            supabase.table("trades").insert({
                "user_id":uid,"challenge_id":ch_id,"symbol":t_sym,
                "type":t_type,"entry_price":t_entry,"exit_price":t_exit,
                "quantity":t_qty,"pnl":est,"closed_at":datetime.utcnow().isoformat()
            }).execute()
            new_bal = balance + est
            new_tl  = min(0, new_bal-initial)
            new_days= days+1
            supabase.table("accounts").update({
                "balance":new_bal,"total_loss":new_tl,
                "days_traded":new_days,"updated_at":datetime.utcnow().isoformat()
            }).eq("challenge_id",ch_id).execute()

            new_pct = ((new_bal-initial)/initial)*100
            if new_pct >= r["target"] and new_days >= r["min_days"]:
                supabase.table("challenges").update({"status":"passed"}).eq("id",ch_id).execute()
                st.balloons()
                st.success("🏆 YOU PASSED! Funded badge unlocked! 🎉")
            elif new_pct <= -r["total_loss"]:
                supabase.table("challenges").update({"status":"failed"}).eq("id",ch_id).execute()
                st.error("❌ Challenge FAILED. Max total loss hit. Buy a new plan to retry.")
            else:
                st.success(f"✅ Trade done! P&L: {es}₹{est:,.0f}") if est>=0 else st.warning(f"⚠️ Trade done! P&L: ₹{est:,.0f}")
            time.sleep(1); st.rerun()

    # Trade history table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:#555;margin-bottom:.6rem;">TRADE HISTORY</div>', unsafe_allow_html=True)
    trades = db_get_trades(uid, challenge["id"])
    if trades:
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);border-radius:12px;overflow:hidden;">', unsafe_allow_html=True)
        st.markdown('<div class="t-header"><span>SYMBOL</span><span>TYPE</span><span>ENTRY</span><span>EXIT</span><span>QTY</span><span>P&L</span></div>', unsafe_allow_html=True)
        for t in trades:
            p=t.get("pnl",0); pc3="var(--green)" if p>=0 else "var(--red)"; ps3="+" if p>=0 else ""
            tag='<span class="tag-b">BUY</span>' if t["type"]=="BUY" else '<span class="tag-s">SELL</span>'
            st.markdown(f'<div class="t-row"><span style="font-weight:600;">{t["symbol"]}</span>{tag}<span>₹{t["entry_price"]:,.1f}</span><span>₹{t["exit_price"]:,.1f}</span><span>{t["quantity"]}</span><span style="color:{pc3};font-family:\'JetBrains Mono\',monospace;font-weight:700;">{ps3}₹{p:,.0f}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:2.5rem;color:#444;background:var(--s1);border:1px solid var(--border);border-radius:12px;">No trades yet — place your first trade above! 📈</div>', unsafe_allow_html=True)
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
            {"name":"Akshay I.","country":"India","profit_pct":18.4,"status":"passed","plan":"elite"},
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
