/**
 * Cole's Kicks — cart, shop filters, checkout binding
 */
(function () {
    const CART_KEY = 'coles_kicks_cart_v1';

    function getCart() {
        try {
            const raw = localStorage.getItem(CART_KEY);
            const parsed = raw ? JSON.parse(raw) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch {
            return [];
        }
    }

    function saveCart(items) {
        localStorage.setItem(CART_KEY, JSON.stringify(items));
        updateNavBadge();
    }

    function updateNavBadge() {
        const cart = getCart();
        const count = cart.reduce((n, i) => n + (i.qty || 0), 0);
        const el = document.getElementById('nav-cart-count');
        if (!el) return;
        if (count > 0) {
            el.textContent = String(count);
            el.classList.remove('d-none');
        } else {
            el.classList.add('d-none');
        }
    }

    let catalogById = {};

    async function loadCatalog() {
        if (Object.keys(catalogById).length) return catalogById;
        try {
            const res = await fetch('/api/shoes');
            if (!res.ok) throw new Error('shoes api');
            const list = await res.json();
            catalogById = Object.fromEntries(list.map((s) => [s.id, s]));
        } catch (e) {
            console.warn('Catalog fetch failed', e);
        }
        return catalogById;
    }

    function addToCart(shoeId) {
        const shoe = catalogById[shoeId];
        if (!shoe) return;
        const cart = getCart();
        const line = cart.find((c) => c.id === shoeId);
        if (line) line.qty = (line.qty || 1) + 1;
        else {
            cart.push({
                id: shoe.id,
                name: shoe.name,
                price: shoe.price,
                qty: 1,
            });
        }
        saveCart(cart);
        if (window.MIS3010App?.utils?.showNotification) {
            window.MIS3010App.utils.showNotification('Added to cart', 'success', 2500);
        }
    }

    async function populateFilters() {
        try {
            const res = await fetch('/api/meta/filters');
            if (!res.ok) return;
            const meta = await res.json();
            const brandSel = document.getElementById('filter-brand');
            const sizeSel = document.getElementById('filter-size');
            const colorSel = document.getElementById('filter-color');
            const maxInput = document.getElementById('filter-max');
            if (brandSel && meta.brands) {
                meta.brands.forEach((b) => {
                    const o = document.createElement('option');
                    o.value = b;
                    o.textContent = b;
                    brandSel.appendChild(o);
                });
            }
            if (sizeSel && meta.sizes) {
                meta.sizes.forEach((s) => {
                    const o = document.createElement('option');
                    o.value = s;
                    o.textContent = s;
                    sizeSel.appendChild(o);
                });
            }
            if (colorSel && meta.colors) {
                meta.colors.forEach((c) => {
                    const o = document.createElement('option');
                    o.value = c;
                    o.textContent = c;
                    colorSel.appendChild(o);
                });
            }
            if (maxInput && meta.max_price != null) {
                maxInput.placeholder = `Up to ${meta.max_price}`;
                maxInput.max = meta.max_price;
            }
        } catch (e) {
            console.warn('Filters meta failed', e);
        }
    }

    function applyShopFilters() {
        const brand = document.getElementById('filter-brand')?.value || '';
        const size = document.getElementById('filter-size')?.value || '';
        const color = document.getElementById('filter-color')?.value || '';
        const maxRaw = document.getElementById('filter-max')?.value;
        const max = maxRaw === '' || maxRaw == null ? null : parseFloat(maxRaw);

        const items = document.querySelectorAll('.shoe-item');
        let visible = 0;
        items.forEach((el) => {
            const okBrand = !brand || el.dataset.brand === brand;
            const okSize = !size || String(el.dataset.size) === String(size);
            const okColor = !color || el.dataset.color === color;
            const price = parseFloat(el.dataset.price);
            const okPrice = max == null || isNaN(max) || price <= max;
            const show = okBrand && okSize && okColor && okPrice;
            el.classList.toggle('d-none', !show);
            if (show) visible += 1;
        });
        const label = document.getElementById('filter-count');
        if (label) label.textContent = `${visible} pair(s) match your filters`;
    }

    function bindShop() {
        populateFilters();
        ['filter-brand', 'filter-size', 'filter-color', 'filter-max'].forEach((id) => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener('change', applyShopFilters);
                el.addEventListener('input', applyShopFilters);
            }
        });
        document.getElementById('filter-reset')?.addEventListener('click', () => {
            const ids = ['filter-brand', 'filter-size', 'filter-color'];
            ids.forEach((i) => {
                const s = document.getElementById(i);
                if (s) s.value = '';
            });
            const m = document.getElementById('filter-max');
            if (m) m.value = '';
            applyShopFilters();
        });
        applyShopFilters();
    }

    function renderCheckout() {
        const cart = getCart();
        const empty = document.getElementById('checkout-cart-empty');
        const list = document.getElementById('checkout-cart-list');
        const totalWrap = document.getElementById('checkout-cart-total-wrap');
        const totalEl = document.getElementById('checkout-cart-total');
        const jsonInput = document.getElementById('cart_json');
        const submit = document.getElementById('checkout-submit');

        if (!list || !jsonInput) return;

        if (!cart.length) {
            empty?.classList.remove('d-none');
            list.classList.add('d-none');
            totalWrap?.classList.add('d-none');
            jsonInput.value = '[]';
            if (submit) submit.disabled = true;
            return;
        }

        empty?.classList.add('d-none');
        list.classList.remove('d-none');
        totalWrap?.classList.remove('d-none');
        list.innerHTML = '';
        let sum = 0;
        cart.forEach((line) => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            const sub = (line.price || 0) * (line.qty || 1);
            sum += sub;
            li.innerHTML = `<span>${line.name} × ${line.qty}</span><span>$${sub.toFixed(2)}</span>`;
            list.appendChild(li);
        });
        if (totalEl) totalEl.textContent = `$${sum.toFixed(2)}`;
        jsonInput.value = JSON.stringify(
            cart.map((c) => ({ name: c.name, price: c.price, qty: c.qty || 1 }))
        );
        if (submit) submit.disabled = false;
    }

    document.addEventListener('DOMContentLoaded', async () => {
        updateNavBadge();
        await loadCatalog();

        document.body.addEventListener('click', (e) => {
            const btn = e.target.closest('.add-to-cart-btn');
            if (!btn) return;
            const id = btn.getAttribute('data-id');
            if (id) addToCart(id);
        });

        if (document.getElementById('shoe-grid')) {
            bindShop();
        }

        if (document.getElementById('checkout-form')) {
            renderCheckout();
        }
    });
})();
