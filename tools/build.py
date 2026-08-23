# -*- coding: utf-8 -*-
"""
Static site generator for the Champion School / Училище Чемпиън website.
Produces plain HTML/CSS/JS into ../dev — no client-side framework, no
build-time dependency is shipped; this script only exists to keep the
repeated header/footer/schema markup consistent across ~14 pages.
Run: python3 tools/build.py
"""
import datetime
import json
import os
import re

from site_data import (
    DOMAIN, SITE, NAV_BG, NAV_EN, FOOTER_LEGAL_BG, FOOTER_LEGAL_EN,
    FAQ_BG, FAQ_EN,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dev")

YEAR = "2026"

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def t(bg, en, lang):
    return bg if lang == "bg" else en


def url_for(lang, path_bg, path_en):
    return path_bg if lang == "bg" else path_en


ICON_MENU = """<svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round"/></svg><svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke-linecap="round"/></svg>"""


def render_header(lang, active_key, bg_url, en_url):
    nav = NAV_BG if lang == "bg" else NAV_EN
    home_url = "/" if lang == "bg" else "/en/"
    brand_name = t(SITE["name_bg"], SITE["name_en"], lang)
    brand_tag = t("Английски за ученици", "English for students", lang)
    logo_alt = t("Лого на училище Чемпиън", "Champion school logo", lang)
    nav_label = t("Основна навигация", "Main navigation", lang)
    lang_label = t("Смяна на езика", "Language switcher", lang)
    menu_label = t("Отвори менюто", "Open menu", lang)

    links = "\n".join(
        '<a href="{url}"{cur}{cta}>{label}</a>'.format(
            url=url,
            cur=' aria-current="page"' if key == active_key else "",
            cta=' class="is-cta"' if key == "enrollment" else "",
            label=label,
        )
        for key, label, url in nav
    )

    header = f"""<a class="skip-link" href="#main">{t("Към съдържанието", "Skip to content", lang)}</a>
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="{home_url}" aria-label="{brand_name} — {t("начало", "home", lang)}">
        <span class="brand-mark"><picture><source type="image/webp" srcset="/img/champion-logo.webp"><img src="/img/champion-logo.png" width="640" height="350" alt="{logo_alt}" decoding="async"></picture></span>
        <span class="brand-text"><span class="name">{brand_name}</span><span class="tag">{brand_tag}</span></span>
      </a>
      <nav class="nav-links" aria-label="{nav_label}">
        {links}
      </nav>
      <div class="nav-right">
        <div class="lang-switch" aria-label="{lang_label}">
          <a href="{bg_url}" aria-current="{'true' if lang == 'bg' else 'false'}" hreflang="bg" lang="bg">BG</a>
          <a href="{en_url}" aria-current="{'true' if lang == 'en' else 'false'}" hreflang="en" lang="en">EN</a>
        </div>
        <button type="button" class="menu-toggle" aria-expanded="false" aria-controls="mobileNav" aria-label="{menu_label}">
          {ICON_MENU}
        </button>
      </div>
    </div>
  </header>
  <div class="mobile-nav" id="mobileNav">
    <div class="container">
      {links}
    </div>
  </div>"""
    return header


def render_footer(lang, bg_url, en_url):
    nav = NAV_BG if lang == "bg" else NAV_EN
    legal = FOOTER_LEGAL_BG if lang == "bg" else FOOTER_LEGAL_EN
    brand_name = t(SITE["name_bg"], SITE["name_en"], lang)
    desc = t(
        "Училище Чемпиън обучава по английски език ученици от 2. до 12. клас в Пловдив — с ясни нива, малки групи и фокус върху реалната комуникация.",
        "Champion School teaches English in Plovdiv to students in grades 2 to 12 — with clear levels, small groups and a focus on real communication.",
        lang,
    )
    nav_heading = t("Навигация", "Navigation", lang)
    contact_heading = t("Контакти", "Contact", lang)
    legal_heading = t("Правна информация", "Legal", lang)

    nav_links = "\n".join(f'<li><a href="{url}">{label}</a></li>' for _, label, url in nav)
    legal_links = "\n".join(f'<li><a href="{url}">{label}</a></li>' for label, url in legal)

    rights = t(f"© {YEAR} Училище Чемпиън. Всички права запазени.", f"© {YEAR} Champion School. All rights reserved.", lang)
    legal_note = t(
        f"Училището се управлява от {SITE['legal_name']}, ЕИК {SITE['legal_eik']}, със седалище и адрес на управление: {SITE['legal_address_bg']}.",
        f"Champion School is operated by {SITE['legal_name']}, UIC (ЕИК) {SITE['legal_eik']}, registered office: {SITE['legal_address_en']}.",
        lang,
    )

    return f"""<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">
            <span class="brand-mark"><picture><source type="image/webp" srcset="/img/champion-logo.webp"><img src="/img/champion-logo.png" width="640" height="350" alt="" loading="lazy" decoding="async"></picture></span>
            <span class="name">{brand_name}</span>
          </div>
          <p>{desc}</p>
        </div>
        <div class="footer-col">
          <h3>{nav_heading}</h3>
          <ul>{nav_links}</ul>
        </div>
        <div class="footer-col">
          <h3>{contact_heading}</h3>
          <ul>
            <li><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></li>
            <li>{t(SITE['address_bg'], SITE['address_en'], lang)}</li>
            <li><a href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3>{legal_heading}</h3>
          <ul>{legal_links}</ul>
          <div class="footer-lang">
            <a href="{bg_url}" aria-current="{'true' if lang == 'bg' else 'false'}">BG</a>
            <a href="{en_url}" aria-current="{'true' if lang == 'en' else 'false'}">EN</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <span>{rights}</span>
      </div>
      <p class="footer-note">{legal_note}</p>
    </div>
  </footer>"""


# ---------------------------------------------------------------------------
# Schema.org node builders
# ---------------------------------------------------------------------------

def org_node(lang):
    return {
        "@type": ["EducationalOrganization", "LocalBusiness"],
        "@id": DOMAIN + "/#organization",
        "name": t(SITE["full_name_bg"], SITE["full_name_en"], lang),
        "alternateName": t(SITE["name_bg"], SITE["name_en"], lang),
        "url": DOMAIN + ("/" if lang == "bg" else "/en/"),
        "logo": DOMAIN + "/img/champion-logo.png",
        "image": DOMAIN + "/img/champion-logo.png",
        "telephone": "+359885712048",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": t(SITE["address_street_bg"], SITE["address_street_en"], lang),
            "addressLocality": t(SITE["locality_bg"], SITE["locality_en"], lang),
            "addressCountry": "BG",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": SITE["latitude"],
            "longitude": SITE["longitude"],
        },
        "areaServed": {"@type": "City", "name": t("Пловдив", "Plovdiv", lang)},
        "priceRange": "329 EUR",
        "email": SITE["email"],
        "sameAs": [SITE["instagram_url"], SITE["facebook_url"]],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": "+359885712048",
                "email": SITE["email"],
                "contactType": "customer service",
                "areaServed": "BG",
                "availableLanguage": ["Bulgarian", "English"],
            }
        ],
    }


def website_node(lang):
    return {
        "@type": "WebSite",
        "@id": DOMAIN + "/#website",
        "url": DOMAIN + ("/" if lang == "bg" else "/en/"),
        "name": t(SITE["name_bg"], SITE["name_en"], lang),
        "inLanguage": t("bg-BG", "en", lang),
        "publisher": {"@id": DOMAIN + "/#organization"},
    }


def webpage_node(lang, path, name, description, has_breadcrumb=False):
    node = {
        "@type": "WebPage",
        "@id": DOMAIN + path + "#webpage",
        "url": DOMAIN + path,
        "name": name,
        "description": description,
        "inLanguage": t("bg-BG", "en", lang),
        "isPartOf": {"@id": DOMAIN + "/#website"},
        "about": {"@id": DOMAIN + "/#organization"},
    }
    if has_breadcrumb:
        node["breadcrumb"] = {"@id": DOMAIN + path + "#breadcrumb"}
    return node


