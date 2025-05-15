from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    account_number = models.CharField(max_length=20, unique=True)
    customer_since = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_number}"
