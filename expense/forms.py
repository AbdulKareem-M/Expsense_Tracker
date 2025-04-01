from django import forms
from .models import Category, Expense


class ExpenseForm(forms.ModelForm):
  class Meta:
    model = Expense
    fields = ['amount', 'date','description','category']
    widgets = {
      'date':forms.DateInput(attrs={'type':'date'})
    }
    
    
class UserForm(forms.Form):
  
  username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter username'}))
  
  first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter first name'}))
  
  last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter last name'}))
  
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'enter password'}))
  
  email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter email'}))
  
    
class LoginForm(forms.Form):
  
  username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter username'}))
  
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'enter password'}))
  