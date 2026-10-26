// Blush & Blade site scripts
document.addEventListener('DOMContentLoaded', () => {
    initBeforeAfter();
    initQuote();
    initBooking();
    initShop();
    initCart();
    updateBadge();
});

const money = n => '$' + Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function initBeforeAfter() {
    document.querySelectorAll('.ba').forEach(ba => {
        const range = ba.querySelector('.ba-range');
        const before = ba.querySelector('.ba-before');
        const handle = ba.querySelector('.ba-handle');
        const update = () => {
            const v = range.value;
            before.style.clipPath = `inset(0 ${100 - v}% 0 0)`;
            handle.style.left = v + '%';
        };
        range.addEventListener('input', update);
        update();
    });
}

function initQuote() {
    const form = document.getElementById('quote-form');
    if (!form) return;
    const out = document.getElementById('quote-result');
    const sqftInput = form.querySelector('[name=sqft]');
    const sqftLabel = document.getElementById('sqft-label');

    async function recalc() {
        sqftLabel.textContent = Number(sqftInput.value).toLocaleString();
        const services = [...form.querySelectorAll('[name=service]:checked')].map(i => i.value);
        if (!services.length) {
            out.innerHTML = '<p class="text-muted mb-0">Select at least one service to see your price.</p>';
            return;
        }
        const res = await fetch('/api/quote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ services, sqft: sqftInput.value, frequency: form.querySelector('[name=frequency]:checked').value })
        });
        const q = await res.json();
        if (!res.ok) { out.innerHTML = `<p class="text-danger mb-0">${q.error}</p>`; return; }
        out.innerHTML =
            q.lines.map(l => `<div class="quote-line"><span>${l.name}</span><strong>${money(l.price)}</strong></div>`).join('') +
            (q.discount ? `<div class="quote-line text-success"><span><i class="fas fa-tag me-1"></i>Bundle discount (10%)</span><strong>-${money(q.discount)}</strong></div>` : '') +
            `<div class="mt-3 text-muted small">${q.frequency} service</div>` +
            `<div class="quote-total">${money(q.total)}</div>` +
            `<a href="/book" class="btn btn-pink w-100 mt-3"><i class="fas fa-calendar-check me-2"></i>Book This Service</a>`;
    }
    form.addEventListener('input', recalc);
    recalc();
}

