from django.db import models

class SignUp(models.Model):
    userName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.TextField()
    otp = models.CharField(max_length=6 , blank=True , null=True)
    is_verified = models.BooleanField(default=False)
    

class StudentDetails(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    age = models.IntegerField()
    

    