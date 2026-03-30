# Mock catalog and site content for Cole's Kicks (demo)

SHOES = [
    {
        "id": "ck-001",
        "name": "Air Jordan 1 Retro High OG",
        "brand": "Nike",
        "size": "10",
        "color": "Red",
        "price": 189.99,
        "condition": "Like new",
        "seller": "JordanFan23",
        "image": "https://placehold.co/480x360/C41E3A/FFFFFF/png?text=AJ1+Chicago",
    },
    {
        "id": "ck-002",
        "name": "Yeezy Boost 350 V2",
        "brand": "Adidas",
        "size": "9.5",
        "color": "Black",
        "price": 265.00,
        "condition": "New",
        "seller": "SoleStreet",
        "image": "https://placehold.co/480x360/1a1a1a/FF6B00/png?text=Yeezy+350",
    },
    {
        "id": "ck-003",
        "name": "New Balance 990v6",
        "brand": "New Balance",
        "size": "11",
        "color": "Grey",
        "price": 210.00,
        "condition": "Excellent",
        "seller": "MidwestKicks",
        "image": "https://placehold.co/480x360/808080/FFFFFF/png?text=NB+990v6",
    },
    {
        "id": "ck-004",
        "name": "Dunk Low Panda",
        "brand": "Nike",
        "size": "8",
        "color": "Black",
        "price": 145.00,
        "condition": "New",
        "seller": "CampusSneaks",
        "image": "https://placehold.co/480x360/0d0d0d/FFFFFF/png?text=Dunk+Low",
    },
    {
        "id": "ck-005",
        "name": "Samba OG",
        "brand": "Adidas",
        "size": "10.5",
        "color": "White",
        "price": 95.00,
        "condition": "Good",
        "seller": "VintageRun",
        "image": "https://placehold.co/480x360/FF6B00/1a1a1a/png?text=Samba+OG",
    },
    {
        "id": "ck-006",
        "name": "Air Max 90 Infrared",
        "brand": "Nike",
        "size": "9",
        "color": "Red",
        "price": 175.50,
        "condition": "Like new",
        "seller": "AirMaxArchive",
        "image": "https://placehold.co/480x360/DC143C/FFFFFF/png?text=AM90",
    },
    {
        "id": "ck-007",
        "name": "Chuck 70 High",
        "brand": "Converse",
        "size": "8.5",
        "color": "Orange",
        "price": 78.00,
        "condition": "Good",
        "seller": "CanvasCo",
        "image": "https://placehold.co/480x360/FF8C00/1a1a1a/png?text=Chuck+70",
    },
    {
        "id": "ck-008",
        "name": "Ultraboost 22",
        "brand": "Adidas",
        "size": "12",
        "color": "Black",
        "price": 132.00,
        "condition": "Excellent",
        "seller": "RunClubIA",
        "image": "https://placehold.co/480x360/111111/FF6B00/png?text=Ultraboost",
    },
]

RECOMMENDED_IDS = ["ck-001", "ck-006", "ck-002", "ck-004"]

REVIEWS = [
    {
        "author": "Alex M.",
        "rating": 5,
        "title": "Legit check passed",
        "body": "Bought Dunks through Cole's Kicks. Authentication was fast and shipping was tracked the whole way.",
        "date": "2026-03-22",
    },
    {
        "author": "Sam R.",
        "rating": 5,
        "title": "Seller dashboard is clear",
        "body": "Listed three pairs for our MIS project demo. Fees are transparent and mock payouts show up instantly.",
        "date": "2026-03-28",
    },
    {
        "author": "Jordan K.",
        "rating": 4,
        "title": "Great filters",
        "body": "Found my size and brand in seconds. Would love live inventory alerts—still, solid class project site.",
        "date": "2026-03-29",
    },
]

CAREERS = [
    {
        "title": "Campus Brand Ambassador",
        "team": "Growth",
        "location": "Ames, IA (Hybrid)",
        "type": "Part-time",
        "summary": "Represent Cole's Kicks on campus, host pop-up authentication workshops, and gather seller feedback.",
    },
    {
        "title": "Junior Full-Stack Engineer",
        "team": "Product",
        "location": "Remote (US)",
        "type": "Internship",
        "summary": "Ship features for search, checkout, and seller analytics using Flask and modern front-end patterns.",
    },
    {
        "title": "Trust & Safety Analyst",
        "team": "Operations",
        "location": "Ames, IA",
        "type": "Full-time",
        "summary": "Review listings, coordinate mock authentications, and help design policies for peer-to-peer resale.",
    },
]

FAQ = [
    {
        "q": "How does buying work?",
        "a": "Browse the shop, add pairs to your cart, and complete checkout. You receive an order ID to track status on the Order Tracker page.",
    },
    {
        "q": "How do sellers get paid?",
        "a": "This demo simulates payouts. In production, Cole's Kicks would connect to secure payouts after delivery confirmation.",
    },
    {
        "q": "Can I return shoes?",
        "a": "Mock policy: eligible within 7 days if unworn and tags intact. Contact support through the Help page.",
    },
    {
        "q": "Is authentication real?",
        "a": "For the MIS3010 project, authentication is simulated. Real launch would partner with verification services.",
    },
]

SEED_ORDERS = [
    {
        "id": "CK-2026-1001",
        "email": "demo@iastate.edu",
        "status": "Delivered",
        "items": [{"name": "Dunk Low Panda", "qty": 1, "price": 145.00}],
        "placed": "2026-03-15",
        "total": 145.00,
    },
    {
        "id": "CK-2026-1002",
        "email": "buyer@example.com",
        "status": "In transit",
        "items": [{"name": "Yeezy Boost 350 V2", "qty": 1, "price": 265.00}],
        "placed": "2026-03-27",
        "total": 265.00,
    },
]

SELLER_STATS = {
    "active_listings": 4,
    "pending_sales": 2,
    "lifetime_sales": 12840.00,
    "avg_ship_time_hours": 18,
}
