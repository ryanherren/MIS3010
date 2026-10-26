"""In-memory mock data for the Hy-Vee storefront (no database; resets on deploy)."""

CATEGORIES = [
    'Produce', 'Meat & Seafood', 'Dairy & Eggs', 'Bakery',
    'Pantry', 'Frozen', 'Beverages', 'Snacks',
]

DIETARY_TAGS = ['Organic', 'Gluten-Free', 'Vegan', 'Local']

# id, name, category, price, unit, emoji, tags, sale_price (None if not on sale), rating, description
_PRODUCTS = [
    (1, 'Bananas', 'Produce', 0.59, 'lb', '🍌', ['Vegan', 'Gluten-Free'], None, 4.7, 'Ripe, sweet Cavendish bananas.'),
    (2, 'Organic Strawberries', 'Produce', 4.99, '1 lb', '🍓', ['Organic', 'Vegan', 'Gluten-Free'], 3.49, 4.6, 'Juicy organic strawberries, perfect for snacking or desserts.'),
    (3, 'Avocados', 'Produce', 1.25, 'each', '🥑', ['Vegan', 'Gluten-Free'], 0.99, 4.4, 'Creamy Hass avocados.'),
    (4, 'Roma Tomatoes', 'Produce', 1.49, 'lb', '🍅', ['Vegan', 'Gluten-Free', 'Local'], None, 4.3, 'Firm Roma tomatoes from Midwest growers.'),
    (5, 'Yellow Onions', 'Produce', 1.19, 'lb', '🧅', ['Vegan', 'Gluten-Free'], None, 4.5, 'Everyday cooking onions.'),
    (6, 'Garlic', 'Produce', 0.79, 'bulb', '🧄', ['Vegan', 'Gluten-Free'], None, 4.6, 'Fresh whole garlic bulbs.'),
    (7, 'Sweet Corn', 'Produce', 0.50, 'ear', '🌽', ['Vegan', 'Gluten-Free', 'Local'], 0.33, 4.9, 'Iowa sweet corn, picked fresh.'),
    (8, 'Limes', 'Produce', 0.39, 'each', '🍋', ['Vegan', 'Gluten-Free'], None, 4.2, 'Bright, tangy limes.'),
    (9, 'Baby Spinach', 'Produce', 3.99, '5 oz', '🥬', ['Organic', 'Vegan', 'Gluten-Free'], None, 4.4, 'Pre-washed organic baby spinach.'),
    (10, 'Hy-Vee Ground Beef 80/20', 'Meat & Seafood', 5.49, 'lb', '🥩', ['Gluten-Free', 'Local'], 4.49, 4.5, 'Fresh ground chuck from Midwest cattle.'),
    (11, 'Boneless Chicken Breast', 'Meat & Seafood', 3.99, 'lb', '🍗', ['Gluten-Free'], None, 4.6, 'All-natural boneless, skinless chicken breasts.'),
    (12, 'Atlantic Salmon Fillet', 'Meat & Seafood', 11.99, 'lb', '🐟', ['Gluten-Free'], 9.99, 4.7, 'Fresh, never-frozen salmon fillets.'),
    (13, 'Iowa Pork Chops', 'Meat & Seafood', 4.29, 'lb', '🥓', ['Gluten-Free', 'Local'], None, 4.8, 'Bone-in Iowa pork chops.'),
    (14, 'Hy-Vee 2% Milk', 'Dairy & Eggs', 3.29, 'gallon', '🥛', ['Gluten-Free', 'Local'], None, 4.7, 'Farm-fresh 2% reduced-fat milk.'),
    (15, 'Large Grade A Eggs', 'Dairy & Eggs', 2.99, 'dozen', '🥚', ['Gluten-Free'], 2.49, 4.6, 'A dozen large Grade A eggs.'),
    (16, 'Shredded Cheddar', 'Dairy & Eggs', 2.79, '8 oz', '🧀', ['Gluten-Free'], None, 4.5, 'Sharp cheddar, finely shredded.'),
    (17, 'Unsalted Butter', 'Dairy & Eggs', 4.49, '1 lb', '🧈', ['Gluten-Free'], None, 4.8, 'Sweet cream unsalted butter.'),
    (18, 'Greek Yogurt', 'Dairy & Eggs', 5.49, '32 oz', '🥣', ['Gluten-Free'], 4.29, 4.4, 'Plain nonfat Greek yogurt.'),
    (19, 'Hy-Vee French Bread', 'Bakery', 2.49, 'loaf', '🥖', ['Vegan'], None, 4.7, 'Baked fresh in-store every morning.'),
    (20, 'Flour Tortillas', 'Bakery', 2.99, '10 ct', '🌮', ['Vegan'], None, 4.3, 'Soft taco-size flour tortillas.'),
    (21, 'Hamburger Buns', 'Bakery', 2.29, '8 ct', '🍔', [], 1.79, 4.2, 'Soft white buns, baked in-store.'),
    (22, 'Chocolate Chip Cookies', 'Bakery', 4.99, '12 ct', '🍪', [], None, 4.9, 'Our famous bakery cookies.'),
    (23, 'Spaghetti Pasta', 'Pantry', 1.29, '16 oz', '🍝', ['Vegan'], None, 4.5, 'Classic durum wheat spaghetti.'),
    (24, 'Marinara Sauce', 'Pantry', 2.99, '24 oz', '🥫', ['Vegan', 'Gluten-Free'], 2.29, 4.4, 'Slow-simmered tomato basil marinara.'),
    (25, 'Extra Virgin Olive Oil', 'Pantry', 8.99, '16.9 oz', '🫒', ['Vegan', 'Gluten-Free'], None, 4.6, 'Cold-pressed extra virgin olive oil.'),
    (26, 'Jasmine Rice', 'Pantry', 3.49, '2 lb', '🍚', ['Vegan', 'Gluten-Free'], None, 4.5, 'Fragrant long-grain jasmine rice.'),
    (27, 'Black Beans', 'Pantry', 0.99, '15 oz', '🫘', ['Vegan', 'Gluten-Free', 'Organic'], None, 4.3, 'Organic canned black beans.'),
    (28, 'Taco Seasoning', 'Pantry', 1.19, '1 oz', '🌶️', ['Vegan', 'Gluten-Free'], None, 4.4, 'Mild taco seasoning blend.'),
    (29, 'All-Purpose Flour', 'Pantry', 3.29, '5 lb', '🌾', ['Vegan'], None, 4.6, 'Unbleached all-purpose flour.'),
    (30, 'Soy Sauce', 'Pantry', 2.79, '15 oz', '🍶', ['Vegan'], None, 4.5, 'Naturally brewed soy sauce.'),
    (31, 'Frozen Pizza', 'Frozen', 6.99, 'each', '🍕', [], 4.99, 4.1, 'Hy-Vee pepperoni pizza, rising crust.'),
    (32, 'Vanilla Ice Cream', 'Frozen', 4.99, '1.5 qt', '🍨', ['Gluten-Free'], None, 4.8, 'Rich and creamy vanilla bean ice cream.'),
    (33, 'Frozen Mixed Vegetables', 'Frozen', 1.99, '12 oz', '🥦', ['Vegan', 'Gluten-Free'], None, 4.3, 'Corn, peas, carrots and green beans.'),
    (34, 'Orange Juice', 'Beverages', 3.99, '52 oz', '🍊', ['Vegan', 'Gluten-Free'], 2.99, 4.6, '100% pure squeezed, no pulp.'),
    (35, 'Hy-Vee Sparkling Water', 'Beverages', 4.49, '12 pk', '💧', ['Vegan', 'Gluten-Free'], None, 4.4, 'Lime-flavored sparkling water.'),
    (36, 'Ground Coffee', 'Beverages', 8.49, '12 oz', '☕', ['Vegan', 'Gluten-Free'], 6.99, 4.7, 'Medium roast Colombian ground coffee.'),
    (37, 'Tortilla Chips', 'Snacks', 3.49, '13 oz', '🌽', ['Vegan', 'Gluten-Free'], None, 4.5, 'Restaurant-style white corn tortilla chips.'),
    (38, 'Salsa', 'Snacks', 3.29, '16 oz', '🍅', ['Vegan', 'Gluten-Free', 'Local'], None, 4.4, 'Medium chunky salsa from a local Iowa maker.'),
    (39, 'Popcorn', 'Snacks', 3.99, '6 ct', '🍿', ['Vegan', 'Gluten-Free'], 2.99, 4.2, 'Microwave butter popcorn.'),
    (40, 'Trail Mix', 'Snacks', 5.99, '26 oz', '🥜', ['Vegan', 'Gluten-Free'], None, 4.6, 'Nuts, raisins and chocolate pieces.'),
]

