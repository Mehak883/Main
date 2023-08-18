from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# import bbhome
class Employee(models.Model):
    email=models.EmailField(primary_key=True)
    first_name=models.CharField(max_length=50,null=False)
    last_name=models.CharField(max_length=50)
    auth_token=models.CharField(max_length=100,null=False)
    user_profile_image=models.ImageField()
    is_email_verified=models.BooleanField(default=False)
    emp_id=models.CharField(max_length=8, null=False)

 

# User=get_user_model()
# class dataemp(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     e_id=models.BigAutoField(primary_key=True,auto_created=True)
#     emp_id=models.CharField(max_length=8, null=False)
    
# class dataemp(AbstractUser):
#     first_name=models.CharField(max_length=15, null=False)
#     lastname=models.CharField(max_length=25)
#     created_at=models.DateTimeField(auto_now_add=True)
#     email=models.EmailField(unique=True, null=False)
#     phone_number=models.CharField(max_length=10,unique=True)
#     emp_bio=models.CharField(max_length=100)
#     user_profile_img=models.ImageField(upload_to="profile")
#     USERNAME_FIELD=['email']
#     REQUIRED_FIELDS=['firstname','email']
# Create your models here.
class question(models.Model):
    question_id=models.BigAutoField(primary_key=True,auto_created=True)
    que=models.TextField(null=False) #long data
    code=models.TextField(default=False,blank=True)
    type=models.CharField(max_length=255,null=False)
    a=models.CharField(max_length=255)
    b=models.CharField(max_length=255)
    c=models.CharField(max_length=255)
    d=models.CharField(max_length=255)
    ans=models.CharField(max_length=2,null=False)
    
class gift(models.Model):
    gift_id=models.BigAutoField(primary_key=True,auto_created=True)
    gift_pic=models.ImageField(upload_to="gifts",default="giftimg.jpg")
    gname=models.CharField(max_length=255)
    price=models.FloatField()
    points_needed=models.FloatField()
    rank_needed=models.IntegerField()
    gdate=models.DateTimeField(auto_now=True)
