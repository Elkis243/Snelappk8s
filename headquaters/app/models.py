from django.db import models
from app_auth.models import User

class Center(models.Model):
    name_center = models.CharField(max_length=100)
    address_center = models.CharField(max_length=200)
    
    def __str__(self) :
        return self.name_center

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    registration_number = models.CharField(max_length=20, unique=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class Subscriber(models.Model):
    code_subscriber = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    type_subscriber = models.CharField(max_length=50)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    invoice_code = models.CharField(max_length=20, unique=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    month = models.CharField(max_length=50) 
    index_invoice = models.CharField(max_length=50)
    consommation = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Impayée') 
    date_invoice = models.DateField(auto_now_add=True, auto_created=True)
    def __str__(self):
        return self.invoice_code