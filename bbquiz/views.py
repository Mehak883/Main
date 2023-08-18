from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as lgn,logout as lmn
from django.contrib.auth.decorators import login_required
from .models import question,gift
from django.http import JsonResponse
import uuid
from bbhome.models import query
from bbhome.views import send_mail_aftr_regis,send_mail_aftr_forget
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()


def login(request):

    return render(request, 'login.html')


def signup_emp(request):
    return render(request, 'signup_emp.html')

def add_gifts(request):
    if request.method == "POST":
        gift_pic=request.FILES.get('gift_pic')
        gname = request.POST["gname"]
        price = request.POST["price"]
        points_needed = request.POST["points_needed"]
        rank_needed=request.POST['rank_needed']
        gifts = gift.objects.create(
            gift_pic=gift_pic, gname=gname, price=price, points_needed=points_needed, rank_needed=rank_needed)
        gifts.save()
        messages.success(request, 'data saved')
        if request.POST.get("save"):
            print("hlo")
            return redirect('/display_gifts')
        if request.POST.get('save_add'):
            return redirect("/add_gifts")
    return render(request, 'add_gifts.html')

def create_ques(request):
   if 'email' not in request.session.keys():
        return redirect('login_que')
   else:  
    if request.method == "POST":
        que = request.POST["que"]
        if request.POST["code"]:
            code=request.POST["code"]
        type = request.POST["type"]
        A = request.POST["A"]
        B = request.POST["B"]
        C = request.POST["C"]
        D = request.POST["D"]
        ans = request.POST["ans"]
        ques = question.objects.create(
            que=que,code=code, type=type, a=A, b=B, c=C, d=D, ans=ans)
        ques.save()
        messages.success(request, 'data saved')
        if request.POST.get("save"):
            print("hlo")
            return redirect('/display_bbques')
        if request.POST.get('save_add'):
            return redirect("/create_ques")
    return render(request, 'create_ques.html')


def display_bbques(request):
   if 'email' not in request.session.keys():
        return redirect('login_que')
   else:
    if request.method == 'POST':
        if (request.POST.get("type") is None or request.POST.get("type") == ""):
            if (request.POST.get('search_que') is not None):
                if (request.POST.get('search_que') != ''):

                    # ques=question.objects.all().order_by('question_id')
                    search_que = request.POST.get('search_que')
                    ques = question.objects.filter(que__contains=search_que)
                    messages.success(request, f'you search for {search_que}')
                    return JsonResponse(list(ques.values()), safe=False)
                else:
                    ques = question.objects.all().order_by('question_id')
                    messages.success(request, 'All Types')
                    return JsonResponse(list(ques.values()), safe=False)

        elif (request.POST.get("type")):
                if (request.POST.get('search_que') != ""):
                    search_que = request.POST.get('search_que')
                    type = request.POST.get('type')
                    ques = question.objects.filter(que__contains=search_que, type=type)
                    messages.success(
                        request, f'you searched for {search_que} ')
                    return JsonResponse(list(ques.values()), safe=False)
                else:
                    type = request.POST.get('type')
                    ques = question.objects.filter(type=type)
                    messages.success(request, f'{type} quesions')
                return JsonResponse(list(ques.values()), safe=False)
    else:
        ques = question.objects.all()
        return render(request,'display_bbques.html',{'ques':ques})

def logout_que(request):
        lmn(request)
    
        return redirect('/login_que')


def edit_bbques(request, question_id):
    editques = question.objects.filter(question_id=question_id).values()
    select_option = editques[0]['type']
    select_option2 = editques[0]['ans']
    if request.method == 'POST':
        q = question()
        q.question_id = editques[0]['question_id']
        q.que = request.POST['que']
        q.code=request.POST['code']
        q.type = request.POST['type']
        q.a = request.POST['A']
        q.b = request.POST['B']
        q.c = request.POST['C']
        q.d = request.POST['D']
        q.ans = request.POST['ans']
        q.save()
        messages.success(
            request, f'question with id : {question_id} is updated')
        return redirect('/display_bbques')
    return render(request, 'edit_bbques.html', {'editques': editques, 'select_option': select_option, 'select_option2': select_option2})


def delete_bbques(request, question_id):
    try:
        print('hlo')
        ques = question.objects.get(question_id=question_id)
        ques.delete()
        messages.success(request, 'question deleted')
        return redirect("/display_bbques")
    except Exception as e:
        print(e)
    return render(request, 'display_bbques.html')


