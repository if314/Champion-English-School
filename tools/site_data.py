# -*- coding: utf-8 -*-
"""
Content source for the Champion School / Училище Чемпиън website.
All factual claims here are limited to information explicitly supplied:
school name, grade range (2nd-12th), Plovdiv address, phone, Instagram.
Everything else (prices, schedules, legal registration numbers) is a
clearly-labelled editable placeholder.
"""

DOMAIN = "https://championenglishplovdiv.com"

SITE = {
    "name_bg": "Училище Чемпиън",
    "name_en": "Champion School",
    "full_name_bg": "Английско езиково училище Чемпиън",
    "full_name_en": "Champion English Language School",
    "tagline_bg": "Английски за ученици от 2. до 12. клас",
    "tagline_en": "English for students in grades 2-12",
    "phone_display": "0885 712 048",
    "phone_href": "tel:+359885712048",
    "address_bg": "бул. „6-ти Септември“ 145, Пловдив",
    "address_en": "145 Shesti Septemvri Blvd, Plovdiv",
    "address_street_bg": "бул. „6-ти Септември“ 145",
    "address_street_en": "145 Shesti Septemvri Blvd",
    "locality_bg": "Пловдив",
    "locality_en": "Plovdiv",
    "country": "BG",
    "instagram_handle": "@champion.english.plovdiv",
    "instagram_url": "https://www.instagram.com/champion.english.plovdiv/",
    "maps_embed_src": "https://www.google.com/maps?q=%D0%B1%D1%83%D0%BB.%20%226-%D1%82%D0%B8%20%D0%A1%D0%B5%D0%BF%D1%82%D0%B5%D0%BC%D0%B2%D1%80%D0%B8%22%20145%2C%20%D0%9F%D0%BB%D0%BE%D0%B2%D0%B4%D0%B8%D0%B2&output=embed",
    "maps_link": "https://www.google.com/maps/search/?api=1&query=%D0%B1%D1%83%D0%BB.+%226-%D1%82%D0%B8+%D0%A1%D0%B5%D0%BF%D1%82%D0%B5%D0%BC%D0%B2%D1%80%D0%B8%22+145%2C+%D0%9F%D0%BB%D0%BE%D0%B2%D0%B4%D0%B8%D0%B2",
    # Registered company details (legal entity operating the school) --
    # used in the footer legal note and the privacy policy's "data
    # controller" section. Distinct from the teaching address above,
    # which is where classes are actually held.
    "legal_name": "Училище Чемпиън ЕООД",
    "legal_eik": "208821346",
    "legal_address_bg": "гр. Пловдив, ул. „Иглика“ 4",
    "legal_address_en": "4 Iglika St, Plovdiv, Bulgaria",
}

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
NAV_BG = [
    ("home", "Начало", "/"),
    ("about", "За Училище Чемпиън", "/#about"),
    ("test", "Тест за ниво", "/test/"),
    ("schedule", "График и цени", "/schedule-prices/"),
    ("enrollment", "Записване", "/enrollment/"),
    ("contacts", "Контакти", "/contacts/"),
]
NAV_EN = [
    ("home", "Home", "/en/"),
    ("about", "About Champion School", "/en/#about"),
    ("test", "Level Test", "/en/test/"),
    ("schedule", "Schedule & Prices", "/en/schedule-prices/"),
    ("enrollment", "Enrollment", "/en/enrollment/"),
    ("contacts", "Contact", "/en/contacts/"),
]

FOOTER_LEGAL_BG = [
    ("Политика за поверителност", "/privacy-policy/"),
    ("Политика за бисквитки", "/cookie-policy/"),
]
FOOTER_LEGAL_EN = [
    ("Privacy Policy", "/en/privacy-policy/"),
    ("Cookie Policy", "/en/cookie-policy/"),
]

