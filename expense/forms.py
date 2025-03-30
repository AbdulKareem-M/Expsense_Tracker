from django import forms
from .models import Category, Expense


class ExpenseForm(forms.ModelForm):
  class Meta:
    model = Expense
    fields = ['amount', 'date','description','category']
    widgets = {
      'date':forms.DateInput(attrs={'type':'date'})
    }