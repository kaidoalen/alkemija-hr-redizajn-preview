# CURSOR-OBJAVA — nova naslovnica alkemija.hr (2026-11-11)

Alen je 11.11.2026. izričito odobrio objavu („Objavi. Preko github, cursor“). Ovaj repo je izvor istine za novu naslovnicu.

## Što je uživo
| URL | Sadržaj |
|---|---|
| https://www.alkemija.hr/ | EN naslovnica (`index.html`) |
| https://www.alkemija.hr/hr/ | HR verzija (`hr/index.html`) |
| https://www.alkemija.hr/it/ | IT verzija (`it/index.html`) |
| https://www.alkemija.hr/home-2/ | STARA Elementor naslovnica (stranica ID 1479, netaknuta), noindex |

## Kako radi
- WP plugin **Alkemija Naslovnica 2026** (`wp-plugin/alkemija-home-2026/`, uploadan kroz wp-admin) na `template_redirect` (prioritet 1) vraća samostalni HTML iz `pages/{en,hr,it}.html` za `/`, `/hr/`, `/it/`. Tema Mesmerize/Elementor se na tim URL-ovima ne učitava.
- Iz `wp_head`/`wp_footer` kopira samo GA4 (G-2Q2SCB4QRW) i Alkemija outbound/mail_id skripte.
- `/home-2/` → filter `request` renderira stranicu 1479 (stara naslovnica, isti CSS pluginova alkemija-sada/sirina), `redirect_canonical` isključen, `wp_robots` noindex,nofollow.
- Kopija stare naslovnice postoji i kao stranica 4467 (Duplicate Page), status draft, slug `home-2-kopija-4467`.
- Kontakt forma → Contact Form 7, forma ID **4469** „Alkemija naslovnica 2026 (EN/HR/IT)“, REST `/wp-json/contact-form-7/v1/contact-forms/4469/feedback`, prima info@alkemija.hr, Reply-To = email posjetitelja. Bez lažnog uspjeha.
- OG slike i logo u Media: `alkemija-home-2026-og2-{en,hr,it}.png`, `alkemija-home-2026-alkemija-logo-gold.png`. Logo je u HTML-u ugrađen (base64, 2x).

## Provjera 11.11.2026. ~01:50 (Europe/Zagreb)
- `/`, `/hr/`, `/it/` 200 (header `X-Alkemija-Home`), `/home-2/` 200 + noindex, visina identična staroj naslovnici; `/cjenik/`, `/pravila-privatnosti/`, `/anketa/` 200; `/start` i dalje 301 → alkemija.com/start/.
- Jedan testni upit s /hr/ → CF7 `mail_sent`, mail stigao na info@alkemija.hr 01:50.
- LiteSpeed cache plugin nije instaliran (nema server cachea za purge).
- Neiskorištene media datoteke prve OG verzije: ID 4470–4472 (mogu se obrisati).

## Izmjena sadržaja
1. Uredi `build/content.py` (tekstovi), `build/style.css`, `build/app.js`, `build/build.py` (karta: `NUDGE`, `LAB`, `COL`, `NAMES`).
2. `python3 build/build.py site site` → `site/index.html`, `site/hr/index.html`, `site/it/index.html`.
3. Kopiraj u `wp-plugin/alkemija-home-2026/pages/{en,hr,it}.html`, zipaj i uploadaj plugin (Plugins > Add New > Upload > Replace current).

## Rollback (odmah)
Plugins > **deaktiviraj „Alkemija Naslovnica 2026“** → `/` opet prikazuje staru Elementor naslovnicu 1479, `/hr/` i `/it/` 404, `/home-2/` prikazuje kopiju 4467.
Puni backup (Duplicator arhiva + baza, WXR, Elementor JSON) je na Grok boxu: `/workspace/alkemija-hr-redizajn-20261111/backup/`.

## Pravila
- Nikad ime „Alen Duka“ na stranici. Bez AI/automatizacije kao prednosti. Bez izmišljenih brojki/klijenata.
- Cjenik `/cjenik/` i ostale stranice nisu dirane.
- Lozinke nikad u repo.

## 1.0.4 (2026-11-11) — Book / Showcase / logotipi sa stare naslovnice
- Hero: tekstualni CTA „Book your appointment / Rezervirajte termin / Prenota un appuntamento” → #kontakt (obrazac se predpopuni zahtjevom za termin). Stara naslovnica NIJE imala booking gumb ni link — nije izmišljen vanjski URL.
- Sekcija 6 (primjer s terena): 2 gumba Showcase, originalni linkovi po jeziku: HR showcase-1-hr / showcase-2-hr, EN showcase-1-en / showcase-2-en, IT showcase-1 / showcase-2 (sve na alkemija.com).
- Nova tamna traka logotipa ispod sekcije 6: 7 logotipa, iste datoteke i redoslijed kao stara naslovnica (alk-logo-select, porta, media, kaido, prima, maslina, zoo), bez linkova.
- Rollback: wp-plugin/rollback-alkemija-home-2026-1.0.3.zip (lokalno na boxu) ili deaktivacija plugina.
