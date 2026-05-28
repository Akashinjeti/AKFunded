<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AKFunded — Built For Real Traders</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --black:#08090a;
  --surface:#0d0f11;
  --card:#111316;
  --card2:#161920;
  --border:rgba(255,255,255,0.06);
  --border2:rgba(255,255,255,0.10);
  --blue:#4A9EFF;
  --blue-dim:rgba(74,158,255,0.08);
  --blue-glow:rgba(74,158,255,0.15);
  --white:#F0F0EE;
  --muted:#6B7280;
  --muted2:#4B5563;
  --green:#34D399;
  --red:#F87171;
  --gold:#D4A844;
  --font-display:'Syne',sans-serif;
  --font-mono:'DM Mono',monospace;
  --font-serif:'Instrument Serif',serif;
}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}
body{background:var(--black);color:var(--white);font-family:var(--font-display);overflow-x:hidden;min-height:100vh}

/* ── SCROLLBAR ── */
::-webkit-scrollbar{width:2px}
::-webkit-scrollbar-track{background:var(--black)}
::-webkit-scrollbar-thumb{background:var(--border2)}

/* ── NOISE OVERLAY ── */
body::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:1;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  opacity:0.022;
}

/* ── AMBIENT LIGHTS ── */
.ambient{position:fixed;pointer-events:none;border-radius:50%;filter:blur(120px);z-index:0}
.ambient-1{width:700px;height:700px;top:-200px;left:-150px;background:radial-gradient(circle,rgba(74,158,255,0.08) 0%,transparent 70%);animation:drift1 18s ease-in-out infinite}
.ambient-2{width:500px;height:500px;bottom:-100px;right:-100px;background:radial-gradient(circle,rgba(52,211,153,0.05) 0%,transparent 70%);animation:drift2 22s ease-in-out infinite}
@keyframes drift1{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,40px)}}
@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-40px,-30px)}}

/* ── LAYOUT ── */
.z{position:relative;z-index:2}
.container{max-width:1280px;margin:0 auto;padding:0 40px}
@media(max-width:768px){.container{padding:0 20px}}

/* ── NAV ── */
nav{
  position:fixed;top:0;left:0;right:0;z-index:100;
  padding:18px 0;
  border-bottom:1px solid var(--border);
  backdrop-filter:blur(24px) saturate(180%);
  -webkit-backdrop-filter:blur(24px) saturate(180%);
  background:rgba(8,9,10,0.72);
  transition:all 0.3s;
}
.nav-inner{display:flex;align-items:center;justify-content:space-between;max-width:1280px;margin:0 auto;padding:0 40px}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none}
.logo-mark{
  width:28px;height:28px;border-radius:6px;
  background:var(--blue);display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;color:#000;letter-spacing:0px;
}
.logo-text{font-size:15px;font-weight:700;color:var(--white);letter-spacing:0.5px}
.logo-badge{font-size:9px;background:rgba(74,158,255,0.15);color:var(--blue);border:1px solid rgba(74,158,255,0.25);padding:2px 7px;border-radius:100px;letter-spacing:0.5px;font-weight:500}
.nav-links{display:flex;align-items:center;gap:36px}
.nav-links a{font-size:13px;color:var(--muted);text-decoration:none;transition:color 0.2s;font-weight:500;letter-spacing:0.2px}
.nav-links a:hover{color:var(--white)}
.nav-cta{display:flex;align-items:center;gap:12px}
.btn-ghost{font-size:13px;color:var(--muted);background:none;border:none;cursor:pointer;font-family:inherit;font-weight:500;padding:8px 16px;border-radius:8px;transition:all 0.2s}
.btn-ghost:hover{color:var(--white);background:rgba(255,255,255,0.05)}
.btn-primary{
  font-size:13px;font-weight:600;padding:9px 20px;border-radius:8px;
  background:var(--white);color:var(--black);border:none;cursor:pointer;font-family:inherit;
  transition:all 0.2s;letter-spacing:0.2px;
}
.btn-primary:hover{background:#d8d8d4;transform:translateY(-1px)}
.btn-primary:active{transform:translateY(0) scale(0.98)}
@media(max-width:900px){.nav-links{display:none}}

/* ── HERO ── */
.hero{
  min-height:100vh;display:grid;grid-template-columns:1fr 1fr;gap:80px;
  align-items:center;padding:120px 0 80px;
}
@media(max-width:1000px){.hero{grid-template-columns:1fr;gap:60px;padding:120px 0 60px;text-align:center}}
.hero-left{display:flex;flex-direction:column;gap:32px}
.hero-eyebrow{
  display:inline-flex;align-items:center;gap:8px;
  font-family:var(--font-mono);font-size:11px;color:var(--blue);letter-spacing:2px;text-transform:uppercase;
  background:var(--blue-dim);border:1px solid rgba(74,158,255,0.15);
  padding:6px 14px;border-radius:100px;width:fit-content;
  animation:fadeUp 0.6s ease both;
}
.eyebrow-dot{width:5px;height:5px;background:var(--blue);border-radius:50%;animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
@media(max-width:1000px){.hero-eyebrow{margin:0 auto}}
.hero-headline{
  font-size:clamp(56px,7vw,88px);font-weight:800;line-height:0.93;
  letter-spacing:-3px;color:var(--white);
  animation:fadeUp 0.6s 0.1s ease both;
}
.hero-headline em{
  font-family:var(--font-serif);font-style:italic;font-weight:400;
  color:transparent;
  -webkit-text-stroke:1px rgba(255,255,255,0.4);
  letter-spacing:-2px;
}
.hero-sub{
  font-size:16px;line-height:1.75;color:var(--muted);max-width:420px;font-weight:400;
  animation:fadeUp 0.6s 0.2s ease both;
}
@media(max-width:1000px){.hero-sub{margin:0 auto}}
.hero-actions{display:flex;align-items:center;gap:16px;animation:fadeUp 0.6s 0.3s ease both}
@media(max-width:1000px){.hero-actions{justify-content:center}}
.btn-lg{
  font-size:14px;font-weight:600;padding:14px 28px;border-radius:10px;
  background:var(--white);color:var(--black);border:none;cursor:pointer;font-family:inherit;
  transition:all 0.25s;letter-spacing:0.2px;
  box-shadow:0 0 0 0 rgba(255,255,255,0);
}
.btn-lg:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(255,255,255,0.08)}
.btn-lg:active{transform:translateY(0) scale(0.98)}
.btn-outline{
  font-size:14px;font-weight:500;padding:14px 28px;border-radius:10px;
  background:transparent;color:var(--white);
  border:1px solid var(--border2);cursor:pointer;font-family:inherit;
  transition:all 0.25s;
}
.btn-outline:hover{background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.2)}
.hero-meta{display:flex;align-items:center;gap:24px;animation:fadeUp 0.6s 0.4s ease both}
@media(max-width:1000px){.hero-meta{justify-content:center}}
.meta-item{display:flex;flex-direction:column;gap:3px}
.meta-val{font-size:22px;font-weight:700;color:var(--white);letter-spacing:-0.5px}
.meta-label{font-size:11px;color:var(--muted);letter-spacing:0.5px;font-family:var(--font-mono)}
.meta-sep{width:1px;height:36px;background:var(--border2)}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

