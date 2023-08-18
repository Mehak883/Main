from django.shortcuts import render,redirect
from django.shortcuts import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as lgn,logout as lmn
from django.contrib.auth.decorators import login_required
from django.views import View
from social_django.models import UserSocialAuth
from bbhome.models import profile as prof
import uuid
import sys
from bbhome.models import points,CustomUser,ranking as rankg,otp_grabber
from bbhome.models import order
from bbquiz.models import question,gift as gifts
from bbhome.models import query
from django.contrib import messages
from django.db.models import *
from django.conf import settings
import http.client
import random
import math
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from bbquiz.helper import send_otp_to_phone

User=get_user_model()
def login(request):
    return render(request,'login.html') 

def logout(request):
        lmn(request)
        return redirect('/login')
@login_required 
def home(request):
    myprofile=User.objects.filter(email=request.user.email).first()
    return render(request,'home.html',{'myprofile':myprofile})

def signup(request):
    if request.method=='POST':
        print('hloo')
        
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        check_user=User.objects.filter(email=email,is_student=True,is_email_verified=True).first()
        try:
            if check_user:
                print('HEllo')
                response_data = {'message': 'Email is already registered.'}
                # messages.success(request,'Email already registered')
                return JsonResponse(response_data)
                # return redirect('/login?next=/home') 
                # return render(request,'login.html',{'response_data':response_data})
            else:
                user_next=User.objects.filter(email=email,is_student=True,is_email_verified=False).first()
                print('hii')
                auth_token=str(uuid.uuid4())
                if user_next:
                    print('hlo')
                    user_next.first_name=firstname
                    user_next.last_name=lastname
                    user_next.auth_token=auth_token
                    user_next.is_student=True
                    user_next.set_password(password)
                    user_next.save()
                else:
                    user=User(email=email,first_name=firstname,last_name=lastname,auth_token=auth_token,is_student=True)
                    user.set_password(password)
                    user.save()
                myprof=User.objects.filter(email=email).first()
                send_mail_aftr_regis(firstname,email,auth_token,'student')
                return JsonResponse({'success':'Mail has been send to you,Kindly check your Mailbox'})
#                 # return redirect('/login?next=/home')
        except Exception as e:
            print(e)         
#     else:

#      return render(request,'home.html')

def send_mail_aftr_regis(name,email,token,profession):
    subject="Your account need to be verified"
    message=f'welcome {name}\nkindly click on the link to verify your email http://127.0.0.1:8000/verify/{token}/{profession} and then login with your credentials'
    email_from =settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,email_from,recipient_list)
 

def verify(request,token,profession):
    print(profession)
    try:
        if profession=='student':
            a=User.objects.filter(auth_token=token).first()
            print(a)
            a.is_email_verified=True
            a.save()
            return redirect('/login')
        if profession=='employee':
            a=User.objects.filter(auth_token=token).first()
            a.is_email_verified=True
            a.save()
            return redirect('/login_que')
    except Exception as e:
        print(e)
def login_check(request):
    print("login")
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print('hlo',email,'dfg')
        print(password) 
        user=User.objects.filter(email=email,is_student=True).first()
        print("user firdt login")
        print(user)
        if user is not None:
            print("User login")
            check_user=authenticate(email=email,password=password)
            if(check_user):
                print('login done')
                lgn(request,check_user)
                if user.is_email_verified :
                    print("login verified")
                    success='Account Verified'
                  
                    return JsonResponse({'success':success})
                else:
                    print("not login")
                    return JsonResponse({'error':'User does not exist'})
            else:
                print('password')
                return JsonResponse({'error':'password incorrect'})
        else:
            return JsonResponse({'error':'User does not exist'})
        

class ContinueWithGoogleView(View):
    def get(self, request):
      
        try:

            mail=UserSocialAuth.objects.latest('uid').uid
            user=User.objects.filter(email=mail).first()
            auth_token=str(uuid.uuid4())
            print(request.user)
            print('Hello')
            user.auth_token=auth_token
            user.is_email_verified=True
            user.is_student=True
            user.save()
