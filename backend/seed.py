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
    "brand_ar": "تناغم غاردينيا",
    "brand_word_a": "Tanaghom",
    "brand_word_b": "Gardenia",
    "founded_year": "2016",
    "tagline_en": "Art is everyone's right.",
    "tagline_ar": "الفن حق الجميع",
    "footer_blurb": "A women-led cultural and civic association founded in Damascus in 2016, using music and art to promote peace, dialogue, and women's empowerment.",
    "address_line1": "Damascus",
    "address_line2": "Syria",
    "email": "hello@tanaghom-gardenia.org",
    "press_email": "press@tanaghom-gardenia.org",
    "phone": "",
    "social_instagram": "#",
    "social_facebook": "#",
    "social_youtube": "#",
    "copyright_year": "2025",
    "copyright_ar": "© ٢٠٢٥ جمعية تناغم غاردينيا",
    "home_stats": [
        {"value": 250, "format": "+", "label": "Youth Trained"},
        {"value": 12, "format": "+", "label": "Concerts in 2025"},
        {"value": 9, "format": "", "label": "Years of Music"},
    ],
    "about_stats": [
        {"value": 250, "format": "+", "label": "Youth Trained"},
        {"value": 12, "format": "+", "label": "Concerts in 2025"},
        {"value": 17, "format": "", "label": "Workshops & Forums"},
        {"value": 4, "format": "", "label": "Major Projects"},
    ],
}


EVENTS = [
    {
        "order": 1,
        "day": "23",
        "month": "Jul 2026",
        "title_en": "Mawaqe' al-Sahab",
        "title_ar": "مواقع السحاب",
        "time": "8:00 PM",
        "venue": "Damascus Opera House · Drama Theater",
        "url": "#",
    },
    {
        "order": 2,
        "day": "",
        "month": "2026",
        "title_en": "Cinema Club",
        "title_ar": "نادي السينما",
        "time": "TBA",
        "venue": "Damascus · To Be Announced",
        "url": "#",
    },
    {
        "order": 3,
        "day": "",
        "month": "Coming Soon",
        "title_en": "Tanaghom Choir Concert",
        "title_ar": "كورال تناغم",
        "time": "TBA",
        "venue": "Damascus",
        "url": "#",
    },
]