/* ── TERMINAL ── */
.hero-right{animation:fadeUp 0.7s 0.2s ease both}
.terminal-wrapper{
  position:relative;
  background:var(--card);
  border:1px solid var(--border2);
  border-radius:20px;
  overflow:hidden;
  box-shadow:0 40px 80px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.04),inset 0 1px 0 rgba(255,255,255,0.08);
}
.terminal-wrapper::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(74,158,255,0.04) 0%,transparent 60%);
  pointer-events:none;z-index:0;
}
.term-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 18px;border-bottom:1px solid var(--border);position:relative;z-index:1;
}
.term-dots{display:flex;gap:6px}
.term-dot{width:10px;height:10px;border-radius:50%}
.term-dot:nth-child(1){background:#FF5F57}
.term-dot:nth-child(2){background:#FEBC2E}
.term-dot:nth-child(3){background:#28C840}
.term-title{font-family:var(--font-mono);font-size:11px;color:var(--muted);letter-spacing:1px}
.term-status{display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:10px;color:var(--green)}
.status-dot{width:5px;height:5px;background:var(--green);border-radius:50%;animation:blink 2s infinite}
.term-body{padding:20px;position:relative;z-index:1}

/* equity chart */
.equity-chart{width:100%;height:130px;position:relative;margin-bottom:20px;overflow:hidden}
.chart-svg{width:100%;height:100%}
.chart-line{stroke:#4A9EFF;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
.chart-fill{fill:url(#chartGrad);opacity:0.25}
.chart-line-path{stroke-dasharray:600;stroke-dashoffset:600;animation:drawLine 2.5s 0.5s ease forwards}
@keyframes drawLine{to{stroke-dashoffset:0}}
.chart-dot{fill:#4A9EFF;r:4;animation:fadeIn 0.3s 3s ease both}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

/* metrics */
.term-metrics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:16px}
.term-metric{
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:10px;padding:12px;
}
.tm-label{font-family:var(--font-mono);font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px}
.tm-val{font-size:18px;font-weight:700;letter-spacing:-0.5px}
.tm-val.pos{color:var(--green)}
.tm-val.neg{color:var(--red)}
.tm-val.blue{color:var(--blue)}
.tm-sub{font-family:var(--font-mono);font-size:9px;color:var(--muted);margin-top:3px}

/* live trades */
.term-trades-header{font-family:var(--font-mono);font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;margin-bottom:8px}
.trade-row{
  display:flex;align-items:center;justify-content:space-between;
  padding:8px 10px;background:rgba(255,255,255,0.02);border:1px solid var(--border);
  border-radius:7px;margin-bottom:4px;
}
.trade-sym{font-weight:600;font-size:12px;letter-spacing:0.5px}
.trade-dir{font-family:var(--font-mono);font-size:9px;padding:2px 7px;border-radius:4px;font-weight:500}
.trade-dir.buy{background:rgba(52,211,153,0.12);color:var(--green)}
.trade-dir.sell{background:rgba(248,113,113,0.12);color:var(--red)}
.trade-pnl{font-family:var(--font-mono);font-size:12px;font-weight:600}
.trade-pnl.pos{color:var(--green)}
.trade-pnl.neg{color:var(--red)}
.trade-price{font-family:var(--font-mono);font-size:10px;color:var(--muted)}
.term-ticker{
  border-top:1px solid var(--border);margin-top:14px;padding-top:12px;overflow:hidden;
}
.ticker-inner2{display:flex;gap:28px;animation:ticker2 30s linear infinite;white-space:nowrap}
@keyframes ticker2{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.tick-item{display:flex;align-items:center;gap:6px;font-family:var(--font-mono);font-size:10px}
.tick-sym{color:var(--white);font-weight:500}
.tick-val{color:var(--muted)}
.tick-chg{font-weight:600}
.tick-chg.up{color:var(--green)}
.tick-chg.dn{color:var(--red)}

/* ── TICKER BAR ── */
.ticker-bar{border-top:1px solid var(--border);border-bottom:1px solid var(--border);background:rgba(13,15,17,0.8);padding:10px 0;overflow:hidden;position:relative;z-index:2}
.ticker-bar::before,.ticker-bar::after{content:'';position:absolute;top:0;bottom:0;width:80px;z-index:3;pointer-events:none}
.ticker-bar::before{left:0;background:linear-gradient(90deg,var(--black),transparent)}
.ticker-bar::after{right:0;background:linear-gradient(270deg,var(--black),transparent)}
.ticker-scroll{display:flex;gap:40px;animation:ticker3 50s linear infinite;white-space:nowrap}
@keyframes ticker3{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.tick2{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-mono);font-size:11px}
.tick2-sym{color:var(--white);font-weight:500;letter-spacing:0.5px}
.tick2-price{color:var(--muted)}
.tick2-chg{font-weight:600}
.tick2-chg.up{color:var(--green)}
.tick2-chg.dn{color:var(--red)}
.tick2-sep{color:rgba(255,255,255,0.12)}

/* ── SECTION BASE ── */
section{padding:100px 0;position:relative;z-index:2}
.section-label{
  font-family:var(--font-mono);font-size:10px;color:var(--blue);letter-spacing:3px;
  text-transform:uppercase;margin-bottom:16px;display:block;
}
.section-title{font-size:clamp(36px,5vw,58px);font-weight:800;letter-spacing:-2px;line-height:1;color:var(--white);margin-bottom:20px}
.section-sub{font-size:16px;color:var(--muted);line-height:1.75;max-width:520px}
.section-header{margin-bottom:64px}
.section-header.center{text-align:center}
.section-header.center .section-sub{margin:0 auto}

/* ── PROGRAMS ── */
.programs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:900px){.programs-grid{grid-template-columns:1fr}}
.prog-card{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:32px;position:relative;overflow:hidden;
  transition:border-color 0.3s,transform 0.3s,box-shadow 0.3s;
  cursor:pointer;
}
.prog-card::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,var(--glow,rgba(74,158,255,0.04)) 0%,transparent 60%);
  opacity:0;transition:opacity 0.3s;
}
.prog-card:hover{transform:translateY(-4px);box-shadow:0 20px 60px rgba(0,0,0,0.4);border-color:var(--card-accent,var(--border2))}
.prog-card:hover::before{opacity:1}
.prog-card.featured{border-color:rgba(74,158,255,0.2);box-shadow:0 0 0 1px rgba(74,158,255,0.08),0 20px 60px rgba(0,0,0,0.3)}
.prog-card.featured::before{opacity:1}
.prog-badge{
  display:inline-block;font-family:var(--font-mono);font-size:9px;letter-spacing:1.5px;
  text-transform:uppercase;padding:4px 10px;border-radius:100px;margin-bottom:24px;font-weight:500;
}
.prog-type{font-size:22px;font-weight:800;letter-spacing:-0.5px;margin-bottom:6px}
.prog-tagline{font-size:13px;color:var(--muted);margin-bottom:28px;font-weight:400}
.prog-price-row{display:flex;align-items:baseline;gap:6px;margin-bottom:4px}
.prog-from{font-family:var(--font-mono);font-size:10px;color:var(--muted);letter-spacing:1px}
.prog-price{font-size:38px;font-weight:800;letter-spacing:-1.5px}
.prog-currency{font-size:18px;font-weight:500;align-self:flex-start;margin-top:8px}
.prog-divider{height:1px;background:var(--border);margin:24px 0}
.prog-rule{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.prog-rule-label{font-size:12px;color:var(--muted)}
.prog-rule-val{font-family:var(--font-mono);font-size:12px;font-weight:600}
.prog-rule-val.g{color:var(--green)}
.prog-rule-val.r{color:var(--red)}
.prog-rule-val.b{color:var(--blue)}
.prog-rule-val.w{color:var(--white)}
.prog-cta{
  width:100%;margin-top:24px;padding:13px;border-radius:10px;
  font-size:13px;font-weight:600;font-family:inherit;cursor:pointer;
  transition:all 0.2s;border:1px solid;
}
.prog-cta.solid{background:var(--white);color:var(--black);border-color:var(--white)}
.prog-cta.solid:hover{background:#d8d8d4}
.prog-cta.outline{background:transparent;color:var(--white);border-color:var(--border2)}
.prog-cta.outline:hover{background:rgba(255,255,255,0.05)}

/* instant */
.prog-card.instant{--glow:rgba(212,168,68,0.06);--card-accent:rgba(212,168,68,0.2)}
/* 2step best value */
.prog-card.twostep{--glow:rgba(52,211,153,0.06);--card-accent:rgba(52,211,153,0.2)}

/* ── PERFORMANCE STRIP ── */
.perf-strip{
  background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:48px;display:grid;grid-template-columns:repeat(5,1fr);gap:0;
}
@media(max-width:900px){.perf-strip{grid-template-columns:repeat(2,1fr);gap:32px;padding:32px}}
.perf-item{text-align:center;position:relative}
.perf-item+.perf-item::before{
  content:'';position:absolute;left:0;top:20%;height:60%;
  width:1px;background:var(--border);
}
@media(max-width:900px){.perf-item+.perf-item::before{display:none}}
.perf-val{font-size:40px;font-weight:800;letter-spacing:-1.5px;line-height:1;margin-bottom:8px}
.perf-val.blue{color:var(--blue)}
.perf-val.green{color:var(--green)}
.perf-val.white{color:var(--white)}
.perf-label{font-family:var(--font-mono);font-size:10px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase}

/* ── SCALING TABLE ── */
.scaling-grid{display:grid;grid-template-columns:1fr 1.4fr;gap:60px;align-items:center}
@media(max-width:900px){.scaling-grid{grid-template-columns:1fr}}
.scaling-table{border:1px solid var(--border);border-radius:16px;overflow:hidden}
.scale-row{display:flex;align-items:center;padding:16px 24px;border-bottom:1px solid var(--border);transition:background 0.2s}
.scale-row:last-child{border-bottom:none}
.scale-row:hover{background:rgba(255,255,255,0.02)}
.scale-row.header{background:var(--card2);padding:12px 24px}
.scale-col-1{flex:1;font-size:13px}
.scale-col-2{width:120px;text-align:center;font-family:var(--font-mono);font-size:12px}
.scale-col-3{width:100px;text-align:right;font-family:var(--font-mono);font-size:13px;font-weight:600}
.scale-row.header .scale-col-1,.scale-row.header .scale-col-2,.scale-row.header .scale-col-3{
  font-family:var(--font-mono);font-size:9px;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;font-weight:400;
}
.scale-level{
  display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:10px;
  vertical-align:middle;
}
.scale-highlight{color:var(--blue)}
.scale-max{color:var(--green);font-weight:700}
.scaling-info{display:flex;flex-direction:column;gap:32px}
.info-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px}
.info-card-icon{font-size:24px;margin-bottom:14px}
.info-card-title{font-size:18px;font-weight:700;margin-bottom:8px;letter-spacing:-0.3px}
.info-card-desc{font-size:13px;color:var(--muted);line-height:1.75}

/* ── TESTIMONIALS ── */
.testi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:900px){.testi-grid{grid-template-columns:1fr}}
.testi-card{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:28px;display:flex;flex-direction:column;gap:20px;
  transition:border-color 0.3s;
}
.testi-card:hover{border-color:var(--border2)}
.testi-quote-mark{font-size:48px;font-family:var(--font-serif);color:var(--border2);line-height:1;margin-bottom:-12px}
.testi-text{font-size:14px;color:var(--muted);line-height:1.8;flex:1}
.testi-text strong{color:var(--white);font-weight:600}
.testi-author{display:flex;align-items:center;gap:12px;padding-top:16px;border-top:1px solid var(--border)}
.testi-avatar{width:36px;height:36px;border-radius:50%;background:var(--blue-dim);border:1px solid rgba(74,158,255,0.2);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--blue)}
.testi-name{font-size:13px;font-weight:600}
.testi-detail{font-family:var(--font-mono);font-size:10px;color:var(--muted);margin-top:2px}

/* ── FAQ ── */
.faq-grid{display:flex;flex-direction:column;gap:0;border:1px solid var(--border);border-radius:16px;overflow:hidden}
.faq-item{border-bottom:1px solid var(--border)}
.faq-item:last-child{border-bottom:none}
.faq-q{
  width:100%;text-align:left;padding:24px 28px;background:none;border:none;cursor:pointer;
  font-family:inherit;font-size:15px;font-weight:600;color:var(--white);
  display:flex;justify-content:space-between;align-items:center;gap:16px;
  transition:background 0.2s;
}
.faq-q:hover{background:rgba(255,255,255,0.02)}
.faq-arrow{
  width:20px;height:20px;border:1px solid var(--border2);border-radius:50%;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
  transition:transform 0.3s,border-color 0.3s;font-size:11px;color:var(--muted);
}
.faq-item.open .faq-arrow{transform:rotate(45deg);border-color:var(--blue);color:var(--blue)}
.faq-a{max-height:0;overflow:hidden;transition:max-height 0.4s ease}
.faq-item.open .faq-a{max-height:200px}
.faq-a-inner{padding:0 28px 24px;font-size:14px;color:var(--muted);line-height:1.8}

/* ── HOW IT WORKS ── */
.steps-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media(max-width:900px){.steps-grid{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.steps-grid{grid-template-columns:1fr}}
.step-card{
  background:var(--card);border:1px solid var(--border);border-radius:16px;
  padding:28px 24px;position:relative;overflow:hidden;
  transition:border-color 0.3s;
}
.step-card:hover{border-color:var(--border2)}
.step-num{
  font-family:var(--font-mono);font-size:11px;color:var(--blue);letter-spacing:2px;
  margin-bottom:20px;display:block;
}
.step-title{font-size:16px;font-weight:700;margin-bottom:10px;letter-spacing:-0.3px}
.step-desc{font-size:13px;color:var(--muted);line-height:1.7}
.step-icon{font-size:28px;margin-bottom:16px;display:block;opacity:0.8}
.step-connector{display:none}

/* ── FOOTER ── */
footer{
  border-top:1px solid var(--border);padding:60px 0 40px;
  position:relative;z-index:2;
}
.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:60px;margin-bottom:60px}
@media(max-width:900px){.footer-grid{grid-template-columns:1fr 1fr;gap:40px}}
@media(max-width:500px){.footer-grid{grid-template-columns:1fr}}
.footer-brand{display:flex;flex-direction:column;gap:16px}
.footer-brand-desc{font-size:13px;color:var(--muted);line-height:1.7;max-width:260px}
.footer-disclaimer{font-size:11px;color:var(--muted2);line-height:1.6;margin-top:8px;max-width:280px}
.footer-col-title{font-family:var(--font-mono);font-size:10px;color:var(--white);letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;font-weight:500}
.footer-links{display:flex;flex-direction:column;gap:10px}
.footer-links a{font-size:13px;color:var(--muted);text-decoration:none;transition:color 0.2s}
.footer-links a:hover{color:var(--white)}
.footer-bottom{display:flex;justify-content:space-between;align-items:center;padding-top:28px;border-top:1px solid var(--border)}
.footer-copy{font-family:var(--font-mono);font-size:11px;color:var(--muted2)}
.footer-socials{display:flex;gap:16px}
.footer-social{
  width:34px;height:34px;border:1px solid var(--border);border-radius:8px;
  display:flex;align-items:center;justify-content:center;font-size:13px;
  color:var(--muted);text-decoration:none;transition:all 0.2s;
}
.footer-social:hover{border-color:var(--border2);color:var(--white);background:rgba(255,255,255,0.04)}

/* ── DIVIDER ── */
.divider{height:1px;background:var(--border);margin:0}

/* ── FEATURE STRIP ── */
.feature-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:1px solid var(--border);border-radius:16px;overflow:hidden;margin-top:60px}
@media(max-width:700px){.feature-strip{grid-template-columns:1fr 1fr}}
.feat{
  padding:28px 24px;border-right:1px solid var(--border);
  transition:background 0.2s;
}
.feat:last-child{border-right:none}
.feat:hover{background:rgba(255,255,255,0.02)}
.feat-icon{font-size:20px;margin-bottom:14px;display:block}
.feat-title{font-size:14px;font-weight:600;margin-bottom:6px;letter-spacing:-0.2px}
.feat-desc{font-size:12px;color:var(--muted);line-height:1.65}

/* ── PAYOUT SECTION ── */
.payout-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
@media(max-width:900px){.payout-grid{grid-template-columns:1fr}}
.payout-visual{
  background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:36px;position:relative;overflow:hidden;
}
.payout-visual::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;background:radial-gradient(circle,rgba(52,211,153,0.08),transparent);pointer-events:none}
.payout-circle{
  width:140px;height:140px;border-radius:50%;margin:0 auto 28px;
  background:conic-gradient(var(--green) 324deg, rgba(255,255,255,0.08) 324deg);
  display:flex;align-items:center;justify-content:center;position:relative;
}
.payout-circle::before{content:'';position:absolute;inset:8px;border-radius:50%;background:var(--card)}
.payout-circle-inner{position:relative;z-index:1;text-align:center}
.payout-pct{font-size:28px;font-weight:800;color:var(--green);letter-spacing:-1px;line-height:1}
.payout-pct-label{font-family:var(--font-mono);font-size:9px;color:var(--muted);letter-spacing:1px}
.payout-rows{display:flex;flex-direction:column;gap:0}
.payout-row{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--border)}
.payout-row:last-child{border-bottom:none}
.payout-row-label{font-size:13px;color:var(--muted)}
.payout-row-val{font-family:var(--font-mono);font-size:13px;font-weight:600}
.payout-row-val.green{color:var(--green)}
.payout-info{display:flex;flex-direction:column;gap:28px}
.payout-point{display:flex;align-items:flex-start;gap:16px}
.payout-point-icon{width:40px;height:40px;border-radius:10px;background:var(--blue-dim);border:1px solid rgba(74,158,255,0.15);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:18px}
.payout-point-content{}
.payout-point-title{font-size:15px;font-weight:700;margin-bottom:5px;letter-spacing:-0.2px}
.payout-point-desc{font-size:13px;color:var(--muted);line-height:1.7}

