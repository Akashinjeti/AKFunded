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

# ─── SUPABASE ──────────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

supabase = get_supabase()

# ─── STYLES ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --gold: #F0B429; --gold-dim: #7a5c0a; --black: #070707;
  --s1: #111; --s2: #181818; --border: #222; --border2: #2a2a2a;
  --text: #E8E8E8; --dim: #666; --green: #00C896; --red: #FF4560; --blue: #4C9BE8;
}

/* ── FORCE BLACK BACKGROUND — cover every Streamlit layer ── */
html, body { background-color: #070707 !important; }
[class*="css"], .main, .stApp, .stApp > div,
section.main, section[data-testid="stSidebar"],
div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stBottom"],
.stApp > header,
.appview-container,
.reportview-container,
.main .block-container,
iframe { background-color: #070707 !important; background: #070707 !important; }

* { font-family: 'DM Sans', sans-serif; color: var(--text); }
#MainMenu, footer, header { visibility: hidden !important; display: none !important; }
.block-container { padding: 1rem 2.5rem 3rem !important; max-width: 1380px !important; }
::-webkit-scrollbar { width: 3px; } ::-webkit-scrollbar-thumb { background: var(--gold-dim); }

/* ── NAVBAR ── */
.ak-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.4rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2.5rem;
}
.ak-logo {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.5rem; letter-spacing: 5px; display: inline-flex; align-items: baseline; gap: 0;
}
.ak-logo .ak-part { color: var(--gold); -webkit-text-fill-color: var(--gold); }
.ak-logo .funded-part { color: #ffffff; -webkit-text-fill-color: #ffffff; }
.ak-beta {
  background: var(--gold); color: #000; font-size: .55rem; font-weight: 800;
  padding: 2px 7px; border-radius: 20px; letter-spacing: 1.5px;
  vertical-align: super; margin-left: 6px; font-family: 'DM Sans', sans-serif;
}
.ak-powered { font-size: .68rem; color: var(--dim); letter-spacing: 2px; text-transform: uppercase; }
.ak-powered b { color: var(--gold); -webkit-text-fill-color: var(--gold); font-weight: 700; }

/* HERO */
.hero { text-align: center; padding: 5rem 0 3.5rem; position: relative; background: transparent !important; }
.hero::before {
  content: ''; position: absolute; top: -40%; left: 50%; transform: translateX(-50%);
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(240,180,41,.09) 0%, transparent 65%);
  pointer-events: none;
}
.hero-chip {
  display: inline-block; border: 1px solid var(--gold-dim); color: var(--gold);
  -webkit-text-fill-color: var(--gold);
  font-size: .65rem; letter-spacing: 3px; padding: 5px 18px;
  border-radius: 20px; margin-bottom: 1.8rem; text-transform: uppercase;
  background: rgba(240,180,41,.05);
}
.hero h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(4rem, 9vw, 9rem); line-height: .93; letter-spacing: 5px; margin: 0 0 1.2rem;
  color: #ffffff; -webkit-text-fill-color: #ffffff;
}
.hero h1 em {
  font-style: normal; color: var(--gold); -webkit-text-fill-color: var(--gold);
  display: inline-block;
}
.hero-sub {
  font-size: 1.05rem; color: #777; -webkit-text-fill-color: #777;
  max-width: 480px; margin: 0 auto 2.5rem; line-height: 1.75;
}

