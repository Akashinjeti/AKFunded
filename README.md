# ⚡ AKFunded — Prop Trading Simulator
### Built & Designed by Akash Injeti

> Simulate. Prove. Get Funded.

India's prop trading challenge platform — trade simulated capital, pass the challenge rules, earn your funded badge.

---

## 🚀 Features
- 🔐 Email auth via Supabase
- 💳 Challenge plans with Razorpay payments (₹199 / ₹399 / ₹799)
- 📊 Live TradingView charts (NSE symbols)
- ⚡ Real-time trade simulation with P&L tracking
- 🎯 Challenge rules engine (profit target, daily loss, total loss, min days)
- 🏆 Leaderboard with funded badges
- 📁 Full trade history per challenge

---

## 🛠️ Tech Stack
| Layer | Tool |
|-------|------|
| Frontend | Streamlit |
| Charts | TradingView Widget |
| Backend/DB | Supabase + PostgreSQL |
| Auth | Supabase Email Auth |
| Payments | Razorpay |
| Hosting | Streamlit Cloud |

---

## ⚙️ Setup

### 1. Supabase — Run SQL
Paste the SQL from `supabase_setup.sql` into your Supabase SQL Editor.

### 2. Streamlit Secrets
In Streamlit Cloud → Settings → Secrets, add:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
RAZORPAY_KEY_ID = "rzp_test_xxxx"
```

### 3. Deploy
- Push code to GitHub
- Connect repo to Streamlit Cloud
- Set main file: `main_app.py`

---

## 📁 File Structure
```
akfunded/
├── main_app.py          # Main Streamlit app
├── requirements.txt     # Dependencies
├── secrets_template.toml # Secrets format (DO NOT commit real keys)
├── supabase_setup.sql   # Database schema
└── README.md
```

---

*Powered by Akash Injeti ⚡*
