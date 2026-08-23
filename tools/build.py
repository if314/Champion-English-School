# -*- coding: utf-8 -*-
"""
Static site generator for the Champion / Чемпиън website.
Produces plain HTML/CSS/JS into ../dev — no client-side framework, no
build-time dependency is shipped; this script only exists to keep the
repeated header/footer/schema markup consistent across ~14 pages.
Run: python3 tools/build.py
"""
import json
import os
import textwrap

from site_data import (
    DOMAIN, SITE, NAV_BG, NAV_EN, FOOTER_LEGAL_BG, FOOTER_LEGAL_EN,
    TEST_QUESTIONS, LEVELS_BG, LEVELS_EN, FAQ_BG, FAQ_EN,
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
    test_url = url_for(lang, "/test/", "/en/test/")
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    brand_name = t("Чемпиън", "Champion", lang)
    brand_tag = t("Училище по английски", "English language school", lang)
    logo_alt = t("Лого на училище Чемпиън", "Champion school logo", lang)
    nav_label = t("Основна навигация", "Main navigation", lang)
    lang_label = t("Смяна на езика", "Language switcher", lang)
    menu_label = t("Отвори менюто", "Open menu", lang)
    test_label = t("Тест за ниво", "Level Test", lang)
    enroll_label = t("Запиши се", "Enroll Now", lang)

    links = "\n".join(
        '<a href="{url}"{cur}>{label}</a>'.format(
            url=url,
            cur=' aria-current="page"' if key == active_key else "",
            label=label,
        )
        for key, label, url in nav
    )

    header = f"""<a class="skip-link" href="#main">{t("Към съдържанието", "Skip to content", lang)}</a>
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="{home_url}" aria-label="{brand_name} — {t("начало", "home", lang)}">
        <span class="brand-mark"><img src="/img/champion-logo.png" width="640" height="350" alt="{logo_alt}"></span>
        <span class="brand-text"><span class="name">{brand_name}</span><span class="tag">{brand_tag}</span></span>
      </a>
      <nav class="nav-links" aria-label="{nav_label}">
        {links}
      </nav>
      <div class="nav-right">
        <div class="nav-cta">
          <a class="btn btn-secondary" href="{test_url}">{test_label}</a>
          <a class="btn btn-primary" href="{enroll_url}">{enroll_label}</a>
        </div>
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
      <div class="mobile-cta">
        <a class="btn btn-secondary btn-block" href="{test_url}">{test_label}</a>
        <a class="btn btn-primary btn-block" href="{enroll_url}">{enroll_label}</a>
      </div>
      <div class="mobile-contact">
        <a href="{SITE['phone_href']}">{SITE['phone_display']}</a>
        <span>{t(SITE['address_bg'], SITE['address_en'], lang)}</span>
      </div>
    </div>
  </div>"""
    return header


def render_footer(lang, bg_url, en_url):
    nav = NAV_BG if lang == "bg" else NAV_EN
    legal = FOOTER_LEGAL_BG if lang == "bg" else FOOTER_LEGAL_EN
    brand_name = t("Чемпиън", "Champion", lang)
    desc = t(
        "Чемпиън е училище по английски език в Пловдив за ученици от 2. до 12. клас — с ясни нива, малки групи и фокус върху реалната комуникация.",
        "Champion is an English language school in Plovdiv for students in grades 2 to 12 — with clear levels, small groups and a focus on real communication.",
        lang,
    )
    nav_heading = t("Навигация", "Navigation", lang)
    contact_heading = t("Контакти", "Contact", lang)
    legal_heading = t("Правна информация", "Legal", lang)

    nav_links = "\n".join(f'<li><a href="{url}">{label}</a></li>' for _, label, url in nav)
    legal_links = "\n".join(f'<li><a href="{url}">{label}</a></li>' for label, url in legal)

    rights = t(f"© {YEAR} Чемпиън. Всички права запазени.", f"© {YEAR} Champion. All rights reserved.", lang)
    legal_note = t(
        "Училището се управлява от [пълно наименование на дружеството], ЕИК [номер], със седалище и адрес на управление: [адрес на управление]. Данните предстои да бъдат допълнени.",
        "Champion is operated by [company legal name], company ID [registration number], registered office: [registered address]. Details to be completed.",
        lang,
    )
    editable = t("Редактируемо", "Editable", lang)

    return f"""<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">
            <span class="brand-mark"><img src="/img/champion-logo.png" width="640" height="350" alt=""></span>
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
      <p class="footer-note"><span class="badge badge-placeholder">{editable}</span> {legal_note}</p>
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
        "alternateName": "Champion",
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
        "areaServed": {"@type": "City", "name": t("Пловдив", "Plovdiv", lang)},
        "sameAs": [SITE["instagram_url"]],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "telephone": "+359885712048",
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
        "name": t("Чемпиън", "Champion", lang),
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
<meta property="og:site_name" content="Champion / Чемпиън">
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
    return html


def write_file(rel_path, content):
    full = os.path.join(OUT, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel_path)


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
        "Чемпиън е училище по английски език в Пловдив за ученици от 2. до 12. клас. Учим децата и учениците да говорят уверено, да разбират бързо и да използват английския извън класната стая.",
        "Champion is an English language school in Plovdiv for students in grades 2 to 12. We help children and teenagers speak with confidence, understand quickly, and use English beyond the classroom.",
        lang,
    )
    cta_test = t("Направи тест за ниво", "Take the level test", lang)
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
            <picture>
              <source type="image/webp" srcset="/img/students-hero-800.webp 800w, /img/students-hero.webp 1400w" sizes="(min-width: 900px) 480px, 92vw">
              <img src="/img/students-hero.jpg" srcset="/img/students-hero-800.jpg 800w, /img/students-hero.jpg 1400w" sizes="(min-width: 900px) 480px, 92vw" width="1400" height="933" alt="{t('Ученици, обучаващи се по английски език', 'Students learning English', lang)}" loading="eager" fetchpriority="high">
            </picture>
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
          <p class="eyebrow">{t("За Чемпиън", "About Champion", lang)}</p>
          <h2 class="section-title">{t("Училище по английски за ученици от 2. до 12. клас", "An English school for students in grades 2 to 12", lang)}</h2>
        </div>
        <div class="grid grid-2">
          <p class="section-lead">{t(
            "Чемпиън е специализирано училище по английски език в Пловдив, създадено за ученици от начален, прогимназиален и гимназиален етап — от 2. до 12. клас. Работим в групи, ясно определени по клас и ниво, за да може всеки ученик да напредва с подходящото за него темпо.",
            "Champion is a dedicated English language school in Plovdiv for students at primary, lower-secondary and upper-secondary level — from grade 2 through grade 12. We work in groups clearly organized by grade and level, so every student can progress at the right pace.",
            lang)}</p>
          <p class="section-lead">{t(
            "Целта ни е проста: учениците да излизат от часовете с реална увереност да говорят, пишат и разбират английски — не просто да наизустяват граматика за оценка.",
            "Our goal is simple: students should leave lessons with real confidence to speak, write and understand English — not just memorize grammar for a grade.",
            lang)}</p>
        </div>
      </div>
    </section>"""

    why_cards = [
        ("🎯", t("Ниво, определено точно", "A precisely matched level", lang),
         t("За всеки ученик правим тест за ниво, преди да предложим група — така обучението не е нито прекалено лесно, нито прекалено трудно.",
           "Every student takes a level test before joining a group, so the course is neither too easy nor too demanding.", lang)),
        ("👥", t("Групи по клас и ниво", "Groups by grade and level", lang),
         t("Групираме учениците по клас и по ниво на владеене на езика, а не само по възраст, за да учат с връстници на сходно ниво.",
           "We group students by grade and by English level, not just age, so they learn alongside peers at a similar stage.", lang)),
        ("💬", t("Фокус върху говоримия език", "A focus on spoken English", lang),
         t("Часовете съчетават граматика и лексика с практика в говоренето, за да могат учениците да прилагат английския извън класната стая.",
           "Lessons combine grammar and vocabulary with speaking practice, so students can use English beyond the classroom.", lang)),
    ]
    why = f"""<section class="section section-alt">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("Защо Чемпиън", "Why Champion", lang)}</p>
          <h2 class="section-title">{t("Защо да изберете Чемпиън", "Why families choose Champion", lang)}</h2>
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
        (t("8.–10. клас", "Grades 8-10", lang), t(
            "Гимназиален етап — по-задълбочена граматика, академична лексика и подготовка за писмени и устни изпитвания в училище.",
            "Upper-secondary stage — deeper grammar, academic vocabulary and preparation for school written and oral assessments.", lang)),
        (t("11.–12. клас", "Grades 11-12", lang), t(
            "Гимназиален етап — увереност пред матура, кандидатстване и бъдещо обучение или работа, изискващи английски.",
            "Upper-secondary stage — confidence for school-leaving exams, applications, and future study or work that requires English.", lang)),
    ]
    grades_section = f"""<section class="section" id="grades">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">{t("По класове", "By grade", lang)}</p>
          <h2 class="section-title">{t("Обучение от 2. до 12. клас", "Courses from grade 2 to grade 12", lang)}</h2>
          <p class="section-lead">{t("Групираме учениците в четири основни степени, съобразени с училищната програма в България.", "We group students into four core stages, aligned with the Bulgarian school curriculum.", lang)}</p>
        </div>
        <div class="grid grid-4">
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
          <h2 class="section-title">{t("Как учим английски в Чемпиън", "How we teach English at Champion", lang)}</h2>
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
          <p>{t("Направете кратък тест за ниво по английски — отнема само няколко минути и дава ориентировъчна представа за нивото на ученика, преди да изберете група.",
                "Take a short English level test — it takes just a few minutes and gives an approximate picture of the student's level before choosing a group.", lang)}</p>
          <div class="actions"><a class="btn btn-primary" href="{test_url}">{cta_test}</a></div>
        </div>
        <div class="panel panel-gold">
          <h3>{t("Ориентировъчни нива", "Approximate levels", lang)}</h3>
          <div class="stack">
            {"".join(f'<div><strong>{lv["name"]}</strong><br><span style="font-size:13.5px">{lv["cefr"].split(chr(183))[0].strip()}</span></div>' for lv in (LEVELS_BG if lang=="bg" else LEVELS_EN))}
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
            "Пълната информация за групите, дните, часовете и цените ще намерите на страница „График и цени“. Точните разписания се потвърждават индивидуално според сформираните групи.",
            "Full details on groups, days, times and prices are available on the “Schedule & Prices” page. Exact schedules are confirmed individually once groups are formed.", lang)}</p>
        </div>
        <div class="grid grid-4">
          {"".join(f'<div class="grade-card"><div class="range">{g}</div><p>{t("Дни, час и цена — уточняват се", "Days, time and price — to be confirmed", lang)}</p><span class="badge badge-placeholder">{t("Уточнява се", "To be confirmed", lang)}</span></div>' for g in [t("2.–4. клас","Grades 2-4",lang), t("5.–7. клас","Grades 5-7",lang), t("8.–10. клас","Grades 8-10",lang), t("11.–12. клас","Grades 11-12",lang)])}
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
            <p>{t("Изпратете запитване онлайн или се обадете — ще потвърдим подходяща група заедно.", "Send an inquiry online or call us — we will confirm a suitable group together.", lang)}</p>
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
            <iframe src="{SITE['maps_embed_src']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{t('Карта с местоположението на Чемпиън', 'Map showing the Champion location', lang)}"></iframe>
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
            <p>{t("Новини, снимки от занятия и полезни материали за учениците на Чемпиън.", "News, glimpses from classes and useful materials for Champion students.", lang)}</p>
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


