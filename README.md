# Smart Personal Finance Tracker 💰

A comprehensive web-based Django application for managing personal finances with income/expense tracking, budget management, spending predictions, and financial insights.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Key Features

### 🔐 User Authentication
- Secure signup, login, and logout
- User profile management
- Password change functionality
- Session-based authentication

### 💸 Transaction Management
- **Full CRUD Operations:** Add, edit, view, and delete transactions
- **Smart Categorization:** Organize income and expenses by category
- **Advanced Filtering:** Filter by date range, type, and category
- **Real-time Summaries:** Track total income, expenses, and balance
- **Transaction Notes:** Add descriptions to transactions

### 📊 Budget Management
- Set budget limits per category (weekly/monthly)
- Visual progress bars showing spending vs. budget
- Color-coded alerts (warning at 90%, critical at 100%)
- Budget utilization percentage tracking
- Over-budget notifications

### 🎯 Smart Insights (Week 3)
- **Spending Predictions:** Forecast future expenses based on historical data
- **Overspending Alerts:** Real-time notifications when approaching budget limits
- **Investment Recommendations:** Calculate potential savings based on income/expense patterns
- **Financial Tips:** Curated advice for better money management

### 📈 Dashboard & Visualizations
- Interactive Chart.js visualizations
- Weekly income vs. expenses bar chart
- Category-wise spending breakdown (pie chart)
- Recent transactions list
- Summary cards with key metrics

### 🎨 Modern UI/UX
- Glassmorphism landing page with animated hero section
- Responsive sidebar navigation for authenticated users
- Dark/light mode toggle with smooth transitions
- Scroll-to-top button and fade-in animations
- Clean fintech-inspired design system
- Mobile-responsive layouts

## 🛠 Tech Stack

### Backend
- **Framework:** Django 5.2
- **Language:** Python 3.10+
- **Database:** SQLite (development), PostgreSQL-ready (production)
- **Authentication:** Django built-in auth system

### Frontend
- **UI Framework:** Bootstrap 5
- **Icons:** Lucide Icons
- **Charts:** Chart.js
- **Animations:** AOS (Animate On Scroll), CSS transitions


## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Shineselorm/smart-finance-tracker.git
cd smart-finance-tracker
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (for admin access)**
```bash
python manage.py createsuperuser
```

6. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📂 Project Structure

```
smart-finance-tracker/
├── mydjango/                  # Main project directory
│   ├── settings.py            # Django settings
│   ├── production_settings.py # Production configuration
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI application
├── users/                     # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
├── transactions/              # Transaction & budget management app
│   ├── models.py              # Category, Transaction, Budget models
│   ├── views.py               # CRUD views
│   ├── forms.py               # Django forms
│   ├── urls.py
│   └── tests.py
├── insights/                  # Financial insights app (Week 3)
│   ├── models.py              # SpendingInsight model
│   ├── views.py
│   ├── utils.py               # Prediction & recommendation logic
│   ├── urls.py
│   └── tests.py
├── templates/                 # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard
│   ├── landing.html           # Public landing page
│   ├── users/                 # Auth templates
│   ├── transactions/          # Transaction templates
│   └── insights/              # Insights templates
├── static/                    # Static files
│   ├── css/
│   │   ├── fintech.css        # Dashboard & internal pages styles
│   │   └── landing.css        # Landing page styles
│   └── js/
│       ├── landing.js         # Landing page interactions
│       └── scripts.js
├── requirements.txt           # Python dependencies
├── Procfile                   # Deployment configuration
├── runtime.txt                # Python version for deployment
├── manage.py                  # Django CLI
└── README.md                  # Documentation (you are here!)
```

## 🧪 Testing

Run all tests:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test users
python manage.py test transactions
python manage.py test insights
```

Run with verbose output:
```bash
python manage.py test --verbosity=2
```

**Test Coverage:**
- ✅ 29 tests passing
- ✅ Model tests (Category, Transaction, Budget, SpendingInsight)
- ✅ View tests (authentication, CRUD operations, filtering)
- ✅ Utility function tests (predictions, alerts, recommendations)
- ✅ Form validation tests

## 📖 Usage Guide

### 1. Create an Account
- Navigate to the landing page
- Click "Get Started" or "Sign Up"
- Fill in username, email, and password
- Log in with your credentials

### 2. Add Categories
- Go to **Categories** in the sidebar
- Click "Add Category"
- Choose a name and type (Income or Expense)
- Save

### 3. Add Transactions
- Navigate to **Transactions**
- Click "Add Transaction"
- Select category, amount, type, date
- Add an optional note
- Save

### 4. Set Budgets
- Go to **Budgets**
- Click "Add Budget"
- Choose a category (expense only)
- Set a limit amount and period (weekly/monthly)
- Save

### 5. View Insights
- Navigate to **Insights** in the sidebar
- View spending predictions, overspending alerts, and investment recommendations
- Mark insights as read or delete them

### 6. Monitor Dashboard
- The **Dashboard** shows:
  - Total income, expenses, and balance
  - Weekly income vs. expenses chart
  - Category-wise spending breakdown
  - Recent transactions

## 🌐 Deployment

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: Set to `False`
   - `DATABASE_URL`: Auto-provided by Render (if using PostgreSQL)
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn mydjango.wsgi:application`

### Deploy to Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
6. Push to Heroku: `git push heroku main`
7. Run migrations: `heroku run python manage.py migrate`
8. Create superuser: `heroku run python manage.py createsuperuser`

##  Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Keep dependencies updated

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request


## 👤 Author

**Selorm Sedzi**
- GitHub: [@Shineselorm](https://github.com/Shineselorm)
- Project: [Smart Finance Tracker](https://github.com/Shineselorm/smart-finance-tracker)

## 🙏 Acknowledgments

- Django documentation
- Bootstrap team
- Chart.js library
- Lucide Icons
- ALX Backend Development Program

## 📧 Support

For support or questions, please open an issue on the [GitHub repository](https://github.com/Shineselorm/smart-finance-tracker/issues).

---

**Note:** This project was developed as part of the ALX Backend Development capstone project.

Made with ❤️ by Shine Selorm Sedziafa
