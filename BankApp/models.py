from django.db import models

# Create your models here.
class newReg(models.Model):
    account_number=models.BigIntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=10)
    amount=models.FloatField()
    mobile_no=models.BigIntegerField()
    address=models.CharField(max_length=50)
    active=models.BooleanField(default=True)

#Empoyee Registration
class empReg(models.Model):
    empid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    mobile=models.BigIntegerField()
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=10)