def test_questions_html(lang):
    label_word = t("Въпрос", "Question", lang)
    parts = []
    for i, item in enumerate(TEST_QUESTIONS):
        opts = "".join(
            f'''<label class="test-option">
              <input type="radio" name="q{i}" value="{letter}" data-correct="{"true" if correct else "false"}">
              <span class="opt-face"><span class="letter">{letter}</span> {text}</span>
            </label>'''
            for letter, text, correct in item["options"]
        )
        active = " is-active" if i == 0 else ""
        parts.append(f'''<div class="test-question{active}" data-index="{i}">
          <div class="q-eyebrow">{item["tag"]}</div>
          <h2>{i + 1}. {item["q"]}</h2>
          <div class="test-options" role="radiogroup" aria-label="{label_word} {i + 1}">
            {opts}
          </div>
        </div>''')
    return "".join(parts)


def test_main(lang):
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    contacts_url = url_for(lang, "/contacts/", "/en/contacts/")
    levels = LEVELS_BG if lang == "bg" else LEVELS_EN
    levels_json = json.dumps(levels, ensure_ascii=False)

    intro = f"""<section class="section-tight">
      <div class="container-narrow">
        <p class="eyebrow">{t("Първа стъпка", "First step", lang)}</p>
        <h1 class="section-title">{t("Тест за ниво по английски език", "English Level Test", lang)}</h1>
        <p class="section-lead">{t(
          "Тестът съдържа 10 кратки въпроса с избираем отговор и отнема около 3–5 минути. Резултатът е ориентировъчен и ни помага да предложим подходяща група преди записване — не е официален изпит или сертификат.",
          "The test has 10 short multiple-choice questions and takes about 3-5 minutes. The result is approximate and helps us suggest a suitable group before enrollment — it is not an official exam or certificate.",
          lang)}</p>
      </div>
    </section>"""

    nowscript = f"""<div class="test-nowscript notice-box container-narrow">
      <p><strong>{t("Нужен е JavaScript.", "JavaScript is required.", lang)}</strong>
      {t("За да преминете интерактивния тест за ниво, моля включете JavaScript в браузъра си, или се обадете на", "To take the interactive level test, please enable JavaScript in your browser, or call us at", lang)}
      <a href="{SITE['phone_href']}">{SITE['phone_display']}</a> {t("за да определим нивото заедно.", "and we will assess the level together.", lang)}</p>
    </div>"""

    test_block = f"""<section class="section-tight test-interactive-only">
      <div class="container">
        <form id="level-test-form" class="test-shell" novalidate
              data-msg-select="{t('Моля, изберете отговор, за да продължите.', 'Please choose an answer to continue.', lang)}"
              data-score-template="{t('Резултат: {score} от {total} верни отговора.', 'Score: {score} out of {total} correct answers.', lang)}">
          <div class="test-progress">
            <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
            <div class="progress-label" id="progressLabel" data-template="{t('Въпрос {current} от {total}', 'Question {current} of {total}', lang)}">{t('Въпрос', 'Question', lang)} 1</div>
          </div>
          {test_questions_html(lang)}
          <p class="field-error" id="testError" role="alert" style="display:none"></p>
          <div class="test-nav">
            <button type="button" id="prevBtn" class="btn btn-secondary" disabled>{t("Назад", "Back", lang)}</button>
            <button type="button" id="nextBtn" class="btn btn-navy" data-label-next="{t('Напред', 'Next', lang)}" data-label-finish="{t('Виж резултата', 'See result', lang)}">{t("Напред", "Next", lang)}</button>
          </div>
        </form>

        <div class="result-panel" id="resultPanel">
          <div class="test-shell">
            <p class="eyebrow">{t("Резултат", "Result", lang)}</p>
            <div class="result-level">
              <span class="lvl-name" id="resultLevelName">—</span>
              <span class="lvl-cefr" id="resultLevelCefr">—</span>
            </div>
            <p id="resultDescription"></p>
            <p id="resultScore" class="text-muted"></p>
            <div class="result-disclaimer">{t(
              "Този резултат е предварителна, вътрешна оценка на Чемпиън и не представлява официален CEFR сертификат или изпит.",
              "This result is a preliminary, internal Champion assessment and does not constitute an official CEFR certificate or exam.", lang)}</div>
            <div class="actions">
              <a class="btn btn-primary" href="{enroll_url}">{t("Запиши се", "Enroll now", lang)}</a>
              <a class="btn btn-secondary" href="{contacts_url}">{t("Свържи се с нас", "Contact us", lang)}</a>
              <button type="button" class="btn btn-ghost" id="retakeBtn">{t("Направи теста отново", "Retake the test", lang)}</button>
            </div>
          </div>
        </div>
      </div>
      <script type="application/json" id="levelData">{levels_json}</script>
    </section>"""

    return intro + nowscript + test_block