def main_que(request):
    if 'email' not in request.session.keys():
        return redirect('login_que')
    else:
        return render(request, 'home_que.html')

def login_que(request):
    return render(request,'login_que.html')

def login_que1(request):
    print('login')    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print('hlo',email,'dfg')
        print(password) 
        user=User.objects.filter(email=email,is_employee=True).first()
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
                    request.session['email']=email
                    
                    return JsonResponse({'success':success})
                else:
                    print("not login")
                    return JsonResponse({'error':'User does not exist'})
            else:
                print('password')
                return JsonResponse({'error':'password incorrect'})
        else:
            return JsonResponse({'error':'User does not exist'})
    

def signup_que(request):
    if request.method=='POST':
        print('hloo')
        
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        check_user=User.objects.filter(email=email,is_employee=True,is_email_verified=True).first()
        try:
            if check_user is not None:
                print('HEllo')
                response_data = {'message': 'Email is already registered.'}
                # messages.success(request,'Email already registered')
                return JsonResponse(response_data)
                # return redirect('/login?next=/home') 
                # return render(request,'login.html',{'response_data':response_data})
            else:
                user_next=User.objects.filter(email=email,is_employee=True,is_email_verified=False).first()
                print('hii')
                auth_token=str(uuid.uuid4())
                if user_next:
                    print('hlo')
                    user_next.first_name=firstname
                    user_next.last_name=lastname
                    user_next.auth_token=auth_token
                    user_next.is_employee=True
                    user_next.set_password(password)
                    user_next.save()
                else:
                    print('hii')
                    user=User(email=email,first_name=firstname,last_name=lastname,auth_token=auth_token,is_employee=True)
                    user.set_password(password)
                    user.save()
                myprof=User.objects.filter(email=email).first()
                send_mail_aftr_regis(firstname,email,auth_token,'employee')
                return JsonResponse({'success':'Mail has been send to you,Kindly check your Mailbox'})
#                 # return redirect('/login?next=/home')
        except Exception as e:
            print(e)   

def forget_pass_que(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        print(name)
        print(email)
        myprof=User.objects.filter(email=email).first()
        if myprof is None:
            return JsonResponse({'forget1':"Employee does not exist"})
        else:
            token=str(uuid.uuid4())
            send_mail_aftr_forget(name,email,token)
            return JsonResponse({'forget2':"Mail has been send to you kindly check your mailbox"})

    return render(request,'D:/brainblaze/bbhome/templates/forget_pass.html')


def reset_que(request,email,token):
    if request.method=='POST':
        password=request.POST.get('password')
        apassword=request.POST.get('apassword')
        if password==apassword:
            myprof=User.objects.filter(email=email).first()
            myprof.set_password(password)
            myprof.save()
            return JsonResponse({'reset3':'Kindly login with new credentials'})
        else:
            return JsonResponse({'reset2':'paswords are mismatched'})
    return render(request,'',{'email':email,'token':token})


def send_mail_reply(name,email,problem):
    subject="Reply to your query"
    message=f'Hi {name}\n'+problem
    email_from =settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,email_from,recipient_list)


def queries(request):
    qry=query.objects.all().order_by('-cid')
    if request.method=='POST':
        cid=request.POST.get('cid')
        problem=request.POST.get('problem')
        print(cid,problem)
        myqry=query.objects.filter(cid=cid).first()
        myqry.replied_by=request.user.email
        myqry.save()
        print('hlo')
        send_mail_reply(myqry.cfname,myqry.cemail,problem)
        messages.success(request,'mail has been sent')
        return redirect('/queries')
    return render(request,'query.html',{'qry':qry})
# def types_bbques(request):pass
    # if (request.POST.get("type")==""):
    #     ques=question.objects.all().order_by('question_id')
    #     messages.success(request,'All Types')
    #     return render(request,'display_bbques.html',{'ques':ques})
    # elif(request.POST.get("type")):
    #     type=request.POST.get('type')
    #     ques=question.objects.filter(type=type)
    #     messages.success(request,f'{type} quesions')
    #     return render(request,'display_bbques.html',{'ques':ques})
# def search_bbques(request):pass
    # if request.method=='POST':
    #     if(request.POST.get('search_que') is not None):
    #     #   print('hlo')
    #         search_que=request.POST.get('search_que')
    #         ques=question.objects.filter(que__contains=search_que)
    #         messages.success(request,f'you search for {search_que}')
    #         return render(request,'display_bbques.html',{'ques':ques})

    # else:
    #     return redirect('/display_bbques')
# Create your views here.