/* ── CTA BANNER ── */
.cta-banner{
  background:var(--card);border:1px solid var(--border);border-radius:24px;
  padding:72px 80px;text-align:center;position:relative;overflow:hidden;
}
.cta-banner::before{content:'';position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:400px;height:400px;background:radial-gradient(circle,rgba(74,158,255,0.06),transparent 70%);pointer-events:none}
.cta-banner-label{font-family:var(--font-mono);font-size:10px;color:var(--blue);letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;display:block}
.cta-banner-title{font-size:clamp(36px,5vw,58px);font-weight:800;letter-spacing:-2px;line-height:1;margin-bottom:20px}
.cta-banner-sub{font-size:16px;color:var(--muted);max-width:460px;margin:0 auto 40px;line-height:1.7}
.cta-banner-actions{display:flex;justify-content:center;gap:16px;flex-wrap:wrap}

/* scroll reveal */
.reveal{opacity:0;transform:translateY(24px);transition:opacity 0.7s ease,transform 0.7s ease}
.reveal.visible{opacity:1;transform:translateY(0)}
</style>
</head>
<body>

<div class="ambient ambient-1"></div>
<div class="ambient ambient-2"></div>

<!-- NAV -->
<nav class="z">
  <div class="nav-inner">
    <a href="#" class="logo">
      <div class="logo-mark">AK</div>
      <span class="logo-text">AKFUNDED</span>
      <span class="logo-badge">BETA</span>
    </a>
    <div class="nav-links">
      <a href="#programs">Programs</a>
      <a href="#scaling">Scaling</a>
      <a href="#payouts">Payouts</a>
      <a href="#leaderboard">Leaderboard</a>
      <a href="#faq">FAQ</a>
    </div>
    <div class="nav-cta">
      <button class="btn-ghost">Sign In</button>
      <button class="btn-primary">Get Funded →</button>
    </div>
  </div>