CHOIRS = [
    {
        "_id": "gardenia",
        "slug": "gardenia",
        "order": 1,
        "name_en": "Gardenia",
        "name_ar": "غاردينيا",
        # home panel
        "label_en": "Women's Choir",
        "label_ar": "كورال نسائي",
        "summary": "A professional all-female choir founded in Damascus in 2016. Combining traditional Syrian melodies with original compositions, Gardenia uses music as a tool for healing, solidarity, and women's empowerment. Winner of Best Women's Choir at the Dubai Choir Festival 2019.",
        "parts_count": "3",
        # choirs detail page
        "detail_label_en": "Professional Women's Choir",
        "count_ar": "سوبرانو · ميتزو · ألتو",
        "desc": "A professional all-female choir of soprano, mezzo-soprano, and alto voices, bringing together young women musicians and singers from various regions across Syria. Gardenia presents vocal works of the highest standard while building bridges among Syrians through the healing power of music.",
        "voices": "SA",
        "parts": "S · Mz · A",
        "conductor_label": "Co-founders",
        "conductor": "Ghada Harb & Safana Bakleh",
        "rehearses": "Weekly · Damascus",
        "season": "12+ concerts",
        "founded": "2016",
        "voice_parts_title_en": "Three voices, one ensemble",
        "voice_parts_title_ar": "ثلاثة أصوات",
        "voice_parts": [
            {"glyph": "𝄞", "name_en": "Soprano", "name_ar": "سوبرانو", "count": ""},
            {"glyph": "𝄞", "name_en": "Mezzo-soprano", "name_ar": "ميتزو سوبرانو", "count": ""},
            {"glyph": "𝄞", "name_en": "Alto", "name_ar": "ألتو", "count": ""},
        ],
        "player": {
            "label": "Gardenia Choir · Damascus",
            "title": "الليلة الواحدة بعد الألف",
            "composer": "Gardenia Choir · Original Production",
            "duration": "",
        },
        "voicemix": {
            "title": "Voice mix · three parts",
            "rows": [
                {"label": "Soprano", "color": "#A8B8A2"},
                {"label": "Mezzo-soprano", "color": "#F5D000"},
                {"label": "Alto", "color": "#8DA086"},
            ],
        },
        "repertoire": [
            {"title": "زغاريد سورية · Syrian Wedding Folk Songs", "composer": "Traditional Syrian · arr. Gardenia", "year": "2017"},
            {"title": "نساء عشقن الإله · Women Who Adored God", "composer": "Gardenia Choir · original", "year": "2018"},
            {"title": "طقوس سورية · Syrian Rituals", "composer": "Gardenia Choir · original program", "year": "2021"},
            {"title": "الليلة الواحدة بعد الألف · The Thousandth Night", "composer": "Gardenia Choir · musical play", "year": "2023"},
            {"title": "مواقع السحاب", "composer": "Gardenia Choir · current season", "year": "2025"},
        ],
        "audition": {
            "heading_html": 'Join <em style="font-style: italic; color: var(--gold);">Gardenia Choir</em>',
            "heading_ar": "انضمي إلى كورال غاردينيا",
            "body": "Gardenia holds open auditions for female singers from all backgrounds across Syria. We believe that appreciating and participating in the creation of art is a human right — bring your voice and your passion.",
            "dates": [
                {"when": "Contact us", "where": "Auditions open periodically"},
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
        "label_en": "Youth Choir",
        "label_ar": "كورال الشباب",
        "summary": "A Syrian family of 250+ young men and women from all Syrian governorates. Founded in 2019 with UNDP support, Tanaghom uses music and choral singing to build social cohesion and advocate for human rights. Their album 'My Voice and Your Voice' was entirely composed by its members.",
        "parts_count": "4",
        "detail_label_en": "Youth Choir",
        "count_ar": "٢٥٠+ صوت",
        "desc": "A Syrian family that includes young men and women from all walks of life, backgrounds, and regions across Syria. Founded in 2019 in Sahnaya, rural Damascus, in partnership with UNDP, Tanaghom uses music as a tool for positive communication, peacebuilding, and social cohesion.",
        "voices": "250+",
        "parts": "SATB",
        "conductor_label": "Founded with",
        "conductor": "UNDP & Gardenia Choir",
        "rehearses": "Workshops across Syria",
        "season": "Multiple events",
        "founded": "2019",
        "voice_parts_title_en": "Voices from across Syria",
        "voice_parts_title_ar": "أصوات من كل سوريا",
        "voice_parts": [
            {"glyph": "𝄞", "name_en": "Soprano", "name_ar": "سوبرانو", "count": ""},
            {"glyph": "𝄞", "name_en": "Alto", "name_ar": "ألتو", "count": ""},
            {"glyph": "𝄢", "name_en": "Tenor", "name_ar": "تينور", "count": ""},
            {"glyph": "𝄢", "name_en": "Bass", "name_ar": "باص", "count": ""},
        ],
        "player": {
            "label": "صوتي وصوتك · My Voice and Your Voice",
            "title": "صوتي وصوتك",
            "composer": "Tanaghom members · composed & performed by youth",
            "duration": "",
        },
        "voicemix": None,
        "repertoire": [
            {"title": "صوتي وصوتك · My Voice and Your Voice", "composer": "Tanaghom members · album, 7 songs on human rights", "year": "2021"},
            {"title": "15+ original compositions", "composer": "Tanaghom members · social cohesion & peace", "year": "2019–2024"},
            {"title": "Songs for Dialogue", "composer": "Tanaghom members · workshop productions", "year": "2022"},
            {"title": "Voices for Diversity", "composer": "Tanaghom members", "year": "2023"},
        ],
        "audition": {
            "heading_html": 'Join <em style="font-style: italic; color: var(--gold);">Tanaghom Choir</em>',
            "heading_ar": "انضم إلى كورال تناغم",
            "body": "Tanaghom is open to young men and women from across Syria who believe that diversity and dialogue are the key to peace and social cohesion. No prior choral experience required — only your voice and your passion for music.",
            "dates": [
                {"when": "Coming soon", "where": "New phase launching"},
            ],
            "cta_label": "Express Interest",
        },
    },
]


VALUES = [
    {
        "order": 1,
        "title_en": "Artistic Creation",
        "title_ar": "الإبداع الفني",
        "body": "We amplify women's voices and shared values through original compositions, performances, and collaborative works that speak to our time and place — from traditional Syrian melodies to new works addressing human rights.",
    },
    {
        "order": 2,
        "title_en": "Cultural Participation",
        "title_ar": "المشاركة الثقافية",
        "body": "We build community connection and social cohesion by bringing together Syrians from different social, religious, and ethnic backgrounds through the shared act of singing — because music is a bridge among communities.",
    },
    {
        "order": 3,
        "title_en": "Civic Engagement",
        "title_ar": "المشاركة المدنية",
        "body": "Through partnerships and public dialogue, we advocate for justice, equality, and freedom of expression. There is no better tool than art to fight violence and radicalism — and to rebuild trust in post-conflict societies.",
    },
    {
        "order": 4,
        "title_en": "Art as a Human Right",
        "title_ar": "الفن حق الجميع",
        "body": "We work to facilitate access to arts and music especially in marginalized and affected communities. Appreciating and participating in the creation of art is a fundamental human right — for every Syrian.",
    },
]


TIMELINE = [
    {
        "order": 1,
        "year": "2016",
        "title_en": "Gardenia is founded",
        "title_ar": "تأسيس غاردينيا",
        "body": "Musicians Ghada Harb and Safana Bakleh found Gardenia Women Choir in Damascus, in the midst of the Syrian conflict. Choral singing as a peaceful, inclusive form of resistance — women from different backgrounds singing together as a civic act of presence and solidarity.",
        "active": False,
    },
    {
        "order": 2,
        "year": "2017",
        "title_en": "Safeguarding Syrian heritage",
        "title_ar": "صون التراث الموسيقي",
        "body": "Funded by Al Mawred (Cultural Resource), the choir documents tens of Syrian folk songs related to wedding rituals from across the country — preserving Syrian identity through music as a mirror of cultural diversity, and as a tool for civil peace.",
        "active": False,
    },
    {
        "order": 3,
        "year": "2019",
        "title_en": "Tanaghom launches · Dubai award",
        "title_ar": "انطلاق تناغم · جائزة دبي",
        "body": "The Tanaghom project launches in Sahnaya, rural Damascus, in partnership with UNDP — using music to build social cohesion among Syrian youth from all backgrounds. The same year, Gardenia wins Best Regional Choir and Best Women's Choir at the Dubai Choir Festival.",
        "active": False,
    },
    {
        "order": 4,
        "year": "2021",
        "title_en": "250 voices, one Syria",
        "title_ar": "٢٥٠ صوتاً، سوريا واحدة",
        "body": "The Tanaghom project trains over 250 young men and women from across Syrian governorates. Participants compose, arrange, and perform 15+ original songs, producing the album 'My Voice and Your Voice' — seven songs addressing human rights in a youthful, contemporary style.",
        "active": False,
    },
    {
        "order": 5,
        "year": "2023",
        "title_en": "The Thousandth Night",
        "title_ar": "الليلة الواحدة بعد الألف",
        "body": "Gardenia premieres its musical play reimagining the women characters of Arabian Nights — presenting a different perspective that gives voice to women who challenge their own narratives. A landmark in the choir's advocacy for gender equality and women's rights through art.",
        "active": False,
    },
    {
        "order": 6,
        "year": "2024",
        "title_en": "Tanaghom project completes",
        "title_ar": "اختتام مشروع تناغم",
        "body": "The five-year UNDP-funded Syrian Tanaghom project (2019–2024) concludes with 17 workshops and forums, 2 music albums on human rights, and a community of 250+ active members. A new phase is being planned.",
        "active": False,
    },
    {
        "order": 7,
        "year": "2025",
        "title_en": "Music for all Syrians",
        "title_ar": "الموسيقى للجميع",
        "body": "Gardenia becomes the first art troupe to perform publicly after the fall of the regime — 12+ concerts and musical events bringing healing, freedom, and solidarity to Syrians. The repertoire advocates for the forcedly disappeared, freedom, and diversity. A national tour with MARS organization is planned.",
        "active": True,
    },
]


LEADERSHIP = [
    {
        "order": 1,
        "initials": "GH",
        "role": "Co-founder & Musical Director",
        "name_en": "Ghada Harb",
        "name_ar": "غادة حرب",
        "bio": "Co-founder of Gardenia Women Choir. Musician and conductor who has guided Gardenia from its founding in Damascus in 2016, believing that music is a powerful tool for healing and peacebuilding in communities.",
    },
    {
        "order": 2,
        "initials": "SB",
        "role": "Co-founder & Musical Director",
        "name_en": "Safana Bakleh",
        "name_ar": "سفانة بقلة",
        "bio": "Co-founder of Gardenia Women Choir. Musician and advocate who helped build Gardenia into an award-winning ensemble and a vehicle for women's empowerment and civic engagement through art.",
    },
]


GALLERY = [
    {"id": 1, "order": 1, "title": "Mawaqe' al-Sahab · مواقع السحاب", "date": "Jul 2025", "venue": "Damascus Opera House", "ensemble": "gardenia", "type": "concert", "year": "2025", "size": "wide", "palette": ["#2a3d28", "#8DA086", "#F5D000"]},
    {"id": 2, "order": 2, "title": "الليلة الواحدة بعد الألف · The Thousandth Night", "date": "2023", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2023", "size": "tall", "palette": ["#1a1a1a", "#3a3414", "#F5D000"]},
    {"id": 3, "order": 3, "title": "طقوس سورية · Syrian Rituals", "date": "2021", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2021", "size": "square", "palette": ["#4a4838", "#A8B8A2", "#FFFFFF"]},
    {"id": 4, "order": 4, "title": "صوتي وصوتك · My Voice and Your Voice", "date": "2021", "venue": "Sahnaya, Rural Damascus", "ensemble": "tanaghom", "type": "concert", "year": "2021", "size": "normal", "palette": ["#1a1a1a", "#F5D000", "#8DA086"]},
    {"id": 5, "order": 5, "title": "Dubai Choir Festival · Best Women's Choir", "date": "2019", "venue": "Dubai", "ensemble": "gardenia", "type": "concert", "year": "2019", "size": "wide", "palette": ["#8DA086", "#2a3d28", "#FFFFFF"]},
    {"id": 6, "order": 6, "title": "Tanaghom Youth Workshop", "date": "2021", "venue": "Damascus Governorate", "ensemble": "tanaghom", "type": "rehearsal", "year": "2021", "size": "normal", "palette": ["#F5D000", "#1a1a1a", "#A8B8A2"]},
    {"id": 7, "order": 7, "title": "نساء عشقن الإله · Women Who Adored God", "date": "2018", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2018", "size": "normal", "palette": ["#1a1a1a", "#4a4838", "#F5D000"]},
    {"id": 8, "order": 8, "title": "Syrian Heritage Documentation", "date": "2017", "venue": "Multiple Cities · Syria", "ensemble": "gardenia", "type": "rehearsal", "year": "2017", "size": "square", "palette": ["#A8B8A2", "#F5D000", "#1a1a1a"]},
    {"id": 9, "order": 9, "title": "Music for all Syrians", "date": "2025", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2025", "size": "tall", "palette": ["#2a3d28", "#1a1a1a", "#F5D000"]},
    {"id": 10, "order": 10, "title": "Tanaghom Community Gathering", "date": "2022", "venue": "Sahnaya · Rural Damascus", "ensemble": "tanaghom", "type": "rehearsal", "year": "2022", "size": "normal", "palette": ["#3a3414", "#1a1a1a", "#A8B8A2"]},
    {"id": 11, "order": 11, "title": "زغاريد سورية · Syrian Wedding Songs", "date": "2017", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2017", "size": "wide", "palette": ["#4a4838", "#A8B8A2", "#FFFFFF"]},
    {"id": 12, "order": 12, "title": "Open Rehearsal · Gardenia", "date": "2025", "venue": "Damascus", "ensemble": "gardenia", "type": "rehearsal", "year": "2025", "size": "normal", "palette": ["#1a1a1a", "#3a3414", "#F5D000"]},
    {"id": 13, "order": 13, "title": "Peace Workshop · Tanaghom · Homs", "date": "2023", "venue": "Homs", "ensemble": "tanaghom", "type": "rehearsal", "year": "2023", "size": "square", "palette": ["#1a1a1a", "#A8B8A2", "#F5D000"]},
    {"id": 14, "order": 14, "title": "First concert after liberation", "date": "Dec 2024", "venue": "Damascus", "ensemble": "gardenia", "type": "concert", "year": "2024", "size": "normal", "palette": ["#2a3d28", "#1a1a1a", "#FFFFFF"]},
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

    db.submissions.create_index("created_at")
    db.gallery.create_index("order")

    print("Seeded:")
    for c in ("site", "events", "choirs", "values", "timeline", "leadership", "gallery"):
        print(f"  {c}: {db[c].count_documents({})}")


if __name__ == "__main__":
    main()
