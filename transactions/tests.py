from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date
from .models import Category, Transaction, Budget


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Food',
            type='expense'
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Food')
        self.assertEqual(self.category.type, 'expense')
        self.assertEqual(str(self.category), 'Food (expense)')


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Salary',
            type='income'
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('1000.00'),
            type='income',
            date=date.today(),
            note='Test transaction'
        )
    
    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, Decimal('1000.00'))
        self.assertEqual(self.transaction.type, 'income')
        self.assertEqual(self.transaction.user, self.user)
    
    def test_transaction_ordering(self):
        """Test that transactions are ordered by date (newest first)."""
        from datetime import timedelta
        
        # Create an older transaction
        older_transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('500.00'),
            type='income',
            date=date.today() - timedelta(days=1),
            note='Older transaction'
        )
        
        transactions = Transaction.objects.all()
        # Newer transactions (self.transaction with today's date) should come first
        self.assertEqual(transactions[0], self.transaction)
        self.assertEqual(transactions[1], older_transaction)


class BudgetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            type='expense'
        )
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            limit_amount=Decimal('500.00'),
            period='monthly'
        )
    
    def test_budget_creation(self):
        self.assertEqual(self.budget.limit_amount, Decimal('500.00'))
        self.assertEqual(self.budget.period, 'monthly')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Food',
            type='expense'
        )
    
    def test_home_view_unauthenticated(self):
        """Test that unauthenticated users see landing page."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
    
    def test_home_view_authenticated(self):
        """Test that authenticated users see dashboard."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('total_income', response.context)
        self.assertIn('total_expense', response.context)
    
    def test_transactions_list_requires_login(self):
        response = self.client.get(reverse('transactions_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_transactions_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('transactions_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transactions_list.html')
    
    def test_transaction_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('transaction_create'), {
            'category': self.category.id,
            'amount': '100.00',
            'type': 'expense',
            'date': date.today(),
            'note': 'Test'
        })
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Redirect after success
    
    def test_transaction_filtering(self):
        """Test transaction filtering by type."""
        self.client.login(username='testuser', password='testpass123')
        
        # Create transactions
        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('100.00'),
            type='expense',
            date=date.today()
        )
        
        income_category = Category.objects.create(name='Salary', type='income')
        Transaction.objects.create(
            user=self.user,
            category=income_category,
            amount=Decimal('1000.00'),
            type='income',
            date=date.today()
        )
        
        # Test filtering by type
        response = self.client.get(reverse('transactions_list') + '?type=expense')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)
    
    def test_budget_create(self):
        """Test creating a budget."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('budget_create'), {
            'category': self.category.id,
            'limit_amount': '500.00',
            'period': 'monthly'
        })
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
    
    def test_category_create(self):
        """Test creating a category."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('category_create'), {
            'name': 'Transport',
            'type': 'expense'
        })
        self.assertEqual(Category.objects.count(), 2)  # Including setup category
        self.assertEqual(response.status_code, 302)