PRODUCTS = [
    {
        'id': p[0], 'name': p[1], 'category': p[2], 'price': p[3], 'unit': p[4],
        'emoji': p[5], 'tags': p[6], 'sale_price': p[7], 'rating': p[8], 'description': p[9],
    }
    for p in _PRODUCTS
]
PRODUCTS_BY_ID = {p['id']: p for p in PRODUCTS}

# Each ingredient optionally links to a product id; pantry staples like salt stay unlinked.
RECIPES = [
    {
        'id': 1, 'name': 'Classic Beef Tacos', 'emoji': '🌮', 'minutes': 25, 'serves': 4,
        'difficulty': 'Easy', 'category': 'Dinner',
        'summary': 'Weeknight tacos with seasoned beef and fresh toppings.',
        'ingredients': [
            {'product_id': 10, 'qty': '1 lb ground beef'},
            {'product_id': 28, 'qty': '1 packet taco seasoning'},
            {'product_id': 20, 'qty': '8 flour tortillas'},
            {'product_id': 16, 'qty': '1 cup shredded cheddar'},
            {'product_id': 4, 'qty': '2 Roma tomatoes, diced'},
            {'product_id': 3, 'qty': '1 avocado, sliced'},
            {'product_id': 8, 'qty': '1 lime, cut in wedges'},
        ],
        'steps': [
            'Brown the ground beef in a skillet over medium-high heat; drain.',
            'Stir in taco seasoning and 2/3 cup water. Simmer 5 minutes.',
            'Warm tortillas, then fill with beef, cheese, tomato and avocado.',
            'Serve with lime wedges.',
        ],
    },
    {
        'id': 2, 'name': 'Garlic Butter Salmon', 'emoji': '🐟', 'minutes': 20, 'serves': 2,
        'difficulty': 'Easy', 'category': 'Dinner',
        'summary': 'Pan-seared salmon with a garlic butter sauce over jasmine rice.',
        'ingredients': [
            {'product_id': 12, 'qty': '1 lb salmon fillet'},
            {'product_id': 17, 'qty': '3 tbsp butter'},
            {'product_id': 6, 'qty': '4 cloves garlic, minced'},
            {'product_id': 26, 'qty': '1 cup jasmine rice'},
            {'product_id': 9, 'qty': '2 cups baby spinach'},
            {'product_id': None, 'qty': 'Salt and pepper to taste'},
        ],
        'steps': [
            'Cook rice according to package directions.',
            'Season salmon and sear skin-side up 4 minutes; flip and cook 3 more.',
            'Add butter and garlic to the pan, spoon over the salmon.',
            'Wilt spinach in the pan juices and serve everything over rice.',
        ],
    },
    {
        'id': 3, 'name': 'Spaghetti Marinara', 'emoji': '🍝', 'minutes': 30, 'serves': 4,
        'difficulty': 'Easy', 'category': 'Dinner',
        'summary': 'A family favorite with garlic bread on the side.',
        'ingredients': [
            {'product_id': 23, 'qty': '1 lb spaghetti'},
            {'product_id': 24, 'qty': '1 jar marinara sauce'},
            {'product_id': 10, 'qty': '1 lb ground beef (optional)'},
            {'product_id': 5, 'qty': '1 onion, diced'},
            {'product_id': 6, 'qty': '3 cloves garlic'},
            {'product_id': 19, 'qty': '1 loaf French bread'},
            {'product_id': 17, 'qty': '4 tbsp butter'},
        ],
        'steps': [
            'Boil spaghetti in salted water until al dente.',
            'Brown beef with onion and garlic, then add marinara and simmer.',
            'Slice French bread, spread with garlic butter, and toast 8 minutes at 400°F.',
            'Toss pasta with sauce and serve with garlic bread.',
        ],
    },
    {
        'id': 4, 'name': 'Strawberry Yogurt Parfait', 'emoji': '🍓', 'minutes': 5, 'serves': 2,
        'difficulty': 'Easy', 'category': 'Breakfast',
        'summary': 'Layers of Greek yogurt, berries and crunchy trail mix.',
        'ingredients': [
            {'product_id': 18, 'qty': '2 cups Greek yogurt'},
            {'product_id': 2, 'qty': '1 cup strawberries, sliced'},
            {'product_id': 1, 'qty': '1 banana, sliced'},
            {'product_id': 40, 'qty': '1/2 cup trail mix'},
        ],
        'steps': [
            'Layer yogurt, fruit and trail mix in two glasses.',
            'Repeat the layers and serve immediately.',
        ],
    },
    {
        'id': 5, 'name': 'Iowa Pork Chops & Sweet Corn', 'emoji': '🌽', 'minutes': 35, 'serves': 4,
        'difficulty': 'Medium', 'category': 'Dinner',
        'summary': 'A Midwest summer classic straight from the grill.',
        'ingredients': [
            {'product_id': 13, 'qty': '4 Iowa pork chops'},
            {'product_id': 7, 'qty': '4 ears sweet corn'},
            {'product_id': 17, 'qty': '4 tbsp butter'},
            {'product_id': 25, 'qty': '2 tbsp olive oil'},
            {'product_id': 6, 'qty': '2 cloves garlic'},
        ],
        'steps': [
            'Rub chops with olive oil, garlic, salt and pepper.',
            'Grill chops 5–6 minutes per side to 145°F; rest 5 minutes.',
            'Grill corn 10 minutes, turning often, then brush with butter.',
        ],
    },
    {
        'id': 6, 'name': 'Chicken Fried Rice', 'emoji': '🍚', 'minutes': 25, 'serves': 4,
        'difficulty': 'Medium', 'category': 'Dinner',
        'summary': 'Better than takeout, ready in under 30 minutes.',
        'ingredients': [
            {'product_id': 11, 'qty': '1 lb chicken breast, diced'},
            {'product_id': 26, 'qty': '3 cups cooked jasmine rice'},
            {'product_id': 15, 'qty': '2 eggs'},
            {'product_id': 33, 'qty': '1 bag mixed vegetables'},
            {'product_id': 30, 'qty': '3 tbsp soy sauce'},
            {'product_id': 6, 'qty': '2 cloves garlic'},
        ],
        'steps': [
            'Stir-fry chicken until cooked through; set aside.',
            'Scramble eggs in the same pan, then add vegetables and garlic.',
            'Add rice and soy sauce; toss over high heat 3 minutes.',
            'Return chicken to the pan and serve.',
        ],
    },
    {
        'id': 7, 'name': 'Game Day Nachos', 'emoji': '🧀', 'minutes': 15, 'serves': 6,
        'difficulty': 'Easy', 'category': 'Snacks',
        'summary': 'Loaded sheet-pan nachos for a crowd.',
        'ingredients': [
            {'product_id': 37, 'qty': '1 bag tortilla chips'},
            {'product_id': 27, 'qty': '1 can black beans, drained'},
            {'product_id': 16, 'qty': '2 cups shredded cheddar'},
            {'product_id': 38, 'qty': '1 jar salsa'},
            {'product_id': 3, 'qty': '2 avocados'},
            {'product_id': 8, 'qty': '1 lime'},
        ],
        'steps': [
            'Spread chips on a sheet pan; top with beans and cheese.',
            'Bake at 400°F for 8 minutes until melted.',
            'Top with salsa and mashed avocado with lime.',
        ],
    },
    {
        'id': 8, 'name': 'Banana Bread', 'emoji': '🍞', 'minutes': 70, 'serves': 8,
        'difficulty': 'Medium', 'category': 'Dessert',
        'summary': 'Moist, tender banana bread — the best use for ripe bananas.',
        'ingredients': [
            {'product_id': 1, 'qty': '3 ripe bananas'},
            {'product_id': 29, 'qty': '2 cups flour'},
            {'product_id': 17, 'qty': '1/2 cup butter, melted'},
            {'product_id': 15, 'qty': '2 eggs'},
            {'product_id': None, 'qty': '3/4 cup sugar, 1 tsp baking soda'},
        ],
        'steps': [
            'Mash bananas and mix with melted butter, eggs and sugar.',
            'Stir in flour and baking soda until just combined.',
            'Bake in a greased loaf pan at 350°F for 55–60 minutes.',
        ],
    },
]
RECIPES_BY_ID = {r['id']: r for r in RECIPES}