def breadcrumb_node(path, items):
    elements = [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": DOMAIN + url}
        for i, (name, url) in enumerate(items)
    ]
    return {"@type": "BreadcrumbList", "@id": DOMAIN + path + "#breadcrumb", "itemListElement": elements}


def faq_node(path, faq_list):
    return {
        "@type": "FAQPage",
        "@id": DOMAIN + path + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_list
        ],
    }


# ---------------------------------------------------------------------------
# Root-relative -> relative path rewriting
#
# Body content is written with root-relative paths ("/assets/...", "/test/")
# because that's simplest to author. Canonical/hreflang/OG tags must stay
# absolute production URLs regardless (they already use DOMAIN + path, so
# they're untouched here). But real navigable href/src/srcset values need to
# become relative, otherwise the site only works once served from the actual
# domain root -- opening dev/ directly (or previewing it under a subpath)
# breaks every link and asset. Fix: rewrite them relative to each page's own
# folder depth, right before writing the file.
# ---------------------------------------------------------------------------

def relative_prefix(path):
    depth = len([s for s in path.split("/") if s])
    return "../" * depth


def to_relative(url, prefix):
    if not url.startswith("/") or url.startswith("//"):
        return url
    rel = prefix + url[1:]
    return rel or "./"


def relativize(html, path):
    prefix = relative_prefix(path)

    def fix_single(m):
        return f'{m.group(1)}="{to_relative(m.group(2), prefix)}"'

    html = re.sub(r'\b(href|src)="(/[^"]*)"', fix_single, html)

    def fix_srcset(m):
        entries = []
        for chunk in m.group(2).split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            url, _, descriptor = chunk.partition(" ")
            entries.append((to_relative(url, prefix) + " " + descriptor).strip())
        return f'{m.group(1)}="{", ".join(entries)}"'

    html = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"', fix_srcset, html)
    return html


# ---------------------------------------------------------------------------
# Page wrapper
# ---------------------------------------------------------------------------

def wrap_page(lang, active_key, path, alt_path, title, description, main_html,
              graph_nodes, breadcrumb_items=None, extra_js=None, body_class=""):
    bg_url = path if lang == "bg" else alt_path
    en_url = alt_path if lang == "bg" else path

    nodes = [org_node(lang), website_node(lang)]
    has_bc = breadcrumb_items is not None
    nodes.append(webpage_node(lang, path, title, description, has_breadcrumb=has_bc))
    if has_bc:
        nodes.append(breadcrumb_node(path, breadcrumb_items))
    nodes.extend(graph_nodes)
    graph = {"@context": "https://schema.org", "@graph": nodes}

    og_image = t("/img/og-image-bg.jpg", "/img/og-image-en.jpg", lang)
    og_locale = t("bg_BG", "en_US", lang)
    og_locale_alt = t("en_US", "bg_BG", lang)

    breadcrumb_html = ""
    if breadcrumb_items:
        items_html = []
        for i, (name, url) in enumerate(breadcrumb_items):
            if i == len(breadcrumb_items) - 1:
                items_html.append(f'<li aria-current="page">{name}</li>')
            else:
                items_html.append(f'<li><a href="{url}">{name}</a></li>')
        breadcrumb_html = f"""<nav class="breadcrumb container" aria-label="{t('Трохи', 'Breadcrumb', lang)}">
      <ol>{''.join(items_html)}</ol>
    </nav>"""

    scripts = ['<script src="/assets/js/main.js" defer></script>']
    if extra_js:
        scripts.append(extra_js)

    html = f"""<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<script>document.documentElement.classList.remove('no-js');</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{DOMAIN}{path}">
<link rel="alternate" hreflang="bg-BG" href="{DOMAIN}{bg_url}">
<link rel="alternate" hreflang="en" href="{DOMAIN}{en_url}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{bg_url}">
<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/img/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="theme-color" content="#0b2c52">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Champion School / Училище Чемпиън">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:image" content="{DOMAIN}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_locale_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{DOMAIN}{og_image}">
<link rel="preload" as="image" href="/img/students-hero.webp" imagesrcset="/img/students-hero-800.webp 800w, /img/students-hero.webp 1400w">
<link rel="stylesheet" href="/assets/css/styles.css">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>
<body class="{body_class}">
  {render_header(lang, active_key, bg_url, en_url)}
  {breadcrumb_html}
  <main id="main">
    {main_html}
  </main>
  {render_footer(lang, bg_url, en_url)}
  {''.join(scripts)}
</body>
</html>
"""
    return relativize(html, path)


def write_file(rel_path, content):
    full = os.path.join(OUT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel_path)


# ---------------------------------------------------------------------------
# CSS / JS minification
#
# No bundler is available in this environment (no node/npm, no pip access),
# so these are small hand-rolled minifiers rather than a real parser. They
# are deliberately conservative and were checked against the specific files
# in tools/assets/ (no url(), no // comments, no regex literals containing
# "//", calc()'s +/- operators never touched) -- if that source ever grows
# more complex, re-verify these assumptions before trusting the output.
# ---------------------------------------------------------------------------

