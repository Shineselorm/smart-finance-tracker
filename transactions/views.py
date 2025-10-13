from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm


def home(request):
    if request.user.is_authenticated:
        # Authenticated users see dashboard with real data
        import json
        from datetime import datetime, timedelta
        
        # Calculate summary stats
        transactions = Transaction.objects.filter(user=request.user)
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense
        
        # Get current month data for charts
        now = datetime.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Monthly income vs expenses (last 4 weeks)
        weekly_data = []
        for i in range(4):
            week_start = current_month_start - timedelta(weeks=3-i)
            week_end = week_start + timedelta(days=7)
            
            week_income = transactions.filter(
                type='income',
                date__gte=week_start,
                date__lt=week_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            week_expense = transactions.filter(
                type='expense',
                date__gte=week_start,
                date__lt=week_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            weekly_data.append({
                'week': f'Week {i+1}',
                'income': float(week_income),
                'expense': float(week_expense)
            })
        
        # Category breakdown
        categories = Category.objects.filter(type='expense')
        category_data = []
        for category in categories:
            amount = transactions.filter(
                type='expense',
                category=category
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            if amount > 0:
                category_data.append({
                    'name': category.name,
                    'amount': float(amount)
                })
        
        # Recent transactions
        recent_transactions = transactions.order_by('-date', '-created_at')[:5]
        
        context = {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'weekly_data': json.dumps(weekly_data),
            'category_data': json.dumps(category_data),
            'recent_transactions': recent_transactions,
        }
        
        return render(request, 'index.html', context)
    else:
        # Non-authenticated users see landing page
        return render(request, 'landing.html')


@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
    
    # Filtering
    category_filter = request.GET.get('category')
    type_filter = request.GET.get('type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if category_filter:
        transactions = transactions.filter(category_id=category_filter)
    if type_filter:
        transactions = transactions.filter(type=type_filter)
    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    
    # Summary calculations
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    
    categories = Category.objects.all()
    
    context = {
        'transactions': transactions,
        'categories': categories,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_filter': category_filter,
        'type_filter': type_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'transactions/transactions_list.html', context)


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transactions_list')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'transactions/transaction_form.html', {'form': form, 'action': 'Add'})


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transactions_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    return render(request, 'transactions/transaction_form.html', {'form': form, 'action': 'Update'})


@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transactions_list')
    
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})


@login_required
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'transactions/categories_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm()
    
    return render(request, 'transactions/category_form.html', {'form': form, 'action': 'Add'})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'transactions/category_form.html', {'form': form, 'action': 'Update'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('categories_list')
    
    return render(request, 'transactions/category_confirm_delete.html', {'category': category})


@login_required
def budgets_list(request):
    budgets = Budget.objects.filter(user=request.user).select_related('category')
    
    # Calculate spending for each budget
    budget_data = []
    for budget in budgets:
        # Calculate date range based on period
        if budget.period == 'weekly':
            start_date = datetime.now() - timedelta(days=7)
        else:  # monthly
            start_date = datetime.now().replace(day=1)
        
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            type='expense',
            date__gte=start_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        percentage = (spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0
        remaining = budget.limit_amount - spent
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'percentage': min(percentage, 100),
            'remaining': remaining,
            'over_budget': spent > budget.limit_amount
        })
    
    context = {'budget_data': budget_data}
    return render(request, 'transactions/budgets_list.html', context)


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budgets_list')
    else:
        form = BudgetForm(user=request.user)
    
    return render(request, 'transactions/budget_form.html', {'form': form, 'action': 'Add'})


@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budgets_list')
    else:
        form = BudgetForm(instance=budget, user=request.user)
    
    return render(request, 'transactions/budget_form.html', {'form': form, 'action': 'Update'})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budgets_list')
    
    return render(request, 'transactions/budget_confirm_delete.html', {'budget': budget})


def placeholder(request, page):
    context = {"page": page}
    return render(request, 'placeholder.html', context)
