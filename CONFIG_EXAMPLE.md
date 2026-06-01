# Configuration Example File

## How to Use This File

1. Copy this file: `cp config.example.py config.py`
2. Update values in `config.py` with your settings
3. Import in `app.py`: `from config import *`

## Development Configuration

```python
# ============================================================================
# FLASK CONFIGURATION - DEVELOPMENT
# ============================================================================

# Flask Settings
DEBUG = True
TESTING = False

# Secret key for session encryption
# Change this to a random string in production!
SECRET_KEY = 'dev-secret-key-change-me'

# Database
DATABASE = 'database.db'

# ============================================================================
# OTP/2FA CONFIGURATION
# ============================================================================

# Demo mode: Print OTP to console instead of sending email
DEMO_MODE = True

# OTP expiration time in minutes
OTP_EXPIRATION_MINUTES = 10

# ============================================================================
# SESSION CONFIGURATION
# ============================================================================

# Session timeout in seconds (1 hour)
PERMANENT_SESSION_LIFETIME = 3600

# ============================================================================
# PASSWORD POLICY
# ============================================================================

# Minimum password length
MIN_PASSWORD_LENGTH = 8

# Username constraints
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20

# ============================================================================
# EMAIL CONFIGURATION (for production)
# ============================================================================

# Email server settings
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'your-email@gmail.com'
# MAIL_PASSWORD = 'your-app-password'

# Or use environment variables:
# import os
# MAIL_SERVER = os.getenv('MAIL_SERVER')
# MAIL_USERNAME = os.getenv('MAIL_USERNAME')
# MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
```

## Production Configuration

```python
# ============================================================================
# FLASK CONFIGURATION - PRODUCTION
# ============================================================================

# Flask Settings
DEBUG = False
TESTING = False

# IMPORTANT: Generate a secure secret key
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = 'your-production-secret-key-here'

# Database
DATABASE = '/var/www/secure-login/database.db'

# ============================================================================
# OTP/2FA CONFIGURATION
# ============================================================================

# Use real email service
DEMO_MODE = False

# OTP expiration time in minutes
OTP_EXPIRATION_MINUTES = 10

# ============================================================================
# SESSION CONFIGURATION
# ============================================================================

# Session settings
SESSION_COOKIE_SECURE = True      # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True    # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
PERMANENT_SESSION_LIFETIME = 3600 # 1 hour

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv('EMAIL_USERNAME')
MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('EMAIL_DEFAULT_SENDER')
```

## Environment Variables (.env file)

Create `.env` file in project root:

```
# Production Settings
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-random-key-here

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password

# Database
DATABASE_URL=sqlite:///database.db

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

Load in app.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY', 'dev-key')
```

## Security Settings for Production

```python
# ============================================================================
# SECURITY HEADERS (Add to app.py)
# ============================================================================

from flask_talisman import Talisman

# Force HTTPS
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'"
    }
)

# ============================================================================
# RATE LIMITING (Optional)
# ============================================================================

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Apply to login route
@limiter.limit("5 per minute")
@app.route('/login', methods=['POST'])
def login():
    pass
```

## Database Configuration

### SQLite (Development)
```python
DATABASE = 'database.db'
```

### PostgreSQL (Production)
```python
import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
```

## Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', 
                                      maxBytes=10240, 
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
```

## Deployment Checklist

- [ ] Change SECRET_KEY to random secure value
- [ ] Set DEBUG = False
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper email service
- [ ] Configure database backups
- [ ] Enable logging
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Configure firewall
- [ ] Use production WSGI server (Gunicorn)
- [ ] Use reverse proxy (Nginx/Apache)
- [ ] Set up CORS if needed
- [ ] Add security headers
- [ ] Configure environment variables
- [ ] Test thoroughly before going live

## Common Issues and Solutions

### SSL Certificate Error
```
# Generate self-signed cert for testing
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# In app.py:
app.run(ssl_context=('cert.pem', 'key.pem'))
```

### Database Connection Issues
- Check database file exists and has proper permissions
- Ensure database path is absolute, not relative
- On production, use managed database service

### Email Not Sending
- Verify SMTP credentials
- Check firewall allows outbound SMTP
- Enable "Less secure app access" for Gmail
- Use app-specific password, not main password

### Session Issues
- Clear browser cookies
- Ensure SECRET_KEY doesn't change between restarts
- Check SESSION_COOKIE settings

---

**Remember: Security is not a feature, it's a requirement!**
Always review and test your security configuration before deployment.
