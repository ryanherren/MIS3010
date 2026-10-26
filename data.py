"""In-memory mock data for Blush & Blade Lawn Co."""

SERVICES = [
    {"id": "mowing", "name": "Lawn Mowing & Edging", "icon": "fa-scissors",
     "desc": "Precision stripes, crisp edges, and clippings swept clean every visit.",
     "rate": "From $0.04 / sq ft", "per_sqft": 0.04, "min": 45},
    {"id": "fertilize", "name": "Fertilization & Weed Control", "icon": "fa-seedling",
     "desc": "A 5-step seasonal program that keeps your turf thick, green, and weed-free.",
     "rate": "From $0.03 / sq ft", "per_sqft": 0.03, "min": 55},
    {"id": "mulch", "name": "Mulch & Garden Beds", "icon": "fa-leaf",
     "desc": "Fresh mulch, bed edging, and plantings that make curb appeal pop.",
     "rate": "From $0.09 / sq ft", "per_sqft": 0.09, "min": 90},
    {"id": "trim", "name": "Hedge & Shrub Trimming", "icon": "fa-tree",
     "desc": "Shaped, healthy, and tidy hedges, shrubs, and ornamental trees.",
     "rate": "From $0.05 / sq ft", "per_sqft": 0.05, "min": 75},
    {"id": "aerate", "name": "Aeration & Overseeding", "icon": "fa-circle-nodes",
     "desc": "Core aeration plus premium seed for a lush, fuller lawn next season.",
     "rate": "From $0.035 / sq ft", "per_sqft": 0.035, "min": 80},
    {"id": "cleanup", "name": "Seasonal Cleanup", "icon": "fa-wind",
     "desc": "Leaf removal, debris hauling, and spring or fall resets.",
     "rate": "From $0.045 / sq ft", "per_sqft": 0.045, "min": 110},
]

FREQUENCY = {  # multiplier on recurring services
    "once": {"label": "One-time", "mult": 1.0},
    "monthly": {"label": "Monthly", "mult": 0.95},
    "biweekly": {"label": "Every 2 weeks", "mult": 0.90},
    "weekly": {"label": "Weekly", "mult": 0.85},
}

PLANS = [
    {"name": "Fresh Cut", "price": 49, "tag": "Weekly mowing for small yards",
     "features": ["Mow, edge & blow", "Up to 5,000 sq ft", "Text updates"], "featured": False},
    {"name": "Full Bloom", "price": 129, "tag": "Our most popular plan",
     "features": ["Everything in Fresh Cut", "Fertilization & weed control", "Hedge trimming", "Up to 10,000 sq ft"], "featured": True},
    {"name": "Estate", "price": 249, "tag": "Total landscape care",
     "features": ["Everything in Full Bloom", "Mulch & bed care", "Seasonal cleanups", "Up to 25,000 sq ft"], "featured": False},
]

PROJECTS = [
    {"title": "Overgrown Backyard Revival", "place": "Maple Heights", "service": "Mowing & Cleanup"},
    {"title": "Front Bed Makeover", "place": "Oakwood Estates", "service": "Mulch & Plantings"},
    {"title": "Patchy Lawn to Lush Turf", "place": "Riverbend", "service": "Aeration & Overseeding"},
    {"title": "Hedge Reshape", "place": "Willow Park", "service": "Hedge Trimming"},
]

