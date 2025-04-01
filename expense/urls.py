from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/dashboard/', views.dashboard, name='dashboard'),
    path('expenses/delete/<int:pk>', views.DeleteExpense.as_view(), name='delete_expense'),
    
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
]