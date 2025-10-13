from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta
from .models import SpendingInsight
from .utils import (
    calculate_spending_prediction,
    check_overspending_alerts,
    generate_investment_recommendation,
    generate_insights_for_user
)
from transactions.models import Transaction, Category, Budget


class SpendingInsightModelTest(TestCase):
    """Test the SpendingInsight model."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_insight_creation(self):
        """Test creating a spending insight."""
        insight = SpendingInsight.objects.create(
            user=self.user,
            insight_type='prediction',
            title='Test Prediction',
            message='This is a test prediction',
            amount=Decimal('1000.00')
        )
        
        self.assertEqual(insight.user, self.user)
        self.assertEqual(insight.insight_type, 'prediction')
        self.assertFalse(insight.is_read)
        self.assertEqual(str(insight), f"Spending Prediction for {self.user.username}")
    
    def test_insight_ordering(self):
        """Test that insights are ordered by creation date (newest first)."""
        insight1 = SpendingInsight.objects.create(
            user=self.user,
            insight_type='alert',
            title='Old Alert',
            message='Old message'
        )
        
        insight2 = SpendingInsight.objects.create(
            user=self.user,
            insight_type='alert',
            title='New Alert',
            message='New message'
        )
        
        insights = SpendingInsight.objects.all()
        self.assertEqual(insights[0], insight2)
        self.assertEqual(insights[1], insight1)


class InsightsUtilsTest(TestCase):
    """Test the insights utility functions."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Food', type='expense')
    
    def test_spending_prediction_insufficient_data(self):
        """Test prediction with insufficient transaction data."""
        prediction = calculate_spending_prediction(self.user)
        self.assertIsNone(prediction)
    
    def test_spending_prediction_with_data(self):
        """Test prediction with sufficient transaction data."""
        # Create 10 transactions over the past 3 months
        for i in range(10):
            Transaction.objects.create(
                user=self.user,
                category=self.category,
                amount=Decimal('100.00'),
                type='expense',
                date=datetime.now() - timedelta(days=i*9)
            )
        
        prediction = calculate_spending_prediction(self.user)
        self.assertIsNotNone(prediction)
        self.assertIn('amount', prediction)
        self.assertIn('average', prediction)
        self.assertIn('confidence', prediction)
        self.assertGreater(prediction['amount'], 0)
    
    def test_overspending_alerts(self):
        """Test overspending alert generation."""
        # Create a budget
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            limit_amount=Decimal('100.00'),
            period='monthly'
        )
        
        # Create a transaction that exceeds the budget
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('95.00'),
            type='expense',
            date=datetime.now()
        )
        
        alerts = check_overspending_alerts(self.user)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['category'], 'Food')
        self.assertEqual(alerts[0]['severity'], 'warning')
    
    def test_investment_recommendation_no_balance(self):
        """Test investment recommendation with no positive balance."""
        # Create expenses only
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.00'),
            type='expense',
            date=datetime.now()
        )
        
        recommendation = generate_investment_recommendation(self.user)
        self.assertIsNone(recommendation)
    
    def test_investment_recommendation_with_balance(self):
        """Test investment recommendation with positive balance."""
        # Create income
        income_category = Category.objects.create(name='Salary', type='income')
        Transaction.objects.create(
            user=self.user,
            category=income_category,
            amount=Decimal('2000.00'),
            type='income',
            date=datetime.now()
        )
        
        # Create expense
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('500.00'),
            type='expense',
            date=datetime.now()
        )
        
        recommendation = generate_investment_recommendation(self.user)
        self.assertIsNotNone(recommendation)
        self.assertIn('balance', recommendation)
        self.assertIn('recommended', recommendation)
        self.assertEqual(recommendation['balance'], 1500.00)


class InsightsViewsTest(TestCase):
    """Test the insights views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
    
    def test_insights_dashboard_requires_login(self):
        """Test that insights dashboard requires authentication."""
        self.client.logout()
        response = self.client.get(reverse('insights_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_insights_dashboard_authenticated(self):
        """Test insights dashboard for authenticated user."""
        response = self.client.get(reverse('insights_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insights/insights_dashboard.html')
        self.assertIn('predictions', response.context)
        self.assertIn('alerts', response.context)
        self.assertIn('recommendations', response.context)
    
    def test_mark_insight_read(self):
        """Test marking an insight as read."""
        insight = SpendingInsight.objects.create(
            user=self.user,
            insight_type='tip',
            title='Test Tip',
            message='Test message',
            is_read=False
        )
        
        response = self.client.get(reverse('mark_insight_read', args=[insight.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        insight.refresh_from_db()
        self.assertTrue(insight.is_read)
    
    def test_delete_insight(self):
        """Test deleting an insight."""
        insight = SpendingInsight.objects.create(
            user=self.user,
            insight_type='tip',
            title='Test Tip',
            message='Test message'
        )
        
        response = self.client.get(reverse('delete_insight', args=[insight.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Verify insight is deleted
        self.assertFalse(SpendingInsight.objects.filter(pk=insight.pk).exists())
    
    def test_user_cannot_access_other_users_insights(self):
        """Test that users can only access their own insights."""
        other_user = User.objects.create_user(username='otheruser', password='testpass123')
        insight = SpendingInsight.objects.create(
            user=other_user,
            insight_type='tip',
            title='Other User Tip',
            message='Test message'
        )
        
        # Try to mark other user's insight as read
        response = self.client.get(reverse('mark_insight_read', args=[insight.pk]))
        self.assertEqual(response.status_code, 404)  # Not found