def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def minify_js(js):
    """Strip /* */ comments, indentation and blank lines. Keeps one
    statement per line (no token-level squeeze) to stay ASI-safe without
    a real tokenizer."""
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    lines = [line.strip() for line in js.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def build_assets():
    src = os.path.join(ROOT, "tools", "assets")

    css = open(os.path.join(src, "styles.css"), encoding="utf-8").read()
    write_file("/assets/css/styles.css", minify_css(css))

    for name in ("main.js",):
        js = open(os.path.join(src, name), encoding="utf-8").read()
        write_file(f"/assets/js/{name}", minify_js(js))


def faq_html(faq_list):
    return "\n".join(
        f'''<details class="faq-item">
          <summary>{q}</summary>
          <div class="faq-answer"><p>{a}</p></div>
        </details>'''
        for q, a in faq_list
    )


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

def home_main(lang):
    test_url = url_for(lang, "/test/", "/en/test/")
    schedule_url = url_for(lang, "/schedule-prices/", "/en/schedule-prices/")
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    contacts_url = url_for(lang, "/contacts/", "/en/contacts/")
    faq = FAQ_BG if lang == "bg" else FAQ_EN

    hero_eyebrow = t("Английски за ученици в Пловдив", "English for students in Plovdiv", lang)
    hero_h1 = t("Английският отваря врати.", "English opens doors.", lang)
    hero_lead = t(
        "Училище Чемпиън обучава по английски език ученици от 2. до 12. клас в Пловдив. Учим децата и учениците да говорят уверено, да разбират бързо и да използват английския извън класната стая.",
        "Champion School teaches English to students in grades 2 to 12 in Plovdiv. We help children and teenagers speak with confidence, understand quickly, and use English beyond the classroom.",
        lang,
    )
    cta_test = t("Тест за ниво", "Level test", lang)
    cta_enroll = t("Запиши се", "Enroll now", lang)

    hero = f"""<section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">{hero_eyebrow}</p>
          <h1>{hero_h1}</h1>
          <p class="hero-lead">{hero_lead}</p>
          <div class="actions">
            <a class="btn btn-primary btn-lg" href="{test_url}">{cta_test}</a>
            <a class="btn btn-secondary btn-lg" href="{enroll_url}">{cta_enroll}</a>
          </div>
          <div class="hero-meta">
            <span class="hero-meta-item"><span class="dot" aria-hidden="true"></span>{t("2.–12. клас", "Grades 2-12", lang)}</span>
            <span class="hero-meta-item"><span class="dot" aria-hidden="true"></span>{t(SITE['address_bg'], SITE['address_en'], lang)}</span>
            <span class="hero-meta-item"><span class="dot" aria-hidden="true"></span><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></span>
          </div>
        </div>
        <div class="hero-media">
          <div class="photo-frame">
            <div class="img-box">
              <picture>
                <source type="image/webp" srcset="/img/students-hero-800.webp 800w, /img/students-hero.webp 1400w" sizes="(min-width: 900px) 480px, 92vw">
                <img src="/img/students-hero.jpg" srcset="/img/students-hero-800.jpg 800w, /img/students-hero.jpg 1400w" sizes="(min-width: 900px) 480px, 92vw" width="1400" height="933" alt="{t('Ученици, обучаващи се по английски език', 'Students learning English', lang)}" loading="eager" fetchpriority="high">
              </picture>
            </div>
          </div>
          <div class="hero-badge">
            <strong>{t("2.–12. клас", "Grades 2-12", lang)}</strong>
            <span>{t("Групи по клас и ниво в Пловдив", "Groups by grade and level in Plovdiv", lang)}</span>
          </div>
        </div>
      </div>
    </section>"""

    about = f"""<section class="section" id="about">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("За Училище Чемпиън", "About Champion School", lang)}</p>
          <h2 class="section-title">{t("Училище по английски за ученици от 2. до 12. клас", "An English school for students in grades 2 to 12", lang)}</h2>
        </div>
        <div class="grid grid-2">
          <p class="section-lead">{t(
            "Училище Чемпиън предлага специализирано обучение по английски език в Пловдив за ученици от начален, прогимназиален и гимназиален етап — от 2. до 12. клас. Работим в групи, ясно определени по клас и ниво, за да може всеки ученик да напредва с подходящото за него темпо.",
            "Champion School provides specialized English language education in Plovdiv for students at primary, lower-secondary and upper-secondary level — from grade 2 through grade 12. We work in groups clearly organized by grade and level, so every student can progress at the right pace.",
            lang)}</p>
          <p class="section-lead">{t(
            "Целта ни е проста: учениците да излизат от часовете с реална увереност да говорят, пишат и разбират английски — не просто да наизустяват граматика за оценка.",
            "Our goal is simple: students should leave lessons with real confidence to speak, write and understand English — not just memorize grammar for a grade.",
            lang)}</p>
        </div>
      </div>
    </section>"""

    why_cards = [
        ("🎯", t("Групи по клас и точно ниво", "Grouped by grade and precise level", lang),
         t("За всеки ученик правим тест за ниво и го включваме в група по клас и ниво на владеене на езика — за връстници на сходен етап и подходящо за него темпо.",
           "We test every student's level and place them in a group matched by grade and English level, alongside peers at a similar stage and pace.", lang)),
        ("💬", t("Фокус върху говоримия език", "A focus on spoken English", lang),
         t("Часовете съчетават граматика и лексика с практика в говоренето, за да могат учениците да прилагат английския извън класната стая.",
           "Lessons combine grammar and vocabulary with speaking practice, so students can use English beyond the classroom.", lang)),
        ("📍", t("Удобна локация", "Convenient location", lang),
         t("Срещу Дондуковата градина, до площад „Съединение“.",
           "Across from Dondukova Garden, near Saedinenie Square, in central Plovdiv.", lang)),
    ]
    why = f"""<section class="section section-alt">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("Защо Училище Чемпиън", "Why Champion School", lang)}</p>
          <h2 class="section-title">{t("Защо да изберете Училище Чемпиън", "Why families choose Champion School", lang)}</h2>
        </div>
        <div class="grid grid-3">
          {"".join(f'<div class="card"><div class="feature-icon" aria-hidden="true">{icon}</div><h3>{h}</h3><p>{p}</p></div>' for icon, h, p in why_cards)}
        </div>
      </div>
    </section>"""

    grades = [
        (t("2.–4. клас", "Grades 2-4", lang), t(
            "Начален етап — първи стъпки в английския чрез игра, песни и лесни разговорни ситуации, изграждащи основа и увереност.",
            "Primary stage — first steps in English through play, songs and simple conversation, building a foundation and confidence.", lang)),
        (t("5.–7. клас", "Grades 5-7", lang), t(
            "Прогимназиален етап — разширяване на речниковия запас и граматиката, с наблягане на четене, писане и говорене.",
            "Lower-secondary stage — expanding vocabulary and grammar, with emphasis on reading, writing and speaking.", lang)),
        (t("8.–12. клас", "Grades 8-12", lang), t(
            "Гимназиален етап — задълбочена граматика, академична лексика и увереност пред писмени и устни изпитвания, матура и бъдещо обучение или работа, изискващи английски.",
            "Upper-secondary stage — deeper grammar, academic vocabulary, and confidence for school assessments, school-leaving exams, and future study or work that requires English.", lang)),
    ]
    grades_section = f"""<section class="section" id="grades">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("По класове", "By grade", lang)}</p>
          <h2 class="section-title">{t("Обучение от 2. до 12. клас", "Courses from grade 2 to grade 12", lang)}</h2>
          <p class="section-lead">{t("Групираме учениците в три основни степени, съобразени с училищната програма в България.", "We group students into three core stages, aligned with the Bulgarian school curriculum.", lang)}</p>
        </div>
        <div class="grid grid-3">
          {"".join(f'<div class="grade-card"><div class="range">{r}</div><p>{p}</p></div>' for r, p in grades)}
        </div>
      </div>
    </section>"""

    approach_items = [
        (t("Тест за ниво преди старт", "A level test before you start", lang), t(
            "Всеки нов ученик преминава тест за ниво, за да попадне в подходяща по знания група.",
            "Every new student takes a level test to join a group that matches their knowledge.", lang)),
        (t("Малки групи", "Small groups", lang), t(
            "Работим с ограничен брой ученици в група, за да имат всички възможност да говорят и да получават обратна връзка.",
            "We keep groups small so every student gets the chance to speak and receive feedback.", lang)),
        (t("Баланс между граматика и говорене", "A balance of grammar and speaking", lang), t(
            "Съчетаваме структурирано изучаване на граматика и лексика с практика в реални разговорни ситуации.",
            "We combine structured grammar and vocabulary work with practice in real conversational situations.", lang)),
        (t("Проследяване на напредъка", "Tracking progress", lang), t(
            "Учениците и родителите получават редовна обратна връзка за развитието на езиковите умения.",
            "Students and parents receive regular feedback on how language skills are developing.", lang)),
    ]
    approach = f"""<section class="section section-alt" id="approach">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("Методика", "Method", lang)}</p>
          <h2 class="section-title">{t("Как учим английски в Училище Чемпиън", "How we teach English at Champion School", lang)}</h2>
        </div>
        <div class="approach-list">
          {"".join(f'<div class="approach-item"><span class="num">{i+1}</span><div><h3>{h}</h3><p>{p}</p></div></div>' for i, (h, p) in enumerate(approach_items))}
        </div>
      </div>
    </section>"""

    assess = f"""<section class="section" id="level-test">
      <div class="container panel-split">
        <div class="panel panel-navy">
          <h2>{t("Не сте сигурни кое ниво е подходящо?", "Not sure which level fits?", lang)}</h2>
          <p>{t("Тестът за ниво се провежда присъствено в училището, с участието на ученика — за да установим точното му ниво на владеене на английски и да препоръчаме подходяща група преди записване.",
                "The level test takes place in person at the school, with the student attending — so we can assess their English level and recommend a suitable group before enrollment.", lang)}</p>
          <div class="actions"><a class="btn btn-primary" href="{test_url}">{cta_test}</a></div>
        </div>
        <div class="panel panel-gold">
          <h3>{t("Предстоящи дати за тест", "Upcoming test dates", lang)}</h3>
          <div class="stack">
            <div><strong>{t("24 и 25 септември, 1 и 2 октомври", "24-25 September, 1-2 October", lang)}</strong><br><span style="font-size:13.5px">{t("от 17:00ч и от 18:30ч", "from 5:00pm and from 6:30pm", lang)}</span></div>
            <div><strong>{t("Времетраене", "Duration", lang)}</strong><br><span style="font-size:13.5px">{t("около 30 мин.", "about 30 min.", lang)}</span></div>
          </div>
        </div>
      </div>
    </section>"""

    schedule_teaser = f"""<section class="section section-alt" id="schedule">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("График и цени", "Schedule & Prices", lang)}</p>
          <h2 class="section-title">{t("Групи по клас, ниво и удобно за вас време", "Groups by grade, level and a convenient time", lang)}</h2>
          <p class="section-lead">{t(
            "Пълният график по дни и часове за всяко ниво ще намерите на страница „График и цени“, заедно с продължителността и цената на курса.",
            "The full day-by-day schedule for each level is available on the “Schedule & Prices” page, along with the course duration and price.", lang)}</p>
        </div>
        <div class="grid grid-3">
          {"".join(f'<div class="grade-card"><div class="range">{g}</div><p>{t("Виж дните и часовете за нивата", "See the days and times for each level", lang)}</p><span class="badge badge-gold"><s style="opacity:.65;font-weight:600">{t("399 €", "€399", lang)}</s> {t("329 € / срок", "€329 / term", lang)}</span></div>' for g in [t("2.–4. клас","Grades 2-4",lang), t("5.–7. клас","Grades 5-7",lang), t("8.–12. клас","Grades 8-12",lang)])}
        </div>
        <div class="actions" style="margin-top:28px">
          <a class="btn btn-navy" href="{schedule_url}">{t("Виж графика и цените", "View schedule & prices", lang)}</a>
        </div>
      </div>
    </section>"""

    enroll_cta = f"""<section class="section">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>{t("Готови сте да запишете детето си?", "Ready to enroll your child?", lang)}</h2>
            <p>{t("Обадете се или ни пишете в Instagram — ще потвърдим подходяща група заедно.", "Call us or message us on Instagram — we will confirm a suitable group together.", lang)}</p>
          </div>
          <div class="actions">
            <a class="btn btn-primary btn-lg" href="{enroll_url}">{cta_enroll}</a>
            <a class="btn btn-secondary btn-lg" href="{test_url}" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4)">{cta_test}</a>
          </div>
        </div>
      </div>
    </section>"""

    location = f"""<section class="section section-alt" id="location">
      <div class="container grid grid-2">
        <div>
          <p class="eyebrow">{t("Локация", "Location", lang)}</p>
          <h2 class="section-title">{t("Намираме се в Пловдив", "We are based in Plovdiv", lang)}</h2>
          <div class="contact-list" style="margin-top:22px">
            <div class="contact-row"><span class="ic" aria-hidden="true">📍</span><div><div class="lbl">{t("Адрес","Address",lang)}</div><span class="val">{t(SITE['address_bg'], SITE['address_en'], lang)}</span></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">📞</span><div><div class="lbl">{t("Телефон","Phone",lang)}</div><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></div></div>
          </div>
          <div class="actions" style="margin-top:22px"><a class="btn btn-navy" href="{contacts_url}">{t("Виж контакти", "View contact details", lang)}</a></div>
        </div>
        <div>
          <div class="map-frame">
            <iframe src="{SITE['maps_embed_src']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{t('Карта с местоположението на Училище Чемпиън', 'Map showing the Champion School location', lang)}"></iframe>
          </div>
          <p style="margin-top:10px"><a class="btn-ghost" href="{SITE['maps_link']}" rel="noopener" target="_blank">{t("Отвори в Google Maps ↗", "Open in Google Maps ↗", lang)}</a></p>
        </div>
      </div>
    </section>"""

    instagram = f"""<section class="section">
      <div class="container">
        <div class="social-panel">
          <div>
            <h2>{t("Последвайте ни в Instagram", "Follow us on Instagram", lang)}</h2>
            <p>{t("Новини, снимки от занятия и полезни материали за учениците на Училище Чемпиън.", "News, glimpses from classes and useful materials for Champion School students.", lang)}</p>
          </div>
          <a class="social-handle" href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a>
        </div>
      </div>
    </section>"""

    faq_section = f"""<section class="section section-alt" id="faq">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">FAQ</p>
          <h2 class="section-title">{t("Често задавани въпроси", "Frequently asked questions", lang)}</h2>
        </div>
        <div class="faq-list">
          {faq_html(faq)}
        </div>
      </div>
    </section>"""

    final_cta = f"""<section class="section">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>{t("Направете следващата стъпка", "Take the next step", lang)}</h2>
            <p>{t("Тест за ниво, записване или директен разговор с нас — изберете това, което е удобно за вас.", "A level test, enrollment, or a direct conversation with us — choose whichever suits you.", lang)}</p>
          </div>
          <div class="actions">
            <a class="btn btn-primary btn-lg" href="{test_url}">{cta_test}</a>
            <a class="btn btn-secondary btn-lg" href="{enroll_url}" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4)">{cta_enroll}</a>
            <a class="btn btn-secondary btn-lg" href="{contacts_url}" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4)">{t("Свържи се с нас", "Contact us", lang)}</a>
          </div>
        </div>
      </div>
    </section>"""

    return hero + about + why + grades_section + approach + assess + schedule_teaser + enroll_cta + location + instagram + faq_section + final_cta


def test_main(lang):
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    contacts_url = url_for(lang, "/contacts/", "/en/contacts/")

    intro = f"""<section class="section-tight">
      <div class="container-narrow">
        <p class="eyebrow">{t("Първа стъпка", "First step", lang)}</p>
        <h1 class="section-title">{t("Тест за ниво по английски език", "English Level Test", lang)}</h1>
        <p class="section-lead">{t(
          "Тестът за ниво се провежда присъствено в Училище Чемпиън. Каним родителите да дойдат заедно с децата си, за да установим точното ниво на владеене на английски език и да препоръчаме подходяща по клас и ниво група преди записване.",
          "The level test takes place in person at Champion School. We invite parents to come together with their children so we can assess the student's English level and recommend a suitable grade-and-level group before enrollment.",
          lang)}</p>
      </div>
    </section>"""

    why = f"""<section class="section-tight section-alt">
      <div class="container-narrow">
        <h2>{t("Защо е важен тестът за ниво?", "Why does the level test matter?", lang)}</h2>
        <p class="section-lead">{t(
          "За да напредва с подходящото за него темпо, всеки нов ученик трябва да бъде разпределен в група, съобразена с реалните му знания. Кратката присъствена среща ни позволява да преценим нивото на владеене на английски и да препоръчаме групата, в която ученикът ще се чувства уверен.",
          "To progress at the right pace, every new student needs to join a group that matches their actual knowledge. The short in-person meeting lets us assess the student's English level and recommend the group where they will feel confident.",
          lang)}</p>
      </div>
    </section>"""

    schedule_card = f"""<div class="card" style="padding:26px 28px">
      <h3 style="margin-top:0">{t("Дати и часове за тестване", "Testing dates and times", lang)}</h3>
      <div class="contact-list">
        <div class="contact-row"><span class="ic" aria-hidden="true">🗓</span><div><div class="lbl">{t("Дати", "Dates", lang)}</div><span class="val">{t("24 и 25 септември, 1 и 2 октомври", "24-25 September, 1-2 October", lang)}</span></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">⏱</span><div><div class="lbl">{t("Часове", "Times", lang)}</div><span class="val">{t("от 17:00ч и от 18:30ч", "from 5:00pm and from 6:30pm", lang)}</span></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">⏳</span><div><div class="lbl">{t("Времетраене", "Duration", lang)}</div><span class="val">{t("около 30 мин.", "about 30 min.", lang)}</span></div></div>
      </div>
    </div>"""

    booking_card = f"""<div class="card" style="padding:26px 28px">
      <h3 style="margin-top:0">{t("Запазете час за тест", "Book a test time", lang)}</h3>
      <p>{t("За да запазите час, свържете се с нас предварително по телефон, Viber или Instagram.", "To book a time, please contact us in advance by phone, Viber or Instagram.", lang)}</p>
      <div class="contact-list">
        <div class="contact-row"><span class="ic" aria-hidden="true">📞</span><div><div class="lbl">{t("Тел. и Viber", "Phone & Viber", lang)}</div><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">📷</span><div><div class="lbl">Instagram</div><a href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a></div></div>
      </div>
      <div class="actions" style="margin-top:18px">
        <a class="btn btn-primary" href="{SITE['phone_href']}">{t("Обадете се", "Call us", lang)}</a>
        <a class="btn btn-secondary" href="{contacts_url}">{t("Свържи се с нас", "Contact us", lang)}</a>
      </div>
    </div>"""

    info_section = f"""<section class="section-tight">
      <div class="container">
        <div class="grid grid-2">
          {schedule_card}
          {booking_card}
        </div>
      </div>
    </section>"""

    final_cta = f"""<section class="section">
      <div class="container">
        <div class="cta-band">
          <div>
            <h2>{t("Готови сте да установим нивото?", "Ready to assess the level?", lang)}</h2>
            <p>{t("Свържете се с нас, за да запазим час, или преминете направо към записване.", "Contact us to book a time, or go straight to enrollment.", lang)}</p>
          </div>
          <div class="actions">
            <a class="btn btn-primary btn-lg" href="{SITE['phone_href']}">{t("Обадете се", "Call us", lang)}</a>
            <a class="btn btn-secondary btn-lg" href="{enroll_url}" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.4)">{t("Запиши се", "Enroll now", lang)}</a>
          </div>
        </div>
      </div>
    </section>"""

    return intro + why + info_section + final_cta


def build_test():
    for lang, path, alt in [("bg", "/test/", "/en/test/"), ("en", "/en/test/", "/test/")]:
        title = t(
            "Тест за ниво по английски език | Училище Чемпиън Пловдив",
            "English Level Test | Champion School Plovdiv",
            lang,
        )
        desc = t(
            "Присъствен тест за ниво по английски в Училище Чемпиън, Пловдив — дати, часове и контакти за записан час, преди записване в подходяща група.",
            "In-person English level test at Champion School, Plovdiv — dates, times and contact details to book a slot, before enrolling in the right group.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("Тест за ниво", "Level Test", lang), path),
        ]
        html = wrap_page(
            lang, "test", path, alt, title, desc, test_main(lang), [],
            breadcrumb_items=breadcrumb,
        )
        write_file(path + "index.html", html)


# Single source of truth for the class schedule -- language-neutral so both
# the HTML table and the Course/CourseInstance JSON-LD are derived from the
# same facts. day_code=None marks a level with no confirmed day/time yet.
SCHEDULE_DEFINITION = [
    ("2.–4. клас", "Grades 2-4", [
        ("Ниво 1", "Level 1", "tue_thu", "18:00", "19:30"),
        ("Ниво 2", "Level 2", "wed_fri", "18:00", "19:30"),
        ("Ниво 3", "Level 3", "wed_fri", "15:30", "17:00"),
    ]),
    ("5.–7. клас", "Grades 5-7", [
        ("Ниво 1 (A1)", "Level 1 (A1)", "tue_thu", "14:00", "15:30"),
        ("Ниво 1 (A1)", "Level 1 (A1)", "sat", "9:00", "12:00"),
        ("Ниво 2 (A1+)", "Level 2 (A1+)", "wed_fri", "14:00", "15:30"),
        ("Ниво 2 (A1+)", "Level 2 (A1+)", "sat", "12:30", "15:30"),
    ]),
    ("8.–12. клас", "Grades 8-12", [
        ("Ниво 1 (Б1)", "Level 1 (B1)", "tue_thu", "14:00", "15:30"),
        ("Ниво 2 (Б1+)", "Level 2 (B1+)", "wed_fri", "14:00", "15:30"),
        ("Ниво 2 (Б1+)", "Level 2 (B1+)", "sat", "9:00", "12:00"),
        ("Ниво 3 (Б2)", "Level 3 (B2)", None, None, None),
    ]),
]

DAY_LABELS_BG = {"tue_thu": "вторник и четвъртък", "wed_fri": "сряда и петък", "sat": "събота"}
DAY_LABELS_EN = {"tue_thu": "Tuesday & Thursday", "wed_fri": "Wednesday & Friday", "sat": "Saturday"}
DAY_SCHEMA = {
    "tue_thu": ["https://schema.org/Tuesday", "https://schema.org/Thursday"],
    "wed_fri": ["https://schema.org/Wednesday", "https://schema.org/Friday"],
    "sat": ["https://schema.org/Saturday"],
}


def _iso_time(hhmm):
    h, m = hhmm.split(":")
    return f"{int(h):02d}:{m}:00"


def schedule_course_node(lang, path):
    """Course + CourseInstance/Offer schema for the Schedule & Prices page,
    built from the same SCHEDULE_DEFINITION as the HTML table. Levels with
    no confirmed day/time (day_code=None) are omitted rather than guessed."""
    place = {
        "@type": "Place",
        "name": t(SITE["name_bg"], SITE["name_en"], lang),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": t(SITE["address_street_bg"], SITE["address_street_en"], lang),
            "addressLocality": t(SITE["locality_bg"], SITE["locality_en"], lang),
            "addressCountry": "BG",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": SITE["latitude"],
            "longitude": SITE["longitude"],
        },
    }
    instances = []
    for grade_bg, grade_en, rows in SCHEDULE_DEFINITION:
        grade = t(grade_bg, grade_en, lang)
        for level_bg, level_en, day_code, start, end in rows:
            if day_code is None:
                continue
            instances.append({
                "@type": "CourseInstance",
                "name": f"{grade} · {t(level_bg, level_en, lang)}",
                "courseMode": "Onsite",
                "location": place,
                "courseSchedule": {
                    "@type": "Schedule",
                    "byDay": DAY_SCHEMA[day_code],
                    "startTime": _iso_time(start),
                    "endTime": _iso_time(end),
                    "repeatFrequency": "P1W",
                    "scheduleTimezone": "Europe/Sofia",
                },
            })

    return {
        "@type": "Course",
        "@id": DOMAIN + path + "#course",
        "name": t("Курс по английски език — Училище Чемпиън", "English Course — Champion School", lang),
        "description": t(
            "Групи по клас и ниво, с продължителност 120 учебни часа на учебен срок. Занятията се провеждат присъствено в Пловдив.",
            "Groups by grade and level, 120 teaching hours per school term. Classes are held in person in Plovdiv.",
            lang,
        ),
        "provider": {"@id": DOMAIN + "/#organization"},
        "url": DOMAIN + path,
        "inLanguage": t("bg-BG", "en", lang),
        "hasCourseInstance": instances,
        "offers": {
            "@type": "Offer",
            "price": "329",
            "priceCurrency": "EUR",
            "url": DOMAIN + path,
            "category": t("Групови занятия по английски език — учебен срок", "English group classes — school term", lang),
        },
    }


