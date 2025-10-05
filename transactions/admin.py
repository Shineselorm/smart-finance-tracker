from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "type", "amount", "date")
    list_filter = ("type", "category")
    search_fields = ("note",)
    autocomplete_fields = ("user", "category")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "period", "limit_amount")
    list_filter = ("period", "category")
    autocomplete_fields = ("user", "category")

# Register your models here.
