// Cyclone Tickets client-side helpers
document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('.sec-row[data-key]');
    const shapes = document.querySelectorAll('.map-sec[data-key]');
    const secInput = document.getElementById('section-input');
    const qty = document.getElementById('qty');
    const addBtn = document.getElementById('add-btn');
    const summary = document.getElementById('pick-summary');
    if (!rows.length) return;

    function select(key) {
        const row = document.querySelector(`.sec-row[data-key="${key}"]`);
        if (!row || row.classList.contains('soldout')) return;
        rows.forEach(r => r.classList.toggle('selected', r === row));
        shapes.forEach(s => s.classList.toggle('selected', s.dataset.key === key));
        secInput.value = key;
        const avail = parseInt(row.dataset.avail, 10);
        qty.max = Math.min(avail, parseInt(qty.dataset.max, 10));
        if (parseInt(qty.value, 10) > qty.max) qty.value = qty.max;
        addBtn.disabled = false;
        update();
        row.scrollIntoView({behavior: 'smooth', block: 'nearest'});
    }
    function update() {
        const row = document.querySelector('.sec-row.selected');
        if (!row) return;
        const total = parseFloat(row.dataset.price) * (parseInt(qty.value, 10) || 0);
        summary.textContent = `${qty.value} × ${row.dataset.name} · $${total.toFixed(2)} before fees`;
    }
    rows.forEach(r => r.addEventListener('click', () => select(r.dataset.key)));
    shapes.forEach(s => s.addEventListener('click', () => select(s.dataset.key)));
    qty.addEventListener('input', update);

    // Keep availability fresh while the page is open
    const eventId = document.body.dataset.event;
    if (eventId) setInterval(async () => {
        try {
            const inv = await (await fetch(`/api/availability/${eventId}`)).json();
            rows.forEach(r => {
                const a = inv[r.dataset.key].avail;
                r.dataset.avail = a;
                r.querySelector('.avail').textContent = a > 0 ? `${a} left` : 'Sold out';
                r.classList.toggle('soldout', a === 0);
            });
        } catch (e) { /* offline, ignore */ }
    }, 15000);
});