def schedule_main(lang):
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    test_url = url_for(lang, "/test/", "/en/test/")
    tbc_note = t("Предстои да се уточни", "To be confirmed", lang)

    def render_group(grade_bg, grade_en, rows):
        grade = t(grade_bg, grade_en, lang)
        body_rows = ""
        for level_bg, level_en, day_code, start, end in rows:
            level = t(level_bg, level_en, lang)
            if day_code is None:
                body_rows += f'<tr><td>{level}</td><td colspan="2" class="tbc">{tbc_note}</td></tr>'
            else:
                days = t(DAY_LABELS_BG[day_code], DAY_LABELS_EN[day_code], lang)
                body_rows += f'<tr><td>{level}</td><td>{days}</td><td>{start}–{end}</td></tr>'
        return f"""<div class="schedule-group">
          <h3>{grade}</h3>
          <div class="table-wrap">
            <table class="schedule-table schedule-table-compact">
              <thead>
                <tr>
                  <th scope="col">{t("Ниво", "Level", lang)}</th>
                  <th scope="col">{t("Дни", "Days", lang)}</th>
                  <th scope="col">{t("Час", "Time", lang)}</th>
                </tr>
              </thead>
              <tbody>{body_rows}</tbody>
            </table>
          </div>
        </div>"""

    groups_html = "".join(render_group(grade_bg, grade_en, rows) for grade_bg, grade_en, rows in SCHEDULE_DEFINITION)

    summary = f"""<div class="card" style="padding:26px 28px">
      <div class="contact-list">
        <div class="contact-row"><span class="ic" aria-hidden="true">⏱</span><div><div class="lbl">{t("Продължителност", "Duration", lang)}</div><span class="val">{t("120 учебни часа, от 3 октомври", "120 teaching hours, starting 3 October", lang)}</span></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">💳</span><div><div class="lbl">{t("Цена", "Price", lang)}</div><span class="val"><s style="color:var(--muted);font-weight:600">{t("399 €", "€399", lang)}</s> {t("329 евро за учебен срок", "EUR 329 per school term", lang)}</span><div style="font-size:13px;color:var(--muted);font-weight:500;margin-top:4px">{t("Учебниците не са включени в цената на курса и се заплащат при записване.", "Textbooks are not included in the course price and are paid for separately at enrollment.", lang)}</div></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">👪</span><div><div class="lbl">{t("Отстъпка", "Discount", lang)}</div><span class="val">{t("10% за второ дете от семейството", "10% for a second child from the same family", lang)}</span></div></div>
      </div>
    </div>"""

    return f"""<section class="section-tight">
      <div class="container">
        <p class="eyebrow">{t("График и цени", "Schedule & Prices", lang)}</p>
        <h1 class="section-title">{t("График и цени", "Schedule & Prices", lang)}</h1>
        <p class="section-lead">{t(
          "По-долу е графикът на групите по клас и ниво за текущия учебен срок, заедно с продължителността и цената на курса.",
          "Below is the schedule of groups by grade and level for the current school term, along with the course duration and price.",
          lang)}</p>

        <h2 class="sr-only">{t("Групи по клас и ниво", "Groups by grade and level", lang)}</h2>
        <div class="stack" style="margin-top:24px">
          {groups_html}
          <h2 class="sr-only">{t("Продължителност, цена и отстъпки", "Duration, price and discounts", lang)}</h2>
          {summary}
        </div>

        <div class="actions" style="margin-top:30px">
          <a class="btn btn-primary btn-lg" href="{enroll_url}">{t("Записване", "Enrollment", lang)}</a>
          <a class="btn btn-secondary btn-lg" href="{test_url}">{t("Тест за ниво", "Level test", lang)}</a>
        </div>
      </div>
    </section>"""


