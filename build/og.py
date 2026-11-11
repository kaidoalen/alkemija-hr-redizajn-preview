import sys,os,asyncio
sys.path.insert(0,'build')
from build import europe_svg, BRAND, L
from playwright.async_api import async_playwright
css='''body{margin:0;width:1200px;height:630px;background:#0f2033;font-family:Inter,"Segoe UI",Roboto,Arial,sans-serif;color:#fff;display:flex;overflow:hidden}
.l{padding:70px 0 60px 80px;width:640px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:14px;color:#fff}.brand-logo{height:92px;width:auto}.brand-sub{font-size:13px;line-height:1.4;letter-spacing:.28em;color:#d9b264;border-left:1px solid rgba(255,255,255,.2);padding-left:14px;font-weight:600}.brand b{display:block;font-size:24px;letter-spacing:.2em}.brand small{display:block;font-size:13px;letter-spacing:.28em;color:#d9b264}
h1{font-size:64px;line-height:1.08;letter-spacing:-.03em;margin:44px 0 24px}
p{font-size:22px;color:#c4ccd8;margin:0;line-height:1.4}.e{margin-top:auto;font-size:15px;letter-spacing:.18em;color:#d9b264;font-weight:600}
.r{flex:1;display:flex;align-items:center;padding-right:40px}
.map{width:100%}.map .land{stroke:#2c4561;stroke-width:2.1;stroke-linecap:round;fill:none}.map .route{fill:none;stroke:#d9b264;stroke-width:1;stroke-dasharray:3 3}
.map .node{fill:#fff}.map .hub{fill:#d9b264;stroke:#0f2033;stroke-width:1.5}.map .pulse{display:none}.map text{font:500 7.2px Inter,Arial;fill:#8fa0b5}.map .sm{font-size:6.3px}.map .lead{fill:none;stroke:#4a6280;stroke-width:.4}.map .hub-l{fill:#fff;font-weight:700;font-size:8.4px}'''
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=await b.new_page(viewport={'width':1200,'height':630})
    for c,t in L.items():
      html=f'<html><head><meta charset=utf-8><style>{css}</style></head><body><div class=l><div class=brand>{BRAND}</div><h1>{t["h1"]}</h1><p>{t["sub2"]}</p><div class=e>B2B BUSINESS DEVELOPMENT | ZAGREB – EUROPE</div></div><div class=r>{europe_svg(t)}</div></body></html>'
      await pg.set_content(html); await pg.wait_for_timeout(200)
      await pg.screenshot(path=f'site/assets/og-{c}.png'); print(c)
    await b.close()
asyncio.run(main())