</nav>

<!-- HERO -->
<section class="z" style="padding:0">
  <div class="container">
    <div class="hero">
      <div class="hero-left">
        <div class="hero-eyebrow">
          <span class="eyebrow-dot"></span>
          Live Trading Platform — Forex · Metals · Oil
        </div>
        <h1 class="hero-headline">
          Built For<br><em>Real Traders.</em>
        </h1>
        <p class="hero-sub">
          Trade with up to $2,000,000 in simulated funding. Prove your edge, keep up to 90% of your profits. No excuses.
        </p>
        <div class="hero-actions">
          <button class="btn-lg">Start Your Challenge</button>
          <button class="btn-outline">View Programs</button>
        </div>
        <div class="hero-meta">
          <div class="meta-item">
            <span class="meta-val">$2M+</span>
            <span class="meta-label">Total Payouts</span>
          </div>
          <div class="meta-sep"></div>
          <div class="meta-item">
            <span class="meta-val">3,500+</span>
            <span class="meta-label">Funded Traders</span>
          </div>
          <div class="meta-sep"></div>
          <div class="meta-item">
            <span class="meta-val">24hr</span>
            <span class="meta-label">Payout Speed</span>
          </div>
        </div>
      </div>

      <!-- TERMINAL -->
      <div class="hero-right">
        <div class="terminal-wrapper">
          <div class="term-header">
            <div class="term-dots">
              <div class="term-dot"></div>
              <div class="term-dot"></div>
              <div class="term-dot"></div>
            </div>
            <span class="term-title">AK TRADING TERMINAL v2.4</span>
            <div class="term-status">
              <div class="status-dot"></div>
              LIVE
            </div>
          </div>
          <div class="term-body">
            <!-- Equity Chart -->
            <div class="equity-chart">
              <svg class="chart-svg" viewBox="0 0 480 130" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="chartGrad" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="0%" stop-color="#4A9EFF" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#4A9EFF" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <path class="chart-fill" d="M0,110 L40,100 L80,90 L120,80 L150,85 L180,70 L210,65 L240,50 L270,45 L300,38 L330,30 L360,22 L400,18 L440,12 L480,8 L480,130 L0,130 Z"/>
                <path class="chart-line" id="chartLinePath" d="M0,110 L40,100 L80,90 L120,80 L150,85 L180,70 L210,65 L240,50 L270,45 L300,38 L330,30 L360,22 L400,18 L440,12 L480,8"/>
                <circle class="chart-dot" cx="480" cy="8"/>
              </svg>
              <div style="position:absolute;top:8px;left:0;display:flex;justify-content:space-between;width:100%;padding:0 4px">
                <div>
                  <div style="font-family:var(--font-mono);font-size:9px;color:var(--muted)">ACCOUNT EQUITY</div>
                  <div style="font-size:20px;font-weight:800;letter-spacing:-0.5px;color:var(--green)">$108,420</div>
                </div>
                <div style="text-align:right">
                  <div style="font-family:var(--font-mono);font-size:9px;color:var(--muted)">30D RETURN</div>
                  <div style="font-size:14px;font-weight:700;color:var(--green)">+8.42%</div>
                </div>
              </div>
            </div>

            <!-- Metrics -->
            <div class="term-metrics">
              <div class="term-metric">
                <div class="tm-label">Win Rate</div>
                <div class="tm-val blue">71.4%</div>
                <div class="tm-sub">↑ 3.2% this week</div>
              </div>
              <div class="term-metric">
                <div class="tm-label">Drawdown</div>
                <div class="tm-val neg">-2.1%</div>
                <div class="tm-sub">Limit: 10%</div>
              </div>
              <div class="term-metric">
                <div class="tm-label">Profit Factor</div>
                <div class="tm-val pos">2.4x</div>
                <div class="tm-sub">Strong edge</div>
              </div>
            </div>

            <!-- Live Trades -->
            <div class="term-trades-header">Active Positions</div>
            <div class="trade-row">
              <span class="trade-sym">XAUUSD</span>
              <span class="trade-dir buy">BUY</span>
              <span class="trade-price">2345.80</span>
              <span class="trade-pnl pos">+$420</span>
            </div>
            <div class="trade-row">
              <span class="trade-sym">EURUSD</span>
              <span class="trade-dir sell">SELL</span>
              <span class="trade-price">1.0842</span>
              <span class="trade-pnl pos">+$180</span>
            </div>
            <div class="trade-row">
              <span class="trade-sym">USOIL</span>
              <span class="trade-dir buy">BUY</span>
              <span class="trade-price">82.45</span>
              <span class="trade-pnl neg">-$95</span>
            </div>

            <!-- Mini Ticker -->
            <div class="term-ticker">
              <div class="ticker-inner2">
                <div class="tick-item"><span class="tick-sym">XAUUSD</span><span class="tick-val">2345.80</span><span class="tick-chg up">+0.42%</span></div>
                <div class="tick-item"><span class="tick-sym">EURUSD</span><span class="tick-val">1.0842</span><span class="tick-chg dn">-0.12%</span></div>
                <div class="tick-item"><span class="tick-sym">GBPUSD</span><span class="tick-val">1.2680</span><span class="tick-chg up">+0.08%</span></div>
                <div class="tick-item"><span class="tick-sym">USOIL</span><span class="tick-val">82.45</span><span class="tick-chg up">+1.20%</span></div>
                <div class="tick-item"><span class="tick-sym">USDJPY</span><span class="tick-val">151.42</span><span class="tick-chg up">+0.31%</span></div>
                <div class="tick-item"><span class="tick-sym">XAUUSD</span><span class="tick-val">2345.80</span><span class="tick-chg up">+0.42%</span></div>
                <div class="tick-item"><span class="tick-sym">EURUSD</span><span class="tick-val">1.0842</span><span class="tick-chg dn">-0.12%</span></div>
                <div class="tick-item"><span class="tick-sym">GBPUSD</span><span class="tick-val">1.2680</span><span class="tick-chg up">+0.08%</span></div>
                <div class="tick-item"><span class="tick-sym">USOIL</span><span class="tick-val">82.45</span><span class="tick-chg up">+1.20%</span></div>
                <div class="tick-item"><span class="tick-sym">USDJPY</span><span class="tick-val">151.42</span><span class="tick-chg up">+0.31%</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- TICKER BAR -->
