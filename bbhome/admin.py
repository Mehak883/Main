from django.contrib import admin
from .models import CustomUser,points,profile,ranking,otp_grabber,query,order
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()

# class profileAdmin(admin.ModelAdmin):
#     list_display=("user","p_id","created_at","auth_token","test_attempted")
# admin.site.register(profile,profileAdmin)
class profileAdmin(admin.ModelAdmin):
    list_display=("user","bio","phone_number",'pincode','address',"education","ecountry","ins_name","city","country")
admin.site.register(profile,profileAdmin)

class pointsAdmin(admin.ModelAdmin):
    list_display=("user","resultid","type","right","wrong",'n_a',"point",'total_que','coins',"date","quiztime","time")
admin.site.register(points,pointsAdmin)

class queryAdmin(admin.ModelAdmin):
    list_display=('cid','cemail','cfname','clname','problem','replied_by','ctime')
admin.site.register(query,queryAdmin)
class rankingAdmin(admin.ModelAdmin):
    list_display=('user','total_rights','gift_coins','rank')
admin.site.register(ranking,rankingAdmin)
# Register your models here.
admin.site.register(User)
class otp_grabberAdmin(admin.ModelAdmin):
    list_display=('phone_number','otp')
admin.site.register(otp_grabber,otp_grabberAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display=('user','gift_id','cprice')
admin.site.register(order,orderAdmin)