STORES = [
    {'id': 1, 'name': 'West Des Moines – Valley West', 'city': 'West Des Moines', 'state': 'IA', 'address': '1700 Valley West Dr', 'phone': '(515) 555-0101', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online', 'Wahlburgers']},
    {'id': 2, 'name': 'Des Moines – Ingersoll', 'city': 'Des Moines', 'state': 'IA', 'address': '3221 Ingersoll Ave', 'phone': '(515) 555-0102', 'hours': '6 AM – 10 PM', 'amenities': ['Pharmacy', 'Aisles Online', 'Floral']},
    {'id': 3, 'name': 'Ankeny – North', 'city': 'Ankeny', 'state': 'IA', 'address': '410 N Ankeny Blvd', 'phone': '(515) 555-0103', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online']},
    {'id': 4, 'name': 'Ames – Lincoln Way', 'city': 'Ames', 'state': 'IA', 'address': '3800 W Lincoln Way', 'phone': '(515) 555-0104', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online', 'Floral']},
    {'id': 5, 'name': 'Cedar Rapids – Collins Rd', 'city': 'Cedar Rapids', 'state': 'IA', 'address': '1843 Collins Rd NE', 'phone': '(319) 555-0105', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Fuel Saver', 'Aisles Online']},
    {'id': 6, 'name': 'Iowa City – Waterfront', 'city': 'Iowa City', 'state': 'IA', 'address': '1720 Waterfront Dr', 'phone': '(319) 555-0106', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Aisles Online', 'Floral']},
    {'id': 7, 'name': 'Omaha – Dodge St', 'city': 'Omaha', 'state': 'NE', 'address': '7910 W Dodge Rd', 'phone': '(402) 555-0107', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online']},
    {'id': 8, 'name': 'Lincoln – South', 'city': 'Lincoln', 'state': 'NE', 'address': '5020 Nebraska Pkwy', 'phone': '(402) 555-0108', 'hours': '6 AM – 10 PM', 'amenities': ['Pharmacy', 'Aisles Online']},
    {'id': 9, 'name': 'Kansas City – Briarcliff', 'city': 'Kansas City', 'state': 'MO', 'address': '4100 N Mulberry Dr', 'phone': '(816) 555-0109', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Aisles Online', 'Wahlburgers']},
    {'id': 10, 'name': 'Columbia – Nifong', 'city': 'Columbia', 'state': 'MO', 'address': '3100 W Broadway', 'phone': '(573) 555-0110', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Fuel Saver', 'Aisles Online']},
    {'id': 11, 'name': 'Overland Park – 135th St', 'city': 'Overland Park', 'state': 'KS', 'address': '6655 W 135th St', 'phone': '(913) 555-0111', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online', 'Floral']},
    {'id': 12, 'name': 'Sioux Falls – 41st St', 'city': 'Sioux Falls', 'state': 'SD', 'address': '3000 S Minnesota Ave', 'phone': '(605) 555-0112', 'hours': '6 AM – 10 PM', 'amenities': ['Pharmacy', 'Aisles Online']},
    {'id': 13, 'name': 'Rochester – Barlow Plaza', 'city': 'Rochester', 'state': 'MN', 'address': '500 37th St NW', 'phone': '(507) 555-0113', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online']},
    {'id': 14, 'name': 'Madison – Fitchburg', 'city': 'Fitchburg', 'state': 'WI', 'address': '2920 Fitchrona Rd', 'phone': '(608) 555-0114', 'hours': '6 AM – 11 PM', 'amenities': ['Pharmacy', 'Market Grille', 'Aisles Online', 'Floral']},
    {'id': 15, 'name': 'Moline – Avenue of the Cities', 'city': 'Moline', 'state': 'IL', 'address': '4064 Avenue of the Cities', 'phone': '(309) 555-0115', 'hours': '6 AM – 10 PM', 'amenities': ['Pharmacy', 'Fuel Saver', 'Aisles Online']},
    {'id': 16, 'name': 'Fargo – 13th Ave', 'city': 'Fargo', 'state': 'ND', 'address': '4325 13th Ave S', 'phone': '(701) 555-0116', 'hours': '6 AM – 10 PM', 'amenities': ['Pharmacy', 'Aisles Online']},
]

STATE_NAMES = {
    'IA': 'Iowa', 'NE': 'Nebraska', 'MO': 'Missouri', 'KS': 'Kansas',
    'SD': 'South Dakota', 'MN': 'Minnesota', 'WI': 'Wisconsin', 'IL': 'Illinois', 'ND': 'North Dakota',
}

AMENITIES = ['Pharmacy', 'Market Grille', 'Fuel Saver', 'Aisles Online', 'Floral', 'Wahlburgers']

COUPONS = [
    {'id': 1, 'title': '$2 off Atlantic Salmon', 'detail': 'Any fresh salmon fillet purchase of 1 lb or more.', 'expires': 'Nov 3', 'icon': 'fa-fish'},
    {'id': 2, 'title': 'Buy 2, Get 1 Free Snacks', 'detail': 'Mix & match chips, popcorn and trail mix.', 'expires': 'Nov 3', 'icon': 'fa-cookie-bite'},
    {'id': 3, 'title': '10¢/gal Fuel Saver', 'detail': 'Earn when you spend $50+ on groceries.', 'expires': 'Nov 10', 'icon': 'fa-gas-pump'},
    {'id': 4, 'title': '$5 off $50 Aisles Online', 'detail': 'First pickup or delivery order.', 'expires': 'Dec 31', 'icon': 'fa-cart-shopping'},
    {'id': 5, 'title': '20% off Bakery Cookies', 'detail': 'Any dozen from the in-store bakery.', 'expires': 'Nov 3', 'icon': 'fa-cookie'},
    {'id': 6, 'title': 'Free Coffee with Breakfast', 'detail': 'At the Market Grille, Mon–Fri before 10 AM.', 'expires': 'Nov 30', 'icon': 'fa-mug-hot'},
]

PROMOS = [
    {'title': 'Fall Harvest Sale', 'subtitle': 'Fresh Midwest produce at prices that fall into place.', 'cta': 'Shop Produce', 'category': 'Produce', 'icon': 'fa-leaf'},
    {'title': 'Fuel Saver + Perks', 'subtitle': 'Earn up to 50¢ off every gallon with Hy-Vee Perks.', 'cta': 'See Deals', 'category': None, 'icon': 'fa-gas-pump'},
    {'title': 'Game Day Headquarters', 'subtitle': 'Chips, salsa and frozen pizza — all on sale this week.', 'cta': 'Shop Snacks', 'category': 'Snacks', 'icon': 'fa-football'},
]

LEADERSHIP = [
    {'name': 'Roman', 'title': 'Chief Executive Officer', 'initials': 'R', 'color': 'navy',
     'bio': 'Roman leads Hy-Vee\'s vision to make lives easier, healthier and happier — and championed the launch of this new digital storefront.'},
    {'name': 'Colleen', 'title': 'Chief Marketing Officer', 'initials': 'C', 'color': 'navy',
     'bio': 'Colleen oversees the Hy-Vee brand and selected navy blue as the foundation of our new look.'},
    {'name': 'Kellen', 'title': 'Co-Chief Marketing Officer', 'initials': 'K', 'color': 'green',
     'bio': 'Kellen co-leads marketing with a focus on fresh, local and seasonal — the inspiration behind our green accents.'},
    {'name': 'Margaret', 'title': 'Brand & Design Lead', 'initials': 'M', 'color': 'baby',
     'bio': 'Margaret shapes the customer experience across stores and online, and chose baby blue to round out our palette.'},
]

FAQS = [
    ('How does Aisles Online pickup work?', 'Shop online, choose a pickup window, and pull into the marked Aisles Online stalls. A Hy-Vee employee will bring your groceries to your car.'),
    ('What is your return policy?', 'If you\'re not completely satisfied, bring the item and receipt to any customer service desk for a full refund or replacement. That\'s our Hy-Vee guarantee.'),
    ('How do I earn Fuel Saver rewards?', 'Link your Hy-Vee Perks account and buy participating items. Discounts load automatically and can be redeemed at any Hy-Vee Fast & Fresh location.'),
    ('Can I transfer a prescription?', 'Yes. Call or visit any Hy-Vee pharmacy with your current pharmacy\'s information and we\'ll handle the rest.'),
    ('Do you offer catering?', 'Absolutely — from party trays to full-service events. Ask at the deli or call your local store.'),
    ('How do I reset my password?', 'Use the "Contact Us" page and our team will help you regain access to your account.'),
]