def build_test():
    for lang, path, alt in [("bg", "/test/", "/en/test/"), ("en", "/en/test/", "/test/")]:
        title = t(
            "Тест за ниво по английски език | Чемпиън Пловдив",
            "English Level Test | Champion Plovdiv",
            lang,
        )
        desc = t(
            "Направете безплатен онлайн тест за ниво по английски. Ориентировъчен резултат за учениците на Чемпиън в Пловдив, преди записване в подходяща група.",
            "Take a free online English level test. An approximate result for Champion students in Plovdiv, before enrolling in the right group.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("Тест за ниво", "Level Test", lang), path),
        ]
        html = wrap_page(
            lang, "test", path, alt, title, desc, test_main(lang), [],
            breadcrumb_items=breadcrumb,
            extra_js='<script src="/assets/js/level-test.js" defer></script>',
        )
        write_file(path + "index.html", html)


def schedule_main(lang):
    enroll_url = url_for(lang, "/enrollment/", "/en/enrollment/")
    test_url = url_for(lang, "/test/", "/en/test/")
    tbc = t("Уточнява се", "To be confirmed", lang)

    groups = [
        ("Junior A", t("2.–4. клас", "Grades 2-4", lang), "Beginner – Elementary"),
        ("Junior B", t("5.–7. клас", "Grades 5-7", lang), "Elementary – Intermediate"),
        ("Senior A", t("8.–10. клас", "Grades 8-10", lang), "Intermediate – Upper-Intermediate"),
        ("Senior B", t("11.–12. клас", "Grades 11-12", lang), "Upper-Intermediate+"),
    ]

    rows = "\n".join(
        f"""<tr>
          <td><strong>{name}</strong></td>
          <td>{grade}</td>
          <td>{level}</td>
          <td class="tbc">{tbc}</td>
          <td class="tbc">{tbc}</td>
          <td class="tbc">{tbc}</td>
          <td class="tbc">{tbc}</td>
        </tr>"""
        for name, grade, level in groups
    )

    cards = "\n".join(
        f"""<div class="schedule-card">
          <div class="grp">{name} · {grade}</div>
          <dl>
            <dt>{t("Ниво", "Level", lang)}</dt><dd>{level}</dd>
            <dt>{t("Дни", "Days", lang)}</dt><dd class="tbc">{tbc}</dd>
            <dt>{t("Час", "Time", lang)}</dt><dd class="tbc">{tbc}</dd>
            <dt>{t("Продължителност", "Duration", lang)}</dt><dd class="tbc">{tbc}</dd>
            <dt>{t("Цена", "Price", lang)}</dt><dd class="tbc">{tbc}</dd>
          </dl>
        </div>"""
        for name, grade, level in groups
    )

    return f"""<section class="section-tight">
      <div class="container">
        <p class="eyebrow">{t("График и цени", "Schedule & Prices", lang)}</p>
        <h1 class="section-title">{t("График и цени", "Schedule & Prices", lang)}</h1>
        <p class="section-lead">{t(
          "По-долу е общата структура на групите по клас и ниво. Точните дни, часове и цени се потвърждават след сформиране на групите за текущата учебна година — свържете се с нас или направете тест за ниво, за да получите актуална информация за вашия ученик.",
          "Below is the general structure of groups by grade and level. Exact days, times and prices are confirmed once groups are formed for the current school year — contact us or take the level test to get up-to-date information for your student.",
          lang)}</p>

        <div class="notice-box" style="margin:26px 0">
          <p><strong>{t("Разписанието предстои да бъде обявено.", "The schedule is yet to be announced.", lang)}</strong>
          {t("Показаните по-долу полета са примерни placeholder-и и предстои да бъдат актуализирани. За точна информация се обадете на", "The fields shown below are example placeholders and will be updated. For exact information, call", lang)}
          <a href="{SITE['phone_href']}">{SITE['phone_display']}</a>.</p>
        </div>

        <div class="table-wrap responsive-cards">
          <table class="schedule-table">
            <caption>{t("Групи по клас и ниво — дните, часовете и цените предстои да бъдат обявени.", "Groups by grade and level — days, times and prices to be announced.", lang)}</caption>
            <thead>
              <tr>
                <th scope="col">{t("Група", "Group", lang)}</th>
                <th scope="col">{t("Клас", "Grade", lang)}</th>
                <th scope="col">{t("Ниво", "Level", lang)}</th>
                <th scope="col">{t("Дни", "Days", lang)}</th>
                <th scope="col">{t("Час", "Time", lang)}</th>
                <th scope="col">{t("Продължителност", "Duration", lang)}</th>
                <th scope="col">{t("Цена", "Price", lang)}</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        <div class="schedule-cards">{cards}</div>

        <div class="actions" style="margin-top:30px">
          <a class="btn btn-primary btn-lg" href="{enroll_url}">{t("Записване", "Enrollment", lang)}</a>
          <a class="btn btn-secondary btn-lg" href="{test_url}">{t("Направи тест за ниво", "Take the level test", lang)}</a>
        </div>
      </div>
    </section>"""


