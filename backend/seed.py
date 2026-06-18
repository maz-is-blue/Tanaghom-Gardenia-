"""
Seed MongoDB with all Tanaghom Gardenia content.

Idempotent: each collection is cleared and repopulated. Run once after the
database is up:

    python seed.py
"""
import os

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "tanaghom_gardenia")


SITE = {
    "_id": "settings",
    "brand_en": "Tanaghom Gardenia",
    "brand_ar": "تناغم وغاردينيا",
    "brand_word_a": "Tanaghom",
    "brand_word_b": "Gardenia",
    "founded_year": "2019",
    "tagline_en": "Where voices become music.",
    "tagline_ar": "حيث تصبح الأصوات موسيقى",
    "footer_blurb": "A non-profit choral society of two ensembles, founded in Beirut in 2019.",
    "address_line1": "Rehearsal Hall · Achrafieh",
    "address_line2": "Beirut, Lebanon",
    "email": "hello@tanaghom-gardenia.org",
    "press_email": "press@tanaghom-gardenia.org",
    "phone": "+961 1 234 567",
    "social_instagram": "#",
    "social_facebook": "#",
    "social_youtube": "#",
    "copyright_year": "2026",
    "copyright_ar": "© ٢٠٢٦ جمعية تناغم وغاردينيا الكورالية",
    "home_stats": [
        {"value": 40, "format": "+", "label": "Active Singers"},
        {"value": 6, "format": "", "label": "Seasons"},
        {"value": 128, "format": "", "label": "Performances"},
    ],
    "about_stats": [
        {"value": 40, "format": "+", "label": "Active Singers"},
        {"value": 128, "format": "", "label": "Performances"},
        {"value": 7, "format": "", "label": "Commissions"},
        {"value": 6, "format": "", "label": "Partner Schools"},
    ],
}


EVENTS = [
    {"order": 1, "day": "24", "month": "May 2026", "title_en": "Songs of the Levant", "title_ar": "أغاني المشرق", "time": "8:00 PM", "venue": "Al-Madina Hall", "url": "#"},
    {"order": 2, "day": "12", "month": "Jun 2026", "title_en": "Vespers Under the Vines", "title_ar": "صلوات تحت الكروم", "time": "7:30 PM", "venue": "Beit Mery Garden", "url": "#"},
    {"order": 3, "day": "03", "month": "Jul 2026", "title_en": "A New Commission · Maalouf", "title_ar": "تكليفٌ جديد · معلوف", "time": "8:30 PM", "venue": "St. Joseph Church", "url": "#"},
    {"order": 4, "day": "18", "month": "Sep 2026", "title_en": "Open Auditions · Fall", "title_ar": "اختبارات قبول · خريف", "time": "All Day", "venue": "Rehearsal Hall", "url": "#"},
]