#             new_profile=profile.objects.create(user=user,auth_token=auth_token) 
#             new_profile.is_email_verified=True
#             new_profile.save()
        except Exception as e:
            print(e)
        return redirect('/home')



@login_required
def profile(request):
    myprofile=User.objects.filter(email=request.user.email).first()
    mycred=prof.objects.filter(user=myprofile).first()
    myrank=rankg.objects.filter(user=myprofile).first()
    mypoint=points.objects.filter(user=myprofile).order_by('-resultid')
    return render(request,'profile.html',{'myprofile':myprofile,'mycred':mycred,'myrank':myrank,'mypoint':mypoint})



@login_required
def bioset(request):
    if(request.method=='POST'):
        bio=request.POST.get('bio')
        myprofile=User.objects.filter(email=request.user.email).first()
        mycred=prof.objects.filter(user=myprofile).first()
        if mycred is not None:
            mycred.bio=bio
            mycred.save()        
        else:
            my=prof()
            my.user=myprofile
            my.bio=bio
            my.save()
    
    return JsonResponse({'bio':bio})
@login_required
def upload(request):
    print('jlo')
    if request.method == 'POST':
        profile_image=request.FILES.get('profile_image')
        if profile_image:
            myprofile=User.objects.filter(email=request.user.email).first()
            myprofile.user_profile_image=profile_image
            myprofile.save()
    return redirect('/profile')
@login_required

def intro(request):
    print('hoo')
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        country=request.POST.get('country')
        city=request.POST.get('city')
        myprofile=User.objects.filter(email=request.user.email).first()
        mycred=prof.objects.filter(user=myprofile).first()
        myprofile.first_name=fname
        myprofile.last_name=lname

        fname1=str(fname).title()
        lname1=str(lname).title()
        city1=str(city).title()
        country1=str(country).title()

        if mycred is not None:
            mycred.city=city
            mycred.country=country
            mycred.save()
        else:
            my=prof()
            my.user=myprofile
            my.city=city
            my.country=country
            my.save()
        myprofile.save()    
    return JsonResponse({'fname':fname1,'lname':lname1,'country':country1,'city':city1})
@login_required

def edu(request):
    print('hoo')
    if request.method == 'POST':
        education=request.POST.get('education')
        ins_name=request.POST.get('ins_name')
        ecountry=request.POST.get('ecountry')
        myprofile=User.objects.filter(email=request.user.email).first()
        mycred=prof.objects.filter(user=myprofile).first()
        education1=str(education).upper()
        ins_name1=str(ins_name).title()
        ecountry1=str(ecountry).title()

        if mycred is not None:
            mycred.education=education
            mycred.ins_name=ins_name
            mycred.ecountry=ecountry
            mycred.save()
        else:
            my=prof()
            my.user=myprofile
            my.education=education
            my.ins_name=ins_name
            my.ecountry=ecountry
            my.save()
    return JsonResponse({'education': education1, 'ins_name': ins_name1, 'ecountry': ecountry1})