def build_schedule():
    for lang, path, alt in [("bg", "/schedule-prices/", "/en/schedule-prices/"), ("en", "/en/schedule-prices/", "/schedule-prices/")]:
        title = t(
            "График и цени за групи по английски | Чемпиън Пловдив",
            "Schedule & Prices for English Groups | Champion Plovdiv",
            lang,
        )
        desc = t(
            "Разгледайте групите по клас и ниво в Чемпиън, Пловдив. Дните, часовете и цените се уточняват според сформираните групи.",
            "Browse groups by grade and level at Champion, Plovdiv. Days, times and prices are confirmed once groups are formed.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("График и цени", "Schedule & Prices", lang), path),
        ]
        html = wrap_page(lang, "schedule", path, alt, title, desc, schedule_main(lang), [], breadcrumb_items=breadcrumb)
        write_file(path + "index.html", html)


def enrollment_main(lang):
    test_url = url_for(lang, "/test/", "/en/test/")
    privacy_url = url_for(lang, "/privacy-policy/", "/en/privacy-policy/")

    steps = [
        (t("Направете тест за ниво", "Take the level test", lang),
         t("Ако все още не сте сигурни за нивото на ученика, направете краткия ни тест онлайн.", "If you are not yet sure of the student's level, take our short online test.", lang)),
        (t("Изберете подходяща група", "Choose a suitable group", lang),
         t("Прегледайте групите по клас и ниво в „График и цени“ или се консултирайте с нас.", "Browse groups by grade and level on “Schedule & Prices” or ask us directly.", lang)),
        (t("Изпратете запитване", "Send an inquiry", lang),
         t("Попълнете формата по-долу или ни се обадете на 0885 712 048.", "Fill in the form below or call us at 0885 712 048.", lang)),
        (t("Получете потвърждение", "Get confirmation", lang),
         t("Ще се свържем с вас, за да потвърдим свободно място, група, ден и час.", "We will contact you to confirm availability, group, day and time.", lang)),
        (t("Започнете обучение", "Start classes", lang),
         t("Ученикът се присъединява към групата и започва редовни занятия по английски.", "The student joins the group and begins regular English classes.", lang)),
    ]
    steps_html = "".join(
        f'<div class="step"><span class="num">{i+1}</span><h3>{h}</h3><p>{p}</p></div>'
        for i, (h, p) in enumerate(steps)
    )

    grade_options = "".join(f'<option value="{g}">{g}</option>' for g in [
        "2 клас", "3 клас", "4 клас", "5 клас", "6 клас", "7 клас",
        "8 клас", "9 клас", "10 клас", "11 клас", "12 клас",
    ]) if lang == "bg" else "".join(f'<option value="Grade {g}">Grade {g}</option>' for g in range(2, 13))

    form = f"""<form class="form js-form" novalidate>
      <div class="form-success" role="status">
        {t("Благодарим ви! Получихме вашето запитване и ще се свържем с вас възможно най-скоро на посочения телефон или имейл.", "Thank you! We have received your inquiry and will contact you as soon as possible by phone or email.", lang)}
      </div>
      <div class="form-fields stack">
        <input type="text" name="website" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="form-row form-row-2">
          <div class="field">
            <label for="parentName">{t("Име на родител", "Parent's name", lang)} *</label>
            <input type="text" id="parentName" name="parentName" required autocomplete="name">
            <span class="field-error">{t("Моля, въведете име.", "Please enter a name.", lang)}</span>
          </div>
          <div class="field">
            <label for="studentName">{t("Име на ученика", "Student's name", lang)} *</label>
            <input type="text" id="studentName" name="studentName" required autocomplete="off">
            <span class="field-error">{t("Моля, въведете име на ученика.", "Please enter the student's name.", lang)}</span>
          </div>
        </div>
        <div class="form-row form-row-2">
          <div class="field">
            <label for="grade">{t("Клас", "Grade", lang)} *</label>
            <select id="grade" name="grade" required>
              <option value="" selected disabled>{t("Изберете клас", "Select a grade", lang)}</option>
              {grade_options}
            </select>
            <span class="field-error">{t("Моля, изберете клас.", "Please select a grade.", lang)}</span>
          </div>
          <div class="field">
            <label for="phone">{t("Телефон", "Phone", lang)} *</label>
            <input type="tel" id="phone" name="phone" required autocomplete="tel" placeholder="08XX XXX XXX">
            <span class="field-error">{t("Моля, въведете валиден телефон.", "Please enter a valid phone number.", lang)}</span>
          </div>
        </div>
        <div class="form-row form-row-2">
          <div class="field">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" autocomplete="email">
            <span class="field-error">{t("Моля, въведете валиден имейл.", "Please enter a valid email.", lang)}</span>
          </div>
          <div class="field">
            <label for="preferredTime">{t("Предпочитан ден/час", "Preferred day/time", lang)}</label>
            <input type="text" id="preferredTime" name="preferredTime" placeholder="{t('напр. следобед, след 17ч.', 'e.g. afternoons, after 5pm', lang)}">
          </div>
        </div>
        <fieldset>
          <legend>{t("Предпочитан начин за контакт", "Preferred contact method", lang)}</legend>
          <label class="radio-row"><input type="radio" name="contactMethod" value="phone" checked> {t("Телефон", "Phone", lang)}</label>
          <label class="radio-row"><input type="radio" name="contactMethod" value="email"> Email</label>
        </fieldset>
        <div class="field">
          <label for="message">{t("Допълнителна информация", "Additional information", lang)}</label>
          <textarea id="message" name="message" rows="4"></textarea>
        </div>
        <label class="checkbox-row">
          <input type="checkbox" name="consent" required>
          <span class="consent">{t('Съгласен/на съм предоставените лични данни да бъдат използвани от Чемпиън единствено за връзка във връзка със записване за обучение, съгласно', 'I agree that the personal data provided will be used by Champion solely to contact me regarding enrollment, in accordance with the', lang)}
          <a href="{privacy_url}">{t("Политиката за поверителност", "Privacy Policy", lang)}</a>. *</span>
        </label>
        <button type="submit" class="btn btn-primary btn-lg btn-block">{t("Изпрати запитване", "Send inquiry", lang)}</button>
      </div>
    </form>
    <!-- Integration note: on submit, POST the validated form data to the
         school's chosen backend or transactional email service (e.g. a
         serverless function or a form-to-email provider). No endpoint is
         wired up yet because no address was supplied for this build. -->"""

    return f"""<section class="section-tight">
      <div class="container-narrow">
        <p class="eyebrow">{t("Записване", "Enrollment", lang)}</p>
        <h1 class="section-title">{t("Записване", "Enrollment", lang)}</h1>
        <p class="section-lead">{t(
          "Записването в Чемпиън става в няколко прости стъпки. Изпратете запитване чрез формата по-долу или се обадете директно — ще се свържем с вас, за да потвърдим подходяща група.",
          "Enrolling at Champion takes a few simple steps. Send an inquiry through the form below or call us directly — we will contact you to confirm a suitable group.",
          lang)}</p>
      </div>
    </section>
    <section class="section-tight section-alt">
      <div class="container"><div class="steps">{steps_html}</div></div>
    </section>
    <section class="section">
      <div class="container-narrow">
        <div class="card" style="padding:32px">{form}</div>
      </div>
    </section>"""