/* STATS */
.stats {
  display: flex; justify-content: center; gap: 4rem;
  padding: 1.8rem 0; border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border); margin-bottom: 3rem;
  background: transparent !important;
}
.stat .n { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: var(--gold); -webkit-text-fill-color: var(--gold); letter-spacing: 2px; display: block; }
.stat .l { font-size: .65rem; color: #666; -webkit-text-fill-color: #666; letter-spacing: 2px; text-transform: uppercase; }

/* PLAN CARDS */
.plans-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-bottom:3rem;}
.plan-card{background:var(--s1);border:1px solid var(--border);border-radius:18px;padding:2rem 1.8rem;position:relative;overflow:hidden;transition:all .25s;}
.plan-card:hover{border-color:var(--gold-dim);transform:translateY(-5px);}
.plan-card.hot{border-color:var(--gold);background:linear-gradient(160deg,#130f00,var(--s1));}
.plan-card.hot::before{content:'MOST POPULAR';position:absolute;top:1rem;right:-2rem;background:var(--gold);color:#000;font-size:.55rem;font-weight:800;padding:3px 3rem;letter-spacing:1.5px;transform:rotate(35deg);}
.plan-name{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:3px;color:var(--dim);margin-bottom:.4rem;}
.plan-capital{font-family:'Bebas Neue',sans-serif;font-size:3.2rem;color:var(--gold);letter-spacing:2px;line-height:1;margin-bottom:1.5rem;}
.plan-rules{list-style:none;padding:0;margin:0 0 1.5rem;}
.plan-rules li{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid var(--border2);font-size:.82rem;color:var(--dim);}
.plan-rules li b{color:var(--text);font-weight:500;}
.plan-price{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:2px;}
.plan-price small{font-family:'DM Sans',sans-serif;font-size:.7rem;color:var(--dim);font-weight:300;letter-spacing:0;}

/* METRICS */
.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem;}
.m-card{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1.2rem 1.4rem;}
.m-label{font-size:.65rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:.4rem;}
.m-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:2px;line-height:1;}
.m-val.g{color:var(--green);} .m-val.r{color:var(--red);} .m-val.o{color:var(--gold);} .m-val.w{color:var(--text);}
.m-sub{font-size:.7rem;color:var(--dim);margin-top:4px;}

/* RULES CARD */
.rules-box{background:var(--s1);border:1px solid var(--border);border-radius:12px;padding:1.4rem;margin-bottom:1.5rem;}
.r-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem;}
.r-name{font-size:.82rem;color:var(--dim);}
.r-val{font-family:'JetBrains Mono',monospace;font-size:.82rem;}
.r-val.ok{color:var(--green);} .r-val.warn{color:var(--gold);} .r-val.bad{color:var(--red);}
.prog{height:3px;background:var(--border);border-radius:3px;overflow:hidden;margin-bottom:1rem;}
.prog-fill{height:100%;border-radius:3px;transition:width .5s;}

/* TRADE TABLE */
.t-header,.t-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr 1.2fr;padding:.7rem 1rem;font-size:.82rem;align-items:center;}
.t-header{color:var(--dim);font-size:.65rem;letter-spacing:1.5px;text-transform:uppercase;border-bottom:1px solid var(--border);}
.t-row{border-bottom:1px solid var(--border2);}
.t-row:last-child{border-bottom:none;}
.tag-b{background:rgba(0,200,150,.12);color:var(--green);padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:700;}
.tag-s{background:rgba(255,69,96,.12);color:var(--red);padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:700;}

/* LEADERBOARD */
.lb-item{display:flex;align-items:center;gap:1rem;background:var(--s1);border:1px solid var(--border);border-radius:10px;padding:.9rem 1.2rem;margin-bottom:.5rem;transition:border-color .2s;}
.lb-item:hover{border-color:var(--gold-dim);}
.lb-rank{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:var(--dim);width:36px;text-align:center;}
.lb-rank.top{color:var(--gold);}
.lb-info{flex:1;}
.lb-name{font-weight:600;font-size:.92rem;}
.lb-country{font-size:.72rem;color:var(--dim);}
.lb-pnl{font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--green);font-size:1rem;}
.lb-badge{font-size:.58rem;padding:2px 8px;border-radius:20px;font-weight:700;letter-spacing:1px;}
.funded-b{background:rgba(240,180,41,.15);color:var(--gold);}
.active-b{background:rgba(0,200,150,.1);color:var(--green);}

/* FOOTER */
.ak-footer{text-align:center;padding:2rem 0 1rem;border-top:1px solid var(--border);margin-top:4rem;color:var(--dim);font-size:.72rem;letter-spacing:1px;}
.ak-footer b{color:var(--gold);}

