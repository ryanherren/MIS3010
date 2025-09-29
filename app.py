from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///mis3010.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

# Contact Model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    service = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Review Model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    service = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    service = SelectField('Service Interested In', choices=[
        ('wedding', 'Wedding Photography'),
        ('portrait', 'Portrait Session'),
        ('event', 'Event Photography'),
        ('commercial', 'Commercial Photography'),
        ('family', 'Family Photos'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    event_date = StringField('Preferred Date (if applicable)')
    message = TextAreaField('Tell us about your vision', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class ReviewForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    rating = SelectField('Rating', choices=[
        ('5', '⭐⭐⭐⭐⭐ Excellent'),
        ('4', '⭐⭐⭐⭐ Very Good'),
        ('3', '⭐⭐⭐ Good'),
        ('2', '⭐⭐ Fair'),
        ('1', '⭐ Poor')
    ], validators=[DataRequired()])
    service = SelectField('Service Used', choices=[
        ('wedding', 'Wedding Photography'),
        ('portrait', 'Portrait Session'),
        ('event', 'Event Photography'),
        ('commercial', 'Commercial Photography'),
        ('family', 'Family Photos'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    comment = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service=form.service.data,
            event_date=form.event_date.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for your message! We\'ll get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            name=form.name.data,
            rating=int(form.rating.data),
            service=form.service.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        flash('Thank you for your review! It will be published after approval.', 'success')
        return redirect(url_for('reviews'))
    
    approved_reviews = Review.query.filter_by(approved=True).order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', form=form, reviews=approved_reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    users = User.query.all()
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    pending_reviews = Review.query.filter_by(approved=False).order_by(Review.created_at.desc()).all()
    return render_template('admin.html', users=users, contacts=contacts, pending_reviews=pending_reviews)

@app.route('/admin/approve_review/<int:review_id>')
@login_required
def approve_review(review_id):
    if not current_user.is_admin():
        flash('Access denied.', 'danger')
        return redirect(url_for('home'))
    
    review = Review.query.get_or_404(review_id)
    review.approved = True
    db.session.commit()
    flash('Review approved successfully!', 'success')
    return redirect(url_for('admin'))

# API Routes
@app.route('/api/time')
def api_time():
    return jsonify({
        'datetime': datetime.now().isoformat(),
        'timestamp': datetime.now().timestamp()
    })

@app.route('/api/users')
@login_required
def api_users():
    if not current_user.is_admin():
        return jsonify({'error': 'Access denied'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    } for user in users])

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    admin = User.query.filter_by(username='jake_admin').first()
    if not admin:
        admin = User(
            username='jake_admin',
            email='jake@jakesphoto.com',
            role='admin'
        )
        admin.set_password('photo123')  # Change this password!
        db.session.add(admin)
        db.session.commit()
        print("Admin user 'jake_admin' created with password 'photo123'")

def create_sample_reviews():
    """Create some sample approved reviews"""
    if Review.query.count() == 0:
        sample_reviews = [
            Review(name="Sarah Johnson", rating=5, service="wedding", 
                  comment="Jake's Photo Crew captured our wedding day perfectly! The photos are absolutely stunning and we couldn't be happier.", approved=True),
            Review(name="Mike Chen", rating=5, service="portrait", 
                  comment="Professional, creative, and so easy to work with. The portrait session was fun and the results exceeded our expectations!", approved=True),
            Review(name="Emily Davis", rating=4, service="family", 
                  comment="Great experience with our family photos. Jake made the kids feel comfortable and got some amazing shots.", approved=True),
        ]
        for review in sample_reviews:
            db.session.add(review)
        db.session.commit()
        print("Sample reviews created")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_sample_reviews()
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
