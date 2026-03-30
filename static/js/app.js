/**
 * StumpSolutions — quote calculator, contact demo, navigation helpers
 */

function formatMoney(n) {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0,
    }).format(n);
}

function computeQuoteEstimate() {
    const count = Math.max(1, parseInt(document.getElementById("stump-count")?.value, 10) || 1);
    const diameter = Math.max(6, parseInt(document.getElementById("avg-diameter")?.value, 10) || 18);
    const depthMod = parseFloat(document.getElementById("grind-depth")?.value) || 1;
    const accessMod = parseFloat(document.getElementById("access")?.value) || 1;
    const debrisMod = parseFloat(document.getElementById("debris")?.value) || 1;

    const visitFee = 85;
    const perStump = 40 + diameter * 3.2;
    const subtotal = visitFee + count * perStump;
    const total = subtotal * depthMod * accessMod * debrisMod;
    const low = Math.round(total * 0.88);
    const high = Math.round(total * 1.12);

    return { low, high, total: Math.round(total) };
}

function renderQuoteResult() {
    const el = document.getElementById("quote-result");
    if (!el) return;

    const { low, high, total } = computeQuoteEstimate();
    el.innerHTML = `
        <p class="display-6 fw-bold text-hot-pink mb-2">${formatMoney(low)} – ${formatMoney(high)}</p>
        <p class="text-muted small mb-2">Midpoint about <strong>${formatMoney(total)}</strong> for ${document.getElementById("stump-count").value} stump(s),
        ~${document.getElementById("avg-diameter").value}" average diameter.</p>
        <p class="small mb-0">Call or email to schedule a quick site check for a firm price.</p>
    `;
}

function setupQuoteForm() {
    const form = document.getElementById("quote-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        renderQuoteResult();
    });

    ["stump-count", "avg-diameter", "grind-depth", "access", "debris"].forEach((id) => {
        const node = document.getElementById(id);
        if (node) {
            node.addEventListener("input", () => {
                if (document.getElementById("quote-result")?.querySelector(".display-6")) {
                    renderQuoteResult();
                }
            });
            node.addEventListener("change", () => {
                if (document.getElementById("quote-result")?.querySelector(".display-6")) {
                    renderQuoteResult();
                }
            });
        }
    });
}

function setupContactForm() {
    const form = document.querySelector(".ss-contact-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = form.querySelector("#c-name")?.value?.trim() || "there";
        window.alert(`Thanks, ${name}! This demo form does not send email — use the phone or email on this page for a real project.`);
    });
}

function setActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll(".navbar-nav .nav-link").forEach((link) => {
        const href = link.getAttribute("href");
        if (href === path) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

function setupMobileNavClose() {
    const collapse = document.querySelector(".navbar-collapse");
    if (!collapse || typeof bootstrap === "undefined") return;

    collapse.querySelectorAll(".nav-link").forEach((link) => {
        link.addEventListener("click", () => {
            if (window.innerWidth < 992) {
                const inst = bootstrap.Collapse.getInstance(collapse);
                if (inst) inst.hide();
            }
        });
    });
}

function init() {
    setupQuoteForm();
    setupContactForm();
    setActiveNav();
    setupMobileNavClose();
}

document.addEventListener("DOMContentLoaded", init);
