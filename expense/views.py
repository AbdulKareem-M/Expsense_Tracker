from django.shortcuts import render, redirect
from .models import Expense, Category
from . forms import ExpenseForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
      expense = form.save(commit = False)
      expense.user = request.user
      expense.save()
      messages.success(request, 'Expense added Successfully!')
      return redirect('expense_list')
    else:
      form = ExpenseForm()
  return render(request, 'expenses/add_expense.html',{'form':form})