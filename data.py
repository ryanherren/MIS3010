"""In-memory data for the Cyclone Tickets demo (resets on restart)."""
from datetime import datetime

# Section shapes are SVG rects/paths on a 600x420 canvas: (x, y, w, h)
VENUES = {
    'jack-trice': {
        'name': 'Jack Trice Stadium',
        'city': 'Ames, IA',
        'capacity': '61,500',
        'surface': 'field',
        # Layout (west on top, north on right): numbered sections 1-19 run down the west
        # (Iowa State) sideline, 20-22 are the south end zone Sukup Club, 23-27 plus O-T
        # are the southeast student corner, 28-41 are the east (visitor) sideline, and the
        # hillside is the north end. Lettered sections are the upper deck.
        'sections': {
            'WEST-CLUB': {'name': 'Jack Trice Club', 'tier': 'Premium', 'rect': (120, 40, 360, 50),
                          'where': 'West (Iowa State) sideline club level above the 50-yard line. Indoor, climate-controlled seating.'},
            'WEST': {'name': 'West Sideline (Sections 1-19)', 'tier': 'Lower Bowl', 'rect': (120, 95, 360, 50),
                     'where': 'Iowa State sideline lower bowl. Sections 8 and 9 sit on the 50-yard line.'},
            'WEST-UP': {'name': 'West Upper Deck (Lettered)', 'tier': 'Upper Deck', 'rect': (120, 5, 360, 30),
                        'where': 'Upper deck above the Iowa State sideline. Sections D, E and F are at midfield.'},
            'EAST': {'name': 'East Sideline (Sections 28-41)', 'tier': 'Lower Bowl', 'rect': (120, 275, 360, 50),
                     'where': 'Visitor sideline lower bowl. Sections 33 and 34 sit on the 50-yard line.'},
            'EAST-UP': {'name': 'East Upper Deck (Lettered)', 'tier': 'Upper Deck', 'rect': (120, 330, 360, 50),
                        'where': 'Upper deck above the visitor sideline. Section W is at midfield.'},
            'SUKUP-CLUB': {'name': 'Sukup End Zone Club (20-22)', 'label': 'SUKUP', 'tier': 'Club', 'rect': (30, 100, 80, 220),
                           'where': 'South end zone club seating, sections 20-22.'},
            'STUDENT': {'name': 'Student Section (23-27, O-T)', 'label': 'STUDENT', 'tier': 'General Admission',
                        'rect': (30, 330, 80, 50), 'ga': True,
                        'where': 'Southeast corner, sections 23-27 and O-T. Open seating, student ID required.'},
            'HILLSIDE-NW': {'name': 'Hillside Northwest', 'label': 'HILL NW', 'tier': 'General Admission',
                            'rect': (490, 100, 80, 105), 'ga': True,
                            'where': 'North end zone hillside, west half. Open seating, first come first served.'},
            'HILLSIDE-NE': {'name': 'Hillside Northeast', 'label': 'HILL NE', 'tier': 'General Admission',
                            'rect': (490, 215, 80, 105), 'ga': True,
                            'where': 'North end zone hillside, east half. Open seating, first come first served.'},
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
    'Premium': 120, 'Club': 85, 'Lower Bowl': 65, 'Upper Deck': 40, 'End Zone': 45,
    'Baseline': 30, 'Upper Level': 22, 'General Admission': 15,
}

SPORTS = {
    'football': {'name': 'Football', 'icon': 'fa-football', 'venue': 'jack-trice', 'mult': 1.0,
                 'blurb': 'Game days at Jack Trice Stadium.'},
    'mens-basketball': {'name': "Men's Basketball", 'icon': 'fa-basketball', 'venue': 'hilton', 'mult': 1.1,
                        'blurb': 'Hilton Magic is real.'},
    'womens-basketball': {'name': "Women's Basketball", 'icon': 'fa-basketball', 'venue': 'hilton', 'mult': 0.7,
                          'blurb': 'Cyclone women ball out at Hilton.'},
    'volleyball': {'name': 'Volleyball', 'icon': 'fa-volleyball', 'venue': 'hilton', 'mult': 0.6,
                   'blurb': 'Loud, fast, and sold out often.'},
}

# Real 2026-27 home schedule from cyclones.com announcements. Missing time = TBA.
# (id, sport, opponent, date[, time], tag)
_RAW_EVENTS = [
    (1, 'football', 'Oklahoma State Cowboys', '2026-10-31', 'Big 12 Play'),
    (2, 'football', 'Cincinnati Bearcats', '2026-11-14', 'Big 12 Play'),
    (3, 'football', 'Kansas State Wildcats', '2026-11-28', 'Regular Season Finale'),
    (4, 'volleyball', 'West Virginia Mountaineers', '2026-10-30 18:30', 'Big 12 Play'),
    (5, 'volleyball', 'Kansas Jayhawks', '2026-11-01 12:00', 'Big 12 Play'),
    (6, 'volleyball', 'BYU Cougars', '2026-11-07 14:00', 'Big 12 Play'),
    (7, 'volleyball', 'Cincinnati Bearcats', '2026-11-16 18:30', 'Big 12 Play'),
    (8, 'volleyball', 'Houston Cougars', '2026-11-25', 'Regular Season Finale'),
    (9, 'mens-basketball', 'Southern Miss Golden Eagles', '2026-11-06', 'Home Opener'),
    (10, 'mens-basketball', 'Southern Jaguars', '2026-11-10', 'Non-Conference'),
    (11, 'mens-basketball', 'Niagara Purple Eagles', '2026-11-15', 'Non-Conference'),
    (12, 'mens-basketball', 'Alcorn State Braves', '2026-12-02', 'Non-Conference'),
    (13, 'mens-basketball', 'Purdue Boilermakers', '2026-12-06', 'First Ames Visit'),
    (14, 'mens-basketball', 'North Carolina Central Eagles', '2026-12-13', 'Non-Conference'),
    (15, 'mens-basketball', 'Northern Arizona Lumberjacks', '2026-12-21', 'Non-Conference'),
    (16, 'mens-basketball', 'New Hampshire Wildcats', '2026-12-29', 'Non-Conference'),
    (17, 'womens-basketball', 'Upper Iowa Peacocks', '2026-10-28', 'Exhibition'),
    (18, 'womens-basketball', 'Grambling State Tigers', '2026-11-02', 'Season Opener'),
    (19, 'womens-basketball', 'Nicholls State Colonels', '2026-11-05', 'Non-Conference'),
    (20, 'womens-basketball', 'Eastern Illinois Panthers', '2026-11-08', 'Non-Conference'),
    (21, 'womens-basketball', 'Howard Bison', '2026-11-12', 'Non-Conference'),
    (22, 'womens-basketball', 'UIC Flames', '2026-11-15', 'Non-Conference'),
    (23, 'womens-basketball', 'Drake Bulldogs', '2026-11-22', 'Non-Conference'),
    (24, 'womens-basketball', 'Norfolk State Spartans', '2026-12-01', 'Non-Conference'),
    (25, 'womens-basketball', 'Loyola Ramblers', '2026-12-06', 'Non-Conference'),
    (26, 'womens-basketball', 'Chicago State Cougars', '2026-12-13', 'Non-Conference'),
]

EVENTS = {}
INVENTORY = {}  # event_id -> section_key -> {'avail': int, 'price': float}


def _build():
    for eid, sport, opp, when, tag in _RAW_EVENTS:
        s = SPORTS[sport]
        venue = VENUES[s['venue']]
        # Marquee games cost a little more
        bump = 1.35 if opp in ('Purdue Boilermakers', 'Oklahoma State Cowboys', 'Kansas State Wildcats', 'Kansas Jayhawks') else 1.0
        EVENTS[eid] = {
            'id': eid, 'sport': sport, 'opponent': opp, 'tag': tag,
            'when': datetime.strptime(when, '%Y-%m-%d %H:%M' if ' ' in when else '%Y-%m-%d'),
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