def build_schedule():
    for lang, path, alt in [("bg", "/schedule-prices/", "/en/schedule-prices/"), ("en", "/en/schedule-prices/", "/schedule-prices/")]:
        title = t(
            "График и цени за групи по английски | Училище Чемпиън Пловдив",
            "Schedule & Prices for English Groups | Champion School Plovdiv",
            lang,
        )
        desc = t(
            "Вижте графика по дни и часове, продължителността и цената на групите по английски в Училище Чемпиън, Пловдив.",
            "See the weekly schedule, course duration and price for English groups at Champion School, Plovdiv.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("График и цени", "Schedule & Prices", lang), path),
        ]
        nodes = [schedule_course_node(lang, path)]
        html = wrap_page(lang, "schedule", path, alt, title, desc, schedule_main(lang), nodes, breadcrumb_items=breadcrumb)
        write_file(path + "index.html", html)


def enrollment_main(lang):
    test_url = url_for(lang, "/test/", "/en/test/")
    contacts_url = url_for(lang, "/contacts/", "/en/contacts/")

    steps = [
        (t("Направете тест за ниво", "Take the level test", lang),
         t("Ако все още не сте сигурни за нивото на ученика, елате на присъствения ни тест за ниво в училището.", "If you are not yet sure of the student's level, come to our in-person level test at the school.", lang)),
        (t("Изберете подходяща група", "Choose a suitable group", lang),
         t("Прегледайте групите по клас и ниво в „График и цени“ или се консултирайте с нас.", "Browse groups by grade and level on “Schedule & Prices” or ask us directly.", lang)),
        (t("Свържете се с нас", "Contact us", lang),
         t("Обадете се на 0885 712 048 (също и Viber) или ни пишете в Instagram.", "Call us at 0885 712 048 (also on Viber), or message us on Instagram.", lang)),
        (t("Получете потвърждение", "Get confirmation", lang),
         t("Ще се свържем с вас, за да потвърдим свободно място, група, ден и час.", "We will contact you to confirm availability, group, day and time.", lang)),
        (t("Започнете обучение", "Start classes", lang),
         t("Ученикът се присъединява към групата и започва редовни занятия по английски.", "The student joins the group and begins regular English classes.", lang)),
    ]
    steps_html = "".join(
        f'<div class="step"><span class="num">{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (h, p) in enumerate(steps)
    )

    contact_card = f"""<div class="card" style="padding:32px">
      <h2 class="sr-only">{t("Свържете се с нас за записване", "Contact us to enroll", lang)}</h2>
      <div class="contact-list">
        <div class="contact-row"><span class="ic" aria-hidden="true">📞</span><div><div class="lbl">{t("Тел. и Viber", "Phone & Viber", lang)}</div><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></div></div>
        <div class="contact-row"><span class="ic" aria-hidden="true">📷</span><div><div class="lbl">Instagram</div><a href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a></div></div>
      </div>
      <div class="actions" style="margin-top:22px">
        <a class="btn btn-primary btn-lg" href="{SITE['phone_href']}">{t("Обадете се", "Call us", lang)}</a>
        <a class="btn btn-secondary btn-lg" href="{contacts_url}">{t("Виж контакти", "View contact details", lang)}</a>
      </div>
    </div>"""

    return f"""<section class="section-tight">
      <div class="container-narrow">
        <p class="eyebrow">{t("Записване", "Enrollment", lang)}</p>
        <h1 class="section-title">{t("Записване", "Enrollment", lang)}</h1>
        <p class="section-lead">{t(
          "Записването в Училище Чемпиън става в няколко прости стъпки. Обадете се или ни пишете в Instagram — ще се свържем с вас, за да потвърдим подходяща група.",
          "Enrolling at Champion School takes a few simple steps. Call us or message us on Instagram — we will contact you to confirm a suitable group.",
          lang)}</p>
      </div>
    </section>
    <section class="section-tight section-alt">
      <div class="container">
        <h2 class="sr-only">{t("Как протича записването", "How enrollment works", lang)}</h2>
        <div class="steps">{steps_html}</div>
      </div>
    </section>
    <section class="section">
      <div class="container-narrow">
        {contact_card}
      </div>
    </section>"""