function initBooking() {
    const wrap = document.getElementById('booking');
    if (!wrap) return;
    const daysEl = document.getElementById('cal-days');
    const slotsEl = document.getElementById('slots');
    const summary = document.getElementById('book-summary');
    const form = document.getElementById('book-form');
    const state = { date: null, slot: null };

    const days = [];
    const today = new Date();
    for (let i = 1; days.length < 14; i++) {
        const d = new Date(today); d.setDate(today.getDate() + i);
        if (d.getDay() !== 0) days.push(d);
    }
    const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

    daysEl.innerHTML = days.map(d => `
        <div class="col-4 col-md-3 col-lg-2">
            <button type="button" class="cal-day" data-date="${iso(d)}">
                <small>${d.toLocaleDateString(undefined, { weekday: 'short' })}</small>
                <span class="d">${d.getDate()}</span>
                <small>${d.toLocaleDateString(undefined, { month: 'short' })}</small>
            </button>
        </div>`).join('');

    function refreshSummary() {
        summary.textContent = state.date && state.slot ? `${state.date} at ${state.slot}` : 'Pick a day and a time';
    }

    async function loadSlots(date) {
        slotsEl.innerHTML = '<p class="text-muted">Loading…</p>';
        const res = await fetch('/api/availability?date=' + date);
        const data = await res.json();
        slotsEl.innerHTML = data.slots.map(s => `
            <div class="col-6 col-md-4"><button type="button" class="slot-btn" data-slot="${s.time}" ${s.available ? '' : 'disabled'}>${s.time}</button></div>`).join('')
            || '<p class="text-muted">No openings that day.</p>';
    }

    daysEl.addEventListener('click', e => {
        const btn = e.target.closest('.cal-day');
        if (!btn) return;
        daysEl.querySelectorAll('.cal-day').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        state.date = btn.dataset.date; state.slot = null;
        refreshSummary(); loadSlots(state.date);
    });
    slotsEl.addEventListener('click', e => {
        const btn = e.target.closest('.slot-btn');
        if (!btn || btn.disabled) return;
        slotsEl.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        state.slot = btn.dataset.slot; refreshSummary();
    });

    form.addEventListener('submit', async e => {
        e.preventDefault();
        const err = document.getElementById('book-error');
        err.classList.add('d-none');
        if (!state.date || !state.slot) { err.textContent = 'Please choose a date and time.'; err.classList.remove('d-none'); return; }
        const body = Object.fromEntries(new FormData(form));
        Object.assign(body, { date: state.date, slot: state.slot });
        const res = await fetch('/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await res.json();
        if (!res.ok) { err.textContent = data.error; err.classList.remove('d-none'); if (res.status === 409) loadSlots(state.date); return; }
        wrap.innerHTML = `<div class="text-center py-5">
            <i class="fas fa-circle-check text-green display-3"></i>
            <h2 class="mt-3">You're booked, ${data.booking.name.split(' ')[0]}!</h2>
            <p class="lead">${data.booking.service} on <strong>${data.booking.date}</strong> at <strong>${data.booking.slot}</strong>.</p>
            <p class="text-muted">Confirmation <strong>${data.confirmation}</strong> · we'll text you the day before.</p>
            <a href="/" class="btn btn-pink mt-2">Back to Home</a></div>`;
    });
}

// ---- Beauty shop: cart lives in localStorage as {productId: qty}; prices always come from the server ----
const CART_KEY = 'bb_cart';
const getCart = () => { try { return JSON.parse(localStorage.getItem(CART_KEY)) || {}; } catch (e) { return {}; } };
const saveCart = c => { try { localStorage.setItem(CART_KEY, JSON.stringify(c)); } catch (e) {} updateBadge(); };

function updateBadge() {
    const n = Object.values(getCart()).reduce((a, b) => a + b, 0);
    document.querySelectorAll('.cart-badge').forEach(b => { b.textContent = n; b.style.display = n ? 'grid' : 'none'; });
}

function toast(msg) {
    let t = document.getElementById('toast');
    if (!t) { t = document.createElement('div'); t.id = 'toast'; t.className = 'toast-bb'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 2000);
}

function initShop() {
    document.addEventListener('click', e => {
        const btn = e.target.closest('.add-to-cart');
        if (!btn) return;
        const qtyInput = document.getElementById('prod-qty');
        const qty = qtyInput ? Math.max(1, parseInt(qtyInput.value) || 1) : 1;
        const cart = getCart();
        cart[btn.dataset.id] = Math.min(20, (cart[btn.dataset.id] || 0) + qty);
        saveCart(cart);
        toast('Added to your bag');
    });

    const grid = document.getElementById('product-grid');
    if (!grid) return;
    const search = document.getElementById('shop-search');
    const sort = document.getElementById('shop-sort');
    let cat = new URLSearchParams(location.search).get('cat') || 'all';
    const pills = document.querySelectorAll('.filter-pill');
    const cards = [...grid.children];
    function apply() {
        const q = search.value.trim().toLowerCase();
        pills.forEach(p => p.classList.toggle('active', p.dataset.cat === cat));
        const sorted = [...cards].sort((a, b) => {
            if (sort.value === 'low') return a.dataset.price - b.dataset.price;
            if (sort.value === 'high') return b.dataset.price - a.dataset.price;
            return a.dataset.order - b.dataset.order;
        });
        sorted.forEach(c => grid.appendChild(c));
        let shown = 0;
        cards.forEach(c => {
            const ok = (cat === 'all' || c.dataset.cat === cat) && (!q || c.dataset.name.includes(q));
            c.style.display = ok ? '' : 'none'; if (ok) shown++;
        });
        document.getElementById('shop-empty').classList.toggle('d-none', shown > 0);
    }
    pills.forEach(p => p.addEventListener('click', () => { cat = p.dataset.cat; apply(); }));
    search.addEventListener('input', apply);
    sort.addEventListener('change', apply);
    apply();
}

function initCart() {
    const root = document.getElementById('cart-root');
    if (!root) return;
    const linesEl = document.getElementById('cart-lines');
    const totalsEl = document.getElementById('cart-totals');
    const freeOver = Number(root.dataset.freeOver);

    async function render() {
        const cart = getCart();
        if (!Object.keys(cart).length) {
            root.querySelector('#cart-full').classList.add('d-none');
            root.querySelector('#cart-empty').classList.remove('d-none');
            return;
        }
        const res = await fetch('/api/cart', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ cart }) });
        const q = await res.json();
        // drop anything the server no longer recognises
        const valid = Object.fromEntries(q.items.map(i => [i.id, i.qty]));
        if (Object.keys(valid).length !== Object.keys(cart).length) saveCart(valid);
        if (!q.items.length) return render();
        root.querySelector('#cart-full').classList.remove('d-none');
        root.querySelector('#cart-empty').classList.add('d-none');
        linesEl.innerHTML = q.items.map(i => `
            <div class="cart-line" style="--sw:${i.color}">
                <div class="cart-thumb"><i class="fas ${i.icon}"></i></div>
                <div class="flex-grow-1"><strong>${i.name}</strong><div class="small text-muted">${i.shade} · ${money(i.price)} each</div></div>
                <div class="d-flex align-items-center gap-2">
                    <button class="qty-btn" data-act="dec" data-id="${i.id}" aria-label="Decrease">−</button>
                    <span style="min-width:1.5rem;text-align:center">${i.qty}</span>
                    <button class="qty-btn" data-act="inc" data-id="${i.id}" aria-label="Increase">+</button>
                </div>
                <strong style="min-width:4.5rem;text-align:right">${money(i.line)}</strong>
                <button class="btn btn-link text-muted p-0" data-act="rm" data-id="${i.id}" aria-label="Remove"><i class="fas fa-trash-can"></i></button>
            </div>`).join('');
        const toFree = Math.max(0, freeOver - q.subtotal);
        totalsEl.innerHTML = `
            <div class="quote-line"><span>Subtotal</span><strong>${money(q.subtotal)}</strong></div>
            <div class="quote-line"><span>Shipping</span><strong>${q.shipping ? money(q.shipping) : 'FREE'}</strong></div>
            <div class="quote-line"><span>Tax</span><strong>${money(q.tax)}</strong></div>
            <div class="mt-3 text-muted small">Order total</div><div class="quote-total">${money(q.total)}</div>
            ${toFree ? `<p class="small text-green mt-2 mb-0"><i class="fas fa-truck me-1"></i>Add ${money(toFree)} more for free shipping</p>` : `<p class="small text-green mt-2 mb-0"><i class="fas fa-truck me-1"></i>You've unlocked free shipping!</p>`}`;
    }

    linesEl.addEventListener('click', e => {
        const b = e.target.closest('[data-act]');
        if (!b) return;
        const cart = getCart(), id = b.dataset.id;
        if (b.dataset.act === 'inc') cart[id] = Math.min(20, (cart[id] || 0) + 1);
        if (b.dataset.act === 'dec') cart[id] = (cart[id] || 1) - 1;
        if (b.dataset.act === 'rm' || cart[id] < 1) delete cart[id];
        saveCart(cart); render();
    });

    document.getElementById('checkout-form').addEventListener('submit', async e => {
        e.preventDefault();
        const err = document.getElementById('checkout-error');
        err.classList.add('d-none');
        const body = Object.fromEntries(new FormData(e.target));
        body.cart = getCart();
        const res = await fetch('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await res.json();
        if (!res.ok) { err.textContent = data.error; err.classList.remove('d-none'); return; }
        saveCart({});
        root.innerHTML = `<div class="text-center py-5">
            <i class="fas fa-circle-check text-green display-3"></i>
            <h2 class="mt-3">Thank you! Your order is in.</h2>
            <p class="lead">Order <strong>${data.order}</strong> · ${money(data.total)}</p>
            <p class="text-muted">A confirmation is headed to ${data.email}.</p>
            <a href="/shop" class="btn btn-pink mt-2">Keep Shopping</a></div>`;
    });
    render();
}
