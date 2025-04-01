from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
  name = models.CharField(max_length=100)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'Categories'
    


class Expense(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateField()
  description = models.CharField(max_length=255)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return f'{self.description} - ${self.amount}'
  

class Budget(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  month = models.DateField()  # We'll just use the first day of each month
    
  def __str__(self):
      return f"{self.category.name} - {self.month.strftime('%B %Y')}"
    
  class Meta:
      unique_together = ['user', 'category', 'month']