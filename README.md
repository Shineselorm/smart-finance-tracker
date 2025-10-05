# Smart Personal Finance Tracker

A web-based Django app to manage income and expenses, set budgets, and get insights.

## Tech Stack
- Python 3.10+
- Django 5
- SQLite (default)

## Quick Start
```bash
# Clone the repo
git clone https://github.com/Shineselorm/smart-finance-tracker.git
cd smart-finance-tracker

# Create and activate virtualenv (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install "Django>=5,<6"

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Admin
```bash
python manage.py createsuperuser
```
Then visit `/admin/` to manage Categories, Transactions, and Budgets.

## Apps
- `users` – user-related features (scaffolded)
- `transactions` – models and placeholder views/urls

## Project Structure
- `templates/` – base layout and home page
- `static/` – CSS/JS static assets

## License
MIT
