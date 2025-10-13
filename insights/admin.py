from django.contrib import admin
from .models import SpendingInsight


@admin.register(SpendingInsight)
class SpendingInsightAdmin(admin.ModelAdmin):
    list_display = ['user', 'insight_type', 'title', 'amount', 'is_read', 'created_at']
    list_filter = ['insight_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
