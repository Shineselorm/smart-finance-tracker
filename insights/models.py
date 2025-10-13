from django.db import models
from django.contrib.auth.models import User

class SpendingInsight(models.Model):
    """
    Stores insights about user spending patterns and predictions.
    """
    INSIGHT_TYPE_CHOICES = [
        ('prediction', 'Spending Prediction'),
        ('alert', 'Overspending Alert'),
        ('recommendation', 'Investment Recommendation'),
        ('tip', 'Financial Tip'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_insight_type_display()} for {self.user.username}"
