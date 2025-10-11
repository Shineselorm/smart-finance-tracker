# Smart Personal Finance Tracker

A comprehensive web-based Django application to manage personal finances with income/expense tracking, budget management, and financial insights.

## ✨ Features

### Week 1 (Completed)
- ✅ Django project setup with SQLite database
- ✅ Core models: Category, Transaction, Budget
- ✅ Django Admin interface for data management
- ✅ Bootstrap 5 responsive UI
- ✅ Static files configuration

### Week 2 (Completed)
- ✅ **User Authentication System**
  - Signup, Login, Logout functionality
  - User profile page with password change
  - Protected routes with `@login_required` decorator
  
- ✅ **Transaction Management (Full CRUD)**
  - Add, edit, delete transactions
  - Filter by category, type, date range
  - Income/expense categorization
  - Summary cards (total income, expenses, balance)
  
- ✅ **Category Management**
  - Create and manage income/expense categories
  - View categories organized by type
  
- ✅ **Budget Management**
  - Set budget limits per category (weekly/monthly)
  - Visual progress bars showing budget usage
  - Over-budget alerts and warnings
  - Remaining balance tracking

- ✅ **Enhanced UI/UX**
  - Django messages framework for user feedback
  - Responsive Bootstrap 5 design
  - Clean, intuitive navigation
  - Dynamic user authentication navbar

## 🛠 Tech Stack
- **Backend:** Python 3.10+, Django 5.2
- **Database:** SQLite (default)
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Testing:** Django TestCase

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Shineselorm/smart-finance-tracker.git
cd smart-finance-tracker

# Create and activate virtual environment (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## 📱 Usage

1. **Sign Up**: Create a new account at `/users/signup/`
2. **Login**: Access your account at `/users/login/`
3. **Add Categories**: Navigate to Categories and create income/expense categories
4. **Add Transactions**: Record your income and expenses with details
5. **Set Budgets**: Create budget limits for expense categories
6. **Monitor**: Track your spending against budgets with visual progress bars

## 🔐 Admin Interface

Access the Django admin at `/admin/` to:
- Manage users
- View and edit all transactions
- Configure categories and budgets

```bash
python manage.py createsuperuser
```

## 🧪 Running Tests

```bash
python manage.py test
```

All 12 tests should pass, covering:
- Model creation and validation
- User authentication flows
- View access controls
- CRUD operations

## 📂 Project Structure

```
smart-finance-tracker/
├── mydjango/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                 # User authentication app
│   ├── forms.py          # Signup and login forms
│   ├── views.py          # Auth views
│   ├── urls.py
│   └── tests.py
├── transactions/          # Core finance app
│   ├── models.py         # Category, Transaction, Budget models
│   ├── forms.py          # Transaction, Category, Budget forms
│   ├── views.py          # CRUD views with filtering
│   ├── urls.py
│   ├── admin.py          # Admin configuration
│   └── tests.py
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Home page
│   ├── users/            # Authentication templates
│   └── transactions/     # Transaction/Budget templates
├── static/
│   ├── css/styles.css    # Custom styles
│   └── js/scripts.js     # Custom JavaScript
├── requirements.txt       # Python dependencies
└── manage.py
```

## 🎯 Upcoming Features (Week 3 & 4)

- 📊 Dashboard with Chart.js visualizations
- 🔮 Spending pattern predictions
- ⚠️ Overspending alerts
- 💡 Investment recommendations
- 📚 Financial education reads
- 🌍 Currency conversion (API integration)

## 📝 License
MIT

## 👤 Author
ALX Backend Development Capstone Project
