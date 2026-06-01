# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python (if not already installed)
Visit: https://www.python.org/downloads/
- Download Python 3.8 or higher
- ✅ Check "Add Python to PATH" during installation

### Step 2: Open Terminal/Command Prompt
Navigate to project folder:
```bash
cd path/to/secure-login-system
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

Output should show:
```
Successfully installed Flask-3.0.0 Werkzeug-3.0.0
```

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open in Browser
Go to: **http://127.0.0.1:5000**

---

## 🧪 Test the App in 2 Minutes

1. **Register a new account**
   - Username: `myuser`
   - Email: `myemail@example.com`
   - Password: `SecurePass123`
   - Click "Create Account"

2. **Login with your account**
   - Enter username and password
   - Click "Sign In"
   - See the Dashboard

3. **Logout**
   - Click "Logout" button
   - See goodbye message

---

## ✅ Common Commands

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Run Application
```bash
python app.py
```

### Stop Application
```bash
Ctrl + C
```

### Install New Package
```bash
pip install package-name
```

### See Installed Packages
```bash
pip list
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Install Python from python.org, add to PATH |
| Module not found | Run `pip install -r requirements.txt` |
| Port already in use | Change port in app.py line: `app.run(port=5001)` |
| CSS not loading | Restart Flask, clear browser cache |
| Database locked | Delete `database.db`, restart app |

---

## 📚 Next Steps

1. **Explore the Code**
   - Open `app.py` and read the comments
   - Check `templates/` folder for HTML pages
   - Review `static/style.css` for styling

2. **Make Modifications**
   - Change colors in CSS
   - Add new form fields
   - Customize error messages

3. **Add Features**
   - Password recovery
   - User profile editing
   - Login history
   - Rate limiting

4. **Learn More**
   - Read README.md for detailed information
   - Check Flask documentation
   - Learn about security best practices

---

## 📞 Need Help?

1. Check **Troubleshooting** section in README.md
2. Read code comments in **app.py**
3. Visit Flask docs: https://flask.palletsprojects.com/
4. Check OWASP for security: https://owasp.org/

---

**Good luck! Happy learning! 🎓**