<div class="ticker-bar z">
  <div class="ticker-scroll">
    <div class="tick2"><span class="tick2-sym">XAUUSD</span><span class="tick2-price">2,345.80</span><span class="tick2-chg up">+0.42%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">XAGUSD</span><span class="tick2-price">29.15</span><span class="tick2-chg dn">-0.18%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">EURUSD</span><span class="tick2-price">1.08420</span><span class="tick2-chg dn">-0.12%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">GBPUSD</span><span class="tick2-price">1.26800</span><span class="tick2-chg up">+0.08%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">USDJPY</span><span class="tick2-price">151.420</span><span class="tick2-chg up">+0.31%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">AUDUSD</span><span class="tick2-price">0.65400</span><span class="tick2-chg dn">-0.22%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">USOIL</span><span class="tick2-price">82.45</span><span class="tick2-chg up">+1.20%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">UKOIL</span><span class="tick2-price">87.30</span><span class="tick2-chg up">+0.95%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">NATGAS</span><span class="tick2-price">2.180</span><span class="tick2-chg dn">-0.85%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">NZDUSD</span><span class="tick2-price">0.60150</span><span class="tick2-chg dn">-0.15%</span></div><span class="tick2-sep">·</span>
    <!-- repeat -->
    <div class="tick2"><span class="tick2-sym">XAUUSD</span><span class="tick2-price">2,345.80</span><span class="tick2-chg up">+0.42%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">XAGUSD</span><span class="tick2-price">29.15</span><span class="tick2-chg dn">-0.18%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">EURUSD</span><span class="tick2-price">1.08420</span><span class="tick2-chg dn">-0.12%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">GBPUSD</span><span class="tick2-price">1.26800</span><span class="tick2-chg up">+0.08%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">USDJPY</span><span class="tick2-price">151.420</span><span class="tick2-chg up">+0.31%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">USOIL</span><span class="tick2-price">82.45</span><span class="tick2-chg up">+1.20%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">UKOIL</span><span class="tick2-price">87.30</span><span class="tick2-chg up">+0.95%</span></div><span class="tick2-sep">·</span>
    <div class="tick2"><span class="tick2-sym">NATGAS</span><span class="tick2-price">2.180</span><span class="tick2-chg dn">-0.85%</span></div><span class="tick2-sep">·</span>
  </div>
