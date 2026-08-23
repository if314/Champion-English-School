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
    "email": "teodora.champion.teaching@gmail.com",
    "facebook_url": "https://www.facebook.com/profile.php?id=61592303458887",
    # Exact pin at the school entrance, supplied directly (not geocoded --
    # бул. „6-ти Септември“ spans several disconnected segments across
    # Plovdiv and free geocoders could not resolve house #145 reliably).
    "latitude": 42.150358,
    "longitude": 24.743059,
    "maps_embed_src": "https://www.google.com/maps?q=42.150358,24.743059&output=embed",
    "maps_link": "https://www.google.com/maps/search/?api=1&query=42.150358,24.743059",
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
     "Обадете се на 0885 712 048 или ни пишете в Instagram @champion.english.plovdiv. Ще се свържем с вас, за да потвърдим група и час."),
    ("Какъв е графикът на групите?",
     "Дните и часовете по клас и ниво са публикувани на страница „График и цени“. Повечето групи вече имат определен ден и час; отделни нива предстои да се уточнят."),
    ("Какви са цените за обучение?",
     "Цената е 329 евро за учебен срок от 120 учебни часа, с 10% отстъпка за второ дете от семейството. Подробности ще намерите на страница „График и цени“."),
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
     "Call us at 0885 712 048 or message us on Instagram @champion.english.plovdiv. We will contact you to confirm the group and schedule."),
    ("What is the groups' schedule?",
     "Days and times by grade and level are published on the “Schedule & Prices” page. Most groups already have a set day and time; a few levels are still to be confirmed."),
    ("What are the prices?",
     "The price is EUR 329 per school term of 120 teaching hours, with a 10% discount for a second child from the same family. See the “Schedule & Prices” page for details."),
]