CHOIRS = [
    {
        "_id": "gardenia",
        "slug": "gardenia",
        "order": 1,
        "name_en": "Gardenia",
        "name_ar": "غاردينيا",
        # home panel
        "label_en": "Mixed Voices",
        "label_ar": "٢٤ صوتاً",
        "summary": "A mixed ensemble drawing on the great choral tradition — from Renaissance polyphony to contemporary Arab composers. Lush, layered, unmistakably alive.",
        "parts_count": "4",
        # choirs detail page
        "detail_label_en": "Mixed Choir",
        "count_ar": "٢٤ صوتاً",
        "desc": "A mixed choir of twenty-four voices — patient, generous, working in the great choral tradition from Renaissance polyphony to the contemporary Arab repertoire.",
        "voices": "24",
        "parts": "SATB",
        "conductor_label": "Conductor",
        "conductor": "M. Khoury",
        "rehearses": "Tue · Thu",
        "season": "5 concerts",
        "founded": "2019",
        "voice_parts_title_en": "Four parts, one room",
        "voice_parts_title_ar": "أربعة أصوات",
        "voice_parts": [
            {"glyph": "𝄞", "name_en": "Soprano", "name_ar": "سوبرانو", "count": "7"},
            {"glyph": "𝄞", "name_en": "Alto", "name_ar": "ألتو", "count": "6"},
            {"glyph": "𝄢", "name_en": "Tenor", "name_ar": "تينور", "count": "5"},
            {"glyph": "𝄢", "name_en": "Bass", "name_ar": "باص", "count": "6"},
        ],
        "player": {
            "label": "Live · Spring Concert · 2025",
            "title": "Sicut cervus — desiderat fontes",
            "composer": "Giovanni Pierluigi da Palestrina · 1604",
            "duration": "4:32",
        },
        "voicemix": {
            "title": "Sicut cervus — voice mix",
            "rows": [
                {"label": "Soprano", "color": "#A8B8A2"},
                {"label": "Alto", "color": "#F5D000"},
                {"label": "Tenor", "color": "#A8B8A2"},
                {"label": "Bass", "color": "#F5D000"},
            ],
        },
        "repertoire": [
            {"title": "Sicut cervus", "composer": "Palestrina", "year": "1604"},
            {"title": "Ave verum corpus", "composer": "W. A. Mozart", "year": "1791"},
            {"title": "Three Adonis Poems", "composer": "Layla Saade · commissioned", "year": "2022"},
            {"title": "Os justi", "composer": "Anton Bruckner", "year": "1879"},
            {"title": "Five Songs from the Levant", "composer": "trad. arr. M. Khoury", "year": "2024"},
            {"title": "There is sweet music here", "composer": "Edward Elgar", "year": "1907"},
            {"title": "Šestina (Six Songs of Quiet)", "composer": "contemporary, premiere", "year": "2026"},
        ],
        "audition": {
            "heading_html": 'Open auditions <em style="font-style: italic; color: var(--gold);">twice a year</em>',
            "heading_ar": "اختبارات قبول",
            "body": "Bring a prepared piece — anything you love, in any language. We hold open auditions every September and February. No prior choral experience required, only a steady ear and a willingness to learn.",
            "dates": [
                {"when": "18 Sep 2026", "where": "Fall Round"},
                {"when": "14 Feb 2027", "where": "Spring Round"},
            ],
            "cta_label": "Request Audition",
        },
    },
    {
        "_id": "tanaghom",
        "slug": "tanaghom",
        "order": 2,
        "name_en": "Tanaghom",
        "name_ar": "تناغم",
        "label_en": "Chamber Choir",
        "label_ar": "١٦ صوتاً",
        "summary": "An intimate chamber choir specializing in Arabic art-song, sacred repertoire, and intricate harmonies that turn small rooms into cathedrals.",
        "parts_count": "8",
        "detail_label_en": "Chamber Choir",
        "count_ar": "١٦ صوتاً",
        "desc": "An intimate chamber choir of sixteen voices specializing in Arabic art-song, sacred repertoire of the Levant, and intricate harmonies that turn small rooms into cathedrals.",
        "voices": "16",
        "parts": "SSAATTBB",
        "conductor_label": "Choirmaster",
        "conductor": "R. Salameh",
        "rehearses": "Wed · Fri",
        "season": "4 concerts",
        "founded": "2021",
        "voice_parts_title_en": "Divisi · eight parts",
        "voice_parts_title_ar": "ثمانية أصوات",
        "voice_parts": [
            {"glyph": "𝄞", "name_en": "Soprano I / II", "name_ar": "سوبرانو", "count": "4"},
            {"glyph": "𝄞", "name_en": "Alto I / II", "name_ar": "ألتو", "count": "4"},
            {"glyph": "𝄢", "name_en": "Tenor I / II", "name_ar": "تينور", "count": "4"},
            {"glyph": "𝄢", "name_en": "Bass I / II", "name_ar": "باص", "count": "4"},
        ],
        "player": {
            "label": "Live · Winter Vespers · 2025",
            "title": "يا أمّ الله — Ya umm Allah",
            "composer": "trad. Maronite · arr. Rami Salameh",
            "duration": "3:48",
        },
        "voicemix": None,  # Tanaghom has no voice-mix block
        "repertoire": [
            {"title": "Ya umm Allah · يا أمّ الله", "composer": "trad. Maronite arr. R. Salameh", "year": "2022"},
            {"title": "Three Adonis Poems · for double choir", "composer": "Layla Saade · commissioned", "year": "2022"},
            {"title": "Tantum Ergo", "composer": "Maurice Duruflé", "year": "1960"},
            {"title": "Wahdaki · وحدكِ", "composer": "Wadih el-Safi arr. R. Salameh", "year": "2023"},
            {"title": "Bogoroditse Devo", "composer": "Sergei Rachmaninoff", "year": "1915"},
            {"title": "Settings of Mahmoud Darwish", "composer": "Hany Maalouf · premiere", "year": "2026"},
        ],
        "audition": {
            "heading_html": 'By invitation, then <em style="font-style: italic;">audition</em>',
            "heading_ar": "دعوة، ثم اختبار",
            "body": "Tanaghom recruits primarily from Gardenia after a full season of singing together. We hold an additional small audition each spring for voices with significant prior choral experience and a reading-level command of Arabic diction.",
            "dates": [
                {"when": "21 Mar 2027", "where": "Spring Round"},
                {"when": "By Invitation", "where": "From Gardenia"},
            ],
            "cta_label": "Express Interest",
        },
    },
]