def build_enrollment():
    for lang, path, alt in [("bg", "/enrollment/", "/en/enrollment/"), ("en", "/en/enrollment/", "/enrollment/")]:
        title = t(
            "Записване в Училище Чемпиън | Английски за ученици в Пловдив",
            "Enrollment at Champion School | English for Students in Plovdiv",
            lang,
        )
        desc = t(
            "Запишете детето си за курс по английски в Училище Чемпиън, Пловдив. Обадете се на 0885 712 048 или ни пишете в Instagram.",
            "Enroll your child in an English course at Champion School, Plovdiv. Call 0885 712 048 or message us on Instagram.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("Записване", "Enrollment", lang), path),
        ]
        html = wrap_page(lang, "enrollment", path, alt, title, desc, enrollment_main(lang), [], breadcrumb_items=breadcrumb)
        write_file(path + "index.html", html)


def contacts_main(lang):
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")

    return f"""<section class="section-tight">
      <div class="container">
        <p class="eyebrow">{t("Контакти", "Contact", lang)}</p>
        <h1 class="section-title">{t("Свържете се с Училище Чемпиън", "Get in touch with Champion School", lang)}</h1>
        <p class="section-lead">{t(
          "Обадете се, пишете ни в Instagram или Facebook, изпратете имейл или ни посетете на място. С удоволствие ще отговорим на въпросите ви за обучението по английски.",
          "Call us, message us on Instagram or Facebook, send an email, or visit us in person. We are happy to answer your questions about English courses.",
          lang)}</p>
      </div>
    </section>
    <section class="section">
      <div class="container grid grid-2">
        <div>
          <h2 class="sr-only">{t("Данни за връзка", "Contact details", lang)}</h2>
          <div class="contact-list">
            <div class="contact-row"><span class="ic" aria-hidden="true">📍</span><div><div class="lbl">{t("Адрес", "Address", lang)}</div><span class="val">{t(SITE['address_bg'], SITE['address_en'], lang)}</span></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">📞</span><div><div class="lbl">{t("Телефон", "Phone", lang)}</div><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">✉️</span><div><div class="lbl">Email</div><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">📷</span><div><div class="lbl">Instagram</div><a href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">👍</span><div><div class="lbl">Facebook</div><a href="{SITE['facebook_url']}" rel="noopener" target="_blank">{t("Страницата ни във Facebook ↗", "Our Facebook page ↗", lang)}</a></div></div>
          </div>
          <p class="text-muted" style="margin-top:20px;font-size:14.5px">{t(
            'Искате да запишете ученик? Разгледайте страница', 'Want to enroll a student? Visit the', lang)}
            <a href="{enroll_url}" class="btn-ghost">{t("„Записване“", "Enrollment page", lang)}</a>.</p>
        </div>
        <div>
          <h2 class="sr-only">{t("Карта", "Map", lang)}</h2>
          <div class="map-frame">
            <iframe src="{SITE['maps_embed_src']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{t('Карта с местоположението на Училище Чемпиън', 'Map showing the Champion School location', lang)}"></iframe>
          </div>
          <p style="margin-top:10px"><a class="btn-ghost" href="{SITE['maps_link']}" rel="noopener" target="_blank">{t("Отвори в Google Maps ↗", "Open in Google Maps ↗", lang)}</a></p>
        </div>
      </div>
    </section>"""


