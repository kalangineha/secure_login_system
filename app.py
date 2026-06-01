"""
Secure Login System using Flask and SQLite
============================================
A beginner-friendly web application demonstrating:
- User registration with password hashing
- Secure login with session management
- SQLite database with parameterized queries
- Optional 2FA with email OTP
- Input validation and security best practices
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import secrets
import string
from datetime import datetime, timedelta
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!
DATABASE = 'database.db'

# Optional: Email configuration for 2FA (uses console print for demo)
# For production, use proper email service (Flask-Mail, SendGrid, etc.)
DEMO_MODE = True  # Set to False and configure email in production


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """Initialize the SQLite database with required tables."""
    # Check if database exists
    if os.path.exists(DATABASE):
        return
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            two_fa_enabled INTEGER DEFAULT 0,
            two_fa_secret TEXT
        )
    ''')
    
    # Create OTP table for 2FA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            otp_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_used INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create login history table (optional, for tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            success INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[✓] Database initialized successfully!")


def get_db_connection():
    """
    Get a connection to the SQLite database.
    Using row_factory to return rows as dictionaries for easier access.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================================

def validate_username(username):
    """
    Validate username format.
    
    Requirements:
    - Length: 3-20 characters
    - Allowed: alphanumeric and underscores
    - Cannot be empty
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."
    
    return True, "Valid"


def validate_password(password):
    """
    Validate password strength.
    
    Requirements:
    - Minimum length: 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    
    return True, "Valid"


def validate_email(email):
    """Validate email format."""
    if not email:
        return False, "Email cannot be empty."
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format."
    
    return True, "Valid"


# ============================================================================
# OTP/2FA FUNCTIONS
# ============================================================================

def generate_otp():
    """Generate a 6-digit OTP code."""
    return ''.join(secrets.choice(string.digits) for _ in range(6))


