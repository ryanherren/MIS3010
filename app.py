from flask import Flask, render_template, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# API Routes
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