REVIEWS = [
    {"name": "Priya N.", "town": "Maple Heights", "stars": 5, "service": "Weekly Mowing",
     "text": "My lawn has never looked this good. The crew is on time every single week and the edges are razor sharp."},
    {"name": "Tom & Linda R.", "town": "Oakwood Estates", "stars": 5, "service": "Mulch & Beds",
     "text": "They transformed our front beds in a day. The neighbors keep asking who did it!"},
    {"name": "Derrick W.", "town": "Riverbend", "stars": 5, "service": "Aeration & Overseeding",
     "text": "Quote took 30 seconds online and the price never changed. Our patchy yard is now thick and green."},
    {"name": "Samantha K.", "town": "Willow Park", "stars": 4, "service": "Hedge Trimming",
     "text": "Great work and friendly team. Booking online was effortless."},
    {"name": "Marcus B.", "town": "Downtown", "stars": 5, "service": "Seasonal Cleanup",
     "text": "Fall cleanup done in one morning, and they hauled everything away. Totally worth it."},
    {"name": "Elena G.", "town": "Maple Heights", "stars": 5, "service": "Fertilization Program",
     "text": "Weeds gone, grass greener. Pink trucks are also just really fun to see in the neighborhood."},
]

TEAM = [
    {"name": "Michael", "role": "Chief Executive Officer", "initials": "M",
     "bio": "Built the company on one idea: a first-class experience on every lawn and for every customer."},
    {"name": "Mackenzie", "role": "Chief Marketing Officer", "initials": "Mk",
     "bio": "The mind behind our hot pink brand. If you spotted the trucks, you've met her work."},
    {"name": "Sam", "role": "Co-Chief Marketing Officer", "initials": "S",
     "bio": "Champions our fresh-cut-grass green and keeps our message as crisp as our edges."},
    {"name": "Margaret", "role": "Brand Coordinator", "initials": "Mg",
     "bio": "Keeps every uniform, invoice, and truck on-brand with our signature light purple."},
]

FAQS = [
    ("How does the online quote work?", "Pick your services, enter your lawn size, and choose a frequency. You get an instant estimate with no phone call needed. We confirm with a quick on-site check before the first visit."),
    ("Do I need to be home during service?", "Nope! As long as we can access the yard, we'll text you before and after every visit with photos."),
    ("What areas do you serve?", "We serve Maple Heights, Oakwood Estates, Riverbend, Willow Park, and Downtown, plus a 15-mile radius around them."),
    ("What if it rains on my service day?", "We automatically reschedule to the next available day and let you know by text. You never pay extra."),
    ("How do I pay?", "We bill after each visit or monthly for recurring plans. We accept all major cards and bank transfer."),
    ("Can I skip or cancel a visit?", "Yes. Skip or cancel up to 24 hours ahead with no fees. Recurring plans have no contracts."),
    ("Are you insured?", "Fully licensed, bonded, and insured. Certificates are available on request."),
    ("Is Blush & Blade Beauty real makeup?", "Yes! Our products have lawn-care names but are real, dermatologist-tested, cruelty-free makeup. No actual fertilizer in the serum."),
    ("How long does makeup shipping take?", "Orders ship in 1 to 2 business days and arrive in 3 to 5. Orders over $40 ship free."),
    ("Can I return makeup I don't love?", "Yes. Return unopened items within 30 days, or tell us if a product didn't work for you and we'll make it right."),
    ("Do you use pet-safe products?", "Yes. Our standard products are pet-friendly once dry, and we'll tell you exactly how long that takes."),
]

TIME_SLOTS = ["8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM"]


# ---- Blush & Blade Beauty ----
CATEGORIES = [
    {"id": "blush", "name": "Blush", "icon": "fa-circle-half-stroke"},
    {"id": "lips", "name": "Lipstick & Lip", "icon": "fa-heart"},
    {"id": "eyes", "name": "Eyes", "icon": "fa-eye"},
    {"id": "face", "name": "Face & Skin", "icon": "fa-face-smile"},
    {"id": "nails", "name": "Nails", "icon": "fa-hand-sparkles"},
    {"id": "tools", "name": "Tools", "icon": "fa-brush"},
    {"id": "bundles", "name": "Bundles", "icon": "fa-gift"},
]

