from django.shortcuts import render, redirect
from .models import Expense, Category, Budget
from . forms import ExpenseForm, UserForm, LoginForm, BudgetForm
from django.contrib import messages
from django.views.generic import View, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from datetime import datetime
from django.urls import reverse_lazy

@login_required
def profile(request):
    return render(request, 'users/profile.html')
class Registerview(View):
  
  def get(self, request):
    
    form = UserForm()
    
    return render(request, 'users/register.html', {'form':form})
  
  def post(self, request):
    
    form = UserForm(request.POST)
    
    if form.is_valid():
      
      User.objects.create_user(**form.cleaned_data)
      
      return redirect('login')
    
  


class LoginView(View):
  
  def get(self, request):
    
    form = LoginForm()
    
    return render(request, 'users/login.html', {'form':form})
  
  def post(self, request):
    
    form = LoginForm(request.POST)
    
    if form.is_valid():
            
      username = form.cleaned_data.get('username')
      
      password  = form.cleaned_data.get('password')
      
      user = authenticate(request, username = username, password = password)
      
      if user:
        
        login(request, user)
        
        return redirect('expense_list')
      
      else:
        
        return render(request, 'users/login.html', {'form':form})

def logout(request):
  logout(request)
  return redirect('logout')

@login_required
def expense_list(request):
  expenses = Expense.objects.filter(user=request.user).order_by('-date')
  categories = Category.objects.all()
  
  return render(request, 'expenses/expense_list.html',{'expenses':expenses, 'category':categories})


@login_required
def add_expense(request):
  if request.method == 'POST':
    form = ExpenseForm(request.POST)
    if form.is_valid():
      expense = form.save(commit=False)
      expense.user = request.user
      expense.save()

      # Debit the budget for the same category
      category = expense.category
      budget = Budget.objects.filter(user=request.user, category=category).first()

      if budget:
        # Debit the budget
        if budget.amount >= expense.amount:
          budget.amount -= expense.amount
          budget.save()
          messages.success(request, 'Expense added and budget debited successfully!')
        else:
          messages.error(request, 'Not enough budget for this expense.')
      else:
        messages.warning(request, 'No budget found for this category.')

        return redirect('expense_list')
  else:
    form = ExpenseForm()
  return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def dashboard(request):
  # Get all expenses for the current user
  expenses = Expense.objects.filter(user=request.user)
    
  # Total expenses
  total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
  # Expenses by category
  expenses_by_category = list(expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total'))
    
  # Expenses by month
  current_year = datetime.now().year
  expenses_by_month = list(expenses.filter(date__year=current_year)
                          .annotate(month=TruncMonth('date'))
                          .values('month')
                          .annotate(total=Sum('amount'))
                          .order_by('month'))
    
  # Convert QuerySet to format suitable for Chart.js
  categories = [item['category__name'] for item in expenses_by_category]
  category_totals = [float(item['total']) for item in expenses_by_category]
    
  months = [item['month'].strftime('%B') for item in expenses_by_month]
  monthly_totals = [float(item['total']) for item in expenses_by_month]
    
  context = {
      'total_expenses': total_expenses,
      'categories_json': json.dumps(categories),
      'category_totals_json': json.dumps(category_totals),
      'months_json': json.dumps(months),
      'monthly_totals_json': json.dumps(monthly_totals),
  }
  
  return render(request, 'expenses/dashboard.html', context)

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-month')
    return render(request, 'expenses/budget_list.html', {'budgets': budgets})

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.month = budget.month.replace(day=1)  # Ensure first day of the month
            
            # Check if budget already exists
            existing_budget = Budget.objects.filter(
                user=request.user,
                category=budget.category,
                month=budget.month
            ).first()

            if existing_budget:
                existing_budget.amount = budget.amount
                existing_budget.save()
                messages.success(request, 'Budget updated successfully!')
            else:
                budget.save()
                messages.success(request, 'Budget added successfully!')

            return redirect('budget_list')
        else:
            print(form.errors)  # Debugging step
            messages.error(request, "There was an error in your form.")
    else:
        form = BudgetForm()

    return render(request, 'expenses/add_budget.html', {'form': form})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-month')
    
    for budget in budgets:
        # Calculate spent for the given category and month
        total_spent = Expense.objects.filter(user=request.user, category=budget.category, date__month=budget.month.month, date__year=budget.month.year).aggregate(Sum('amount'))['amount__sum'] or 0
        budget.spent = total_spent
        budget.remaining = budget.amount - total_spent
        # Calculate the progress as percentage
        if budget.amount > 0:
            budget.progress = (total_spent / budget.amount) * 100
        else:
            budget.progress = 0

    return render(request, 'expenses/budget_list.html', {'budgets': budgets})


class DeleteExpense(DeleteView):
  model = Expense
  template_name = 'expenses/delete_expense.html'
  success_url = reverse_lazy('expense_list')