from django.shortcuts import render, redirect
from .models import Expense, Category
from . forms import ExpenseForm, UserForm, LoginForm
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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