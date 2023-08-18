from django.db import models
from django.contrib.auth.models import AbstractUser
from bbquiz.models import question
from .manager import UserManager
class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    auth_token=models.CharField(max_length=100)
    user_profile_image=models.ImageField(upload_to="profile",default="defaultprofile.jpg")
    is_email_verified=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_employee=models.BooleanField(default=False)
    test_attempted=models.IntegerField(default=0)
    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
  

    def __str__(self):
        return self.email

class profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    bio=models.TextField(default='write your bio here')
    address=models.TextField(default=False,blank=True)
    pincode=models.IntegerField(default=False,blank=True)
    phone_number=models.CharField(max_length=15 , default=False,blank=True)
    education=models.CharField(max_length=100 ,default='education')
    ins_name=models.CharField(max_length=100 ,default='institute')
    ecountry=models.CharField(max_length=100, default='country')
    city=models.CharField(max_length=25 ,default='city')
    country=models.CharField(max_length=25 ,default='country')


class points(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE )
    resultid=models.IntegerField(primary_key=True,auto_created=True) 
    type=models.CharField(max_length=30)
    right=models.IntegerField()
    wrong=models.IntegerField()
    n_a=models.IntegerField()
    point=models.FloatField()
    total_que=models.IntegerField(default=False,blank=True)
    coins=models.IntegerField(default=0)
    date=models.DateField(auto_now=True)
    quiztime=models.IntegerField()
    time=models.TimeField(auto_now=True)

class ranking(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    total_rights= models.IntegerField(default=0)
    gift_coins=models.IntegerField(default=0)
    rank=models.IntegerField(default=0)

class order(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gift_id=models.BigAutoField(primary_key=True)
    cprice=models.IntegerField(default=0)
    

class otp_grabber(models.Model):
    phone_number=models.CharField(max_length=15 , primary_key=True)
    otp=models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"{self.phone_number} {self.otp}"

class query(models.Model):
    cid=models.IntegerField(primary_key=True,auto_created=True) 
    cemail=models.CharField(default=False,blank=True ,max_length=100)
    cfname=models.CharField(default=False,blank=True ,max_length=100) 
    clname=models.CharField(default=False,blank=True, max_length=100)
    problem=models.CharField(default=False,blank=True,max_length=100)
    replied_by=models.EmailField(default='-1',blank=True ,max_length=100)
    ctime=models.DateTimeField()
