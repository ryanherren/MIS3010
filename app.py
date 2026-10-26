from flask import (Flask, render_template, jsonify, request, session,
                   redirect, url_for, flash, abort, Response)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import hashlib
import json
import os
import secrets

import data

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cyclone-tickets-dev-key')

SERVICE_FEE = 3.00  # per ticket
MAX_PER_ORDER = 8


# ---------- helpers ----------
def current_user():
    email = session.get('user')
    return data.USERS.get(email) and {'email': email, **data.USERS[email]}


def login_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if not current_user():
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login', next=request.path))
        return f(*a, **kw)
    return wrapper


def cart_lines():
    """Resolve the session cart into display lines with prices."""
    lines = []
    for item in session.get('cart', []):
        ev = data.EVENTS.get(item['event'])
        inv = data.INVENTORY.get(item['event'], {}).get(item['section'])
        if not ev or not inv:
            continue
        sec = data.VENUES[ev['venue_key']]['sections'][item['section']]
        lines.append({
            'event': ev, 'sport': data.SPORTS[ev['sport']], 'section_key': item['section'],
            'section': sec, 'qty': item['qty'], 'price': inv['price'],
            'avail': inv['avail'], 'subtotal': inv['price'] * item['qty'],
        })
    return lines


def cart_totals(lines):
    subtotal = sum(l['subtotal'] for l in lines)
    fees = sum(l['qty'] for l in lines) * SERVICE_FEE
    return {'subtotal': subtotal, 'fees': fees, 'total': subtotal + fees,
            'count': sum(l['qty'] for l in lines)}


@app.context_processor
def inject_globals():
    count = sum(i['qty'] for i in session.get('cart', []))
    return {'user': current_user(), 'cart_count': count, 'sports': data.SPORTS,
            'now_year': datetime.now().year}


@app.template_filter('money')
def money(v):
    return f'${v:,.2f}'


@app.template_filter('gamedate')
def gamedate(d):
    return d.strftime('%a, %b %-d, %Y')


@app.template_filter('gametime')
def gametime(d):
    if d.hour == 0 and d.minute == 0:
        return 'Time TBA'
    return d.strftime('%-I:%M %p')


def sport_events(sport_key=None):
    evs = [e for e in data.EVENTS.values() if sport_key in (None, e['sport'])]
    return sorted(evs, key=lambda e: e['when'])


def event_stats(ev):
    inv = data.INVENTORY[ev['id']]
    return {'avail': sum(s['avail'] for s in inv.values()),
            'from': min(s['price'] for s in inv.values())}


# ---------- pages ----------
@app.route('/')
def home():
    featured = [e for e in sport_events() if e['when'].date() >= datetime.now().date()][:4]
    return render_template('home.html', featured=featured, stats=event_stats)


@app.route('/sports/<sport_key>')
def sport(sport_key):
    if sport_key not in data.SPORTS:
        abort(404)
    return render_template('sport.html', sport=data.SPORTS[sport_key], key=sport_key,
                           events=sport_events(sport_key), stats=event_stats,
                           venue=data.VENUES[data.SPORTS[sport_key]['venue']])


@app.route('/event/<int:event_id>')
def event(event_id):
    ev = data.EVENTS.get(event_id)
    if not ev:
        abort(404)
    venue = data.VENUES[ev['venue_key']]
    rows = []
    for key, sec in venue['sections'].items():
        inv = data.INVENTORY[event_id][key]
        rows.append({'key': key, **sec, **inv})
    return render_template('event.html', ev=ev, sport=data.SPORTS[ev['sport']],
                           venue=venue, rows=rows, max_qty=MAX_PER_ORDER)


@app.route('/about')
def about():
    return render_template('about.html')


# ---------- cart ----------
@app.route('/cart')
def cart():
    lines = cart_lines()
    return render_template('cart.html', lines=lines, totals=cart_totals(lines), fee=SERVICE_FEE)


