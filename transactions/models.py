from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    date = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} {self.type} {self.amount} on {self.date}"


class Budget(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    PERIOD_CHOICES = (
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
    )
    period = models.CharField(max_length=7, choices=PERIOD_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.category} - {self.period}: {self.limit_amount}"
