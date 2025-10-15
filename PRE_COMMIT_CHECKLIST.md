# ✅ Pre-Commit Security Checklist

## 🔒 Before Pushing to GitHub - Run This Checklist

### 1. Check for Hardcoded Secrets
```bash
# Search for potential secrets
grep -r "password\|secret\|key" . --exclude-dir=.git --exclude="*.md" --exclude="env.template"
```

**Expected:** Only test files should show passwords (like `testpass123`)

### 2. Verify .env is Ignored
```bash
git check-ignore .env
```

**Expected:** Should show `.env` (meaning it's ignored)

### 3. Check What Will Be Committed
```bash
git status
git add -n .
```

**Expected:** No `.env` files, no database files, no secrets

### 4. Review Environment Variables
- ✅ SECRET_KEY uses environment variable
- ✅ Database uses environment variable
- ✅ No hardcoded passwords
- ✅ No API keys in code

### 5. Test Local Environment
```bash
# Create .env file for local development
cp env.template .env
# Edit .env with your local values
```

---

## 🚨 If You Find Secrets

### Immediate Actions:
1. **Remove from code**
2. **Add to .gitignore**
3. **Use environment variables instead**
4. **Change exposed secrets immediately**

### Example Fix:
```python
# ❌ BAD - Hardcoded secret
SECRET_KEY = 'django-insecure-abc123...'

# ✅ GOOD - Environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-for-dev')
```

---

## 📋 Safe to Commit

### ✅ These files are safe:
- Code files (`.py`, `.html`, `.css`, `.js`)
- Configuration templates (`env.template`)
- Documentation (`.md` files)
- Requirements (`requirements.txt`)
- Static files
- Templates

### ❌ Never commit:
- `.env` files
- Database files (`.sqlite3`, `.db`)
- Secret keys
- Passwords
- API keys
- Personal information

---

## 🎯 Quick Commands

### Check everything is secure:
```bash
# 1. Check git status
git status

# 2. Check for secrets
grep -r "password\|secret\|key" . --exclude-dir=.git --exclude="*.md" --exclude="env.template"

# 3. Verify .env is ignored
git check-ignore .env

# 4. See what would be committed
git add -n .
```

### If all checks pass:
```bash
git add .
git commit -m "Add secure environment variable management"
git push origin main
```

---

## 🔐 Production Deployment

### Set these in Render Environment:
```
SECRET_KEY = (generate new one)
DEBUG = False
ALLOWED_HOSTS = .onrender.com
DATABASE_URL = (auto-populated)
ADMIN_USERNAME = youradmin
ADMIN_PASSWORD = YourSecurePassword123!
EMERGENCY_SECRET = random-secret-xyz-999
```

### Generate new SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

**Remember: Security is everyone's responsibility!** 🔒