VALUES = [
    {"order": 1, "title_en": "Patience", "title_ar": "صبر", "body": "A choir is built one rehearsal at a time. We trust the long, slow work of listening and adjusting."},
    {"order": 2, "title_en": "Two tongues", "title_ar": "لسانان", "body": "Arabic and the wider repertoire share equal weight in everything we program. Neither is a footnote."},
    {"order": 3, "title_en": "Open doors", "title_ar": "أبواب مفتوحة", "body": "We audition twice a year and never charge a fee. If you can carry a tune, we'll teach you the rest."},
    {"order": 4, "title_en": "New work", "title_ar": "أعمال جديدة", "body": "Every season we commission at least one new piece from a regional composer — alive, today, here."},
]


TIMELINE = [
    {"order": 1, "year": "2019", "title_en": "A small circle begins", "title_ar": "بداية صغيرة", "body": "Eighteen singers gather in a borrowed church basement in Achrafieh. Our first conductor, Maya Khoury, leads the first rehearsal — a Palestrina motet, sung badly and joyfully.", "active": False},
    {"order": 2, "year": "2020", "title_en": "First public concert", "title_ar": "الحفل الأوّل", "body": '"Songs for a Difficult Year" — performed outdoors, in a private garden, four months after the August explosion. Two hundred guests, one rehearsal-less programme, the beginnings of an audience.', "active": False},
    {"order": 3, "year": "2021", "title_en": "Tanaghom is born", "title_ar": "ولادة تناغم", "body": "A chamber group splits from the main ensemble to focus on Arabic art-song and sacred repertoire. Sixteen voices, the same hall, a separate mission.", "active": False},
    {"order": 4, "year": "2022", "title_en": "First commission", "title_ar": "التكليف الأول", "body": "We commission Layla Saade to write a setting of three Adonis poems for double choir. The piece tours four cities; the recording reaches forty thousand listeners.", "active": False},
    {"order": 5, "year": "2023", "title_en": "Schools programme", "title_ar": "برنامج المدارس", "body": "Our outreach programme begins with three Beirut schools and forty-two children. Today, six schools and over a hundred children sing with us each season.", "active": False},
    {"order": 6, "year": "2024", "title_en": "The new rehearsal hall", "title_ar": "قاعتنا الجديدة", "body": "After two years of fundraising, we move into a permanent rehearsal hall — sprung floors, real acoustics, a piano that holds its tune. The first home we have called our own.", "active": False},
    {"order": 7, "year": "2026", "title_en": "Season seven", "title_ar": "الموسم السابع", "body": "Forty active singers, two ensembles, a five-concert main season and a new commission from Hany Maalouf premiering at St. Joseph Church this July.", "active": True},
]


LEADERSHIP = [
    {"order": 1, "initials": "MK", "role": "Artistic Director", "name_en": "Maya Khoury", "name_ar": "مايا خوري", "bio": "Founding conductor. Trained at the Lebanese Conservatoire and the Hochschule für Musik in Stuttgart. Conducts both ensembles."},
    {"order": 2, "initials": "RS", "role": "Choirmaster · Tanaghom", "name_en": "Rami Salameh", "name_ar": "رامي سلامة", "bio": "Specialist in Arabic sacred repertoire and Levantine art-song. Joined the society in 2021 to lead the founding of Tanaghom."},
    {"order": 3, "initials": "NH", "role": "Executive Director", "name_en": "Nour Hadad", "name_ar": "نور حداد", "bio": "Runs everything that isn't singing — programming, finance, our schools partnership, and the long list of people who lend us their time."},
]


