from flask import Flask, render_template, jsonify, request, abort
from datetime import datetime, date, timedelta
import os

import data

app = Flask(__name__)

BOOKINGS = []  # in-memory; resets on restart
ORDERS = []
PRODUCT_BY_ID = {p['id']: p for p in data.PRODUCTS}


# Pages
@app.route('/')
def home():
    return render_template('home.html', services=data.SERVICES, plans=data.PLANS,
                           reviews=data.REVIEWS[:3], projects=data.PROJECTS,
                           featured=[PRODUCT_BY_ID[i] for i in ('fresh-cut-blush', 'sod-solid-lipstick', 'weed-whacker-mascara')])

@app.route('/services')
def services():
    return render_template('services.html', services=data.SERVICES, plans=data.PLANS)

@app.route('/quote')
def quote():
    return render_template('quote.html', services=data.SERVICES, frequency=data.FREQUENCY)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', projects=data.PROJECTS)

@app.route('/book')
def book():
    return render_template('book.html', services=data.SERVICES, slots=data.TIME_SLOTS)

@app.route('/reviews')
def reviews():
    avg = sum(r['stars'] for r in data.REVIEWS) / len(data.REVIEWS)
    return render_template('reviews.html', reviews=data.REVIEWS, avg=round(avg, 1))

@app.route('/shop')
def shop():
    return render_template('shop.html', products=data.PRODUCTS, categories=data.CATEGORIES)

@app.route('/shop/<pid>')
def product(pid):
    item = PRODUCT_BY_ID.get(pid)
    if not item:
        abort(404)
    related = [p for p in data.PRODUCTS if p['cat'] == item['cat'] and p['id'] != pid][:3]
    cat = next(c for c in data.CATEGORIES if c['id'] == item['cat'])
    return render_template('product.html', p=item, related=related, cat=cat)

@app.route('/bundle')
def bundle():
    b = data.BUNDLE
    box = [PRODUCT_BY_ID[i] for i in b['beauty_box']['items']]
    item = PRODUCT_BY_ID[b['id']]
    return render_template('bundle.html', b=b, box=box, item=item,
                           box_value=round(sum(p['price'] for p in box), 2))

@app.route('/cart')
def cart():
    return render_template('cart.html', free_over=data.FREE_SHIPPING_OVER)

@app.route('/about')
def about():
    return render_template('about.html', team=data.TEAM)

@app.route('/faq')
def faq():
    return render_template('faq.html', faqs=data.FAQS)


# API
@app.route('/api/quote', methods=['POST'])
def api_quote():
    body = request.get_json(silent=True) or {}
    try:
        sqft = int(body.get('sqft', 0))
    except (TypeError, ValueError):
        sqft = 0
    if sqft < 500 or sqft > 200000:
        return jsonify({'error': 'Enter a lawn size between 500 and 200,000 sq ft.'}), 400
    selected = [s for s in data.SERVICES if s['id'] in body.get('services', [])]
    if not selected:
        return jsonify({'error': 'Choose at least one service.'}), 400
    freq = data.FREQUENCY.get(body.get('frequency'), data.FREQUENCY['once'])

    lines, total = [], 0.0
    for s in selected:
        price = max(s['min'], sqft * s['per_sqft'])
        # recurring discount only applies to mowing-type visits, not one-off jobs
        if s['id'] in ('mowing', 'fertilize', 'trim'):
            price *= freq['mult']
        lines.append({'name': s['name'], 'price': round(price, 2)})
        total += price
    if len(selected) >= 3:
        discount = round(total * 0.10, 2)
        total -= discount
    else:
        discount = 0
    return jsonify({'lines': lines, 'discount': discount, 'total': round(total, 2),
                    'frequency': freq['label']})

@app.route('/api/availability')
def api_availability():
    day = request.args.get('date', '')
    try:
        d = date.fromisoformat(day)
    except ValueError:
        return jsonify({'error': 'Invalid date'}), 400
    if d.weekday() == 6 or d <= date.today() - timedelta(days=1):
        return jsonify({'date': day, 'slots': []})
    taken = {b['slot'] for b in BOOKINGS if b['date'] == day}
    # deterministic "busy" slots so the calendar feels real
    busy = {data.TIME_SLOTS[(d.day + i) % len(data.TIME_SLOTS)] for i in range(2)}
    slots = [{'time': t, 'available': t not in taken and t not in busy} for t in data.TIME_SLOTS]
    return jsonify({'date': day, 'slots': slots})

@app.route('/api/book', methods=['POST'])
def api_book():
    b = request.get_json(silent=True) or {}
    required = ['name', 'email', 'phone', 'address', 'date', 'slot', 'service']
    if any(not str(b.get(k, '')).strip() for k in required):
        return jsonify({'error': 'Please fill in every field.'}), 400
    if any(x['date'] == b['date'] and x['slot'] == b['slot'] for x in BOOKINGS):
        return jsonify({'error': 'That time was just taken. Please pick another.'}), 409
    b = {k: str(b[k]).strip() for k in required}
    BOOKINGS.append(b)
    return jsonify({'ok': True, 'confirmation': f"BB-{len(BOOKINGS):04d}", 'booking': b})

def price_cart(raw):
    """Price a cart {product_id: qty} from server-side prices only."""
    items, subtotal = [], 0.0
    for pid, qty in (raw or {}).items():
        p = PRODUCT_BY_ID.get(pid)
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            continue
        if not p or qty < 1:
            continue
        qty = min(qty, 20)
        line = round(p['price'] * qty, 2)
        items.append({'id': pid, 'name': p['name'], 'shade': p['shade'], 'color': p['color'],
                      'icon': p['icon'], 'price': p['price'], 'qty': qty, 'line': line})
        subtotal += line
    subtotal = round(subtotal, 2)
    shipping = 0 if (not items or subtotal >= data.FREE_SHIPPING_OVER) else data.SHIPPING_FLAT
    tax = round(subtotal * data.TAX_RATE, 2)
    return {'items': items, 'subtotal': subtotal, 'shipping': shipping, 'tax': tax,
            'total': round(subtotal + shipping + tax, 2), 'count': sum(i['qty'] for i in items)}

@app.route('/api/cart', methods=['POST'])
def api_cart():
    return jsonify(price_cart((request.get_json(silent=True) or {}).get('cart')))

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    body = request.get_json(silent=True) or {}
    priced = price_cart(body.get('cart'))
    if not priced['items']:
        return jsonify({'error': 'Your cart is empty.'}), 400
    required = ['name', 'email', 'address', 'city', 'zip']
    if any(not str(body.get(k, '')).strip() for k in required):
        return jsonify({'error': 'Please fill in your shipping details.'}), 400
    ORDERS.append({'customer': {k: str(body[k]).strip() for k in required}, **priced})
    return jsonify({'ok': True, 'order': f"BBB-{len(ORDERS):04d}", 'total': priced['total'],
                    'email': str(body['email']).strip()})

@app.route('/api/time')
def api_time():
    return jsonify({'datetime': datetime.now().isoformat(),
                    'timestamp': datetime.now().timestamp()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
