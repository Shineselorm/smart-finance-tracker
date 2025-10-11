from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Transactions
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Categories
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Budgets
    path('budgets/', views.budgets_list, name='budgets_list'),
    path('budgets/add/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    
    # Placeholder
    path('<str:page>/', views.placeholder, name='placeholder'),
]
