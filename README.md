# MIS 3010 Web Application

A modern Flask web application built for MIS 3010 class demonstrations, featuring responsive design, user authentication, and RESTful API endpoints.

## Features

### Frontend Technologies
- **Bootstrap 5** - Responsive framework with modern UI components
- **Font Awesome** - Comprehensive icon library
- **Vanilla JavaScript** - No heavy frameworks, pure ES6+ JavaScript
- **Jinja2** - Server-side templating
- **CSS Custom Properties** - Modern theming system
- **Mobile-first** - Responsive design approach

### Backend Technologies
- **Python Flask** - Lightweight web framework
- **SQLAlchemy ORM** - Database abstraction layer
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling with CSRF protection
- **Dual Database Support** - SQLite for development, PostgreSQL for production
- **User Role Management** - Admin and regular user roles
- **RESTful API** - JSON endpoints for AJAX functionality

## Pages

1. **Home Page** (`/`)
   - Welcome message with current date and time
   - Continuously updating clock (HH:MM:SS)
   - Feature showcase cards
   - User-specific content when logged in

2. **About Me Page** (`/about`)
   - Personal profile with photo
   - Company logos and descriptions
   - Professional titles and roles
   - Technical skills showcase
   - Contact information and social links

3. **Login Page** (`/login`)
   - User authentication form
   - Demo credentials display
   - Form validation with error handling

4. **Admin Panel** (`/admin`)
   - User management dashboard
   - Statistics cards
   - API testing interface
   - Admin-only access

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone or download the project:**
   ```bash
   cd /path/to/MIS3010
   ```

2. **Install dependencies:**
   
   **For Python 3.13+ users:**
   ```bash
   pip install -r requirements-py313.txt
   ```
   
   **For Python 3.8-3.12 users:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Alternative (recommended for Python 3.13):**
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Open your browser and go to: `http://localhost:3010`
   - Login with demo credentials:
     - Username: `ryanherren`
     - Password: `admin123`

### Default Admin Account

The application automatically creates an admin user on first run:
- **Username:** `ryanherren`
- **Password:** `admin123` ⚠️ **Change this in production!**
- **Role:** Admin
- **Email:** `ryan@example.com`

## Project Structure

```
MIS3010/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── mis3010.db            # SQLite database (created on first run)
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles with CSS variables
│   ├── js/
│   │   └── app.js        # JavaScript functionality
│   └── images/
│       ├── placeholder-profile.svg
│       └── placeholder-logo.svg
└── templates/            # Jinja2 templates
    ├── base.html         # Base template with navigation
    ├── home.html         # Home page
    ├── about.html        # About me page
    ├── login.html        # Login form
    └── admin.html        # Admin panel
```

## API Endpoints

### Public Endpoints
- `GET /api/time` - Returns current server time in JSON format

### Protected Endpoints (Admin only)
- `GET /api/users` - Returns list of all users with details

## Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string (defaults to SQLite)
- `SECRET_KEY` - Flask secret key for sessions (change in production)

### Database Configuration
- **Development:** SQLite (`mis3010.db`)
- **Production:** PostgreSQL (set `DATABASE_URL` environment variable)

## Customization

### Adding Your Own Content

1. **Profile Photo:**
   - Replace `static/images/profile.jpg` with your photo
   - Recommended size: 200x200px, square format

2. **Company Logos:**
   - Add your company logos as `static/images/company1-logo.png`, etc.
   - Recommended format: PNG with transparent background
   - Maximum height: 80px

3. **Personal Information:**
   - Edit `templates/about.html` to update:
     - Personal description
     - Company information
     - Professional titles
     - Technical skills
     - Contact links

4. **Styling:**
   - Modify `static/css/style.css` to customize:
     - Color scheme (CSS custom properties in `:root`)
     - Typography
     - Layout and spacing
     - Responsive breakpoints

## Security Notes

⚠️ **Important for Production:**
1. Change the default admin password
2. Set a strong `SECRET_KEY` environment variable
3. Use HTTPS in production
4. Configure proper database security
5. Enable CSRF protection (already included via Flask-WTF)
6. Consider rate limiting for login attempts

## Browser Support

- **Modern Browsers:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile:** iOS Safari 14+, Chrome Mobile 90+
- **Features:** CSS Grid, Flexbox, ES6+, Fetch API

## Development Notes

### Adding New Features
1. **Database Models:** Add to `app.py` and run `db.create_all()`
2. **Templates:** Create in `templates/` directory
3. **Static Assets:** Add to appropriate `static/` subdirectory
4. **Routes:** Add to `app.py` with proper authentication decorators

### JavaScript Architecture
- Main app object: `MIS3010App`
- Modular structure with utilities
- Event-driven architecture
- API integration helpers

### CSS Architecture
- CSS custom properties for theming
- Mobile-first responsive design
- Bootstrap 5 integration
- Dark mode support (prefers-color-scheme)

## Troubleshooting

### Python 3.13 Compatibility Issues

If you encounter build errors with `psycopg2-binary`, this is due to Python 3.13 compatibility. Solutions:

1. **Use the Python 3.13 requirements file:**
   ```bash
   pip install -r requirements-py313.txt
   ```

2. **Install packages individually:**
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF
   ```

3. **For PostgreSQL support in production:**
   ```bash
   # Modern approach (recommended)
   pip install "psycopg[binary]"
   
   # OR traditional approach (requires PostgreSQL dev libraries)
   pip install psycopg2
   ```

### Common Issues

- **Port already in use:** Change the port in `app.py` from 5000 to another port
- **Permission errors:** Use `python3` instead of `python` on some systems
- **Module not found:** Ensure you're in the correct directory and packages are installed

## License

This project is created for educational purposes in MIS 3010. Feel free to use and modify for learning and demonstration purposes.

## Author

**Ryan Herren**
- Entrepreneur • Developer • Educator
- Built for MIS 3010 class demonstrations
