# Deployment Guide for Smart Personal Finance Tracker

This guide provides step-by-step instructions for deploying the Smart Personal Finance Tracker to various cloud platforms.

## 📋 Pre-Deployment Checklist

- [ ] All tests passing (`python manage.py test`)
- [ ] Static files collecting successfully (`python manage.py collectstatic`)
- [ ] Database migrations up to date (`python manage.py migrate`)
- [ ] Environment variables configured
- [ ] Secret key generated for production
- [ ] DEBUG set to False in production

## 🚀 Deployment Options

### Option 1: Deploy to Render

[Render](https://render.com) is recommended for its simplicity and free tier support.

#### Step 1: Prepare Your Repository

Ensure your code is pushed to GitHub:
```bash
git add -A
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Create a Render Account

1. Sign up at https://render.com
2. Connect your GitHub account

#### Step 3: Create a Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Shineselorm/smart-finance-tracker`
3. Configure the service:
   - **Name:** `smart-finance-tracker` (or your preferred name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn mydjango.wsgi:application`

#### Step 4: Set Environment Variables

Add the following environment variables in Render dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.10.15` | Python version |
| `SECRET_KEY` | Generate new key* | Django secret key |
| `DEBUG` | `False` | Disable debug mode |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed hostnames |

*Generate a new secret key using:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 5: Add PostgreSQL Database (Optional)

1. In Render dashboard, create a new PostgreSQL database
2. Copy the **Internal Database URL**
3. Add it as environment variable:
   - `DATABASE_URL`: Your PostgreSQL connection string

#### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete (5-10 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

#### Step 7: Post-Deployment

Run migrations and create superuser via Render Shell:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

### Option 2: Deploy to Heroku

#### Step 1: Install Heroku CLI

Download from https://devcenter.heroku.com/articles/heroku-cli

#### Step 2: Login to Heroku

```bash
heroku login
```

#### Step 3: Create a New App

```bash
heroku create your-app-name
```

#### Step 4: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 5: Set Environment Variables

```bash
heroku config:set SECRET_KEY='your-generated-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='.herokuapp.com'
```

#### Step 6: Deploy

```bash
git push heroku main
```

#### Step 7: Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

#### Step 8: Open Your App

```bash
heroku open
```

---

### Option 3: Deploy to Railway

#### Step 1: Create Railway Account

Sign up at https://railway.app

#### Step 2: New Project from GitHub

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

#### Step 3: Add PostgreSQL

1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway will auto-provide `DATABASE_URL`

#### Step 4: Configure Environment Variables

Add in Railway dashboard:
- `SECRET_KEY`: Your generated key
- `DEBUG`: False
- `ALLOWED_HOSTS`: `.railway.app`

#### Step 5: Deploy

Railway will automatically deploy. Your app will be available at:
`https://your-app-name.up.railway.app`

---

## 🔧 Production Settings

The project includes `mydjango/production_settings.py` with:

✅ Security headers (HSTS, XSS protection)  
✅ WhiteNoise for static files  
✅ PostgreSQL database support  
✅ Gunicorn WSGI server  
✅ Secure cookies  
✅ SSL redirect  

To use production settings:
```bash
export DJANGO_SETTINGS_MODULE=mydjango.production_settings
```

Or in your platform's environment variables.

---

## 🔐 Security Best Practices

1. **Never commit sensitive data**
   - Use environment variables for `SECRET_KEY`
   - Never commit `.env` files

2. **Use HTTPS in production**
   - Most platforms provide free SSL certificates
   - Enable `SECURE_SSL_REDIRECT` in production

3. **Keep dependencies updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

4. **Set strong SECRET_KEY**
   - Minimum 50 characters
   - Use random alphanumeric characters

5. **Enable ALLOWED_HOSTS**
   - Only allow your domain
   - Example: `['myapp.com', 'www.myapp.com']`

---

## 🧪 Testing Production Locally

Before deploying, test production settings locally:

1. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn mydjango.wsgi:application
   ```

3. **Check for errors:**
   ```bash
   python manage.py check --deploy
   ```

---

## 📊 Monitoring and Logs

### Render
View logs in Render dashboard under "Logs" tab

### Heroku
```bash
heroku logs --tail
```

### Railway
View logs in Railway dashboard

---

## 🆘 Troubleshooting

### Static files not loading
- Ensure `collectstatic` ran successfully
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise is installed and configured

### Database connection errors
- Verify `DATABASE_URL` environment variable
- Check PostgreSQL addon is active
- Ensure `psycopg2-binary` is in requirements.txt

### Application won't start
- Check Gunicorn is installed
- Verify `Procfile` is present and correct
- Review platform logs for detailed errors

### 500 Internal Server Error
- Set `DEBUG=True` temporarily to see error details
- Check application logs
- Verify all migrations are applied

---

## 📝 Post-Deployment Checklist

- [ ] Application accessible via URL
- [ ] Static files loading correctly
- [ ] Database migrations applied
- [ ] Superuser account created
- [ ] Admin panel accessible
- [ ] User registration working
- [ ] Transaction CRUD operations working
- [ ] Charts displaying correctly
- [ ] Insights generating properly

---

## 🔄 Continuous Deployment

### Automatic Deployment on Push

Most platforms support automatic deployment:

**Render:** Automatically deploys on every push to `main` branch

**Heroku:** Enable automatic deploys in dashboard:
1. Go to "Deploy" tab
2. Connect GitHub repository
3. Enable "Automatic Deploys"

**Railway:** Automatically deploys on every push

---

## 📞 Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Open an issue on GitHub

---

**Made with ❤️ by Selorm Sedzi**