/* STREAMLIT OVERRIDES */
.stButton > button { background: var(--gold) !important; color: #000 !important; font-weight: 700 !important; border: none !important; border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; letter-spacing: 1px !important; transition: opacity .2s !important; }
.stButton > button:hover { opacity: .8 !important; }
.stButton > button p { color: #000 !important; -webkit-text-fill-color: #000 !important; }
div[data-testid="stTabs"] [data-baseweb="tab-list"] { background: var(--s1) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 3px !important; gap: 3px !important; }
div[data-testid="stTabs"] [data-baseweb="tab"] { color: var(--dim) !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; }
div[data-testid="stTabs"] [aria-selected="true"] { background: var(--gold) !important; color: #000 !important; border-radius: 8px !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }
.stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input { background: var(--s2) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 8px !important; }
label[data-testid="stWidgetLabel"] { color: var(--dim) !important; font-size: .78rem !important; letter-spacing: 1px !important; }
/* Kill any white/light backgrounds injected by Streamlit */
div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"],
div[data-testid="column"], div[data-testid="stMarkdownContainer"],
div.element-container, div.stMarkdown { background: transparent !important; }
p, span, div { color: var(--text); }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────────
for k, v in [("user", None), ("page", "home")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPERS ────────────────────────────────────────────────────
RULES = {
    "starter": {"target": 8, "daily_loss": 4, "total_loss": 8, "min_days": 5},
    "pro":     {"target": 10,"daily_loss": 5, "total_loss": 10,"min_days": 5},
    "elite":   {"target": 10,"daily_loss": 5, "total_loss": 10,"min_days": 7},
}
PLANS = [
    {"name":"STARTER","capital":50000, "price":199,"slug":"starter"},
    {"name":"PRO",    "capital":100000,"price":399,"slug":"pro"},
    {"name":"ELITE",  "capital":500000,"price":799,"slug":"elite"},
]

def nav():
    logged_in = st.session_state.user is not None
    name = st.session_state.user.get("name","") if logged_in else ""

    st.markdown("""
    <div class="ak-nav">
      <div style="display:flex;align-items:center;">
        <span class="ak-logo"><span class="ak-part">AK</span><span class="funded-part">FUNDED</span></span>
        <span class="ak-beta">BETA</span>
      </div>
      <div class="ak-powered">Powered by <b>Akash Injeti</b></div>
    </div>""", unsafe_allow_html=True)

    # Nav buttons row right below navbar line
    if logged_in:
        c1,c2,c3,c4,c5 = st.columns([3,1,1,1,1])
        with c2:
            if st.button("DASHBOARD", key="nav_dash"): goto("dashboard")
        with c3:
            if st.button("LEADERBOARD", key="nav_lb"): goto("leaderboard")
        with c4:
            if st.button("BUY PLAN", key="nav_buy"): goto("plans")
        with c5:
            if st.button("LOGOUT", key="nav_logout"):
                supabase.auth.sign_out()
                st.session_state.user = None
                goto("home")
    else:
        c1,c2,c3 = st.columns([4,1,1])
        with c2:
            if st.button("LEADERBOARD", key="nav_lb2"): goto("leaderboard")
        with c3:
            if st.button("LOGIN", key="nav_login"): goto("auth")

def footer():
    st.markdown("""
    <div class="ak-footer">
      <b>AKFUNDED</b> &nbsp;·&nbsp; Built & Designed by <b>Akash Injeti</b>
      &nbsp;·&nbsp; Simulate. Prove. Get Funded. &nbsp;·&nbsp; ⚡
    </div>""", unsafe_allow_html=True)

def get_challenge_and_account():
    if not st.session_state.user:
        return None, None
    uid = st.session_state.user["id"]
    ch = supabase.table("challenges").select("*").eq("user_id", uid).eq("status","active").maybe_single().execute()
    if not ch.data:
        return None, None
    acc = supabase.table("accounts").select("*").eq("challenge_id", ch.data["id"]).maybe_single().execute()
    return ch.data, acc.data

def goto(page):
    st.session_state.page = page
    st.rerun()

# ─── ROUTER ─────────────────────────────────────────────────────
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    nav()

    st.markdown("""
    <div class="hero">
      <div class="hero-chip">⚡ India's Prop Trading Simulator</div>
      <h1>PROVE YOUR <em>EDGE.</em><br>GET FUNDED.</h1>
      <p class="hero-sub">Trade simulated capital. Pass the challenge. Earn your funded badge. Built for serious Indian traders.</p>
    </div>
    <div class="stats">
      <div class="stat"><span class="n">₹50L+</span><span class="l">Capital Simulated</span></div>
      <div class="stat"><span class="n">340+</span><span class="l">Active Traders</span></div>
      <div class="stat"><span class="n">87</span><span class="l">Funded Badges</span></div>
      <div class="stat"><span class="n">4.9★</span><span class="l">Trader Rating</span></div>
    </div>

    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:3px;margin-bottom:.3rem;color:#E8E8E8;">CHALLENGE PLANS</div>
    <div style="color:#666;font-size:.85rem;margin-bottom:1.5rem;">One-time fee. Prove your skills. Unlock your funded badge.</div>

    <div class="plans-grid">
      <div class="plan-card">
        <div class="plan-name">STARTER</div>
        <div class="plan-capital">₹50K</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+8%</b></li>
          <li><span>Max Daily Loss</span><b>-4%</b></li>
          <li><span>Max Total Loss</span><b>-8%</b></li>
          <li><span>Min Trading Days</span><b>5 days</b></li>
        </ul>
        <div class="plan-price">₹199 <small>/ one-time</small></div>
      </div>
      <div class="plan-card hot">
        <div class="plan-name">PRO</div>
        <div class="plan-capital">₹1L</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+10%</b></li>
          <li><span>Max Daily Loss</span><b>-5%</b></li>
          <li><span>Max Total Loss</span><b>-10%</b></li>
          <li><span>Min Trading Days</span><b>5 days</b></li>
        </ul>
        <div class="plan-price">₹399 <small>/ one-time</small></div>
      </div>
      <div class="plan-card">
        <div class="plan-name">ELITE</div>
        <div class="plan-capital">₹5L</div>
        <ul class="plan-rules">
          <li><span>Profit Target</span><b>+10%</b></li>
          <li><span>Max Daily Loss</span><b>-5%</b></li>
          <li><span>Max Total Loss</span><b>-10%</b></li>
          <li><span>Min Trading Days</span><b>7 days</b></li>
        </ul>
        <div class="plan-price">₹799 <small>/ one-time</small></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,1,2])
    with c2:
        if st.button("🚀 START TRADING", use_container_width=True): goto("auth")

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: AUTH
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "auth":
    nav()
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown("""
        <div style="background:var(--s1);border:1px solid var(--border);border-radius:18px;padding:2.5rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;">JOIN AKFUNDED</div>
          <div style="color:var(--dim);font-size:.85rem;margin-bottom:1.8rem;">Create your trader profile to begin</div>
        </div>""", unsafe_allow_html=True)

        t1, t2 = st.tabs(["  SIGN IN  ", "  SIGN UP  "])
        with t1:
            email = st.text_input("Email", placeholder="you@email.com", key="si_email")
            pwd   = st.text_input("Password", type="password", placeholder="••••••••", key="si_pwd")
            if st.button("SIGN IN →", use_container_width=True, key="si_btn"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    p = supabase.table("profiles").select("*").eq("id", res.user.id).maybe_single().execute()
                    st.session_state.user = {
                        "id": res.user.id,
                        "email": res.user.email,
                        "name": p.data.get("name", email.split("@")[0]) if p.data else email.split("@")[0]
                    }
                    goto("dashboard")
                except Exception as e:
                    st.error(f"❌ {e}")

        with t2:
            name    = st.text_input("Full Name", placeholder="Akash Injeti", key="su_name")
            email2  = st.text_input("Email", placeholder="you@email.com", key="su_email")
            pwd2    = st.text_input("Password", type="password", placeholder="Min 6 chars", key="su_pwd")
            country = st.selectbox("Country", ["🇮🇳 India","🇺🇸 USA","🇬🇧 UK","🇦🇪 UAE","🇸🇬 Singapore","Other"])
            if st.button("CREATE ACCOUNT →", use_container_width=True, key="su_btn"):
                try:
                    res = supabase.auth.sign_up({"email": email2, "password": pwd2})
                    uid = res.user.id
                    supabase.table("profiles").insert({
                        "id": uid, "name": name, "email": email2,
                        "country": country.split(" ",1)[-1]
                    }).execute()
                    st.session_state.user = {"id": uid, "email": email2, "name": name}
                    st.success("✅ Account created! Check email to verify, then buy a plan.")
                    time.sleep(1)
                    goto("plans")
                except Exception as e:
                    st.error(f"❌ {e}")
    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: PLANS (buy challenge)
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "plans":
    if not st.session_state.user: goto("auth")
    nav()
    name = st.session_state.user.get("name","Trader")
    st.markdown(f"""
    <div style="margin-bottom:2rem;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;">WELCOME, {name.upper()} 👋</div>
      <div style="color:var(--dim);font-size:.85rem;">Select a challenge to start trading with simulated capital</div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, plan in enumerate(PLANS):
        with cols[i]:
            r = RULES[plan["slug"]]
            cap_str = f"₹{plan['capital']//100000}L" if plan['capital'] >= 100000 else f"₹{plan['capital']//1000}K"
            hot = plan["slug"] == "pro"
            border = "var(--gold)" if hot else "var(--border)"
            st.markdown(f"""
            <div style="background:var(--s1);border:2px solid {border};border-radius:18px;padding:2rem;text-align:center;{'background:linear-gradient(160deg,#130f00,var(--s1));' if hot else ''}">
              <div class="plan-name">{plan['name']}</div>
              <div class="plan-capital">{cap_str}</div>
              <ul class="plan-rules" style="text-align:left;">
                <li><span>Profit Target</span><b>+{r['target']}%</b></li>
                <li><span>Max Daily Loss</span><b>-{r['daily_loss']}%</b></li>
                <li><span>Max Total Loss</span><b>-{r['total_loss']}%</b></li>
                <li><span>Min Days</span><b>{r['min_days']} days</b></li>
              </ul>
              <div class="plan-price">₹{plan['price']}</div>
            </div>""", unsafe_allow_html=True)

            if st.button(f"BUY {plan['name']}", key=f"buy_{plan['slug']}", use_container_width=True):
                rz_key = st.secrets.get("RAZORPAY_KEY_ID","rzp_test_placeholder")
                # Razorpay checkout
                st.markdown(f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                <script>
                  var rzp = new Razorpay({{
                    key: "{rz_key}",
                    amount: {plan['price']*100},
                    currency: "INR",
                    name: "AKFunded",
                    description: "{plan['name']} Challenge",
                    prefill: {{email: "{st.session_state.user.get('email','')}"}},
                    theme: {{color: "#F0B429"}},
                    handler: function(r){{ alert("✅ Payment successful! Challenge activated."); }}
                  }});
                  rzp.open();
                </script>""", unsafe_allow_html=True)

                # Create records
                uid = st.session_state.user["id"]
                ch = supabase.table("challenges").insert({
                    "user_id": uid, "plan": plan["slug"],
                    "capital": plan["capital"], "status": "active"
                }).execute()
                ch_id = ch.data[0]["id"]
                supabase.table("accounts").insert({
                    "user_id": uid, "challenge_id": ch_id,
                    "balance": plan["capital"], "initial_capital": plan["capital"],
                    "daily_loss": 0, "total_loss": 0, "days_traded": 0
                }).execute()
                st.success(f"✅ {plan['name']} Challenge activated! {cap_str} ready.")
                time.sleep(1)
                goto("dashboard")
    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.user: goto("auth")
    nav()

    challenge, account = get_challenge_and_account()

    if not challenge or not account:
        st.markdown("""
        <div style="text-align:center;padding:5rem 2rem;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:var(--dim);">NO ACTIVE CHALLENGE</div>
          <div style="color:var(--dim);margin-top:.5rem;margin-bottom:2rem;">Buy a challenge plan to begin trading</div>
        </div>""", unsafe_allow_html=True)
        _, c, _ = st.columns([2,1,2])
        with c:
            if st.button("BUY A CHALLENGE →", use_container_width=True): goto("plans")
        footer()
        st.stop()

    balance  = account["balance"]
    initial  = account["initial_capital"]
    pnl      = balance - initial
    pnl_pct  = (pnl / initial) * 100
    days     = account["days_traded"]
    plan_key = challenge["plan"]
    r        = RULES.get(plan_key, RULES["pro"])
    name     = st.session_state.user.get("name", "Trader")

    # Header
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:2rem;">
      <div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;">TRADING DASHBOARD</div>
        <div style="color:var(--dim);font-size:.85rem;">Welcome back, {name}</div>
      </div>
      <div style="background:linear-gradient(135deg,var(--gold),#c88a00);color:#000;font-weight:800;font-size:.72rem;padding:7px 18px;border-radius:20px;letter-spacing:1.5px;">
        ⚡ {plan_key.upper()} CHALLENGE
      </div>
    </div>""", unsafe_allow_html=True)

    # Metrics
    pc = "g" if pnl >= 0 else "r"
    ps = "+" if pnl >= 0 else ""
    target_c = "g" if pnl_pct >= r["target"] else "o"
    st.markdown(f"""
    <div class="metric-row">
      <div class="m-card">
        <div class="m-label">Account Balance</div>
        <div class="m-val o">₹{balance:,.0f}</div>
        <div class="m-sub">Initial: ₹{initial:,.0f}</div>
      </div>
      <div class="m-card">
        <div class="m-label">Total P&L</div>
        <div class="m-val {pc}">{ps}₹{pnl:,.0f}</div>
        <div class="m-sub">{ps}{pnl_pct:.2f}%</div>
      </div>
      <div class="m-card">
        <div class="m-label">Days Traded</div>
        <div class="m-val w">{days}<span style="font-size:1.1rem;color:var(--dim);"> / {r['min_days']}</span></div>
        <div class="m-sub">Minimum required days</div>
      </div>
      <div class="m-card">
        <div class="m-label">Profit Target</div>
        <div class="m-val {target_c}">+{r['target']}%</div>
        <div class="m-sub">{ps}{pnl_pct:.2f}% achieved</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Rules progress
    profit_prog  = min((pnl_pct / r["target"]) * 100, 100) if r["target"] else 0
    daily_limit  = initial * r["daily_loss"]  / 100
    total_limit  = initial * r["total_loss"]  / 100
    daily_used   = min(abs(account.get("daily_loss", 0))  / daily_limit  * 100, 100) if daily_limit else 0
    total_used   = min(abs(account.get("total_loss", 0))  / total_limit  * 100, 100) if total_limit else 0

    def pbar(pct, color): return f'<div class="prog"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>'
    def rclass(pct): return "bad" if pct > 80 else "ok"

    st.markdown(f"""
    <div class="rules-box">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:var(--dim);margin-bottom:1rem;">CHALLENGE RULES TRACKER</div>
      <div class="r-row"><span class="r-name">🎯 Profit Target (+{r['target']}%)</span><span class="r-val ok">{pnl_pct:.2f}% / +{r['target']}%</span></div>
      {pbar(profit_prog, 'var(--green)' if profit_prog >= 100 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">🔴 Max Daily Loss (-{r['daily_loss']}%)</span><span class="r-val {rclass(daily_used)}">{daily_used:.1f}% used</span></div>
      {pbar(daily_used, 'var(--red)' if daily_used > 80 else 'var(--gold)')}
      <div class="r-row"><span class="r-name">🚫 Max Total Loss (-{r['total_loss']}%)</span><span class="r-val {rclass(total_used)}">{total_used:.1f}% used</span></div>
      {pbar(total_used, 'var(--red)' if total_used > 80 else '#F0B429')}
    </div>""", unsafe_allow_html=True)

    # Chart + Trade form
    col_chart, col_trade = st.columns([2, 1])

    with col_chart:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:var(--dim);margin-bottom:.6rem;">LIVE CHART — TRADINGVIEW</div>', unsafe_allow_html=True)
        st.components.v1.html("""
        <div class="tradingview-widget-container" style="height:430px;">
          <div id="tv_chart" style="height:100%;width:100%;"></div>
          <script src="https://s3.tradingview.com/tv.js"></script>
          <script>
          new TradingView.widget({
            width:"100%", height:430,
            symbol:"NSE:NIFTY", interval:"15",
            timezone:"Asia/Kolkata", theme:"dark", style:"1", locale:"en",
            toolbar_bg:"#111", enable_publishing:false,
            hide_top_toolbar:false, save_image:false,
            container_id:"tv_chart",
            backgroundColor:"#070707",
            gridColor:"rgba(34,34,34,0.6)"
          });
          </script>
        </div>""", height=440)

    with col_trade:
        st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:var(--dim);margin-bottom:.6rem;">PLACE TRADE</div>', unsafe_allow_html=True)
        symbol = st.selectbox("Symbol", ["NIFTY","BANKNIFTY","RELIANCE","TCS","INFY","HDFCBANK","TATAMOTORS","WIPRO","SBIN","ICICIBANK"], key="sym")
        ttype  = st.selectbox("Trade Type", ["BUY","SELL"], key="ttype")
        entry  = st.number_input("Entry Price (₹)", min_value=1.0, value=100.0, step=0.5, key="entry")
        qty    = st.number_input("Quantity (Lots)", min_value=1, value=10, step=1, key="qty")
        exit_  = st.number_input("Exit Price (₹)", min_value=1.0, value=105.0, step=0.5, key="exit")

        est_pnl = (exit_ - entry) * qty if ttype == "BUY" else (entry - exit_) * qty
        pc2 = "var(--green)" if est_pnl >= 0 else "var(--red)"
        ps2 = "+" if est_pnl >= 0 else ""

        st.markdown(f"""
        <div style="background:var(--s2);border:1px solid var(--border);border-radius:10px;padding:1rem;margin:.8rem 0;text-align:center;">
          <div style="font-size:.62rem;color:var(--dim);letter-spacing:2px;margin-bottom:4px;">ESTIMATED P&L</div>
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:{pc2};letter-spacing:2px;">{ps2}₹{est_pnl:,.0f}</div>
        </div>""", unsafe_allow_html=True)

        if st.button("⚡ EXECUTE TRADE", use_container_width=True, key="exec"):
            uid   = st.session_state.user["id"]
            ch_id = challenge["id"]

            supabase.table("trades").insert({
                "user_id": uid, "challenge_id": ch_id,
                "symbol": symbol, "type": ttype,
                "entry_price": entry, "exit_price": exit_,
                "quantity": qty, "pnl": est_pnl,
                "closed_at": datetime.utcnow().isoformat()
            }).execute()

            new_bal       = balance + est_pnl
            new_total_loss = min(0, new_bal - initial)
            new_days      = days + 1

            supabase.table("accounts").update({
                "balance": new_bal,
                "total_loss": new_total_loss,
                "days_traded": new_days,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("challenge_id", ch_id).execute()

            new_pnl_pct = ((new_bal - initial) / initial) * 100
            if new_pnl_pct >= r["target"] and new_days >= r["min_days"]:
                supabase.table("challenges").update({"status":"passed"}).eq("id", ch_id).execute()
                st.balloons()
                st.success("🏆 YOU PASSED! Funded badge unlocked! 🎉")
            elif new_pnl_pct <= -r["total_loss"]:
                supabase.table("challenges").update({"status":"failed"}).eq("id", ch_id).execute()
                st.error("❌ Challenge FAILED. Max total loss hit. Buy a new plan to retry.")
            else:
                if est_pnl >= 0:
                    st.success(f"✅ Trade done! P&L: +₹{est_pnl:,.0f}")
                else:
                    st.warning(f"⚠️ Trade done! P&L: ₹{est_pnl:,.0f}")
            time.sleep(1)
            st.rerun()

    # Trade History
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Bebas Neue\',sans-serif;font-size:1rem;letter-spacing:2px;color:var(--dim);margin-bottom:.8rem;">TRADE HISTORY</div>', unsafe_allow_html=True)

    trades = supabase.table("trades").select("*").eq("challenge_id", challenge["id"]).order("closed_at", desc=True).limit(25).execute().data or []

    if trades:
        st.markdown('<div style="background:var(--s1);border:1px solid var(--border);border-radius:12px;overflow:hidden;">', unsafe_allow_html=True)
        st.markdown('<div class="t-header"><span>SYMBOL</span><span>TYPE</span><span>ENTRY</span><span>EXIT</span><span>QTY</span><span>P&L</span></div>', unsafe_allow_html=True)
        for t in trades:
            p = t.get("pnl", 0)
            pc3 = "var(--green)" if p >= 0 else "var(--red)"
            ps3 = "+" if p >= 0 else ""
            tag = '<span class="tag-b">BUY</span>' if t["type"] == "BUY" else '<span class="tag-s">SELL</span>'
            st.markdown(f"""
            <div class="t-row">
              <span style="font-weight:600;">{t['symbol']}</span>
              {tag}
              <span>₹{t['entry_price']:,.1f}</span>
              <span>₹{t['exit_price']:,.1f}</span>
              <span>{t['quantity']}</span>
              <span style="color:{pc3};font-family:'JetBrains Mono',monospace;font-weight:700;">{ps3}₹{p:,.0f}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--dim);background:var(--s1);border:1px solid var(--border);border-radius:12px;">No trades yet — place your first trade above! 📈</div>', unsafe_allow_html=True)

    footer()

# ══════════════════════════════════════════════════════════════
# PAGE: LEADERBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "leaderboard":
    nav()
    st.markdown("""
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:3px;margin-bottom:.3rem;">🏆 LEADERBOARD</div>
    <div style="color:var(--dim);font-size:.85rem;margin-bottom:1.5rem;">Top traders ranked by profit % — updated live</div>""", unsafe_allow_html=True)

    try:
        data = supabase.table("leaderboard").select("*").limit(20).execute().data or []
    except:
        data = []

    if not data:
        data = [
            {"name":"Akshay I.","country":"India","profit_pct":18.4,"status":"passed","plan":"elite"},
            {"name":"Priya M.","country":"India","profit_pct":15.2,"status":"passed","plan":"pro"},
            {"name":"Kiran T.","country":"India","profit_pct":12.7,"status":"active","plan":"pro"},
            {"name":"Arun K.","country":"India","profit_pct":11.1,"status":"passed","plan":"starter"},
            {"name":"Sneha R.","country":"India","profit_pct":9.8, "status":"active","plan":"pro"},
            {"name":"Dev P.",  "country":"India","profit_pct":8.3, "status":"active","plan":"starter"},
        ]

    medals = ["🥇","🥈","🥉"]
    for i, t in enumerate(data):
        rank   = i + 1
        medal  = medals[i] if i < 3 else f"#{rank}"
        rc     = "top" if rank <= 3 else ""
        funded = t.get("status") == "passed"
        badge_class = "funded-b" if funded else "active-b"
        badge_text  = "FUNDED" if funded else "ACTIVE"
        profit = t.get("profit_pct", 0)
        st.markdown(f"""
        <div class="lb-item">
          <div class="lb-rank {rc}">{medal}</div>
          <div class="lb-info">
            <div class="lb-name">{t.get('name','Trader')}</div>
            <div class="lb-country">{t.get('country','')}</div>
          </div>
          <div class="lb-pnl">+{profit:.2f}%</div>
          <div class="lb-badge {badge_class}">{badge_text}</div>
        </div>""", unsafe_allow_html=True)

    footer()