def create_otp(user_id):
    """
    Create and store an OTP code for the user.
    OTP expires in 10 minutes.
    """
    otp_code = generate_otp()
    expiry_time = datetime.now() + timedelta(minutes=10)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert OTP into database
    cursor.execute('''
        INSERT INTO otp_codes (user_id, otp_code, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, otp_code, expiry_time))
    
    conn.commit()
    conn.close()
    
    return otp_code


def verify_otp(user_id, otp_code):
    """
    Verify the OTP code provided by the user.
    Check if code exists, hasn't expired, and hasn't been used.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch the OTP code
    cursor.execute('''
        SELECT * FROM otp_codes
        WHERE user_id = ? AND otp_code = ? AND is_used = 0
        ORDER BY created_at DESC
        LIMIT 1
    ''', (user_id, otp_code))
    
    otp_record = cursor.fetchone()
    
    if not otp_record:
        conn.close()
        return False, "Invalid OTP code."
    
    # Check if OTP has expired
    expiry_time = datetime.fromisoformat(otp_record['expires_at'])
    if datetime.now() > expiry_time:
        conn.close()
        return False, "OTP code has expired. Please request a new one."
    
    # Mark OTP as used
    cursor.execute('''
        UPDATE otp_codes
        SET is_used = 1
        WHERE id = ?
    ''', (otp_record['id'],))
    
    conn.commit()
    conn.close()
    
    return True, "OTP verified successfully!"


def send_otp_email(email, otp_code):
    """
    Send OTP to user's email.
    In demo mode, prints to console.
    In production, use Flask-Mail or SendGrid.
    """
    if DEMO_MODE:
        print(f"\n" + "="*50)
        print(f"[EMAIL OTP SIMULATION]")
        print(f"To: {email}")
        print(f"Subject: Your Login OTP Code")
        print(f"---")
        print(f"Your OTP code is: {otp_code}")
        print(f"This code will expire in 10 minutes.")
        print("="*50 + "\n")
    else:
        # In production, implement actual email sending
        pass


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def user_exists(username):
    """Check if a user with the given username already exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user is not None


def register_user(username, password, email):
    """
    Register a new user with hashed password.
    
    Process:
    1. Validate inputs
    2. Hash password using werkzeug
    3. Insert into database using parameterized query
    """
    # Validate username
    is_valid, message = validate_username(username)
    if not is_valid:
        return False, message
    
    # Check if username already exists
    if user_exists(username):
        return False, "Username already exists. Please choose another."
    
    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        return False, message
    
    # Validate email
    is_valid, message = validate_email(email)
    if not is_valid:
        return False, message
    
    # Hash password using werkzeug (similar to bcrypt)
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert user using parameterized query (prevents SQL injection)
        cursor.execute('''
            INSERT INTO users (username, password_hash, email)
            VALUES (?, ?, ?)
        ''', (username, password_hash, email))
        
        conn.commit()
        conn.close()
        
        return True, "Registration successful! Please login."
    
    except sqlite3.IntegrityError:
        return False, "An error occurred during registration. Please try again."
    except Exception as e:
        print(f"Error during registration: {e}")
        return False, "An unexpected error occurred."


def login_user(username, password):
    """
    Verify username and password.
    
    Process:
    1. Query database for user using parameterized query
    2. Verify password using werkzeug
    3. Return user info if valid
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user is None:
        return False, None, "Username or password is incorrect."
    
    # Verify password using werkzeug
    if not check_password_hash(user['password_hash'], password):
        return False, None, "Username or password is incorrect."
    
    return True, dict(user), "Login successful!"


def get_user(user_id):
    """Retrieve user information by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    
    return dict(user) if user else None


# ============================================================================
# ROUTES - REGISTRATION
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page and form handler.
    GET: Display registration form
    POST: Process registration
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        email = request.form.get('email', '').strip()
        
        # Validate that passwords match
        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))
        
        # Register user
        success, message = register_user(username, password, email)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')


# ============================================================================
# ROUTES - LOGIN
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page and form handler.
    GET: Display login form
    POST: Process login
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate inputs
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('login'))
        
        # Verify credentials
        success, user, message = login_user(username, password)
        
        if not success:
            flash(message, 'error')
            return redirect(url_for('login'))
        
        # Check if 2FA is enabled
        if user['two_fa_enabled']:
            # Store temporary user info and redirect to 2FA verification
            session['temp_user_id'] = user['id']
            session['temp_username'] = user['username']
            
            # Generate and send OTP
            otp_code = create_otp(user['id'])
            send_otp_email(user['email'], otp_code)
            
            flash('OTP code sent to your email. Please enter it to continue.', 'info')
            return redirect(url_for('verify_otp'))
        
        # No 2FA: Create session
        session['user_id'] = user['id']
        session['username'] = user['username']
        
        flash(f'Welcome back, {user["username"]}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


# ============================================================================
# ROUTES - 2FA OTP VERIFICATION
# ============================================================================

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp_route():
    """
    OTP verification page for 2FA.
    """
    if 'temp_user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp', '').strip()
        user_id = session.get('temp_user_id')
        
        if not otp_code:
            flash('Please enter the OTP code.', 'error')
            return redirect(url_for('verify_otp_route'))
        
        # Verify OTP
        success, message = verify_otp(user_id, otp_code)
        
        if not success:
            flash(message, 'error')
            return redirect(url_for('verify_otp_route'))
        
        # OTP verified: Create session
        session['user_id'] = user_id
        session['username'] = session.get('temp_username')
        
        # Clean up temporary session data
        session.pop('temp_user_id', None)
        session.pop('temp_username', None)
        
        flash('2FA verification successful! Welcome!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('verify_otp.html', username=session.get('temp_username'))


# ============================================================================
# ROUTES - DASHBOARD (Protected)
# ============================================================================

@app.route('/dashboard')
def dashboard():
    """
    Dashboard page (accessible only to logged-in users).
    This route demonstrates session-based access control.
    """
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    # Get user information
    user = get_user(session['user_id'])
    
    if not user:
        session.clear()
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=user)


# ============================================================================
# ROUTES - LOGOUT
# ============================================================================

@app.route('/logout')
def logout():
    """
    Logout route that destroys the user session.
    """
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'success')
    return redirect(url_for('login'))


# ============================================================================
# ROUTES - HOME
# ============================================================================

@app.route('/')
def home():
    """Home page - redirects based on login status."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', error="Internal server error"), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run Flask app
    print("\n" + "="*50)
    print("Secure Login System - Flask App")
    print("="*50)
    print("Starting server on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
