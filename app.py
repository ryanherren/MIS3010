from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from urllib.parse import urlparse
import os

from store_data import (
    PRODUCTS, PRODUCTS_BY_ID, CATEGORIES, DIETARY_TAGS, RECIPES, RECIPES_BY_ID,
    STORES, STATE_NAMES, AMENITIES, COUPONS, PROMOS, LEADERSHIP, FAQS,
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hy-vee-dev-secret')

# In-memory accounts (reset on every deploy). A demo account is seeded for class.
USERS = {
    'demo@hy-vee.com': {
        'name': 'Demo Shopper',
        'password': generate_password_hash('hyvee123'),
        'clipped': set(),
    }
}
MESSAGES = []


def current_user():
    email = session.get('user')
    return USERS.get(email) if email else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            flash('Please sign in to continue.', 'warning')
            # POST-only actions (clip, checkout) send the user back to the page they came from
            next_url = request.path if request.method == 'GET' else urlparse(request.referrer or '').path
            return redirect(url_for('login', next=next_url or None))
        return view(*args, **kwargs)
    return wrapped


def effective_price(product):
    return product['sale_price'] if product['sale_price'] is not None else product['price']


def recipes_using(product_id):
    return [r for r in RECIPES if any(i['product_id'] == product_id for i in r['ingredients'])]


def cart_items():
    items = []
    for pid, qty in session.get('cart', {}).items():
        product = PRODUCTS_BY_ID.get(int(pid))
        if product:
            items.append({'product': product, 'qty': qty, 'line_total': effective_price(product) * qty})
    return items


def add_to_cart(product_id, qty=1):
    cart = session.get('cart', {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + qty
    session['cart'] = cart


@app.context_processor
def inject_globals():
    return {
        'user': current_user(),
        'cart_count': sum(session.get('cart', {}).values()),
        'price_of': effective_price,
        'year': datetime.now().year,
    }


# Pages
@app.route('/')
def home():
    on_sale = [p for p in PRODUCTS if p['sale_price'] is not None][:8]
    return render_template('home.html', promos=PROMOS, on_sale=on_sale,
                           recipes=RECIPES[:4], categories=CATEGORIES, store_count=len(STORES))


@app.route('/products')
def products():
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    tags = request.args.getlist('tag')
    on_sale = request.args.get('sale') == '1'
    sort = request.args.get('sort', 'featured')
    max_price = request.args.get('max_price', type=float)

    results = PRODUCTS
    if q:
        needle = q.lower()
        results = [p for p in results if needle in p['name'].lower()
                   or needle in p['description'].lower() or needle in p['category'].lower()]
    if category:
        results = [p for p in results if p['category'] == category]
    if tags:
        results = [p for p in results if all(t in p['tags'] for t in tags)]
    if on_sale:
        results = [p for p in results if p['sale_price'] is not None]
    if max_price:
        results = [p for p in results if effective_price(p) <= max_price]

    sorters = {
        'price_asc': lambda p: effective_price(p),
        'price_desc': lambda p: -effective_price(p),
        'name': lambda p: p['name'],
        'rating': lambda p: -p['rating'],
    }
    if sort in sorters:
        results = sorted(results, key=sorters[sort])

    return render_template('products.html', products=results, categories=CATEGORIES,
                           dietary_tags=DIETARY_TAGS, q=q, category=category, tags=tags,
                           on_sale=on_sale, sort=sort, max_price=max_price)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = PRODUCTS_BY_ID.get(product_id) or abort(404)
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    return render_template('product_detail.html', product=product,
                           recipes=recipes_using(product_id), related=related)


@app.route('/recipes')
def recipes():
    category = request.args.get('category', '')
    q = request.args.get('q', '').strip().lower()
    results = RECIPES
    if category:
        results = [r for r in results if r['category'] == category]
    if q:
        results = [r for r in results if q in r['name'].lower() or any(
            i['product_id'] and q in PRODUCTS_BY_ID[i['product_id']]['name'].lower() for i in r['ingredients'])]
    recipe_categories = sorted({r['category'] for r in RECIPES})
    return render_template('recipes.html', recipes=results, recipe_categories=recipe_categories,
                           category=category, q=request.args.get('q', ''))


@app.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = RECIPES_BY_ID.get(recipe_id) or abort(404)
    ingredients = [{**i, 'product': PRODUCTS_BY_ID.get(i['product_id'])} for i in recipe['ingredients']]
    total = sum(effective_price(i['product']) for i in ingredients if i['product'])
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients, total=total)


@app.route('/recipes/<int:recipe_id>/add-all', methods=['POST'])
def recipe_add_all(recipe_id):
    recipe = RECIPES_BY_ID.get(recipe_id) or abort(404)
    pids = {i['product_id'] for i in recipe['ingredients'] if i['product_id']}
    for pid in pids:
        add_to_cart(pid)
    flash(f'Added {len(pids)} ingredients for {recipe["name"]} to your cart.', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))


@app.route('/locations')
def locations():
    q = request.args.get('q', '').strip().lower()
    state = request.args.get('state', '')
    amenity = request.args.get('amenity', '')
    results = STORES
    if q:
        results = [s for s in results if q in s['city'].lower() or q in s['name'].lower() or q in s['address'].lower()]
    if state:
        results = [s for s in results if s['state'] == state]
    if amenity:
        results = [s for s in results if amenity in s['amenities']]
    states = sorted({s['state'] for s in STORES})
    return render_template('locations.html', stores=results, states=states, state_names=STATE_NAMES,
                           amenities=AMENITIES, q=request.args.get('q', ''), state=state, amenity=amenity)


@app.route('/deals')
def deals():
    sale_products = [p for p in PRODUCTS if p['sale_price'] is not None]
    user = current_user()
    clipped = user['clipped'] if user else set()
    return render_template('deals.html', coupons=COUPONS, sale_products=sale_products,
                           promos=PROMOS, clipped=clipped)


@app.route('/deals/clip/<int:coupon_id>', methods=['POST'])
@login_required
def clip_coupon(coupon_id):
    current_user()['clipped'].add(coupon_id)
    flash('Coupon clipped to your Hy-Vee Perks account!', 'success')
    return redirect(url_for('deals'))


@app.route('/leadership')
def leadership():
    return render_template('leadership.html', leaders=LEADERSHIP)


@app.route('/customer-service', methods=['GET', 'POST'])
def customer_service():
    order_result = None
    if request.method == 'POST':
        order = request.form.get('order', '').strip()
        if order:
            order_result = {'order': order, 'status': 'Ready for pickup',
                            'store': STORES[0]['name'], 'window': 'Today, 4:00 – 5:00 PM'}
        else:
            flash('Enter an order number to look it up.', 'warning')
    return render_template('customer_service.html', faqs=FAQS, order_result=order_result)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        if not (name and email and message):
            flash('Please fill out your name, email and message.', 'danger')
        else:
            MESSAGES.append({'name': name, 'email': email, 'topic': request.form.get('topic'),
                             'store': request.form.get('store'), 'message': message,
                             'sent': datetime.now().isoformat()})
            flash(f'Thanks, {name}! Our team will get back to you within one business day.', 'success')
            return redirect(url_for('contact'))
    return render_template('contact.html', stores=STORES)


# Cart
@app.route('/cart')
def cart():
    items = cart_items()
    subtotal = sum(i['line_total'] for i in items)
    savings = sum((i['product']['price'] - effective_price(i['product'])) * i['qty'] for i in items)
    return render_template('cart.html', items=items, subtotal=subtotal, savings=savings, stores=STORES)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    product = PRODUCTS_BY_ID.get(product_id) or abort(404)
    add_to_cart(product_id, max(1, request.form.get('qty', 1, type=int)))
    flash(f'{product["name"]} added to your cart.', 'success')
    return redirect(request.referrer or url_for('products'))


@app.route('/cart/update/<int:product_id>', methods=['POST'])
def cart_update(product_id):
    cart = session.get('cart', {})
    qty = request.form.get('qty', 0, type=int)
    if qty > 0:
        cart[str(product_id)] = qty
    else:
        cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    if not session.get('cart'):
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    session['cart'] = {}
    order_no = datetime.now().strftime('HV%m%d%H%M%S')
    flash(f'Order {order_no} placed! We\'ll text you when it\'s ready for Aisles Online pickup.', 'success')
    return redirect(url_for('account'))


# Accounts
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = USERS.get(email)
        if user and check_password_hash(user['password'], request.form.get('password', '')):
            session['user'] = email
            flash(f'Welcome back, {user["name"]}!', 'success')
            next_url = request.args.get('next', '')
            return redirect(next_url if next_url.startswith('/') and not next_url.startswith('//') else url_for('account'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not (name and email and len(password) >= 6):
            flash('Name, email and a password of at least 6 characters are required.', 'danger')
        elif email in USERS:
            flash('An account with that email already exists.', 'warning')
        else:
            USERS[email] = {'name': name, 'password': generate_password_hash(password), 'clipped': set()}
            session['user'] = email
            flash(f'Welcome to Hy-Vee Perks, {name}!', 'success')
            return redirect(url_for('account'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been signed out.', 'info')
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    user = current_user()
    clipped = [c for c in COUPONS if c['id'] in user['clipped']]
    return render_template('account.html', email=session['user'], clipped=clipped)


# API Routes
@app.route('/api/products')
def api_products():
    return jsonify(PRODUCTS)


@app.route('/api/time')
def api_time():
    return jsonify({
        'datetime': datetime.now().isoformat(),
        'timestamp': datetime.now().timestamp()
    })


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    app.run(debug=debug, host='0.0.0.0', port=port)
