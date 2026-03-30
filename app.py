from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


@app.route("/grades")
def grades():
    return render_template("grades.html")


@app.route("/progress")
def progress():
    return render_template("progress.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, host="0.0.0.0", port=port)
