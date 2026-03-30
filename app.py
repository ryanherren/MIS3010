import json
import os
from datetime import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from mock_data import (
    SHOES,
    RECOMMENDED_IDS,
    REVIEWS,
    CAREERS,
    FAQ,
    SEED_ORDERS,
    SELLER_STATS,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "coles-kicks-mis3010-dev-key")

# In-memory orders (demo): merges seed + checkout-created orders
_orders = {o["id"]: dict(o) for o in SEED_ORDERS}


def _next_order_id():
    nums = []
    for k in _orders:
        try:
            nums.append(int(k.split("-")[-1]))
        except ValueError:
            continue
    n = max(nums, default=1000) + 1
    return f"CK-2026-{n}"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/shop")
def shop():
    return render_template("shop.html", shoes=SHOES)


@app.route("/sell")
def sell():
    return render_template("sell.html", stats=SELLER_STATS, shoes=SHOES[:5])


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        cart_json = request.form.get("cart_json", "[]")
        if not name or not email:
            flash("Please enter your name and email to complete purchase.", "danger")
            return redirect(url_for("checkout"))

        try:
            cart = json.loads(cart_json)
        except json.JSONDecodeError:
            cart = []

        if not cart:
            flash("Your cart is empty.", "warning")
            return redirect(url_for("shop"))

        oid = _next_order_id()
        total = sum(float(item.get("price", 0)) * int(item.get("qty", 1)) for item in cart)
        _orders[oid] = {
            "id": oid,
            "name": name,
            "email": email,
            "status": "Processing",
            "items": cart,
            "placed": datetime.now().strftime("%Y-%m-%d"),
            "total": round(total, 2),
        }
        session["last_order_id"] = oid
        flash(f"Order placed! Your order ID is {oid}.", "success")
        return redirect(url_for("order_success", order_id=oid))

    return render_template("checkout.html")


@app.route("/order/success/<order_id>")
def order_success(order_id):
    order = _orders.get(order_id)
    return render_template("order_success.html", order=order)


@app.route("/orders")
def orders():
    return render_template("order_tracker.html")


@app.route("/orders/lookup", methods=["POST"])
def orders_lookup():
    oid = request.form.get("order_id", "").strip().upper()
    if not oid:
        flash("Enter an order ID.", "warning")
        return redirect(url_for("orders"))
    order = _orders.get(oid) or _orders.get(oid.replace(" ", ""))
    if not order:
        flash("No order found with that ID. Try CK-2026-1001 for a sample.", "danger")
        return redirect(url_for("orders"))
    return render_template("order_tracker.html", order=order)


@app.route("/recommended")
def recommended():
    by_id = {s["id"]: s for s in SHOES}
    picks = [by_id[i] for i in RECOMMENDED_IDS if i in by_id]
    return render_template("recommended.html", shoes=picks)


@app.route("/help")
def help_page():
    return render_template("help.html", faq=FAQ, reviews=REVIEWS)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/careers")
def careers():
    return render_template("careers.html", roles=CAREERS)


@app.route("/api/shoes")
def api_shoes():
    brand = request.args.get("brand", "").strip()
    size = request.args.get("size", "").strip()
    color = request.args.get("color", "").strip()
    max_price = request.args.get("max_price", type=float)
    min_price = request.args.get("min_price", type=float)

    out = []
    for s in SHOES:
        if brand and s["brand"].lower() != brand.lower():
            continue
        if size and str(s["size"]) != str(size):
            continue
        if color and s["color"].lower() != color.lower():
            continue
        if min_price is not None and s["price"] < min_price:
            continue
        if max_price is not None and s["price"] > max_price:
            continue
        out.append(s)
    return jsonify(out)


@app.route("/api/meta/filters")
def api_meta_filters():
    brands = sorted({s["brand"] for s in SHOES})
    sizes = sorted({str(s["size"]) for s in SHOES}, key=lambda x: float(x))
    colors = sorted({s["color"] for s in SHOES})
    prices = [s["price"] for s in SHOES]
    return jsonify(
        {
            "brands": brands,
            "sizes": sizes,
            "colors": colors,
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
        }
    )


@app.route("/api/time")
def api_time():
    return jsonify(
        {
            "datetime": datetime.now().isoformat(),
            "timestamp": datetime.now().timestamp(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)