# ---------------------------------------------------------------------------
# Reference levels shown on the level-test page (not tied to a scored quiz --
# the test itself is held in person at the school).
# ---------------------------------------------------------------------------
LEVELS_BG = [
    {"name": "Начинаещи", "cefr": "Ориентировъчно ниво A1 · Beginner",
     "description": "Ученикът прави първи стъпки в английския език. Препоръчваме групи с фокус върху основна лексика, произношение и прости изречения."},
    {"name": "Елементарно ниво", "cefr": "Ориентировъчно ниво A1–A2 · Elementary",
     "description": "Ученикът разбира и използва познати думи и изрази в прости ситуации. Подходящи са групи, изграждащи по-широк речников запас и основна граматика."},
    {"name": "Предсредно ниво", "cefr": "Ориентировъчно ниво A2–B1 · Pre-Intermediate",
     "description": "Ученикът се справя с познати теми и прости разговори. Препоръчваме групи с фокус върху разширяване на граматиката и увереност в говоренето."},
    {"name": "Средно ниво", "cefr": "Ориентировъчно ниво B1–B2 · Intermediate",
     "description": "Ученикът разбира и изразява мнение по познати и по-абстрактни теми. Подходящи са групи с по-задълбочена граматика и практика в говоренето и писането."},
    {"name": "Средно напреднало ниво", "cefr": "Ориентировъчно ниво B2 · Upper-Intermediate",
     "description": "Ученикът общува свободно на широк кръг теми с добра граматическа точност. Препоръчваме групи с фокус върху академична лексика и по-сложни текстове."},
    {"name": "Напреднало ниво", "cefr": "Ориентировъчно ниво C1 · Advanced",
     "description": "Ученикът владее английски на високо ниво, включително по-сложни граматически структури и нюанси в изразяването. Подходящи са напреднали групи с академичен и практически фокус."},
]
LEVELS_EN = [
    {"name": "Beginner", "cefr": "Approximate level A1 · Beginner",
     "description": "The student is taking their first steps in English. We recommend groups focused on core vocabulary, pronunciation and simple sentences."},
    {"name": "Elementary", "cefr": "Approximate level A1–A2 · Elementary",
     "description": "The student understands and uses familiar words and phrases in simple situations. Groups that build a wider vocabulary and basic grammar are a good fit."},
    {"name": "Pre-Intermediate", "cefr": "Approximate level A2–B1 · Pre-Intermediate",
     "description": "The student can handle familiar topics and simple conversations. We recommend groups that expand grammar and build speaking confidence."},
    {"name": "Intermediate", "cefr": "Approximate level B1–B2 · Intermediate",
     "description": "The student understands and expresses opinions on familiar and some abstract topics. Groups with deeper grammar and more speaking and writing practice fit well."},
    {"name": "Upper-Intermediate", "cefr": "Approximate level B2 · Upper-Intermediate",
     "description": "The student communicates fluently on a wide range of topics with good grammatical accuracy. We recommend groups focused on academic vocabulary and more complex texts."},
    {"name": "Advanced", "cefr": "Approximate level C1 · Advanced",
     "description": "The student has a strong command of English, including complex grammar and nuanced expression. Advanced groups with an academic and practical focus are suitable."},
]

# ---------------------------------------------------------------------------
# FAQ (shared meaning, localized)
# ---------------------------------------------------------------------------
FAQ_BG = [
    ("За кои класове е подходящо обучението в Училище Чемпиън?",
     "Училище Чемпиън предлага обучение по английски за ученици от 2. до 12. клас, разпределени в групи според клас и ниво на владеене на езика."),
    ("Как се определя нивото на ученика?",
     "Нивото се определя чрез кратък присъствен тест в самото училище — датите и часовете са посочени на страницата „Тест за ниво“, преди да изберете подходяща група."),
    ("Как протича тестът за ниво?",
     "Тестът се провежда на място в училището с личното участие на ученика и отнема около 30 минути. Резултатът ни помага да препоръчаме подходяща група."),
    ("Как да избера подходяща група?",
     "След теста за ниво препоръчваме група според клас и резултат. При записване можем да обсъдим и коригираме избора при нужда."),
    ("Къде се провеждат занятията?",
     "Занятията се провеждат в Пловдив, на бул. „6-ти Септември“ 145."),
    ("Как мога да запиша ученик?",
     "Записването става чрез формата на страница „Записване“ или по телефона на 0885 712 048. Ще се свържем с вас, за да потвърдим група и час."),
    ("Какъв е графикът на групите?",
     "Дните и часовете на групите се уточняват според сформирания състав за текущата учебна година. Общата структура по клас и ниво е показана на страница „График и цени“."),
    ("Какви са цените за обучение?",
     "Цените зависят от групата, нивото и продължителността на курса. Актуална информация ще намерите на страница „График и цени“ или като се свържете с нас."),
]
FAQ_EN = [
    ("Which grades is Champion School suitable for?",
     "Champion School offers English courses for students in grades 2 through 12, grouped by grade and by English level."),
    ("How is a student's level determined?",
     "The level is determined with a short in-person test at the school — dates and times are listed on the “Level Test” page — before choosing a suitable group."),
    ("How does the level test work?",
     "The test takes place at the school with the student attending in person and takes about 30 minutes. The result helps us recommend a suitable group."),
    ("How do I choose the right group?",
     "After the level test we recommend a group based on grade and result. We can discuss and adjust the choice further during enrollment."),
    ("Where are the classes held?",
     "Classes are held in Plovdiv, at 145 Shesti Septemvri Blvd."),
    ("How can I enroll a student?",
     "Enrollment is done through the form on the “Enrollment” page or by phone at 0885 712 048. We will contact you to confirm the group and schedule."),
    ("What is the groups' schedule?",
     "Group days and times are confirmed once each group is formed for the current school year. The general structure by grade and level is shown on the “Schedule & Prices” page."),
    ("What are the prices?",
     "Prices depend on the group, level and course duration. Up-to-date information is available on the “Schedule & Prices” page or by contacting us."),
]
