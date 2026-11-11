# -*- coding: utf-8 -*-
"""Generates standalone pages: site/index.html (EN), site/hr/index.html, site/it/index.html.
mode 'site' -> relative language links; mode 'preview' -> absolute preview URLs (JSON arg)."""
import json, html, sys, os
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from content import L
BASE = 'https://www.alkemija.hr/'
PRIVACY = 'https://www.alkemija.hr/pravila-privatnosti/'
LINKEDIN = 'https://www.linkedin.com/company/alkemija/'
WA = 'https://wa.me/38598516852'
CF7_ID = 4469  # Contact Form 7 form 'Alkemija naslovnica 2026 (EN/HR/IT)' -> info@alkemija.hr
ENDPOINT = f'https://www.alkemija.hr/wp-json/contact-form-7/v1/contact-forms/{CF7_ID}/feedback'
M = json.load(open(os.path.join(D, 'map.json')))
CSS = open(os.path.join(D, 'style.css'), encoding='utf-8').read()
JS = open(os.path.join(D, 'app.js'), encoding='utf-8').read()
e = html.escape
ICON = {
 'factory':'<path d="M3 21V10l6 4V10l6 4V6l6 3v12z"/><path d="M7 17h2M12 17h2M17 17h2"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
 'boxes':'<path d="M3 8l9-5 9 5-9 5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',
 'gear':'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'chat':'<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 'eye':'<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'check':'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'wa':'<path d="M20 11.6a8.2 8.2 0 01-12.2 7.2L3.5 20l1.3-4.1A8.2 8.2 0 1120 11.6z"/><path d="M9.2 8.2c.2 3.1 2.6 5.6 5.7 6l1-1.3 1.5.8c-.3.9-1.2 1.6-2.2 1.5-3.6-.4-6.4-3.2-6.8-6.8-.1-1 .6-1.9 1.5-2.2l.9 1.5z" fill="currentColor" stroke="none"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>',
 'web':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>',
}
def ic(n): return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICON[n]}</svg>'
import base64
LOGO = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(D, '..', 'site', 'assets', 'alkemija-logo-gold.png'), 'rb').read()).decode()
# Original gold Alkemija logo (source: alkemija.com/wp-content/uploads/2026/11/alkemija-logo-gold-tamna-pozadina.png), embedded at 2x
BRAND = (f'<img class="brand-logo" src="{LOGO}" alt="Alkemija" width="227" height="156" decoding="async">'
         '<span class="brand-sub" aria-hidden="true">BUSINESS<br>STUDIO</span>')

# ---- Hero map: positions are approximate on purpose (clean layout over precision) ----
NUDGE = {'Beograd':(213,168),'Sarajevo':(197,180),'Pristina':(218,186),'Podgorica':(203,196),'Skopje':(221,201)}
CURVE = {'Tunis': (178, 215)}  # custom control point so the Tunis line passes east of Rome
SKIP = {'Ljubljana'}  # too close to Zagreb
NAMES = {  # localised labels
 'en':{'Paris':'Paris','Roma':'Rome','Athina':'Athens','Pristina':'Pristina'},
 'hr':{'Paris':'Pariz','Roma':'Rim','Athina':'Atena','Pristina':'Priština'},
 'it':{'Paris':'Parigi','Roma':'Roma','Athina':'Atene','Pristina':'Pristina'},
}
# label placement: (dx, dy, anchor) relative to the node
LAB = {'Paris':(-5,2.3,'end'),'Amsterdam':(0,-6,'middle'),'Wien':(5,-3,'start'),'Warszawa':(5,-3,'start'),
       'Milano':(0,-6,'middle'),'Madrid':(5,6,'start'),'Roma':(-5,4,'end'),'Athina':(5,4,'start'),'Rabat':(5,4,'start'),'Tunis':(5,4,'start')}
