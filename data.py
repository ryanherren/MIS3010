"""In-memory data for the Cyclone Tickets demo (resets on restart)."""
from datetime import datetime

# Section shapes are SVG rects/paths on a 600x420 canvas: (x, y, w, h)
VENUES = {
    'jack-trice': {
        'name': 'Jack Trice Stadium',
        'city': 'Ames, IA',
        'capacity': '61,500',
        'surface': 'field',
        'sections': {
            'WEST-CLUB': {'name': 'West Club Level', 'tier': 'Premium', 'rect': (120, 40, 360, 50),
                          'where': 'West sideline, upper club level, 50-yard line. Indoor lounge access.'},
            'WEST': {'name': 'West Sideline', 'tier': 'Lower Bowl', 'rect': (120, 95, 360, 50),
                     'where': 'West sideline, rows 1-40, between the 20-yard lines.'},
            'EAST': {'name': 'East Sideline', 'tier': 'Lower Bowl', 'rect': (120, 275, 360, 50),
                     'where': 'East sideline (visitors side), rows 1-40, between the 20-yard lines.'},
            'EAST-UP': {'name': 'East Upper Deck', 'tier': 'Upper Deck', 'rect': (120, 330, 360, 50),
                        'where': 'East sideline upper deck, sections UD1-UD12. Great views, steep stairs.'},
            'NORTH': {'name': 'North End Zone', 'tier': 'End Zone', 'rect': (30, 100, 80, 220),
                      'where': 'North end zone, behind the Cyclone tunnel.'},
            'SOUTH': {'name': 'South End Zone', 'tier': 'End Zone', 'rect': (490, 100, 80, 220),
                      'where': 'South end zone, beside the video board.'},
            'GA-STU': {'name': 'General Admission Student Section', 'tier': 'General Admission',
                       'rect': (30, 330, 80, 50), 'where': 'Southeast corner bleachers. Open seating, valid student ID required.',
                       'ga': True},
            'GA-LAWN': {'name': 'General Admission Family Zone', 'tier': 'General Admission',
                        'rect': (490, 330, 80, 50), 'where': 'Northeast corner bleachers. Open seating, first come first served.',
                        'ga': True},
        },
    },
    'hilton': {
        'name': 'Hilton Coliseum',
        'city': 'Ames, IA',
        'capacity': '14,267',
        'surface': 'court',
        'sections': {
            'COURTSIDE': {'name': 'Courtside', 'tier': 'Premium', 'rect': (170, 120, 260, 30),
                          'where': 'Row A along the home bench side, steps from the court.'},
            'LOWER-N': {'name': 'Lower Bowl North', 'tier': 'Lower Bowl', 'rect': (150, 50, 300, 60),
                        'where': 'Sections 101-108, north sideline, rows 1-25.'},
            'LOWER-S': {'name': 'Lower Bowl South', 'tier': 'Lower Bowl', 'rect': (150, 310, 300, 60),
                        'where': 'Sections 109-116, south sideline, rows 1-25.'},
            'BASELINE-W': {'name': 'West Baseline', 'tier': 'Baseline', 'rect': (50, 110, 90, 200),
                           'where': 'Sections 117-122, behind the west basket.'},
            'BASELINE-E': {'name': 'East Baseline', 'tier': 'Baseline', 'rect': (460, 110, 90, 200),
                           'where': 'Sections 123-128, behind the east basket.'},
            'UPPER': {'name': 'Upper Concourse', 'tier': 'Upper Level', 'rect': (150, 380, 300, 30),
                      'where': 'Sections 201-220, top of the Hilton. Best value.'},
            'GA-CY': {'name': 'General Admission Cyclone Rows', 'tier': 'General Admission',
                      'rect': (20, 20, 110, 50), 'where': 'Northwest corner. Open seating, first come first served.',
                      'ga': True},
            'GA-STU': {'name': 'General Admission Student Section', 'tier': 'General Admission',
                       'rect': (470, 20, 110, 50), 'where': 'Northeast corner. Open seating, student ID required.',
                       'ga': True},
        },
    },
}

