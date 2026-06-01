# 🛠️ Customization and Extension Guide

This guide shows you how to add new features and customize the application to fit your needs.

---

## 📝 Table of Contents

1. [Database Modifications](#database-modifications)
2. [Adding New Pages](#adding-new-pages)
3. [Adding Form Fields](#adding-form-fields)
4. [Styling Customization](#styling-customization)
5. [Feature Implementations](#feature-implementations)

---

## 🗄️ Database Modifications

### Adding a New Column to Users Table

**Step 1: Add column to database initialization**

In `app.py`, modify the `init_db()` function:

```python
def init_db():
    # ... existing code ...
    
    # Add this ALTER TABLE statement AFTER creating the users table
    cursor.execute('''
        ALTER TABLE users ADD COLUMN phone_number TEXT
    ''')
    # Note: This only works if users table doesn't exist
    # For existing database, delete database.db and restart
```

**Step 2: Update the register form**

In `templates/register.html`, add:

```html
<div class="mb-3">
    <label for="phone" class="form-label">Phone Number</label>
    <input type="tel" class="form-control" id="phone" name="phone" 
           placeholder="(123) 456-7890">
</div>
```

**Step 3: Update the Flask route**

In `app.py`, modify the `register` route:

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ... existing code ...
        phone = request.form.get('phone', '').strip()
        
        # Update register_user call
        success, message = register_user(username, password, email, phone)
```

**Step 4: Update register_user function**

```python
def register_user(username, password, email, phone=''):
    # ... validation code ...
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, phone_number)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, email, phone))
        
        conn.commit()
        conn.close()
        return True, "Registration successful!"
```

---

## 📄 Adding New Pages

### Example: User Profile Page

**Step 1: Create template file**

Create `templates/profile.html`:

```html
{% extends "base.html" %}

{% block title %}User Profile - Secure Login System{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">User Profile</h5>
                </div>
                <div class="card-body">
                    <p><strong>Username:</strong> {{ user.username }}</p>
                    <p><strong>Email:</strong> {{ user.email }}</p>
                    <p><strong>Member Since:</strong> {{ user.created_at }}</p>
                    
                    <form method="POST" action="{{ url_for('update_profile') }}">
                        <div class="mb-3">
                            <label class="form-label">New Email</label>
                            <input type="email" class="form-control" name="email">
                        </div>
                        <button type="submit" class="btn btn-primary">Update Profile</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Step 2: Add route in app.py**

```python
@app.route('/profile')
def profile():
    """User profile page (protected route)."""
    if 'user_id' not in session:
        flash('Please login first.', 'error')
        return redirect(url_for('login'))
    
    user = get_user(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    """Update user profile."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_email = request.form.get('email')
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET email = ? WHERE id = ?
    ''', (new_email, user_id))
    
    conn.commit()
    conn.close()
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))
```

**Step 3: Add link to navigation**

In `templates/base.html`, update navbar:

```html
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('profile') }}">Profile</a>
</li>
```

---

## 📋 Adding Form Fields

### Example: Adding a "Favorite Color" Field

**Step 1: Add database column**

```python
# Add to init_db() in users table creation
cursor.execute('''
    ALTER TABLE users ADD COLUMN favorite_color TEXT
''')
```

**Step 2: Add to registration form**

```html
<div class="mb-3">
    <label for="color" class="form-label">Favorite Color</label>
    <input type="color" class="form-control" id="color" name="color">
</div>
```

**Step 3: Handle in Flask route**

```python
color = request.form.get('color', '#0000FF')
success, message = register_user(username, password, email, color)
```

---

## 🎨 Styling Customization

### Change Primary Color

In `static/style.css`:

```css
:root {
    /* Change from blue to green */
    --primary-color: #28a745;  /* was #007bff */
    --secondary-color: #6c757d;
    /* ... rest of colors ... */
}
```

### Add Custom Background

```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* or background image */
    background-image: url('path/to/image.jpg');
    background-attachment: fixed;
}
```

### Customize Card Styling

```css
.card {
    /* Add shadow */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    /* Add border */
    border: 2px solid #007bff;
    /* Round corners more */
    border-radius: 15px;
}
```

---

## 🚀 Feature Implementations

### 1. Password Recovery/Reset

**Database Table**

```python
cursor.execute('''
    CREATE TABLE password_resets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reset_token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
```

**Route**

```python
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            expiry = datetime.now() + timedelta(hours=1)
            
            cursor.execute('''
                INSERT INTO password_resets (user_id, reset_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user['id'], reset_token, expiry))
            
            conn.commit()
        
        conn.close()
        flash('Check your email for password reset link.', 'info')
        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')
```

### 2. Login History

**Database Table**

```python
cursor.execute('''
    CREATE TABLE login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        success INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
```

**Log Login**

```python
def log_login(user_id, success=True):
    """Log login attempt."""
    from flask import request
    
    ip_address = request.remote_addr
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO login_history (user_id, ip_address, success)
        VALUES (?, ?, ?)
    ''', (user_id, ip_address, success))
    
    conn.commit()
    conn.close()

# Call in login route
if success:
    log_login(user['id'], True)
```

### 3. Account Lockout

```python
def attempt_login(username, password, max_attempts=5):
    """Login with attempt tracking."""
    # Get recent failed attempts
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as attempts 
        FROM login_history 
        WHERE user_id = (
            SELECT id FROM users WHERE username = ?
        )
        AND success = 0
        AND login_time > datetime('now', '-15 minutes')
    ''', (username,))
    
    result = cursor.fetchone()
    attempts = result['attempts'] if result else 0
    
    if attempts >= max_attempts:
        flash('Too many failed login attempts. Please try again later.', 'error')
        return False, None, "Account temporarily locked"
    
    # Proceed with normal login
    return login_user(username, password)
```

### 4. User Roles/Permissions

**Database Table**

```python
cursor.execute('''
    CREATE TABLE user_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,  -- 'admin', 'moderator', 'user'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
```

**Check Permission**

```python
def has_permission(user_id, required_role):
    """Check if user has required permission."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT role FROM user_roles 
        WHERE user_id = ? AND role = ?
    ''', (user_id, required_role))
    
    permission = cursor.fetchone()
    conn.close()
    
    return permission is not None

def admin_only(f):
    """Decorator for admin-only routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not has_permission(session.get('user_id'), 'admin'):
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Usage
@app.route('/admin')
@admin_only
def admin_panel():
    return render_template('admin.html')
```

### 5. Email Verification

**Update Registration**

```python
def register_user(username, password, email):
    # ... existing validation ...
    
    verification_token = secrets.token_urlsafe(32)
    
    cursor.execute('''
        INSERT INTO users (username, password_hash, email, email_verified)
        VALUES (?, ?, ?, ?)
    ''', (username, password_hash, email, 0))
    
    # Send verification email
    send_verification_email(email, verification_token)
    
    flash('Check your email to verify your account!', 'info')
```

---

## 📚 Best Practices for Extending

### Do's ✅

- Always validate user input
- Use parameterized queries
- Hash passwords and sensitive data
- Log important actions
- Test thoroughly
- Document your changes
- Use meaningful variable names
- Add comments to new code
- Follow existing code style

### Don'ts ❌

- Don't hardcode sensitive values
- Don't concatenate user input into SQL
- Don't store plain-text passwords
- Don't skip validation
- Don't remove security features
- Don't modify database directly without backup
- Don't expose error messages to users
- Don't commit .env or database files

---

## 🧪 Testing Your Changes

```python
# Add to app.py for testing
if __name__ == '__main__':
    # Test mode
    app.config['TESTING'] = True
    
    # Create test database
    TEST_DB = 'test_database.db'
    
    # Run tests
    init_db()
    app.run(debug=True)
```

---

## 📖 Common Modifications Summary

| Feature | Files to Modify | Difficulty |
|---------|-----------------|-----------|
| Add database field | app.py, register.html, route | Easy |
| Add new page | Create .html, add route | Easy |
| Change colors | static/style.css | Easy |
| Add login history | app.py (database + route) | Medium |
| Add 2FA | app.py, templates | Medium |
| Add user roles | app.py (database + logic) | Hard |
| Email integration | app.py, requirements.txt | Hard |
| API endpoints | app.py | Hard |

---

## 🔗 Resources

- Flask Extension Registry: https://flask.palletsprojects.com/extensions/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Python Security: https://owasp.org/
- Bootstrap Docs: https://getbootstrap.com/docs/

---

**Happy coding! Have fun extending the application! 🎉**