GALLERY = [
    {"id": 1, "order": 1, "title": "Songs of the Levant", "date": "May 2025", "venue": "Al-Madina Hall", "ensemble": "gardenia", "type": "concert", "year": "2025", "size": "wide", "palette": ["#2a3d28", "#8DA086", "#F5D000"]},
    {"id": 2, "order": 2, "title": "Winter Vespers", "date": "Dec 2024", "venue": "St. Joseph Church", "ensemble": "tanaghom", "type": "concert", "year": "2024", "size": "tall", "palette": ["#1a1a1a", "#3a3414", "#F5D000"]},
    {"id": 3, "order": 3, "title": "Open Rehearsal", "date": "Mar 2025", "venue": "Rehearsal Hall", "ensemble": "gardenia", "type": "rehearsal", "year": "2025", "size": "square", "palette": ["#4a4838", "#A8B8A2", "#FFFFFF"]},
    {"id": 4, "order": 4, "title": "Three Adonis Poems", "date": "Oct 2024", "venue": "Sursock Museum", "ensemble": "tanaghom", "type": "concert", "year": "2024", "size": "normal", "palette": ["#1a1a1a", "#F5D000", "#8DA086"]},
    {"id": 5, "order": 5, "title": "Garden Recital", "date": "Jun 2024", "venue": "Beit Mery", "ensemble": "gardenia", "type": "concert", "year": "2024", "size": "wide", "palette": ["#8DA086", "#2a3d28", "#FFFFFF"]},
    {"id": 6, "order": 6, "title": "Schools Programme", "date": "Apr 2025", "venue": "Rehearsal Hall", "ensemble": "gardenia", "type": "rehearsal", "year": "2025", "size": "normal", "palette": ["#F5D000", "#1a1a1a", "#A8B8A2"]},
    {"id": 7, "order": 7, "title": "Maronite Sacred Hymns", "date": "Nov 2023", "venue": "Bkerké", "ensemble": "tanaghom", "type": "concert", "year": "2023", "size": "normal", "palette": ["#1a1a1a", "#4a4838", "#F5D000"]},
    {"id": 8, "order": 8, "title": "Sectional · Sopranos", "date": "Feb 2025", "venue": "Rehearsal Hall", "ensemble": "gardenia", "type": "rehearsal", "year": "2025", "size": "square", "palette": ["#A8B8A2", "#F5D000", "#1a1a1a"]},
    {"id": 9, "order": 9, "title": "Layla Saade Premiere", "date": "Sep 2024", "venue": "Al-Madina Hall", "ensemble": "gardenia", "type": "concert", "year": "2024", "size": "tall", "palette": ["#2a3d28", "#1a1a1a", "#F5D000"]},
    {"id": 10, "order": 10, "title": "Tuning the Hall", "date": "Jan 2024", "venue": "Rehearsal Hall", "ensemble": "tanaghom", "type": "rehearsal", "year": "2024", "size": "normal", "palette": ["#3a3414", "#1a1a1a", "#A8B8A2"]},
    {"id": 11, "order": 11, "title": "Songs for a Difficult Year", "date": "Aug 2023", "venue": "Private Garden", "ensemble": "gardenia", "type": "concert", "year": "2023", "size": "wide", "palette": ["#4a4838", "#A8B8A2", "#FFFFFF"]},
    {"id": 12, "order": 12, "title": "Wahdaki · وحدكِ", "date": "Mar 2024", "venue": "Sursock Museum", "ensemble": "tanaghom", "type": "concert", "year": "2024", "size": "normal", "palette": ["#1a1a1a", "#3a3414", "#F5D000"]},
    {"id": 13, "order": 13, "title": "Section Read-Through", "date": "Sep 2023", "venue": "Rehearsal Hall", "ensemble": "tanaghom", "type": "rehearsal", "year": "2023", "size": "square", "palette": ["#1a1a1a", "#A8B8A2", "#F5D000"]},
    {"id": 14, "order": 14, "title": "Bruckner · Os justi", "date": "Apr 2024", "venue": "St. Joseph Church", "ensemble": "gardenia", "type": "concert", "year": "2024", "size": "normal", "palette": ["#2a3d28", "#1a1a1a", "#FFFFFF"]},
]


def main():
    db = MongoClient(MONGO_URI)[MONGO_DB]

    db.site.replace_one({"_id": "settings"}, SITE, upsert=True)

    db.events.delete_many({})
    db.events.insert_many(EVENTS)

    db.choirs.delete_many({})
    db.choirs.insert_many(CHOIRS)

    db.values.delete_many({})
    db.values.insert_many(VALUES)

    db.timeline.delete_many({})
    db.timeline.insert_many(TIMELINE)

    db.leadership.delete_many({})
    db.leadership.insert_many(LEADERSHIP)

    db.gallery.delete_many({})
    db.gallery.insert_many(GALLERY)

    # Helpful indexes
    db.submissions.create_index("created_at")
    db.gallery.create_index("order")

    print("Seeded:")
    for c in ("site", "events", "choirs", "values", "timeline", "leadership", "gallery"):
        print(f"  {c}: {db[c].count_documents({})}")


if __name__ == "__main__":
    main()