@login_required
def quiz_html(request):
    ques1=list(question.objects.filter(type='Html'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def bbresult(request,id,length):
    myprofile=User.objects.filter(email=request.user.email).first()
     
    percentid=points.objects.filter(resultid=id).first()

    print(percentid.resultid)
    percent=list(points.objects.filter(type=percentid.type).order_by('-coins','quiztime'))
    print('coins : ',percent[0].coins)
    lp=len(percent)
    q=1
    lp_id=int()
    for i in percent:
        if(percentid.resultid==i.resultid):
            lp_id=q
            break
        q+=1
    print(lp,"    ",lp_id)
    per=(lp_id*100)/lp
    print('percent :',100-per)
        
    print('my name : ',myprofile.email)
    min = int(percentid.quiztime) // (60 * 1000)
    sec = (int(percentid.quiztime) % (60 * 1000)) / 1000;    
    print(min,int(sec))
    min1=10-int(min)
    sec1=60-int(sec)
    grade=math.trunc(100-per)
    g=str()
    if grade>=95:
        g='Outstanding'
    if grade<95 and grade>=85:
        g='Excellent'
    if grade<85 and grade>=75:
        g='Great'
    if grade<75 and grade>=65:
        g='Good'
    if grade<65 and grade>=55:
        g='Average'
    if grade<55:
        g='Need Improvement'
    return render(request,'result.html',{'name':myprofile.first_name,'type':percentid.type,'count':percentid.right,'n_a':percentid.n_a,'wrong':percentid.wrong,'coins':percentid.coins,'point':percentid.point,'min':min1,'sec':sec1,'percent':math.trunc(100-per),'length':length,'id':percentid.resultid,'rank':lp_id,'grade':g})
@login_required

def result(request):
    print(request.user.email)
    if request.method=='POST':
        quizque=list()
        length=int(request.POST.get('length'))
        print(length,'wefr')
        for i in range(1,length+1):
            que=request.POST.get(f'q{i}')
            ans=request.POST.get(f'ans{i}')
            quizque.append([que,ans])
        time=request.POST.get('time')
        print(time)
        min = int(time) // (60 * 1000)
        sec = (int(time) % (60 * 1000)) / 1000;    
        print(min,int(sec))
        min1=10-int(min)
        sec1=60-int(sec)
        myprofile=User.objects.filter(email=request.user.email).first()
        count=0
        cna=0
        for i in quizque:
            que=question.objects.filter(question_id=int(i[0])).first()
            type1=que.type
            if(i[1] is not None ):
                if(que.ans==i[1]):
                    count+=1
            else:
                cna+=1
        print(count)
        print('cna :', cna)
        wrg=length-(count+cna)
        pt=(count*100)/length
        pt=round(pt,2)
        if(count==length):
            coins=5
        elif(count ==(length-1)):
            coins=4
        elif(count ==(length-2)):
            coins=3 
        elif(count==(length-3)):
            coins=2
        elif(count==(length-4)):
            coins=1
        else:
            coins=0
        
        # rank=myrank(pt,myprofile)
        mypoint=points(user=myprofile,type=type1,right=count,n_a=cna,coins=coins,total_que=length,wrong=wrg,point=pt,quiztime=time)
        mypoint.save()
        find_rank(myprofile)
        my=points.objects.filter(user=myprofile).last()
        return redirect(reverse('bbresult',kwargs={'id':my.resultid,'length':my.total_que}))

       
        
# def total_points(myprofile):
#     for
#     for points1 in points.objects.all().order_by('point') :
#         if myprofile==points1.user:
#             return rank
#         else:
#            rank+=1
def find_rank(myprofile):
    try:
        user1 = User.objects.get(email=myprofile.email)
        
        points1 = points.objects.filter(user=user1)
        if points1 is None:
            pt=points()
            pt.user=user1
            pt.save()
        else:    
            users_total= CustomUser.objects.annotate(total_right=Sum('points__coins'))
            gift_order= CustomUser.objects.annotate(gift_coins=Sum('order__cprice'))
        dict_total={}
        cg={}
        cg1={}
        for user in users_total:
            print(f"User: {user.email}, Total Right: {user.total_right}")
            if user.total_right is None:
                dict_total[user]=0
            if user.total_right is not None:
                  dict_total[user]=user.total_right
        for e in gift_order:
            print(e.email,e.gift_coins)
            if e.gift_coins is None:
                cg[e]=0
            else:
                cg[e]=e.gift_coins
        for k,v in dict_total.items():
            for k1,v1 in cg.items():
                if(k==k1):
                    cg1[k]=(v-v1)
        print(cg)

        sorted_dict = dict(sorted(dict_total.items(), key=lambda x: x[1],reverse=True))
        rank=0
        for k,v in sorted_dict.items():
            if rankg.objects.filter(user=k).first():
                rank+=1
                r=rankg.objects.filter(user=k).first()
                r.total_rights=v
                r.rank=rank
                r.save() 
                print('if block')
            else:
                r=rankg()
                rank+=1
                r.user=k
                r.total_rights=v
                r.rank=rank
                r.save()
                print('else block')
        
        for k,v in cg1.items():
            if rankg.objects.filter(user=k).first():
                r=rankg.objects.filter(user=k).first()
                r.gift_coins=v
                r.save()
    except Exception as e:
        print(e) 

# def ranking(request):
 
       
#         total_rights = points1.aggregate(Sum('right'))['right__sum']
#         total_wrongs = points1.aggregate(Sum('wrong'))['wrong__sum']
#         total_n_a = points1.aggregate(Sum('n_a'))['n_a__sum']
        
#         total_percentage=(total_rights*100)/(total_n_a+total_rights+total_wrongs)
#         print('Total percentage are :',total_percentage)
   
#     return HttpResponse('rank finder')

def check(request):
    myprofile=User.objects.filter(email=request.user.email).first()

    if request.method == "POST":
        codereaddata=request.POST.get('codearea')
        try:
            original_stdout=sys.stdout
            sys.stdout=open('file.txt','w')
            exec(codereaddata) 
            sys.stdout.close()
            sys.stdout=original_stdout
            output=open('file.txt','r').read()
            return JsonResponse({'output':output})
        except Exception as e:
            sys.stdout=original_stdout
            output=str(e)
            print(e)
            print('hi every')
            return JsonResponse({'output_error':output})
        # return render(request,'check.html',{'output':output,'mehak':0})
        # return render(request,'check.html',{'code':codereaddata,'output':output})
    return render(request,'check.html',{'myprofile':myprofile})


@login_required
def quiz_python(request):
    ques1=list(question.objects.filter(type='Python'))
    random.shuffle(ques1)

    ques=list(ques1[0:15:1])
    print('questions :  ',ques)
    return render(request,'quiiz.html',{'ques':ques})


@login_required
def quiz_aptitude(request):
    ques1=list(question.objects.filter(type='Aptitude'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def quiz_java(request):
    ques1=list(question.objects.filter(type='Java'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def quiz_javascript(request):
    ques1=list(question.objects.filter(type='Javascript'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def quiz_cpp(request):
    ques1=list(question.objects.filter(type='C++'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def quiz_clang(request):
    ques1=list(question.objects.filter(type='C'))
    random.shuffle(ques1)
    ques=ques1[0:15:1]
    return render(request,'quiiz.html',{'ques':ques})
@login_required
def gift(request):
    g1=gifts.objects.all()
    if request.method=="POST":
        gifty=request.POST.dict()
        giftid=int(gifty['gift_id'])
        print(giftid, type(giftid))
        myprofile=User.objects.filter(email=request.user.email).first()
        find_rank(myprofile)
        myrankg=rankg.objects.filter(user=myprofile).first()
        mygift=gifts.objects.filter(gift_id=giftid).first()
        print(mygift)
        mycoins=myrankg.gift_coins
        myrank=myrankg.rank
        if mygift.rank_needed == 0:
            if(mycoins<mygift.points_needed):
                print('hlo')
                msg="you don't have sufficient coins"  
                return JsonResponse({'msg1':msg})
            else:
                return JsonResponse({'open':1,'gift_id':giftid})   
            
        elif mygift.points_needed==0:
            if(myrank>mygift.rank_needed):
                print('hi')
                msg="Sorry, your rank is less than required rank" 
                return JsonResponse({'msg1':msg})
            else:
                return JsonResponse({'open':1,'gift_id':giftid})   
        else:
            if(mycoins<mygift.points_needed and myrank>mygift.rank_needed):
                print('klp')
                msg='you are not eligible to get this'
                return JsonResponse({'msg1':msg})
            elif(mycoins<mygift.points_needed):
                msg="you don't have sufficient coins"  
                return JsonResponse({'msg1':msg})
            elif(myrank>mygift.rank_needed):
                msg="Sorry, your rank is less than required rank" 
                return JsonResponse({'msg1':msg})
            else:
                return JsonResponse({'open':1,'gift_id':giftid})   
    myprofile=User.objects.filter(email=request.user.email).first()
    
    return render(request,'gift.html',{'gift':g1,'myprofile':myprofile})


def send_otp(request):
    if request.method=='POST':
        phone=request.POST.get('phone')
        if phone is None:
            return JsonResponse({'phone_v':'Phone number is Required'})
        else:
            otp=send_otp_to_phone(phone)
            print(otp)
            temp=otp_grabber.objects.create(phone_number=phone,otp=otp)
            temp.save()
            msg=f'OTP is Sent to {phone}'
            return JsonResponse({'message':msg})
        




def send_mail_aftr_forget(name,email,token):
    subject="Your account need to be verified"
    message=f'welcome {name}\nkindly click on the link to change password http://127.0.0.1:8000/reset/{email}/{token} and then login with your new credentials'
    email_from =settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,email_from,recipient_list)



        
def forget_pass(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        print(name)
        print(email)
        myprof=User.objects.filter(email=email).first()
        if myprof is None:
            return JsonResponse({'forget1':"User does not exist"})
        else:
            token=str(uuid.uuid4())
            send_mail_aftr_forget(name,email,token)
            return JsonResponse({'forget2':"Mail has been send to you kindly check your mailbox"})

    return render(request,'forget_pass.html')


def reset(request,email,token):
    if request.method=='POST':
        password=request.POST.get('password')
        apassword=request.POST.get('apassword')
        if password==apassword:
            
            myprof=User.objects.filter(email=email).first()
            myprof.set_password(password)
            myprof.save()
            if myprof.is_student==True:
                return JsonResponse({'reset1':'Kindly login with new credentials'})
            if myprof.is_employee==True:
                return JsonResponse({'reset3':'Kindly login with new credentials'})

        else:
            return JsonResponse({'reset2':'paswords are mismatched'})
    return render(request,'reset.html',{'email':email,'token':token})
def verify_otp(request):
    if request.method=='POST':
        phone1=request.POST.get('phone1')
        otp1=request.POST.get('otp1')
        myotp=otp_grabber.objects.filter(phone_number=phone1).first()
        if(otp1==myotp.otp):
            myotp.delete()
            myprofile=User.objects.filter(email=request.user.email).first()
            iam=prof.objects.filter(user=myprofile).first()
            iam.phone_number=phone1
            iam.save()
            return JsonResponse({'phn_open':1})
        # if otp_grabber.objects.filter(phone_number=phone1):
        else:
            myotp.delete()
            return JsonResponse({'otp_not':'Invalid Credentials'})

def add_address(request):
    if request.method=='POST':
        gift_id=int(request.POST.get('gift_id'))
        print(gift_id)
        g1=gifts.objects.filter(gift_id=gift_id).first()
        pincode=request.POST.get('pincode')
        addr=request.POST.get('addr')
        myprofile=User.objects.filter(email=request.user.email).first()
        order1=order(user=myprofile,gift_id=gift_id,cprice=g1.points_needed)
        order1.save()
        iam=prof.objects.filter(user=myprofile).first()
        iam.pincode=pincode
        iam.address=addr
        iam.save()
        return JsonResponse({'address1':'Your Order is placed'})


@login_required
def rank(request):
    myprof=User.objects.filter(email=request.user.email).first()
    l=[]
    myrank=rankg.objects.all().order_by('rank')
    for i in myrank:
        if i.user.is_email_verified is not None and i.user.is_student !=False:
         
            l.append(i)
    print(l)
    return render(request,'rank.html',{'myprofile':myprof,'myrank':l})


@login_required
def about(request):
    myprof=User.objects.filter(email=request.user.email).first()

    return render(request,'about.html',{'myprofile':myprof})
from datetime import datetime

def contact(request):
    myprof=User.objects.filter(email=request.user.email).first()
    if request.method=='POST':
        cemail=request.POST.get('cemail')
        cfname=request.POST.get('cfname')
        clname=request.POST.get('clname')
        problem=request.POST.get('problem')
        q1=query(cemail=cemail,cfname=cfname,clname=clname,problem=problem,ctime=datetime.now())
        q1.save()
        return JsonResponse({'contactmsg':'your query is recieved, you will get mail soon'})
    return render(request,'contact.html',{'myprofile':myprof})