@app.route('/cart/add', methods=['POST'])
def cart_add():
    try:
        event_id = int(request.form['event'])
        qty = int(request.form['qty'])
    except (KeyError, ValueError):
        abort(400)
    key = request.form.get('section', '')
    inv = data.INVENTORY.get(event_id, {}).get(key)
    if not inv or qty < 1:
        abort(400)
    cart = session.get('cart', [])
    existing = next((i for i in cart if i['event'] == event_id and i['section'] == key), None)
    new_qty = (existing['qty'] if existing else 0) + qty
    if new_qty > min(MAX_PER_ORDER, inv['avail']):
        flash(f'Only {min(MAX_PER_ORDER, inv["avail"])} tickets are available for that section per order.', 'danger')
        return redirect(url_for('event', event_id=event_id))
    if existing:
        existing['qty'] = new_qty
    else:
        cart.append({'event': event_id, 'section': key, 'qty': qty})
    session['cart'] = cart
    flash('Added to your cart.', 'success')
    return redirect(url_for('cart'))


@app.route('/cart/remove', methods=['POST'])
def cart_remove():
    event_id, key = int(request.form['event']), request.form['section']
    session['cart'] = [i for i in session.get('cart', [])
                       if not (i['event'] == event_id and i['section'] == key)]
    return redirect(url_for('cart'))


# ---------- checkout ----------
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    lines = cart_lines()
    if not lines:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('home'))
    totals = cart_totals(lines)
    if request.method == 'POST':
        digits = ''.join(c for c in request.form.get('card', '') if c.isdigit())
        if len(digits) < 13 or not request.form.get('name', '').strip():
            flash('Enter the name on the card and a valid card number (demo: any 16 digits).', 'danger')
            return render_template('checkout.html', lines=lines, totals=totals)
        for l in lines:
            if l['qty'] > l['avail']:
                flash(f'Sorry, only {l["avail"]} tickets are left for {l["section"]["name"]}.', 'danger')
                return redirect(url_for('cart'))
        order_id = 'ISU-' + secrets.token_hex(3).upper()
        ticket_ids = []
        for l in lines:
            inv = data.INVENTORY[l['event']['id']][l['section_key']]
            sold = sum(1 for t in data.TICKETS.values()
                       if t['event'] == l['event']['id'] and t['section_key'] == l['section_key'])
            inv['avail'] -= l['qty']
            for n in range(l['qty']):
                tid = 'CY' + secrets.token_hex(4).upper()
                ga = l['section'].get('ga')
                data.TICKETS[tid] = {
                    'id': tid, 'order': order_id, 'event': l['event']['id'],
                    'section_key': l['section_key'], 'price': l['price'], 'owner': session['user'],
                    'row': None if ga else (sold + n) // 20 + 1,
                    'seat': None if ga else (sold + n) % 20 + 1,
                }
                ticket_ids.append(tid)
        data.ORDERS[order_id] = {'id': order_id, 'user': session['user'], 'tickets': ticket_ids,
                                 'total': totals['total'], 'placed': datetime.now()}
        session['cart'] = []
        return redirect(url_for('confirmation', order_id=order_id))
    return render_template('checkout.html', lines=lines, totals=totals)


def ticket_view(t):
    ev = data.EVENTS[t['event']]
    return {**t, 'ev': ev, 'sport': data.SPORTS[ev['sport']],
            'section': data.VENUES[ev['venue_key']]['sections'][t['section_key']]}


@app.route('/confirmation/<order_id>')
@login_required
def confirmation(order_id):
    order = data.ORDERS.get(order_id)
    if not order or order['user'] != session['user']:
        abort(404)
    return render_template('confirmation.html', order=order,
                           tickets=[ticket_view(data.TICKETS[t]) for t in order['tickets']])