# color is the swatch shown on the card; every name is a lawn-care pun
PRODUCTS = [
    {"id": "fresh-cut-blush", "name": "Fresh Cut Blush", "cat": "blush", "price": 18.00, "color": "#FF4FA3", "icon": "fa-circle-half-stroke",
     "desc": "Our signature hot pink powder blush. Buildable color with a soft, dewy finish.", "badge": "Bestseller", "shade": "Hot Pink"},
    {"id": "morning-dew-blush", "name": "Morning Dew Cream Blush", "cat": "blush", "price": 20.00, "color": "#FFB3D1", "icon": "fa-droplet",
     "desc": "A lightweight cream blush that melts into skin for a glow like grass at sunrise.", "badge": "", "shade": "Petal Pink"},
    {"id": "lavender-lawn-blush", "name": "Lavender Lawn Blush", "cat": "blush", "price": 18.00, "color": "#C9A8EE", "icon": "fa-spa",
     "desc": "A cool lilac-toned blush for a fresh, unexpected pop of color.", "badge": "New", "shade": "Light Purple"},
    {"id": "sod-solid-lipstick", "name": "Sod Solid Lipstick", "cat": "lips", "price": 16.00, "color": "#E0116F", "icon": "fa-heart",
     "desc": "A rich, long-wear matte pink that stays put all day, like freshly laid sod.", "badge": "Bestseller", "shade": "Deep Pink"},
    {"id": "edge-trimmer-lip-liner", "name": "Edge Trimmer Lip Liner", "cat": "lips", "price": 12.00, "color": "#B80C5B", "icon": "fa-pen",
     "desc": "Crisp, precise definition for the sharpest lip line on the block.", "badge": "", "shade": "Berry"},
    {"id": "clipping-gloss", "name": "Clippings Lip Gloss", "cat": "lips", "price": 14.00, "color": "#FF8CC6", "icon": "fa-droplet",
     "desc": "High-shine, non-sticky gloss with a hint of peppermint.", "badge": "", "shade": "Clear Pink"},
    {"id": "green-thumb-balm", "name": "Green Thumb Lip Balm", "cat": "lips", "price": 9.00, "color": "#6FD23A", "icon": "fa-leaf",
     "desc": "Cucumber-mint tinted balm that hydrates and gives a fresh green-to-pink shift.", "badge": "New", "shade": "Fresh Green"},
    {"id": "weed-whacker-mascara", "name": "Weed Whacker Mascara", "cat": "eyes", "price": 15.00, "color": "#2A1B3D", "icon": "fa-eye",
     "desc": "Volumizing, lengthening mascara that tackles every last lash.", "badge": "", "shade": "Black"},
    {"id": "mulch-matte-palette", "name": "Mulch Matte Eyeshadow Palette", "cat": "eyes", "price": 28.00, "color": "#8B5E3C", "icon": "fa-table-cells",
     "desc": "Twelve earthy matte shades, from topsoil brown to bark, plus two pink pops.", "badge": "Bestseller", "shade": "12 Shades"},
    {"id": "hedge-trimmer-liner", "name": "Hedge Trimmer Eyeliner", "cat": "eyes", "price": 13.00, "color": "#2F8A0C", "icon": "fa-pen-nib",
     "desc": "A waterproof gel liner in deep forest green for clean, shaped wings.", "badge": "", "shade": "Forest Green"},
    {"id": "lawn-primer", "name": "Level Lawn Primer", "cat": "face", "price": 24.00, "color": "#F4EEFC", "icon": "fa-flask",
     "desc": "A smoothing primer that evens out your canvas, pores and all.", "badge": "", "shade": "Universal"},
    {"id": "topsoil-foundation", "name": "Topsoil Foundation", "cat": "face", "price": 32.00, "color": "#D9A877", "icon": "fa-bottle-droplet",
     "desc": "Medium-coverage, breathable foundation in 24 shades. Builds a strong base.", "badge": "", "shade": "24 Shades"},
    {"id": "fertilizer-serum", "name": "Fertilizer Glow Serum", "cat": "face", "price": 38.00, "color": "#B6EE8F", "icon": "fa-seedling",
     "desc": "Vitamin C and hyaluronic acid serum to help your skin grow radiant.", "badge": "New", "shade": "Serum"},
    {"id": "sprinkler-setting-spray", "name": "Sprinkler Setting Spray", "cat": "face", "price": 20.00, "color": "#D8C4F2", "icon": "fa-spray-can-sparkles",
     "desc": "A fine, even mist that locks in makeup for up to 16 hours.", "badge": "Bestseller", "shade": "Mist"},
    {"id": "aerator-scrub", "name": "Aerator Lip Scrub", "cat": "face", "price": 11.00, "color": "#FFD1E6", "icon": "fa-flask",
     "desc": "Sugar scrub that gently exfoliates and preps lips for color.", "badge": "", "shade": "Sugar"},
    {"id": "grass-green-polish", "name": "Grass Green Nail Polish", "cat": "nails", "price": 10.00, "color": "#4CBB17", "icon": "fa-hand-sparkles",
     "desc": "A bold, chip-resistant fresh-cut green. Looks great against hot pink.", "badge": "", "shade": "Fresh Green"},
    {"id": "pink-flamingo-polish", "name": "Lawn Flamingo Nail Polish", "cat": "nails", "price": 10.00, "color": "#FF1493", "icon": "fa-hand-sparkles",
     "desc": "Our hot pink polish, named after the classic yard decoration.", "badge": "Bestseller", "shade": "Hot Pink"},
    {"id": "rake-brush-set", "name": "Rake & Roll Brush Set", "cat": "tools", "price": 36.00, "color": "#A77FE0", "icon": "fa-brush",
     "desc": "Eight vegan brushes for face and eyes, in a pink carrying case.", "badge": "", "shade": "8 Brushes"},
    {"id": "leaf-blower-dryer", "name": "Leaf Blower Mini Fan", "cat": "tools", "price": 15.00, "color": "#7ED348", "icon": "fa-fan",
     "desc": "A handheld fan that dries lashes and polish in seconds.", "badge": "", "shade": "Green"},
    {"id": "lawn-bag-kit", "name": "Yard Work Makeup Bag", "cat": "tools", "price": 22.00, "color": "#FF5CB1", "icon": "fa-bag-shopping",
     "desc": "A roomy waterproof makeup bag with a green zip. Fits the whole collection.", "badge": "", "shade": "Pink"},
    {"id": "beauty-blade-bundle", "name": "Beauty + Blade Signature Bundle", "cat": "bundles", "price": 229.00, "color": "#FF1493", "icon": "fa-heart",
     "desc": "A Beauty Box for her and the Blade Signature Lawn Care Package for him. Includes a lawn service voucher redeemable on our booking page.", "badge": "Bundle", "shade": "Beauty Box + Lawn Package"},
    {"id": "full-lawn-set", "name": "The Full Lawn Gift Set", "cat": "face", "price": 59.00, "color": "#FF1493", "icon": "fa-gift",
     "desc": "Fresh Cut Blush, Sod Solid Lipstick, Weed Whacker Mascara, and a bag. Save 25%.", "badge": "Gift Set", "shade": "Set of 4"},
]

SHIPPING_FLAT = 5.99
FREE_SHIPPING_OVER = 40.00
TAX_RATE = 0.07


BUNDLE = {
    "id": "beauty-blade-bundle",
    "retail": 266.00,
    "beauty_box": {
        "title": "The Beauty Box",
        "tagline": "For her: our hot pink favorites in a gift-ready box",
        "items": ["fresh-cut-blush", "sod-solid-lipstick", "weed-whacker-mascara", "sprinkler-setting-spray", "lawn-bag-kit"],
    },
    "blade_package": {
        "title": "The Blade Signature Package",
        "tagline": "For him: a full signature visit from our crew",
        "items": ["Precision mow, stripe & edge", "Fertilization & weed control", "Hedge & shrub trimming", "Leaf & debris blow-off", "Pink Blade Co. trucker hat"],
        "value": 175.00,
    },
}
