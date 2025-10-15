# 🔒 Security Guide - Protecting Your Sensitive Data

## ⚠️ IMPORTANT: Never Commit Secrets to Git!

This guide shows you how to safely manage environment variables and sensitive information.

---

## 🛡️ What NOT to Commit

### ❌ NEVER commit these to GitHub:

- Database passwords
- API keys
- Secret keys
- Admin passwords
- Email credentials
- Any `.env` files
- Production database URLs
- Personal information

### ✅ Safe to commit:

- Code files (`.py`, `.html`, `.css`, `.js`)
- Configuration templates
- Documentation
- Requirements files
- Static files

---

## 🔧 Environment Variable Management

### For Local Development:

1. **Create `.env` file** (this is already in `.gitignore`):
   ```bash
   # Create your local environment file
   cp env.template .env
   ```

2. **Edit `.env` with your local values**:
   ```bash
   SECRET_KEY=your-local-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=localpassword123
   EMERGENCY_SECRET=local-secret-123
   ```

3. **Install python-dotenv** (optional, for automatic loading):
   ```bash
   pip install python-dotenv
   ```

### For Production (Render):

Set environment variables in Render Dashboard:
- Go to your Web Service → Environment tab
- Add each variable manually
- Values are encrypted and secure

---

## 🔐 Secure Deployment Checklist

### Before Pushing to GitHub:

- [ ] Check `.gitignore` includes `.env` files
- [ ] Verify no secrets in code files
- [ ] Remove any hardcoded passwords
- [ ] Test that `.env` is not tracked by git

### Commands to check:

```bash
# Check what files are tracked
git status

# Check if .env is ignored
git check-ignore .env

# See what would be committed
git add -n .
```

---

## 🚨 If You Accidentally Commit Secrets

### Immediate Actions:

1. **Remove from Git history:**
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch .env' \
   --prune-empty --tag-name-filter cat -- --all
   ```

2. **Force push to GitHub:**
   ```bash
   git push origin --force --all
   ```

3. **Change all exposed secrets immediately:**
   - Generate new SECRET_KEY
   - Change database passwords
   - Update admin passwords
   - Regenerate API keys

---

## 🔑 Generating Secure Secrets

### Django Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Random Passwords:
```bash
# Generate random password
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Emergency Secret:
```bash
# Generate random secret
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📋 Environment Variables Reference

### Required for Production:

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | Django security | `django-insecure-abc123...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed domains | `.onrender.com` |
| `DATABASE_URL` | Database connection | `postgresql://user:pass@host:5432/db` |
| `ADMIN_USERNAME` | Admin username | `youradmin` |
| `ADMIN_PASSWORD` | Admin password | `SecurePass123!` |
| `EMERGENCY_SECRET` | Emergency access | `random-secret-xyz-999` |

### Optional:

| Variable | Purpose | Example |
|----------|---------|---------|
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Use TLS | `True` |
| `EMAIL_HOST_USER` | Email username | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password | `your-app-password` |

---

## 🛠️ Local Development Setup

### 1. Create local environment:
```bash
# Copy template
cp env.template .env

# Edit with your local values
nano .env  # or use your preferred editor
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run migrations:
```bash
python manage.py migrate
```

### 4. Create superuser:
```bash
python manage.py createsuperuser
```

### 5. Run development server:
```bash
python manage.py runserver
```

---

## 🚀 Production Deployment (Render)

### 1. Set Environment Variables in Render:

Go to: **Render Dashboard → Your Service → Environment**

Add these variables:

```
SECRET_KEY = (generate new one)
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = (auto-populated when you link database)
ADMIN_USERNAME = youradmin
ADMIN_EMAIL = your@email.com
ADMIN_PASSWORD = YourSecurePassword123!
EMERGENCY_SECRET = random-secret-xyz-999
```

### 2. Deploy:
```bash
git add .
git commit -m "Deploy with secure environment variables"
git push origin main
```

---

## 🔍 Security Best Practices

### ✅ DO:

- Use strong, unique passwords
- Generate random secret keys
- Use environment variables for all secrets
- Keep `.env` files in `.gitignore`
- Use HTTPS in production
- Set `DEBUG=False` in production
- Regularly rotate secrets
- Use different secrets for different environments

### ❌ DON'T:

- Commit `.env` files
- Hardcode passwords in code
- Use simple passwords like "admin123"
- Share secrets in chat/email
- Use production secrets in development
- Leave debug mode on in production
- Use the same secrets everywhere

---

## 🆘 Emergency Access

If you get locked out of admin:

### Method 1: Use Emergency Endpoint
```
https://your-app.onrender.com/users/emergency/?secret=YOUR_EMERGENCY_SECRET&username=admin&password=NewPass123
```

### Method 2: Connect to Database
Use TablePlus with your database credentials to reset password directly.

### Method 3: Redeploy with New Admin
Update `ADMIN_PASSWORD` in Render environment and redeploy.

---

## 📊 Monitoring Security

### Check for Exposed Secrets:

```bash
# Search for potential secrets in code
grep -r "password" . --exclude-dir=.git
grep -r "secret" . --exclude-dir=.git
grep -r "key" . --exclude-dir=.git
```

### Regular Security Tasks:

- [ ] Rotate secrets monthly
- [ ] Check for exposed credentials
- [ ] Update dependencies
- [ ] Review access logs
- [ ] Backup database securely

---

## 🎯 Quick Security Checklist

Before every deployment:

- [ ] No secrets in code files
- [ ] `.env` files not tracked by git
- [ ] Strong passwords set
- [ ] Different secrets for different environments
- [ ] Debug mode off in production
- [ ] HTTPS enabled
- [ ] Database credentials secure

---

**Remember: Security is an ongoing process, not a one-time setup!** 🔒

---

**Last Updated:** October 2025