def build_contacts():
    for lang, path, alt in [("bg", "/contacts/", "/en/contacts/"), ("en", "/en/contacts/", "/contacts/")]:
        title = t(
            "Контакти | Училище Чемпиън – английски език в Пловдив",
            "Contact | Champion School, Plovdiv",
            lang,
        )
        desc = t(
            f"Свържете се с Училище Чемпиън в Пловдив: {SITE['address_bg']}, тел. {SITE['phone_display']}, Instagram {SITE['instagram_handle']}.",
            f"Contact Champion School in Plovdiv: {SITE['address_en']}, phone {SITE['phone_display']}, Instagram {SITE['instagram_handle']}.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("Контакти", "Contact", lang), path),
        ]
        html = wrap_page(lang, "contacts", path, alt, title, desc, contacts_main(lang), [], breadcrumb_items=breadcrumb)
        write_file(path + "index.html", html)


def legal_main(lang, kind):
    privacy_url = url_for(lang, "/privacy-policy/", "/en/privacy-policy/")
    if kind == "privacy":
        title = t("Политика за поверителност", "Privacy Policy", lang)
        body = f"""
        <p>{t(
          "Уебсайтът на Училище Чемпиън не съдържа форми за въвеждане на лични данни и не събира, не съхранява и не обработва лични данни чрез сайта.",
          "The Champion School website does not contain any forms for entering personal data, and does not collect, store, or process personal data through the site.",
          lang)}</p>
        <p>{t(
          "Ако се свържете с нас по телефон, Viber или Instagram, комуникацията се осъществява извън този уебсайт, чрез съответната услуга, и не е предмет на тази политика.",
          "If you contact us by phone, Viber, or Instagram, that communication takes place outside this website, through the respective service, and is not covered by this policy.",
          lang)}</p>
        <h2>{t("Администратор на сайта", "Site operator", lang)}</h2>
        <p>{t(
          f"{SITE['legal_name']}, ЕИК {SITE['legal_eik']}, със седалище и адрес на управление: {SITE['legal_address_bg']}.",
          f"{SITE['legal_name']}, UIC (ЕИК) {SITE['legal_eik']}, registered office: {SITE['legal_address_en']}.",
          lang)}</p>
        <h2>{t("Бъдещи промени", "Future changes", lang)}</h2>
        <p>{t(
          "Ако в бъдеще добавим начин за събиране на лични данни чрез сайта (например форма за записване), тази политика ще бъде актуализирана съответно, включително информация за администратора, целите на обработване и правата ви като субект на данни.",
          "If we add a way to collect personal data through the site in the future (for example, an enrollment form), this policy will be updated accordingly, including information about the data controller, the purposes of processing, and your rights as a data subject.",
          lang)}</p>
        <h2>{t("Бисквитки", "Cookies", lang)}</h2>
        <p>{t("Информация за използваните бисквитки ще намерите в", "Information about the cookies used can be found in our", lang)}
        <a href="{url_for(lang, '/cookie-policy/', '/en/cookie-policy/')}">{t("Политиката за бисквитки", "Cookie Policy", lang)}</a>.</p>
        """
    else:
        title = t("Политика за бисквитки", "Cookie Policy", lang)
        body = f"""
        <p>{t(
          "Уебсайтът на Училище Чемпиън понастоящем не използва аналитични, рекламни или маркетингови бисквитки. Използват се единствено технически необходими механизми на браузъра (например запомняне на избрания език), без които определени функции на сайта не биха работили.",
          "The Champion School website does not currently use analytics, advertising or marketing cookies. Only strictly necessary browser mechanisms are used (for example, remembering a language choice), without which certain site features would not work.",
          lang)}</p>
        <p>{t("Ако в бъдеще добавим аналитични или маркетингови бисквитки, тази страница ще бъде актуализирана и, при необходимост, ще поискаме съгласието ви.", "If we add analytics or marketing cookies in the future, this page will be updated and, where required, we will ask for your consent.", lang)}</p>
        <h2>{t("Как да управлявате бисквитките", "How to manage cookies", lang)}</h2>
        <p>{t("Повечето браузъри позволяват управление и изтриване на бисквитки чрез настройките си. Ограничаването на бисквитките може да засегне функционалността на някои сайтове.", "Most browsers allow you to manage and delete cookies through their settings. Restricting cookies may affect the functionality of some websites.", lang)}</p>
        <p>{t("За въпроси относно тази политика, свържете се с нас на", "For questions about this policy, contact us at", lang)}
        <a href="{SITE['phone_href']}">{SITE['phone_display']}</a>.</p>
        <p>{t(f"Бисквитките на този сайт се управляват от {SITE['legal_name']}, ЕИК {SITE['legal_eik']}. Пълни данни за администратора на лични данни ще намерите в", f"Cookies on this site are managed by {SITE['legal_name']}, UIC (ЕИК) {SITE['legal_eik']}. Full data-controller details are available in the", lang)}
        <a href="{privacy_url}">{t("Политиката за поверителност", "Privacy Policy", lang)}</a>.</p>
        """

    return f"""<section class="section-tight">
      <div class="container-narrow">
        <p class="eyebrow">{t("Правна информация", "Legal", lang)}</p>
        <h1 class="section-title">{title}</h1>
      </div>
    </section>
    <section class="section">
      <div class="container-narrow stack" style="font-size:15.5px;color:var(--muted);line-height:1.7">
        {body}
      </div>
    </section>"""