# Balkan cluster: labels in a column to the east with thin leader lines
COL_X = 246; COL = [('Beograd',166),('Sarajevo',177),('Pristina',188),('Podgorica',199),('Skopje',210)]
def europe_svg(t):
    w, h = M['w'], M['h']
    d = ''.join(f'M{x} {y}h0' for x, y in M['dots'])
    c = {k: tuple(NUDGE.get(k, v)) for k, v in M['cities'].items() if k not in SKIP}
    hub = c['Zagreb']; nm = lambda k: NAMES[t['lang']].get(k, k)
    lines = []; nodes = []
    for i, (name, (x, y)) in enumerate(c.items()):
        if name == 'Zagreb': continue
        mx, my = (hub[0]+x)/2, (hub[1]+y)/2 - abs(hub[0]-x)*0.18 - 6
        if name in CURVE: mx, my = CURVE[name]
        lines.append(f'<path class="route" style="animation-delay:-{i*0.9:.1f}s" d="M{hub[0]} {hub[1]}Q{mx:.1f} {my:.1f} {x} {y}"/>')
        nodes.append(f'<circle class="node" cx="{x}" cy="{y}" r="{2 if name in dict(COL) else 2.4}"/>')
    lab = ''.join(f'<text x="{c[n][0]+dx}" y="{c[n][1]+dy}" text-anchor="{an}">{e(nm(n))}</text>' for n, (dx, dy, an) in LAB.items())
    lead = ''.join(f'<path class="lead" d="M{c[n][0]+2.5} {c[n][1]}L{COL_X-3} {ly-1.8}"/>' for n, ly in COL)
    lab += ''.join(f'<text class="sm" x="{COL_X}" y="{ly}">{e(nm(n))}</text>' for n, ly in COL)
    return (f'<svg class="map" viewBox="-6 -6 {w+12:.0f} {h+12:.0f}" role="img" aria-labelledby="mapt"><title id="mapt">{e(t["map_title"])}</title>'
            f'<path class="land" d="{d}"/><g>{"".join(lines)}</g><g>{lead}</g><g>{"".join(nodes)}</g>'
            f'<g class="labels">{lab}<text class="hub-l" x="{hub[0]-5}" y="{hub[1]-6}" text-anchor="end">Zagreb</text></g>'
            f'<circle class="pulse" cx="{hub[0]}" cy="{hub[1]}" r="5"/><circle class="hub" cx="{hub[0]}" cy="{hub[1]}" r="4.2"/></svg>')

Q = {'en': ('“', '”'), 'hr': ('„', '”'), 'it': ('«', '»')}
IDS = ['za-koga', 'usluge', 'kako-radimo', 'paketi', 'kontakt']

