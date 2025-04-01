from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/dashboard/', views.dashboard, name='dashboard'),
    path('expenses/delete/<int:pk>', views.DeleteExpense.as_view(), name='delete_expense'),
    path('expenses/update/<int:pk>', views.UpdateExpense.as_view(), name='update_expense'),
    
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/delete/<int:pk>', views.DeleteBudget.as_view(), name='delete_budget'),
    path('budgets/update/<int:pk>', views.UpdateBudget.as_view(), name='update_budget'),
]