@app.route('/my-tickets')
@login_required
def my_tickets():
    ts = [ticket_view(t) for t in data.TICKETS.values() if t['owner'] == session['user']]
    ts.sort(key=lambda t: t['ev']['when'])
    return render_template('my_tickets.html', tickets=ts)


# ---------- wallet ----------
def own_ticket(tid):
    t = data.TICKETS.get(tid)
    if not t or t['owner'] != session.get('user'):
        abort(404)
    return t


def barcode_bars(tid):
    digest = hashlib.sha256(tid.encode()).digest()
    bits = ''.join(f'{b:08b}' for b in digest)[:120]
    return [(i, 2 if bits[i] == '1' else 1) for i in range(len(bits))]


@app.route('/wallet/<tid>')
@login_required
def wallet(tid):
    t = ticket_view(own_ticket(tid))
    return render_template('wallet.html', t=t, bars=barcode_bars(tid))


@app.route('/wallet/<tid>/pass.json')
@login_required
def wallet_pass(tid):
    t = ticket_view(own_ticket(tid))
    # Demo payload in PassKit field layout. A real .pkpass must be signed with an
    # Apple Developer certificate, which we would add before launch.
    payload = {
        'formatVersion': 1, 'passTypeIdentifier': 'pass.edu.iastate.cyclonetickets',
        'serialNumber': t['id'], 'organizationName': 'Iowa State Athletics',
        'description': f"{t['sport']['name']} vs {t['ev']['opponent']}",
        'backgroundColor': 'rgb(200,16,46)', 'foregroundColor': 'rgb(241,190,72)',
        'barcode': {'format': 'PKBarcodeFormatQR', 'message': t['id'], 'messageEncoding': 'iso-8859-1'},
        'eventTicket': {
            'primaryFields': [{'key': 'event', 'label': 'GAME', 'value': f"Cyclones vs {t['ev']['opponent']}"}],
            'secondaryFields': [{'key': 'when', 'label': 'DATE', 'value': f"{gamedate(t['ev']['when'])} {gametime(t['ev']['when'])}"},
                                {'key': 'venue', 'label': 'VENUE', 'value': t['ev']['venue']}],
            'auxiliaryFields': [{'key': 'section', 'label': 'SECTION', 'value': t['section']['name']},
                                {'key': 'seat', 'label': 'ROW/SEAT',
                                 'value': 'GA' if not t['row'] else f"{t['row']}/{t['seat']}"}],
        },
    }
    return Response(json.dumps(payload, indent=2), mimetype='application/json',
                    headers={'Content-Disposition': f'attachment; filename={tid}-pass.json'})


# ---------- auth ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        pw = request.form.get('password', '')
        if not name or '@' not in email or len(pw) < 6:
            flash('Enter your name, a valid email, and a password of at least 6 characters.', 'danger')
        elif email in data.USERS:
            flash('An account with that email already exists. Try logging in.', 'danger')
        else:
            data.USERS[email] = {'name': name, 'pw': generate_password_hash(pw)}
            session['user'] = email
            flash(f'Welcome to Cyclone Tickets, {name.split()[0]}!', 'success')
            return redirect(request.args.get('next') or url_for('home'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        u = data.USERS.get(email)
        if u and check_password_hash(u['pw'], request.form.get('password', '')):
            session['user'] = email
            nxt = request.args.get('next', '')
            return redirect(nxt if nxt.startswith('/') and not nxt.startswith('//') else url_for('home'))
        flash('Incorrect email or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# API Routes
@app.route('/api/availability/<int:event_id>')
def api_availability(event_id):
    inv = data.INVENTORY.get(event_id)
    if inv is None:
        abort(404)
    return jsonify({k: v for k, v in inv.items()})


@app.route('/api/time')
def api_time():
    return jsonify({
        'datetime': datetime.now().isoformat(),
        'timestamp': datetime.now().timestamp()
    })


if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    app.run(debug=debug, host='0.0.0.0', port=port)