def page(code, mode, preview=None):
    t = L[code]; f = t['f']; q = Q[code]
    def href(c):
        if mode == 'preview': return preview[c]
        up = '../' if t['path'] else ''
        return (up + L[c]['path']) or './'
    canon = BASE + t['path']
    nav = ''.join(f'<a href="#{i}">{e(n)}</a>' for i, n in zip(IDS, t['nav']))
    mnav = ''.join(f'<li><a href="#{i}">{e(n)}</a></li>' for i, n in zip(IDS, t['nav']))
    langs = ''.join(f'<a href="{href(c)}" hreflang="{c}" lang="{c}" title="{t["lang_names"][c]}"' + (' aria-current="page"' if c == code else '') + f'>{c.upper()}</a>' for c in ['en', 'hr', 'it'])
    alts = '\n'.join(f'<link rel="alternate" hreflang="{c}" href="{BASE + L[c]["path"]}">' for c in ['en', 'hr', 'it']) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Alkemija Business Studio", "legalName": "Alkemija, obrt",
          "url": canon, "email": "info@alkemija.hr", "telephone": "+385 98 516 852", "taxID": "34772291906",
          "address": {"@type": "PostalAddress", "streetAddress": "3. Pile 10", "postalCode": "10000", "addressLocality": "Zagreb", "addressCountry": "HR"},
          "sameAs": [LINKEDIN, "https://alkemija.com/"], "inLanguage": t['lang'], "description": t['desc']}
    groups = ''.join(f'<article class="card aud rv">{ic(["factory","globe","boxes","gear"][i])}<h3>{e(n)}</h3><p>{e(d)}</p></article>' for i, (n, d) in enumerate(t['groups']))
    svcs = ''
    for i, (n, s, d, inc) in enumerate(t['services']):
        lis = ''.join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in inc)
        svcs += (f'<article class="card svc rv"><span class="num">0{i+1}</span><h3>{e(n)}</h3><p class="slogan">{q[0]}{e(s)}{q[1]}</p>'
                 f'<p class="desc">{e(d)}</p><h4>{e(t["incl"])}</h4><ul class="ticks">{lis}</ul>'
                 f'<a class="tlink" href="#kontakt" data-svc="{i}">{e(t["cta1"])} {ic("arrow")}</a></article>')
    steps = ''.join(f'<li class="step rv"><span class="n" aria-hidden="true">0{i+1}</span><h3><span class="sr">0{i+1} — </span>{e(n)}</h3><p>{e(d)}</p></li>' for i, (n, d) in enumerate(t['steps']))
    packs = ''
    for i, (n, p, items) in enumerate(t['packs']):
        ft = i == 1
        lis = ''.join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in items)
        badge = f'<span class="badge">{e(t["rec"])}</span>' if ft else ''
        packs += (f'<article class="card pack rv{" featured" if ft else ""}" aria-labelledby="p{i}">{badge}<h3 class="name" id="p{i}">{n}</h3>'
                  f'<p class="price">{e(t["cur"](p))}</p><p class="vatx">{e(t["vat_short"])}</p><ul class="ticks">{lis}</ul>'
                  f'<a class="btn {"btn-gold" if ft else "btn-line"}" href="#kontakt" data-pack="{n}">{e(t["pack_cta"])}</a></article>')
    case = ''.join(f'<div{" class=kpi" if 4 <= i <= 6 else ""}><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for i, (a, b) in enumerate(t['case']))
    why = ''.join(f'<article class="card rv">{ic(["pin","chat","eye"][i])}<h3>{e(n)}</h3><p>{e(d)}</p></article>' for i, (n, d) in enumerate(t['why']))
    opts = f'<option value="">{e(f["pack_none"])}</option>' + ''.join(f'<option value="{n}">{n} — {e(t["cur"](p))}</option>' for n, p, _ in t['packs'])
    msg = json.dumps(dict(err=f['err'], err_email=f['err_email'], mailto=f['mailto_msg'], sending=f['sending'], ok=f['ok'], fail=f['fail'],
                          subject=f['subject'], labels=[f['name'], f['company'], f['email'], f['market'], f['goal'], f['pack']]), ensure_ascii=False)
    R = '<span class="req" aria-hidden="true">*</span>'
    return f'''<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{canon}">
{alts}
<meta name="theme-color" content="#0f2033">
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Alkemija Business Studio">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:image" content="https://www.alkemija.hr/wp-content/uploads/alkemija-home-2026-og2-{code}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t['og_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<!-- Structured data: only facts confirmed by the business -->
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>

<!-- ============ HEADER / NAVIGATION (sticky) ============ -->
<header class="hdr" id="top">
  <div class="wrap">
    <a class="brand" href="#top" aria-label="Alkemija Business Studio">{BRAND}</a>
    <nav class="nav" aria-label="{e(t['menu'])}">{nav}</nav>
    <div class="hdr-r">
      <nav class="langs" aria-label="Language">{langs}</nav>
      <a class="btn btn-gold" href="#kontakt">{e(t['nav_cta'])}</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="{e(t['menu'])}"><span></span></button>
    </div>
  </div>
  <div class="mnav" id="mnav"><ul>{mnav}</ul><div class="wrap" style="padding-bottom:1.25rem"><a class="btn btn-gold" href="#kontakt">{e(t['nav_cta'])}</a></div></div>
</header>

<main id="main">
<!-- ============ 1. HERO ============ -->
<section class="hero" aria-labelledby="h1">
  <div class="wrap hero-g">
    <div>
      <p class="eyebrow"><span class="p">B2B BUSINESS DEVELOPMENT</span><span class="sep" aria-hidden="true">|</span><span class="p">ZAGREB – EUROPE</span></p>
      <h1 id="h1">{e(t['h1'])}</h1>
      <p class="sub">{e(t['sub'])}</p>
      <p class="sub2">{e(t['sub2'])}</p>
      <div class="ctas">
        <a class="btn btn-gold" href="#kontakt">{e(t['cta1'])} {ic('arrow')}</a>
        <a class="btn btn-line" href="{WA}" target="_blank" rel="noopener">{ic('wa')} {e(t['wa'])}</a>
      </div>
    </div>
    <div class="map-box">
      {europe_svg(t)}
      <div class="dcard c1"><span>{e(t['card1'][0])}</span><b>{e(t['card1'][1])}</b></div>
      <div class="dcard c2"><span>{e(t['card2'][0])}</span><b>{e(t['card2'][1])}</b></div>
    </div>
  </div>
</section>

<!-- ============ 2. WHO WE HELP ============ -->
<section class="alt" id="za-koga" aria-labelledby="s2">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s2_kicker'])}</p><h2 id="s2">{e(t['s2_h'])}</h2></div>
    <div class="grid g2 g4">{groups}</div>
    <p class="after"><a class="tlink" href="#kontakt">{e(t['cta3'])} {ic('arrow')}</a></p>
  </div>
</section>

<!-- ============ 3. SERVICES ============ -->
<section id="usluge" aria-labelledby="s3">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s3_kicker'])}</p><h2 id="s3">{e(t['s3_h'])}</h2></div>
    <div class="grid g3">{svcs}</div>
  </div>
</section>

<!-- ============ 4. HOW WE WORK ============ -->
<section class="alt" id="kako-radimo" aria-labelledby="s4">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s4_kicker'])}</p><h2 id="s4">{e(t['s4_h'])}</h2></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<!-- ============ 5. PACKAGES ============ -->
<section id="paketi" aria-labelledby="s5">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s5_kicker'])}</p><h2 id="s5">{e(t['s5_h'])}</h2></div>
    <div class="grid g3 packs">{packs}</div>
    <div class="notes"><p>{e(t['vat'])}</p><p>{e(t['target_note'])}</p><p>{e(t['limits'])}</p></div>
  </div>
</section>

<!-- ============ 6. CASE FROM THE FIELD — placeholders: replace only with a real, client-approved case ============ -->
<section class="alt" aria-labelledby="s6">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s6_kicker'])}</p><h2 id="s6">{e(t['s6_h'])}</h2></div>
    <div class="case rv"><span class="tag">{e(t['case_note'])}</span><dl>{case}</dl></div>
  </div>
</section>

<!-- ============ 7. WHY ALKEMIJA ============ -->
<section class="why" aria-labelledby="s7">
  <div class="wrap">
    <div class="head"><p class="kicker">{e(t['s7_kicker'])}</p><h2 id="s7">{e(t['s7_h'])}</h2></div>
    <div class="grid g3">{why}</div>
  </div>
</section>

<!-- ============ 8. ADDITIONAL SUPPORT (secondary) ============ -->
<section class="support" aria-labelledby="s8">
  <div class="wrap"><div class="box"><h2 id="s8">{e(t['s8_h'])}</h2><p>{e(t['s8_p'])}</p></div></div>
</section>

<!-- ============ 9. FINAL CALL TO ACTION ============ -->
<section class="final" aria-labelledby="s9">
  <div class="wrap">
    <h2 id="s9">{e(t['s9_h'])}</h2>
    <p>{e(t['s9_p'])}</p>
    <div class="ctas">
      <a class="btn btn-gold" href="#kontakt">{e(t['s9_cta'])} {ic('arrow')}</a>
      <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ic('wa')} {e(t['wa'])}</a>
    </div>
  </div>
</section>

<!-- ============ 10. CONTACT ============ -->
<section id="kontakt" aria-labelledby="s10">
  <div class="wrap contact-g">
    <div class="cinfo">
      <p class="kicker">{e(t['s10_kicker'])}</p>
      <h2 id="s10">{e(t['s10_h'])}</h2>
      <address>
        <p class="org">ALKEMIJA BUSINESS STUDIO</p>
        <p>{e(t['city'])}</p>
        <ul>
          <li>{ic('mail')}<div><span>{e(t['l_email'])}</span><a href="mailto:info@alkemija.hr">info@alkemija.hr</a></div></li>
          <li>{ic('wa')}<div><span>{e(t['l_wa'])}</span><a href="{WA}" target="_blank" rel="noopener">+385 98 516 852</a></div></li>
          <li>{ic('web')}<div><span>{e(t['l_web'])}</span><a href="https://alkemija.hr">https://alkemija.hr</a></div></li>
        </ul>
      </address>
    </div>
    <!--
      CONTACT FORM — CONFIGURATION NEEDED BEFORE GOING LIVE
      A standalone HTML file has no server side. Put a real endpoint into data-endpoint, e.g. the
      Contact Form 7 REST route on alkemija.hr (CF7 5.9.2 is active on the site):
        https://www.alkemija.hr/wp-json/contact-form-7/v1/contact-forms/FORM_ID/feedback
      CF7 form fields: your-name, your-company, your-email, your-market, your-message, your-package.
      While data-endpoint is empty the form never pretends to send: it opens the visitor's
      email app with a pre-filled message to info@alkemija.hr and says so on screen.
    -->
    <form class="card" id="inquiry" novalidate data-endpoint="{ENDPOINT if mode == 'site' else ''}" data-cf7="{CF7_ID}" data-mailto="info@alkemija.hr"><input type="hidden" name="page-lang" value="{t['lang'].upper()}">
      <div class="fg">
        <div><label for="f-name">{e(f['name'])} {R}</label><input id="f-name" name="your-name" autocomplete="name" required></div>
        <div><label for="f-company">{e(f['company'])} {R}</label><input id="f-company" name="your-company" autocomplete="organization" required></div>
        <div><label for="f-email">{e(f['email'])} {R}</label><input id="f-email" name="your-email" type="email" autocomplete="email" inputmode="email" required></div>
        <div><label for="f-market">{e(f['market'])}</label><input id="f-market" name="your-market" placeholder="{e(f['market_ph'])}"></div>
        <div class="full"><label for="f-goal">{e(f['goal'])} {R}</label><textarea id="f-goal" name="your-message" required></textarea></div>
        <div class="full"><label for="f-pack">{e(f['pack'])}</label><select id="f-pack" name="your-package">{opts}</select></div>
        <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
        <div class="full consent"><input id="f-consent" name="consent" type="checkbox" value="1" required><label for="f-consent">{e(f['consent_pre'])}<a href="{PRIVACY}" target="_blank" rel="noopener">{e(f['consent_link'])}</a>{e(f['consent_post'])} {R}</label></div>
        <div class="full"><button class="btn btn-dark" type="submit">{e(f['send'])} {ic('arrow')}</button></div>
      </div>
      <div class="fstatus" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>
</main>

<!-- ============ FOOTER ============ -->
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div><a class="brand" href="#top" aria-label="Alkemija Business Studio">{BRAND}</a><p class="tag">{e(t['footer_tag'])}</p></div>
      <div>
        <h3>{e(t['s10_kicker'])}</h3>
        <ul>
          <li>{e(t['legal'])}</li>
          <li>3. Pile 10, HR-10000 Zagreb</li>
          <li>OIB 34772291906</li>
          <li>Tel/WhatsApp <a href="{WA}" target="_blank" rel="noopener">+385 98 516 852</a></li>
          <li><a href="mailto:info@alkemija.hr">info@alkemija.hr</a></li>
        </ul>
      </div>
      <div>
        <h3>Web</h3>
        <ul>
          <li><a href="https://alkemija.hr">alkemija.hr</a></li>
          <li><a href="https://alkemija.com">alkemija.com</a></li>
          <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn — {e(t['li_inv'])}</a></li>
          <li><a href="{PRIVACY}">{e(t['privacy'])}</a></li>
        </ul>
      </div>
    </div>
    <div class="fbot"><span>© 2026 Alkemija Business Studio · {e(t['rights'])}</span><nav class="langs" aria-label="Language">{langs}</nav></div>
  </div>
</footer>

<!-- Mobile CTA bar: appears after the hero, hides at the contact form -->
<div class="mbar">
  <a class="btn btn-gold" href="#kontakt">{e(t['cta1'])}</a>
  <a class="btn btn-line" href="{WA}" target="_blank" rel="noopener">{ic('wa')} WhatsApp</a>
</div>

<script>
{JS.replace('__MSG__', msg)}</script>
</body>
</html>
'''

if __name__ == '__main__':
    out = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else 'site'
    preview = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    for c in ['en', 'hr', 'it']:
        p = os.path.join(out, L[c]['path'], 'index.html') if mode == 'site' else os.path.join(out, f'alkemija-{c}.html')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(page(c, mode, preview))
        print(p, os.path.getsize(p))