# base price per tier, per sport multiplier applied by event
TIER_PRICE = {
    'Premium': 120, 'Lower Bowl': 65, 'Upper Deck': 40, 'End Zone': 45,
    'Baseline': 30, 'Upper Level': 22, 'General Admission': 15,
}

SPORTS = {
    'football': {'name': 'Football', 'icon': 'fa-football', 'venue': 'jack-trice', 'mult': 1.0,
                 'blurb': 'Game days at Jack Trice Stadium.'},
    'mens-basketball': {'name': "Men's Basketball", 'icon': 'fa-basketball', 'venue': 'hilton', 'mult': 1.1,
                        'blurb': 'Hilton Magic is real.'},
    'womens-basketball': {'name': "Women's Basketball", 'icon': 'fa-basketball', 'venue': 'hilton', 'mult': 0.7,
                          'blurb': 'Cyclone women ball out at Hilton.'},
    'wrestling': {'name': 'Wrestling', 'icon': 'fa-hand-fist', 'venue': 'hilton', 'mult': 0.8,
                  'blurb': 'Cael Sanderson-era power, Cyclone-style.'},
    'volleyball': {'name': 'Volleyball', 'icon': 'fa-volleyball', 'venue': 'hilton', 'mult': 0.6,
                   'blurb': 'Loud, fast, and sold out often.'},
}

# (id, sport, opponent, date, home?)
_RAW_EVENTS = [
    (1, 'football', 'Iowa Hawkeyes', '2026-09-12 15:30', 'Cy-Hawk Game'),
    (2, 'football', 'Kansas State Wildcats', '2026-10-03 11:00', 'Big 12 Opener'),
    (3, 'football', 'Texas Tech Red Raiders', '2026-11-07 14:00', 'Homecoming'),
    (4, 'football', 'Oklahoma State Cowboys', '2026-11-21 18:00', 'Senior Night'),
    (5, 'mens-basketball', 'Kansas Jayhawks', '2026-12-05 19:00', 'Big 12 Showdown'),
    (6, 'mens-basketball', 'Iowa Hawkeyes', '2026-12-11 18:00', 'Cy-Hawk Series'),
    (7, 'mens-basketball', 'Baylor Bears', '2027-01-17 14:00', 'Big 12 Play'),
    (8, 'womens-basketball', 'Drake Bulldogs', '2026-11-20 18:30', 'Season Opener'),
    (9, 'womens-basketball', 'TCU Horned Frogs', '2027-01-24 13:00', 'Big 12 Play'),
    (10, 'wrestling', 'Iowa Hawkeyes', '2027-02-01 19:00', 'Cy-Hawk Dual'),
    (11, 'wrestling', 'Oklahoma State Cowboys', '2027-02-14 14:00', 'Big 12 Dual'),
    (12, 'volleyball', 'Nebraska Cornhuskers', '2026-10-30 19:00', 'Rivalry Night'),
    (13, 'volleyball', 'Kansas Jayhawks', '2026-11-13 19:00', 'Big 12 Play'),
]

EVENTS = {}
INVENTORY = {}  # event_id -> section_key -> {'avail': int, 'price': float}


def _build():
    for eid, sport, opp, when, tag in _RAW_EVENTS:
        s = SPORTS[sport]
        venue = VENUES[s['venue']]
        # Marquee games cost a little more
        bump = 1.35 if opp in ('Iowa Hawkeyes', 'Kansas Jayhawks') else 1.0
        EVENTS[eid] = {
            'id': eid, 'sport': sport, 'opponent': opp, 'tag': tag,
            'when': datetime.strptime(when, '%Y-%m-%d %H:%M'),
            'venue_key': s['venue'], 'venue': venue['name'],
        }
        INVENTORY[eid] = {}
        for key, sec in venue['sections'].items():
            price = round(TIER_PRICE[sec['tier']] * s['mult'] * bump)
            r = (eid * 37 + len(key) * 101) % 7
            base = 400 if sec.get('ga') else 80 + r * 25
            INVENTORY[eid][key] = {'avail': base, 'price': max(price, 5)}


_build()

USERS = {}    # email -> {'name', 'pw'}
ORDERS = {}   # order_id -> dict
TICKETS = {}  # ticket_id -> dict