def build_enrollment():
    for lang, path, alt in [("bg", "/enrollment/", "/en/enrollment/"), ("en", "/en/enrollment/", "/enrollment/")]:
        title = t(
            "Записване в Чемпиън | Английски за ученици в Пловдив",
            "Enrollment at Champion | English for Students in Plovdiv",
            lang,
        )
        desc = t(
            "Запишете детето си за курс по английски в Чемпиън, Пловдив. Изпратете запитване онлайн или се обадете на 0885 712 048.",
            "Enroll your child in an English course at Champion, Plovdiv. Send an inquiry online or call 0885 712 048.",
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
    privacy_url = url_for(lang, "/privacy-policy/", "/en/privacy-policy/")

    form = f"""<form class="form js-form" novalidate>
      <div class="form-success" role="status">
        {t("Благодарим ви! Съобщението е получено — ще се свържем с вас скоро.", "Thank you! Your message has been received — we will get back to you soon.", lang)}
      </div>
      <div class="form-fields stack">
        <input type="text" name="website" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="field">
          <label for="cName">{t("Име", "Name", lang)} *</label>
          <input type="text" id="cName" name="name" required autocomplete="name">
          <span class="field-error">{t("Моля, въведете име.", "Please enter a name.", lang)}</span>
        </div>
        <div class="form-row form-row-2">
          <div class="field">
            <label for="cPhone">{t("Телефон", "Phone", lang)}</label>
            <input type="tel" id="cPhone" name="phone" autocomplete="tel">
          </div>
          <div class="field">
            <label for="cEmail">Email</label>
            <input type="email" id="cEmail" name="email" autocomplete="email">
          </div>
        </div>
        <p class="hint">{t("Моля, посочете поне един начин за връзка — телефон или имейл.", "Please provide at least one way to reach you — phone or email.", lang)}</p>
        <div class="field">
          <label for="cMessage">{t("Съобщение", "Message", lang)} *</label>
          <textarea id="cMessage" name="message" rows="5" required></textarea>
          <span class="field-error">{t("Моля, въведете съобщение.", "Please enter a message.", lang)}</span>
        </div>
        <label class="checkbox-row">
          <input type="checkbox" name="consent" required>
          <span class="consent">{t('Съгласен/на съм личните ми данни да бъдат използвани от Чемпиън единствено за отговор на това запитване, съгласно', 'I agree that my personal data will be used by Champion solely to respond to this inquiry, in accordance with the', lang)}
          <a href="{privacy_url}">{t("Политиката за поверителност", "Privacy Policy", lang)}</a>. *</span>
        </label>
        <button type="submit" class="btn btn-primary btn-lg btn-block">{t("Изпрати съобщение", "Send message", lang)}</button>
      </div>
    </form>"""

    return f"""<section class="section-tight">
      <div class="container">
        <p class="eyebrow">{t("Контакти", "Contact", lang)}</p>
        <h1 class="section-title">{t("Свържете се с Чемпиън", "Get in touch with Champion", lang)}</h1>
        <p class="section-lead">{t(
          "Пишете ни, обадете се или ни последвайте в Instagram. С удоволствие ще отговорим на въпросите ви за обучението по английски.",
          "Write to us, call, or follow us on Instagram. We are happy to answer your questions about English courses.",
          lang)}</p>
      </div>
    </section>
    <section class="section">
      <div class="container grid grid-2">
        <div>
          <div class="contact-list">
            <div class="contact-row"><span class="ic" aria-hidden="true">📍</span><div><div class="lbl">{t("Адрес", "Address", lang)}</div><span class="val">{t(SITE['address_bg'], SITE['address_en'], lang)}</span></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">📞</span><div><div class="lbl">{t("Телефон", "Phone", lang)}</div><a href="{SITE['phone_href']}">{SITE['phone_display']}</a></div></div>
            <div class="contact-row"><span class="ic" aria-hidden="true">📷</span><div><div class="lbl">Instagram</div><a href="{SITE['instagram_url']}" rel="noopener" target="_blank">{SITE['instagram_handle']}</a></div></div>
          </div>
          <div class="map-frame" style="margin-top:24px">
            <iframe src="{SITE['maps_embed_src']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="{t('Карта с местоположението на Чемпиън', 'Map showing the Champion location', lang)}"></iframe>
          </div>
          <p style="margin-top:10px"><a class="btn-ghost" href="{SITE['maps_link']}" rel="noopener" target="_blank">{t("Отвори в Google Maps ↗", "Open in Google Maps ↗", lang)}</a></p>
          <p class="text-muted" style="margin-top:16px;font-size:14.5px">{t(
            'Искате да запишете ученик? Разгледайте страница', 'Want to enroll a student? Visit the', lang)}
            <a href="{enroll_url}" class="btn-ghost">{t("„Записване“", "Enrollment page", lang)}</a>.</p>
        </div>
        <div class="card" style="padding:30px">{form}</div>
      </div>
    </section>"""


def build_contacts():
    for lang, path, alt in [("bg", "/contacts/", "/en/contacts/"), ("en", "/en/contacts/", "/contacts/")]:
        title = t(
            "Контакти | Чемпиън – английски език в Пловдив",
            "Contact | Champion – English Language School in Plovdiv",
            lang,
        )
        desc = t(
            f"Свържете се с Чемпиън в Пловдив: {SITE['address_bg']}, тел. {SITE['phone_display']}, Instagram {SITE['instagram_handle']}.",
            f"Contact Champion in Plovdiv: {SITE['address_en']}, phone {SITE['phone_display']}, Instagram {SITE['instagram_handle']}.",
            lang,
        )
        breadcrumb = [
            (t("Начало", "Home", lang), "/" if lang == "bg" else "/en/"),
            (t("Контакти", "Contact", lang), path),
        ]
        html = wrap_page(lang, "contacts", path, alt, title, desc, contacts_main(lang), [], breadcrumb_items=breadcrumb)
        write_file(path + "index.html", html)


def legal_main(lang, kind):
    editable = t("Редактируемо", "Editable", lang)
    privacy_url = url_for(lang, "/privacy-policy/", "/en/privacy-policy/")
    if kind == "privacy":
        title = t("Политика за поверителност", "Privacy Policy", lang)
        body = f"""
        <p>{t(
          "Чемпиън събира лични данни (име на родител, име на ученик, клас, телефон, имейл и съобщение) единствено чрез формите за записване и контакт на този сайт, с цел да отговори на запитване или да организира записване за обучение по английски език.",
          "Champion collects personal data (parent's name, student's name, grade, phone, email and message) only through this site's enrollment and contact forms, in order to respond to an inquiry or arrange enrollment in an English course.",
          lang)}</p>
        <h2>{t("Администратор на лични данни", "Data controller", lang)}</h2>
        <p><span class="badge badge-placeholder">{editable}</span> {t(
          "[Пълно наименование на дружеството], ЕИК [ЕИК номер], със седалище и адрес на управление: [адрес на управление на дружеството].",
          "[Company legal name], company ID [registration number], registered office: [registered address].",
          lang)}</p>
        <h2>{t("Какви данни обработваме", "What data we process", lang)}</h2>
        <p>{t("Име на родител/настойник, име на ученик, клас, телефон, имейл адрес и съдържанието на изпратеното съобщение.", "Parent/guardian name, student name, grade, phone number, email address, and the content of the message sent.", lang)}</p>
        <h2>{t("Цел на обработването", "Purpose of processing", lang)}</h2>
        <p>{t("Данните се използват единствено за връзка с вас във връзка с записване за обучение или отговор на запитване. Не се използват за маркетингови цели без изрично съгласие.", "The data is used solely to contact you regarding enrollment or to respond to an inquiry. It is not used for marketing purposes without explicit consent.", lang)}</p>
        <h2>{t("Съхранение", "Retention", lang)}</h2>
        <p><span class="badge badge-placeholder">{editable}</span> {t("Срокът на съхранение на данните предстои да бъде определен и допълнен тук.", "The data retention period is to be determined and added here.", lang)}</p>
        <h2>{t("Вашите права", "Your rights", lang)}</h2>
        <p>{t("Съгласно приложимото законодателство за защита на личните данни имате право на достъп, коригиране, изтриване и възражение срещу обработването на личните ви данни. За да упражните тези права, свържете се с нас на", "Under applicable data protection law, you have the right to access, correct, delete, and object to the processing of your personal data. To exercise these rights, contact us at", lang)}
        <a href="{SITE['phone_href']}">{SITE['phone_display']}</a>.</p>
        <h2>{t("Бисквитки", "Cookies", lang)}</h2>
        <p>{t("Информация за използваните бисквитки ще намерите в", "Information about the cookies used can be found in our", lang)}
        <a href="{url_for(lang, '/cookie-policy/', '/en/cookie-policy/')}">{t("Политиката за бисквитки", "Cookie Policy", lang)}</a>.</p>
        """
    else:
        title = t("Политика за бисквитки", "Cookie Policy", lang)
        body = f"""
        <p>{t(
          "Уебсайтът на Чемпиън понастоящем не използва аналитични, рекламни или маркетингови бисквитки. Използват се единствено технически необходими механизми на браузъра (например запомняне на избрания език), без които определени функции на сайта не биха работили.",
          "The Champion website does not currently use analytics, advertising or marketing cookies. Only strictly necessary browser mechanisms are used (for example, remembering a language choice), without which certain site features would not work.",
          lang)}</p>
        <p>{t("Ако в бъдеще добавим аналитични или маркетингови бисквитки, тази страница ще бъде актуализирана и, при необходимост, ще поискаме съгласието ви.", "If we add analytics or marketing cookies in the future, this page will be updated and, where required, we will ask for your consent.", lang)}</p>
        <h2>{t("Как да управлявате бисквитките", "How to manage cookies", lang)}</h2>
        <p>{t("Повечето браузъри позволяват управление и изтриване на бисквитки чрез настройките си. Ограничаването на бисквитките може да засегне функционалността на някои сайтове.", "Most browsers allow you to manage and delete cookies through their settings. Restricting cookies may affect the functionality of some websites.", lang)}</p>
        <p>{t("За въпроси относно тази политика, свържете се с нас на", "For questions about this policy, contact us at", lang)}
        <a href="{SITE['phone_href']}">{SITE['phone_display']}</a>.</p>
        <p><span class="badge badge-placeholder">{editable}</span> {t("Пълното правно наименование на дружеството-администратор предстои да бъде добавено тук, вижте", "The full legal name of the controlling company is to be added here, see the", lang)}
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
         t("Политика за поверителност | Чемпиън", "Privacy Policy | Champion", "bg"),
         "Политика за поверителност | Чемпиън", "Privacy Policy | Champion",
         "Как Чемпиън обработва личните данни, изпратени чрез формите за записване и контакт на сайта.",
         "How Champion processes personal data submitted through the site's enrollment and contact forms."),
        ("cookie", "/cookie-policy/", "/en/cookie-policy/",
         None,
         "Политика за бисквитки | Чемпиън", "Cookie Policy | Champion",
         "Информация за бисквитките, използвани на уебсайта на Чемпиън.",
         "Information about the cookies used on the Champion website."),
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
            "Английски език за деца и ученици в Пловдив | Чемпиън",
            "English Courses for Children & Students in Plovdiv | Champion",
            lang,
        )
        desc = t(
            "Чемпиън е училище по английски език в Пловдив за ученици от 2. до 12. клас. Направете безплатен тест за ниво и запишете детето си в подходяща група.",
            "Champion is an English language school in Plovdiv for students in grades 2-12. Take a free level test and enroll your child in the right group.",
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


def build_robots():
    content = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
    write_file("/robots.txt", content)


def build_sitemap():
    urls = []
    for bg_path, en_path in PAGE_PAIRS:
        for path, alt in [(bg_path, en_path), (en_path, bg_path)]:
            urls.append(f"""  <url>
    <loc>{DOMAIN}{path}</loc>
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


def main():
    build_home()
    build_test()
    build_schedule()
    build_enrollment()
    build_contacts()
    build_legal()
    build_robots()
    build_sitemap()
    print("\nDone.")


if __name__ == "__main__":
    main()