</div>

<!-- PERFORMANCE STRIP -->
<section class="z" style="padding:60px 0">
  <div class="container reveal">
    <div class="perf-strip">
      <div class="perf-item">
        <div class="perf-val blue">$2M+</div>
        <div class="perf-label">Total Payouts</div>
      </div>
      <div class="perf-item">
        <div class="perf-val green">3,500+</div>
        <div class="perf-label">Funded Traders</div>
      </div>
      <div class="perf-item">
        <div class="perf-val white">180+</div>
        <div class="perf-label">Countries</div>
      </div>
      <div class="perf-item">
        <div class="perf-val green">90%</div>
        <div class="perf-label">Max Profit Split</div>
      </div>
      <div class="perf-item">
        <div class="perf-val white">24hr</div>
        <div class="perf-label">Payout Processing</div>
      </div>
    </div>
  </div>
</section>

<!-- PROGRAMS -->
<section id="programs" class="z">
  <div class="container">
    <div class="section-header center reveal">
      <span class="section-label">Funding Programs</span>
      <h2 class="section-title">Choose your path<br>to funding.</h2>
      <p class="section-sub">Three distinct programs. One goal — get you funded and trading with real capital.</p>
    </div>
    <div class="programs-grid reveal">

      <!-- INSTANT -->
      <div class="prog-card instant" style="--glow:rgba(212,168,68,0.06)">
        <div class="prog-badge" style="background:rgba(212,168,68,0.1);color:var(--gold);border:1px solid rgba(212,168,68,0.2)">Instant Access</div>
        <div class="prog-type" style="color:var(--gold)">Instant Funded</div>
        <div class="prog-tagline">No evaluation. Trade immediately.</div>
        <div class="prog-price-row">
          <span class="prog-from">From</span>
          <span class="prog-currency" style="color:var(--gold)">$</span>
          <span class="prog-price" style="color:var(--gold)">299</span>
        </div>
        <div class="prog-divider"></div>
        <div class="prog-rule"><span class="prog-rule-label">Profit Split</span><span class="prog-rule-val" style="color:var(--gold)">70–75%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Daily Loss</span><span class="prog-rule-val r">−3%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Max Loss</span><span class="prog-rule-val r">−6%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Evaluation</span><span class="prog-rule-val g">None</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Time Limit</span><span class="prog-rule-val g">None</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Account Size</span><span class="prog-rule-val w">$5K – $100K</span></div>
        <button class="prog-cta outline">Start Instant →</button>
      </div>

      <!-- ONE-STEP (FEATURED) -->
      <div class="prog-card featured" style="--glow:rgba(74,158,255,0.08)">
        <div style="position:absolute;top:20px;right:20px;background:var(--blue-dim);color:var(--blue);border:1px solid rgba(74,158,255,0.2);font-family:var(--font-mono);font-size:9px;padding:4px 10px;border-radius:100px;letter-spacing:1px">Most Popular</div>
        <div class="prog-badge" style="background:var(--blue-dim);color:var(--blue);border:1px solid rgba(74,158,255,0.2)">Single Phase</div>
        <div class="prog-type" style="color:var(--blue)">One-Step Challenge</div>
        <div class="prog-tagline">One phase, then fully funded.</div>
        <div class="prog-price-row">
          <span class="prog-from">From</span>
          <span class="prog-currency" style="color:var(--blue)">$</span>
          <span class="prog-price" style="color:var(--blue)">79</span>
        </div>
        <div class="prog-divider"></div>
        <div class="prog-rule"><span class="prog-rule-label">Profit Split</span><span class="prog-rule-val b">80%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Profit Target</span><span class="prog-rule-val g">+8%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Daily Loss</span><span class="prog-rule-val r">−5%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Max Loss</span><span class="prog-rule-val r">−10%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Min Days</span><span class="prog-rule-val w">5 days</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Account Size</span><span class="prog-rule-val w">$5K – $100K</span></div>
        <button class="prog-cta solid">Start Challenge →</button>
      </div>

      <!-- TWO-STEP -->
      <div class="prog-card twostep" style="--glow:rgba(52,211,153,0.06)">
        <div class="prog-badge" style="background:rgba(52,211,153,0.08);color:var(--green);border:1px solid rgba(52,211,153,0.2)">Best Value</div>
        <div class="prog-type" style="color:var(--green)">Two-Step Challenge</div>
        <div class="prog-tagline">Highest split. Lowest entry price.</div>
        <div class="prog-price-row">
          <span class="prog-from">From</span>
          <span class="prog-currency" style="color:var(--green)">$</span>
          <span class="prog-price" style="color:var(--green)">49</span>
        </div>
        <div class="prog-divider"></div>
        <div class="prog-rule"><span class="prog-rule-label">Profit Split</span><span class="prog-rule-val" style="color:var(--green)">90%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Phase 1 Target</span><span class="prog-rule-val g">+8%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Phase 2 Target</span><span class="prog-rule-val g">+5%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Daily Loss</span><span class="prog-rule-val r">−5%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Max Loss</span><span class="prog-rule-val r">−10%</span></div>
        <div class="prog-rule"><span class="prog-rule-label">Account Size</span><span class="prog-rule-val w">$5K – $100K</span></div>
        <button class="prog-cta outline" style="border-color:rgba(52,211,153,0.3);color:var(--green)">Start Two-Step →</button>
      </div>
    </div>

    <!-- Feature strip -->
    <div class="feature-strip reveal">
      <div class="feat">
        <span class="feat-icon">⚡</span>
        <div class="feat-title">Instant Activation</div>
        <div class="feat-desc">Challenges activate the moment you sign up. No waiting, no delays.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">🔒</span>
        <div class="feat-title">No Time Limits</div>
        <div class="feat-desc">Trade at your own pace. No calendar pressure. Pure performance focus.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">📊</span>
        <div class="feat-title">All Instruments</div>
        <div class="feat-desc">Forex majors, XAUUSD, XAGUSD, Crude Oil, Natural Gas — all included.</div>
      </div>
      <div class="feat">
        <span class="feat-icon">💸</span>
        <div class="feat-title">24hr Payouts</div>
        <div class="feat-desc">Withdrawal processed within 24 hours, every time. No friction.</div>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="z" style="background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-header center reveal">
      <span class="section-label">Process</span>
      <h2 class="section-title">Four steps<br>to funded.</h2>
    </div>
    <div class="steps-grid reveal">
      <div class="step-card">
        <span class="step-num">01 —</span>
        <span class="step-icon">🎯</span>
        <div class="step-title">Pick a Program</div>
        <div class="step-desc">Instant Funded, One-Step, or Two-Step. Choose your account size from $5K to $100K. Activate in seconds.</div>
      </div>
      <div class="step-card">
        <span class="step-num">02 —</span>
        <span class="step-icon">📈</span>
        <div class="step-title">Pass the Evaluation</div>
        <div class="step-desc">Hit the profit target while respecting daily and maximum drawdown limits. Trade any supported instrument.</div>
      </div>
      <div class="step-card">
        <span class="step-num">03 —</span>
        <span class="step-icon">✅</span>
        <div class="step-title">Verify & Get Funded</div>
        <div class="step-desc">Complete identity verification and receive your funded account credentials. Ready to trade with real capital.</div>
      </div>
      <div class="step-card">
        <span class="step-num">04 —</span>
        <span class="step-icon">🚀</span>
        <div class="step-title">Scale to $2,000,000</div>
        <div class="step-desc">Consistent performance unlocks scaling milestones. Your account grows alongside your track record.</div>
      </div>
    </div>
  </div>
