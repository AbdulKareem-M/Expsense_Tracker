from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('register/',views.Registerview.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
]