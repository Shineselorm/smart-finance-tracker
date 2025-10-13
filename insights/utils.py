"""
Utility functions for generating financial insights, predictions, and recommendations.
"""
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Avg
from transactions.models import Transaction, Budget
from .models import SpendingInsight


def calculate_spending_prediction(user):
    """
    Predict next month's spending based on historical average.
    Returns a dictionary with prediction details.
    """
    transactions = Transaction.objects.filter(user=user, type='expense')
    
    if transactions.count() < 5:
        return None
    
    # Calculate average monthly spending (last 3 months)
    three_months_ago = datetime.now() - timedelta(days=90)
    recent_spending = transactions.filter(date__gte=three_months_ago).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Average per month
    avg_monthly = float(recent_spending) / 3
    predicted_next_month = avg_monthly * 1.05  # Add 5% buffer
    
    return {
        'amount': round(predicted_next_month, 2),
        'average': round(avg_monthly, 2),
        'confidence': 'medium' if transactions.count() > 20 else 'low'
    }


def check_overspending_alerts(user):
    """
    Check if user is over budget in any category and return alerts.
    Returns a list of alert dictionaries.
    """
    alerts = []
    budgets = Budget.objects.filter(user=user)
    
    for budget in budgets:
        # Calculate spending in this category for the current period
        if budget.period == 'weekly':
            start_date = datetime.now() - timedelta(days=7)
        else:  # monthly
            start_date = datetime.now().replace(day=1)
        
        spent = Transaction.objects.filter(
            user=user,
            category=budget.category,
            type='expense',
            date__gte=start_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        percentage = (float(spent) / float(budget.limit_amount)) * 100 if budget.limit_amount > 0 else 0
        
        if percentage >= 90:
            alerts.append({
                'category': budget.category.name,
                'spent': float(spent),
                'limit': float(budget.limit_amount),
                'percentage': round(percentage, 1),
                'severity': 'critical' if percentage >= 100 else 'warning'
            })
    
    return alerts


def generate_investment_recommendation(user):
    """
    Calculate potential savings/investment amount based on income and expenses.
    Returns a dictionary with recommendation details.
    """
    # Get income and expenses for current month
    month_start = datetime.now().replace(day=1)
    
    transactions = Transaction.objects.filter(user=user, date__gte=month_start)
    income = float(transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0)
    expenses = float(transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0)
    
    balance = income - expenses
    
    if balance <= 0:
        return None
    
    # Recommend saving 20-30% of remaining balance
    conservative_save = balance * 0.20
    moderate_save = balance * 0.25
    aggressive_save = balance * 0.30
    
    return {
        'balance': round(balance, 2),
        'conservative': round(conservative_save, 2),
        'moderate': round(moderate_save, 2),
        'aggressive': round(aggressive_save, 2),
        'recommended': round(moderate_save, 2)  # Default to moderate
    }


def generate_insights_for_user(user):
    """
    Generate all types of insights for a user and save them to the database.
    """
    # Clear old unread insights (older than 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    SpendingInsight.objects.filter(user=user, is_read=False, created_at__lt=week_ago).delete()
    
    # Spending Prediction
    prediction = calculate_spending_prediction(user)
    if prediction:
        SpendingInsight.objects.get_or_create(
            user=user,
            insight_type='prediction',
            title='Next Month Spending Forecast',
            defaults={
                'message': f'Based on your recent spending patterns, you are likely to spend around GH₵{prediction["amount"]} next month. Your average monthly spending is GH₵{prediction["average"]}.',
                'amount': Decimal(str(prediction['amount']))
            }
        )
    
    # Overspending Alerts
    alerts = check_overspending_alerts(user)
    for alert in alerts:
        severity_text = "CRITICAL" if alert['severity'] == 'critical' else "WARNING"
        SpendingInsight.objects.get_or_create(
            user=user,
            insight_type='alert',
            title=f'{severity_text}: {alert["category"]} Budget Alert',
            defaults={
                'message': f'You have spent GH₵{alert["spent"]:.2f} ({alert["percentage"]:.1f}%) of your GH₵{alert["limit"]:.2f} budget for {alert["category"]}.',
                'amount': Decimal(str(alert['spent']))
            }
        )
    
    # Investment Recommendation
    recommendation = generate_investment_recommendation(user)
    if recommendation:
        SpendingInsight.objects.get_or_create(
            user=user,
            insight_type='recommendation',
            title='Investment Opportunity',
            defaults={
                'message': f'You have GH₵{recommendation["balance"]:.2f} in available balance this month. Consider saving GH₵{recommendation["recommended"]:.2f} (25%) towards your financial goals or investments.',
                'amount': Decimal(str(recommendation['recommended']))
            }
        )
    
    return True