def build_legal():
    pages = [
        ("privacy", "/privacy-policy/", "/en/privacy-policy/",
         t("Политика за поверителност | Училище Чемпиън", "Privacy Policy | Champion School", "bg"),
         "Политика за поверителност | Училище Чемпиън", "Privacy Policy | Champion School",
         "Уебсайтът на Училище Чемпиън не съдържа форми и не събира лични данни през сайта.",
         "The Champion School website contains no forms and collects no personal data through the site."),
        ("cookie", "/cookie-policy/", "/en/cookie-policy/",
         None,
         "Политика за бисквитки | Училище Чемпиън", "Cookie Policy | Champion School",
         "Информация за бисквитките, използвани на уебсайта на Училище Чемпиън.",
         "Information about the cookies used on the Champion School website."),
    ]
    for kind, path_bg, path_en, _unused, title_bg, title_en, desc_bg, desc_en in pages:
        for lang, path, alt in [("bg", path_bg, path_en), ("en", path_en, path_bg)]:
            title = t(title_bg, title_en, lang)
            desc = t(desc_bg, desc_en, lang)
            label = t("Политика за поверителност" if kind == "privacy" else "Политика за бисквитки",
                       "Privacy Policy" if kind == "privacy" else "Cookie Policy", lang)
            breadcrumb = [
                (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
                (label, path),
            ]
            html = wrap_page(lang, "legal", path, alt, title, desc, legal_main(lang, kind), [], breadcrumb_items=breadcrumb)
            write_file(path + "index.html", html)


def build_home():
    for lang, path, alt in [("bg", "/", "/en/"), ("en", "/en/", "/")]:
        title = t(
            "Английски език за деца и ученици в Пловдив | Училище Чемпиън",
            "English Courses for Children & Students in Plovdiv | Champion School",
            lang,
        )
        desc = t(
            "Училище Чемпиън обучава по английски език ученици от 2. до 12. клас в Пловдив. Направете присъствен тест за ниво и запишете детето си в подходяща група.",
            "Champion School teaches English in Plovdiv to students in grades 2-12. Take our in-person level test and enroll your child in the right group.",
            lang,
        )
        nodes = [faq_node(path, FAQ_BG if lang == "bg" else FAQ_EN)]
        html = wrap_page(lang, "home", path, alt, title, desc, home_main(lang), nodes)
        write_file(path + "index.html" if path.endswith("/") else path, html)


# ---------------------------------------------------------------------------
# robots.txt / sitemap.xml
# ---------------------------------------------------------------------------

PAGE_PAIRS = [
    ("/", "/en/"),
    ("/test/", "/en/test/"),
    ("/schedule-prices/", "/en/schedule-prices/"),
    ("/enrollment/", "/en/enrollment/"),
    ("/contacts/", "/en/contacts/"),
    ("/privacy-policy/", "/en/privacy-policy/"),
    ("/cookie-policy/", "/en/cookie-policy/"),
]


def build_htaccess():
    """
    Apache config for compression + a few safe, related defaults. Only
    relevant on an Apache/LiteSpeed host that reads .htaccess -- GitHub
    Pages (this repo's CNAME target) ignores it entirely and gzip/brotli-
    compresses everything automatically via its own CDN regardless. Keep
    this file for portability if the site is ever self-hosted on Apache.
    """
    content = """# Compression -----------------------------------------------------------
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/css text/javascript text/xml
  AddOutputFilterByType DEFLATE application/javascript application/x-javascript
  AddOutputFilterByType DEFLATE application/json application/xml application/xhtml+xml
  AddOutputFilterByType DEFLATE application/rss+xml application/ld+json
  AddOutputFilterByType DEFLATE image/svg+xml
  <IfModule mod_setenvif.c>
    BrowserMatch ^Mozilla/4 gzip-only-text/html
    BrowserMatch ^Mozilla/4\\.0[678] no-gzip
    BrowserMatch \\bMSIE !no-gzip !gzip-only-text/html
  </IfModule>
</IfModule>

<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/css text/javascript
  AddOutputFilterByType BROTLI_COMPRESS application/javascript application/json
  AddOutputFilterByType BROTLI_COMPRESS application/xml application/xhtml+xml application/ld+json
  AddOutputFilterByType BROTLI_COMPRESS image/svg+xml
</IfModule>

# Already-compressed formats: don't try to recompress them.
<IfModule mod_deflate.c>
  SetEnvIfNoCase Request_URI \\.(?:jpe?g|png|webp|gif|ico|woff2?)$ no-gzip
</IfModule>

# Caching ------------------------------------------------------------------
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css                "access plus 1 year"
  ExpiresByType application/javascript  "access plus 1 year"
  ExpiresByType image/png               "access plus 1 year"
  ExpiresByType image/jpeg              "access plus 1 year"
  ExpiresByType image/webp              "access plus 1 year"
  ExpiresByType image/x-icon            "access plus 1 year"
  ExpiresByType text/html               "access plus 0 seconds"
</IfModule>
"""
    write_file("/.htaccess", content)


def build_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    write_file("/robots.txt", content)


def build_sitemap():
    build_date = datetime.date.today().isoformat()
    urls = []
    for bg_path, en_path in PAGE_PAIRS:
        for path, alt in [(bg_path, en_path), (en_path, bg_path)]:
            urls.append(f"""  <url>
    <loc>{DOMAIN}{path}</loc>
    <lastmod>{build_date}</lastmod>
    <xhtml:link rel="alternate" hreflang="bg-BG" href="{DOMAIN}{bg_path}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{en_path}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{bg_path}"/>
  </url>""")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>
"""
    write_file("/sitemap.xml", content)


def build_llms_txt():
    """
    llms.txt -- a plain-text/Markdown briefing for AI assistants and LLM
    crawlers (distinct from robots.txt, which only grants crawl permission).
    Emerging convention: H1 title, a one-line blockquote summary, then
    Markdown-link sections. Content here is limited to facts already
    published elsewhere on the site -- nothing new is asserted.
    """
    content = f"""# Champion School / Училище Чемпиън

> English language school in Plovdiv, Bulgaria, teaching students in grades 2 through 12. Bulgarian-first site with a full English version under /en/.

Champion School ({SITE['full_name_en']}, registered as {SITE['legal_name']}, UIC {SITE['legal_eik']}) teaches English as a foreign language to school-age students, grouped by grade and by English level (Beginner through Advanced / CEFR A1-C1). Classes are held in Plovdiv, Bulgaria, at {SITE['address_street_en']}. Phone: {SITE['phone_display']} ({SITE['phone_href']}). Instagram: {SITE['instagram_handle']} ({SITE['instagram_url']}).

Current class days, times and prices by grade and level are published on the Schedule & Prices page; contact the school directly to confirm availability.

## Key pages (Bulgarian, default)

- [Home]({DOMAIN}/): what Champion School is, who it teaches, why families choose it, FAQ
- [Level Test]({DOMAIN}/test/): in-person level test held at the school (not an online quiz); see the page for current test dates, times and how to book
- [Schedule & Prices]({DOMAIN}/schedule-prices/): published days, times, duration and price by grade and level (a few levels still to be confirmed)
- [Enrollment]({DOMAIN}/enrollment/): how to enroll a student, step by step; contact by phone or Instagram
- [Contact]({DOMAIN}/contacts/): address, phone, Instagram, map
- [Privacy Policy]({DOMAIN}/privacy-policy/)
- [Cookie Policy]({DOMAIN}/cookie-policy/)

## Key pages (English)

- [Home]({DOMAIN}/en/)
- [Level Test]({DOMAIN}/en/test/)
- [Schedule & Prices]({DOMAIN}/en/schedule-prices/)
- [Enrollment]({DOMAIN}/en/enrollment/)
- [Contact]({DOMAIN}/en/contacts/)

## Notes for automated systems

- The site is static HTML; all page content (including FAQ answers and the level-test dates) is present in the initial HTML response, not injected client-side.
- Structured data (Schema.org JSON-LD: EducationalOrganization, LocalBusiness, WebSite, WebPage, BreadcrumbList, FAQPage) is embedded on every page and is the preferred source for structured facts.
- Do not infer prices, schedules, teacher names, enrollment statistics, or accreditations that are not stated on the pages above -- the site deliberately omits these rather than publishing placeholder figures.
"""
    write_file("/llms.txt", content)


def main():
    build_assets()
    build_home()
    build_test()
    build_schedule()
    build_enrollment()
    build_contacts()
    build_legal()
    build_robots()
    build_sitemap()
    build_llms_txt()
    build_htaccess()
    print("\nDone.")


if __name__ == "__main__":
    main()