</section>

<!-- SCALING -->
<section id="scaling" class="z">
  <div class="container">
    <div class="scaling-grid">
      <div class="reveal">
        <span class="section-label">Scaling Plan</span>
        <h2 class="section-title">Your capital<br>grows with you.</h2>
        <p class="section-sub" style="margin-bottom:40px">Consistent profitability is rewarded with account scale-ups. From $5K to $2,000,000 in simulated funding.</p>
        <div class="scaling-table">
          <div class="scale-row header">
            <span class="scale-col-1">Milestone</span>
            <span class="scale-col-2">Account Size</span>
            <span class="scale-col-3">Split</span>
          </div>
          <div class="scale-row">
            <span class="scale-col-1"><span class="scale-level" style="background:#6B7280"></span>Entry Level</span>
            <span class="scale-col-2">$5K – $25K</span>
            <span class="scale-col-3">80%</span>
          </div>
          <div class="scale-row">
            <span class="scale-col-1"><span class="scale-level" style="background:#4A9EFF"></span>Funded Trader</span>
            <span class="scale-col-2">$50K – $100K</span>
            <span class="scale-col-3 scale-highlight">85%</span>
          </div>
          <div class="scale-row">
            <span class="scale-col-1"><span class="scale-level" style="background:#34D399"></span>Senior Trader</span>
            <span class="scale-col-2">$200K – $500K</span>
            <span class="scale-col-3 scale-highlight">88%</span>
          </div>
          <div class="scale-row">
            <span class="scale-col-1"><span class="scale-level" style="background:#D4A844"></span>Elite Trader</span>
            <span class="scale-col-2">$500K – $1M</span>
            <span class="scale-col-3 scale-highlight">90%</span>
          </div>
          <div class="scale-row">
            <span class="scale-col-1"><span class="scale-level" style="background:#F87171"></span>Master Trader</span>
            <span class="scale-col-2 scale-max">Up to $2M</span>
            <span class="scale-col-3 scale-max">90%+</span>
          </div>
        </div>
      </div>
      <div class="scaling-info reveal">
        <div class="info-card">
          <div class="info-card-icon">📊</div>
          <div class="info-card-title">Performance-Based Growth</div>
          <div class="info-card-desc">Scale-ups are triggered automatically when you hit profitability milestones. No application required, no committee review.</div>
        </div>
        <div class="info-card">
          <div class="info-card-icon">🛡</div>
          <div class="info-card-title">Protections at Scale</div>
          <div class="info-card-desc">As your account grows, your drawdown rules remain consistent. We protect your capital and your progress simultaneously.</div>
        </div>
        <div class="info-card">
          <div class="info-card-icon">⚡</div>
          <div class="info-card-title">No Ceiling on Talent</div>
          <div class="info-card-desc">The best traders get the most capital. Simple. There is no arbitrary cap — your results determine your limit.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PAYOUTS -->
<section id="payouts" class="z" style="background:var(--surface);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="payout-grid">
      <div class="reveal">
        <span class="section-label">Payout System</span>
        <h2 class="section-title">Your profits,<br>fast.</h2>
        <p class="section-sub" style="margin-bottom:48px">Up to 90% profit split, processed within 24 hours. No games, no holds, no nonsense.</p>
        <div class="payout-info">
          <div class="payout-point">
            <div class="payout-point-icon">⚡</div>
            <div class="payout-point-content">
              <div class="payout-point-title">24-Hour Processing</div>
              <div class="payout-point-desc">Every payout request is processed within 24 hours. We built systems that prioritize your time.</div>
            </div>
          </div>
          <div class="payout-point">
            <div class="payout-point-icon">🌍</div>
            <div class="payout-point-content">
              <div class="payout-point-title">Global Transfers</div>
              <div class="payout-point-desc">Receive payouts via bank wire, UPI, or crypto. Available in 180+ countries.</div>
            </div>
          </div>
          <div class="payout-point">
            <div class="payout-point-icon">📅</div>
            <div class="payout-point-content">
              <div class="payout-point-title">Bi-Weekly Schedule</div>
              <div class="payout-point-desc">Request withdrawals on a bi-weekly basis. First payout available after your 7th trading day.</div>
            </div>
          </div>
        </div>
      </div>
      <div class="payout-visual reveal">
        <div class="payout-circle">
          <div class="payout-circle-inner">
            <div class="payout-pct">90%</div>
            <div class="payout-pct-label">YOURS</div>
          </div>
        </div>
        <div class="payout-rows">
          <div class="payout-row">
            <span class="payout-row-label">Two-Step Profit Split</span>
            <span class="payout-row-val green">90%</span>
          </div>
          <div class="payout-row">
            <span class="payout-row-label">One-Step Profit Split</span>
            <span class="payout-row-val green">80%</span>
          </div>
          <div class="payout-row">
            <span class="payout-row-label">Instant Funded Split</span>
            <span class="payout-row-val" style="color:var(--gold)">75%</span>
          </div>
          <div class="payout-row">
            <span class="payout-row-label">Processing Time</span>
            <span class="payout-row-val" style="color:var(--blue)">24 hours</span>
          </div>
          <div class="payout-row">
            <span class="payout-row-label">Min Payout</span>
            <span class="payout-row-val green">$50</span>
          </div>
          <div class="payout-row">
            <span class="payout-row-label">Payout Methods</span>
            <span class="payout-row-val" style="color:var(--white)">Wire · UPI · Crypto</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section id="leaderboard" class="z">
  <div class="container">
    <div class="section-header center reveal">
      <span class="section-label">Funded Traders</span>
      <h2 class="section-title">Real results.<br>Real traders.</h2>
      <p class="section-sub">Hundreds of traders funded across India, UAE, Singapore, and 177 other countries.</p>
    </div>
    <div class="testi-grid reveal">
      <div class="testi-card">
        <div class="testi-quote-mark">"</div>
        <div class="testi-text">Passed the <strong>$50K One-Step</strong> on XAUUSD in 4 trading days. The rules are straightforward, the platform is solid, and my payout arrived same afternoon I requested it.</div>
        <div class="testi-author">
          <div class="testi-avatar">RS</div>
          <div>
            <div class="testi-name">Rahul S.</div>
            <div class="testi-detail">$50K Funded · +$4,200 Payout · One-Step</div>
          </div>
        </div>
      </div>
      <div class="testi-card">
        <div class="testi-quote-mark">"</div>
        <div class="testi-text">The <strong>Two-Step gives 90% split</strong> at the most affordable entry point I found anywhere. Already completed three funded accounts. The scaling structure is what keeps me here.</div>
        <div class="testi-author">
          <div class="testi-avatar">PM</div>
          <div>
            <div class="testi-name">Priya M.</div>
            <div class="testi-detail">$25K Funded · +$2,250 Payout · Two-Step</div>
          </div>
        </div>
      </div>
      <div class="testi-card">
        <div class="testi-quote-mark">"</div>
        <div class="testi-text"><strong>Instant Funded is exceptional</strong> for traders who already know what they're doing. Got funded on day one, started trading USOIL immediately. My kind of platform.</div>
        <div class="testi-author">
          <div class="testi-avatar">KT</div>
          <div>
            <div class="testi-name">Kiran T.</div>
            <div class="testi-detail">$25K Instant Funded · 3 Accounts Completed</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="z" style="background:var(--surface);border-top:1px solid var(--border)">
  <div class="container">
    <div class="section-header center reveal" style="margin-bottom:48px">
      <span class="section-label">FAQ</span>
      <h2 class="section-title">Common questions.</h2>
    </div>
    <div style="max-width:760px;margin:0 auto" class="reveal">
      <div class="faq-grid">
        <div class="faq-item open">
          <button class="faq-q" onclick="toggleFaq(this)">
            What instruments can I trade?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">All Forex major and minor pairs, Gold (XAUUSD), Silver (XAGUSD), WTI and Brent Crude Oil, and Natural Gas. The full instrument list is available across all programs with no restrictions on which pairs you can use.</div>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            Is there a time limit to pass the challenge?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">No time limits on any program. You trade at your own pace. The only requirement for One-Step and Two-Step programs is a minimum number of trading days (5 and 4 respectively), which ensures disciplined, consistent trading rather than one lucky session.</div>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            How quickly are payouts processed?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">All payout requests are processed within 24 hours. Funds arrive via your chosen method — bank wire, UPI, or crypto. Payouts are available bi-weekly once you've completed your minimum trading day requirement.</div>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            What happens if I breach a rule?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">The account is automatically marked as failed and you receive an immediate notification with the specific reason. You can start a new challenge at any time — many successful traders needed more than one attempt before passing.</div>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            Are accounts simulated?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">Yes. All accounts on AKFunded are simulated prop trading environments. This means you trade in conditions that mirror real markets, with real rules and real profit tracking, without risking live market exposure beyond the evaluation fee.</div>
          </div>
        </div>
        <div class="faq-item">
          <button class="faq-q" onclick="toggleFaq(this)">
            Can I hold trades over the weekend?
            <div class="faq-arrow">+</div>
          </button>
          <div class="faq-a">
            <div class="faq-a-inner">Yes, weekend holding is permitted. There are no restrictions on swing trading or position holding duration. You manage your own risk, and we manage the platform rules consistently.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- CTA BANNER -->
