from django.urls import path
from . import views

urlpatterns = [
    #user
    path('register/',views.Registerview.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    
    #expenses
    path('', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/dashboard/', views.dashboard, name='dashboard'),
    path('expenses/delete/<int:pk>', views.DeleteExpense.as_view(), name='delete_expense'),
    path('expenses/update/<int:pk>', views.UpdateExpense.as_view(), name='update_expense'),
    
    #budgets
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/delete/<int:pk>', views.DeleteBudget.as_view(), name='delete_budget'),
    path('budgets/update/<int:pk>', views.UpdateBudget.as_view(), name='update_budget'),
]