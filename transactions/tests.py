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
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
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