<section class="z">
  <div class="container reveal">
    <div class="cta-banner">
      <span class="cta-banner-label">Ready to start?</span>
      <h2 class="cta-banner-title">Prove your edge.<br>Get funded.</h2>
      <p class="cta-banner-sub">Join 3,500+ funded traders. Activate your challenge today and start trading with capital that scales.</p>
      <div class="cta-banner-actions">
        <button class="btn-lg">Start Your Challenge →</button>
        <button class="btn-outline">View All Programs</button>
      </div>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="z">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="#" class="logo">
          <div class="logo-mark">AK</div>
          <span class="logo-text">AKFUNDED</span>
        </a>
        <div class="footer-brand-desc">A prop trading evaluation platform built for serious traders. Prove your edge and trade with funded capital up to $2,000,000.</div>
        <div class="footer-disclaimer">All accounts are simulated. AKFunded is a trading evaluation platform. Past performance does not guarantee future results.</div>
      </div>
      <div>
        <div class="footer-col-title">Programs</div>
        <div class="footer-links">
          <a href="#">Instant Funded</a>
          <a href="#">One-Step Challenge</a>
          <a href="#">Two-Step Challenge</a>
          <a href="#">Scaling Plan</a>
          <a href="#">Payout System</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Platform</div>
        <div class="footer-links">
          <a href="#">Dashboard</a>
          <a href="#">Live Markets</a>
          <a href="#">AI Coach</a>
          <a href="#">Trade Journal</a>
          <a href="#">Leaderboard</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Company</div>
        <div class="footer-links">
          <a href="#">About</a>
          <a href="https://www.instagram.com/akfunded" target="_blank">Instagram @akfunded</a>
          <a href="#">Refer & Earn</a>
          <a href="#">Support</a>
          <a href="#">Terms</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">© 2025 AKFunded · Built by Akash Injeti · All accounts simulated</div>
      <div class="footer-socials">
        <a href="https://www.instagram.com/akfunded" class="footer-social" target="_blank" title="Instagram">IG</a>
        <a href="#" class="footer-social" title="Email">✉</a>
      </div>
    </div>
  </div>
</footer>

<script>
/* Scroll reveal */
const revealEls = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.transitionDelay = (i * 0.05) + 's';
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
revealEls.forEach(el => observer.observe(el));

/* FAQ toggle */
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/* Nav scroll effect */
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (window.scrollY > 40) {
    nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
  } else {
    nav.style.borderBottomColor = 'rgba(255,255,255,0.06)';
  }
});

/* Chart animation */
const chartPath = document.getElementById('chartLinePath');
if (chartPath) {
  const len = chartPath.getTotalLength ? chartPath.getTotalLength() : 600;
  chartPath.style.strokeDasharray = len;
  chartPath.style.strokeDashoffset = len;
  chartPath.style.animation = `drawLine 2.5s 0.8s ease forwards`;
}

/* Animated counters */
function animateVal(el, end, prefix='', suffix='') {
  let start = 0;
  const duration = 1800;
  const startTime = performance.now();
  const update = (t) => {
    const p = Math.min((t - startTime) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    el.textContent = prefix + Math.round(start + (end - start) * ease).toLocaleString() + suffix;
    if (p < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

/* Animate terminal trade prices */
const prices = { 'XAUUSD': 2345.80, 'EURUSD': 1.08420, 'USOIL': 82.45 };
setInterval(() => {
  document.querySelectorAll('.trade-price').forEach((el, i) => {
    const syms = Object.keys(prices);
    const base = prices[syms[i]] || 1;
    const delta = (Math.random() - 0.5) * base * 0.0002;
    const newVal = base + delta;
    el.textContent = newVal < 10 ? newVal.toFixed(5) : newVal.toFixed(2);
  });
}, 1800);

/* Equity counter animation */
setInterval(() => {
  const eq = document.querySelector('.hero-left ~ div .tm-val.pos');
}, 3000);

/* Magnetic button effect */
document.querySelectorAll('.btn-lg, .btn-primary').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.12}px, ${y * 0.12}px) translateY(-2px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
  });
});
</script>
</body>
</html>
