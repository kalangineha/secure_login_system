# 🔐 Secure Login System - Flask Web Application

A beginner-friendly, secure login system built with Python Flask and SQLite. This project demonstrates essential web security concepts and best practices for building authentication systems.

![Project Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![Flask Version](https://img.shields.io/badge/Flask-3.0+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Security Features](#security-features)
- [Learning Resources](#learning-resources)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

---

## ✨ Features

### Core Functionality
✅ **User Registration**
- Create new accounts with username and password
- Email validation
- Strong password requirements (8+ chars, uppercase, lowercase, numbers)
- Duplicate username detection

✅ **User Login**
- Secure password verification
- Session-based authentication
- Error messages for invalid credentials

✅ **Dashboard**
- Protected route requiring login
- User profile information display
- Account statistics

✅ **Logout**
- Session destruction
- Secure cleanup

✅ **Session Management**
- Flask session tokens
- Automatic session handling
- Protected pages that redirect to login

### Security Features
🔒 **Password Security**
- PBKDF2-SHA256 hashing (via Werkzeug)
- Passwords never stored in plain text
- Strong password validation

🔒 **Database Security**
- Parameterized queries (prevents SQL injection)
- SQLite with proper schema
- Input sanitization

🔒 **Session Security**
- Secure Flask sessions
- Session tokens
- Automatic session management

🔒 **Optional Two-Factor Authentication (2FA)**
- Email-based OTP codes
- 10-minute code expiration
- One-time use codes
- Demo email printing (upgrade for production)

🔒 **Input Validation**
- Username format validation
- Email validation
- Password strength requirements
- No empty fields allowed

---

## 📁 Project Structure

```
secure-login-system/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database (auto-created)
├── README.md                   # This file
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── register.html          # User registration page
│   ├── login.html             # User login page
│   ├── dashboard.html         # User dashboard (protected)
│   ├── verify_otp.html        # 2FA OTP verification
│   └── error.html             # Error pages
│
└── static/                     # Static files
    └── style.css              # Custom CSS styling
```

### File Descriptions

**app.py** (Main Application)
- Flask app initialization and configuration
- Database functions and initialization
- Input validation functions
- OTP/2FA functions
- Authentication functions
- All route handlers
- ~550 lines with detailed comments

**Templates**
- **base.html**: Navigation bar and flash messages template
- **register.html**: Registration form with password validation display
- **login.html**: Login form with demo credentials info
- **dashboard.html**: Protected page with user info and feature overview
- **verify_otp.html**: 2FA verification form
- **error.html**: Generic error page

**Static/style.css**
- Custom Bootstrap extensions
- Responsive design
- Form styling
- Card animations
- Accessibility features

---

## 📦 Requirements

### System Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Python Packages
- Flask 3.0.0 - Web framework
- Werkzeug 3.0.0 - Password hashing and utilities

See `requirements.txt` for complete list.

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Using Git (if available)
git clone <repository-url>
cd secure-login-system

# Or manually download and extract the ZIP file
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

You should see output:
```
==================================================
Secure Login System - Flask App
==================================================
Starting server on http://127.0.0.1:5000
Press Ctrl+C to stop the server
==================================================
```

### Step 5: Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

## 💻 Usage

### Testing the Application

#### 1. **Register a New Account**
   - Go to the Register page
   - Username: `testuser` (3-20 chars, alphanumeric + underscore)
   - Email: `test@example.com`
   - Password: `Test@12345` (must meet requirements)
   - Click "Create Account"

#### 2. **Login with Your Account**
   - Go to the Login page
   - Enter your username and password
   - Click "Sign In"
   - You'll be redirected to the Dashboard

#### 3. **View Dashboard**
   - See your account information
   - View security status
   - Learn about the application features

#### 4. **Logout**
   - Click the "Logout" button
   - Your session is destroyed
   - You'll be redirected to the login page

#### 5. **Test 2FA (Optional)**
   - When 2FA is enabled for your account
   - After entering correct login credentials
   - You'll be prompted for OTP code
   - OTP is printed to console (demo mode)
   - Enter the 6-digit code to complete login

### Demo Test Case

**Demo Account** (for quick testing):
- Username: `testuser`
- Password: `Test@12345`
- Email: `test@example.com`

---

## 🔒 Security Features Explained

### 1. Password Hashing
```python
# Passwords are hashed using PBKDF2-SHA256
password_hash = generate_password_hash(password, method='pbkdf2:sha256')

# Verification uses constant-time comparison
if check_password_hash(stored_hash, provided_password):
    # Login successful
```

**Why?** Hashing ensures that even if database is breached, passwords remain secure.

### 2. SQL Injection Prevention
```python
# ✓ GOOD - Parameterized query
cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

# ✗ BAD - String concatenation (VULNERABLE!)
cursor.execute(f'SELECT * FROM users WHERE username = {username}')
```

**Why?** Parameterized queries ensure user input is treated as data, not code.

### 3. Input Validation
```python
# Validate username format
if not re.match(r'^[a-zA-Z0-9_]+$', username):
    return False, "Invalid username format"

# Validate password strength
if not re.search(r'[A-Z]', password):
    return False, "Password must contain uppercase"
```

**Why?** Prevents invalid or malicious input from being processed.

### 4. Session Management
```python
session['user_id'] = user['id']
session['username'] = user['username']

# Protected routes check for session
if 'user_id' not in session:
    return redirect(url_for('login'))
```

**Why?** Sessions maintain user state securely without repeatedly sending credentials.

### 5. 2FA with OTP
```python
# Generate unique 6-digit code
otp_code = generate_otp()

# Store with expiration time
expiry_time = datetime.now() + timedelta(minutes=10)

# Verify and mark as used
cursor.execute('''
    UPDATE otp_codes SET is_used = 1 WHERE id = ?
''', (otp_record['id'],))
```

**Why?** 2FA adds extra layer - even if password is compromised, attacker needs OTP code.

---

## 📚 Learning Resources

### Security Concepts Demonstrated

1. **Authentication vs Authorization**
   - Authentication: Verifying user identity (login)
   - Authorization: Checking what user is allowed to do (dashboard access)

2. **Password Security Best Practices**
   - Never store plain-text passwords
   - Use salted hashes (modern libraries do this automatically)
   - Enforce strong password requirements
   - Use PBKDF2, bcrypt, or Argon2 for hashing

3. **OWASP Top 10 Vulnerabilities Addressed**
   - A01: Broken Authentication → Session management
   - A03: Injection → Parameterized queries
   - A04: Insecure Design → Security validation
   - A05: Security Misconfiguration → Session security

4. **Database Security**
   - Parameterized queries
   - Input validation
   - Proper schema design
   - User data isolation

5. **Web Application Security**
   - HTTPS in production (use gunicorn + nginx)
   - CSRF protection (Flask built-in)
   - XSS prevention (template escaping)
   - Secure headers (add Flask-Talisman in production)

### Recommended Learning Path

1. **Beginners**: Read through `app.py` comments to understand flow
2. **Intermediate**: Modify templates or add new features
3. **Advanced**: 
   - Implement password recovery via email
   - Add rate limiting to prevent brute force
   - Implement account lockout after failed attempts
   - Add user profile editing
   - Create admin dashboard

### External Resources

- Flask Documentation: https://flask.palletsprojects.com/
- OWASP Security: https://owasp.org/
- Password Hashing: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- SQLite: https://www.sqlite.org/docs.html

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Database is locked"
**Solution:**
- Close the application
- Delete `database.db`
- Restart the application

### Issue: Cannot access localhost:5000
**Solution:**
1. Ensure Flask is running (check terminal for startup message)
2. Try http://127.0.0.1:5000 instead of http://localhost:5000
3. Check if port 5000 is available: `netstat -an | findstr :5000`
4. Change port in `app.py`: `app.run(port=5001)`

### Issue: Static files (CSS) not loading
**Solution:**
- Restart Flask development server
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure `static/` folder exists

### Issue: OTP code not appearing
**Solution:**
- Check terminal output (prints to console in demo mode)
- Enable print output to see the OTP code
- For production, configure email service

### Issue: Password requirements too strict
**Solution:**
- Modify validation in `validate_password()` function
- Reduce minimum length or character requirements
- Uncomment/modify regex patterns

---

## 🚀 Production Deployment

### Before Going Live

1. **Change Secret Key**
   ```python
   app.secret_key = 'your-secret-key-change-this-in-production'
   ```
   Generate secure key:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Enable HTTPS**
   - Use SSL/TLS certificates
   - Nginx or Apache as reverse proxy
   - Use Flask-Talisman for security headers

3. **Configure Email**
   - Replace demo OTP printing with Flask-Mail
   - Use SendGrid, AWS SES, or similar service

4. **Add Environment Variables**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

5. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

6. **Database Security**
   - Regular backups
   - Encryption at rest
   - Proper file permissions

7. **Monitoring & Logging**
   - Log failed login attempts
   - Monitor for suspicious activity
   - Set up alerts for errors

---

## 🔄 Future Improvements

### Easy Additions
- [ ] Password recovery via email
- [ ] User profile editing
- [ ] Login history tracking
- [ ] Remember me functionality
- [ ] Account deactivation

### Intermediate Features
- [ ] Rate limiting (prevent brute force)
- [ ] Account lockout (after N failed attempts)
- [ ] Email verification on registration
- [ ] Password reset with time-limited token
- [ ] User roles and permissions

### Advanced Features
- [ ] Social login (Google, GitHub OAuth)
- [ ] Biometric authentication
- [ ] Device fingerprinting
- [ ] Geolocation tracking
- [ ] Admin dashboard
- [ ] Audit logging

### Security Enhancements
- [ ] CAPTCHA on login/register
- [ ] API authentication (JWT tokens)
- [ ] Rate limiting per IP
- [ ] Security question backup
- [ ] Recovery codes for 2FA

---

## 📝 Code Comments Guide

The code includes detailed comments explaining:

**Structure Comments**
```python
# ============================================================================
# DESCRIPTIVE SECTION TITLE
# ============================================================================
```

**Function Comments**
```python
def function_name():
    """
    One-line description of what function does.
    
    Additional details about parameters and return values.
    """
```

**Logic Comments**
```python
# Brief explanation of why this code is important
important_code_here()
```

**Warning Comments**
```python
# ⚠️ IMPORTANT: Explanation of why this matters
security_critical_code()
```

---

## 📄 License

This project is provided as an educational resource. Feel free to use, modify, and distribute for learning purposes.

---

## 👨‍🏫 Created For Learning

This project is designed to teach:
- Flask web framework basics
- Authentication and authorization
- Database design and security
- Input validation and sanitization
- Password hashing best practices
- Session management
- User experience design
- Responsive web design with Bootstrap

**Perfect for:**
- Students learning web development
- Developers new to security concepts
- Portfolio projects
- Understanding authentication systems

---

## 🤝 Contributing

Found a bug or have an improvement? Feel free to:
1. Report issues
2. Suggest improvements
3. Submit pull requests
4. Share feedback

---

## ❓ FAQ

**Q: Can I use this in production?**
A: Not directly. You should add HTTPS, email service, real database server, etc. See "Production Deployment" section.

**Q: How do I enable real email for OTP?**
A: Install Flask-Mail, configure SMTP, and replace the `send_otp_email()` function.

**Q: Is the password hashing secure?**
A: Yes, PBKDF2-SHA256 is recommended by OWASP. Werkzeug adds salt automatically.

**Q: Can I customize the UI?**
A: Yes! All templates are in `templates/` folder and CSS is in `static/style.css`.

**Q: How do I reset the database?**
A: Delete `database.db` and restart the app. It will create a new database.

**Q: Can I add more users?**
A: Yes! Use the Register page to create new accounts. Each user is stored in SQLite.

---

## 📞 Support

For questions or issues:
1. Check Troubleshooting section
2. Review code comments in `app.py`
3. Check Flask documentation
4. Review OWASP security guidelines

---

**Happy Learning! 🎓**

This project was created to help developers understand secure authentication systems. The code is intentionally commented extensively so beginners can learn the concepts. Enjoy!
