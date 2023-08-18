from django.contrib import admin
from .models import question,Employee,gift
class EmployeeAdmin(admin.ModelAdmin):
    list_display=("email",'first_name','last_name','auth_token','user_profile_image','is_email_verified','emp_id')
admin.site.register(Employee,EmployeeAdmin)
class questionAdmin(admin.ModelAdmin):
    list_display=("question_id","que","code","type","a","b","c","d","ans")
admin.site.register(question,questionAdmin)
class giftAdmin(admin.ModelAdmin):
    list_display=('gift_id','gift_pic','gname','price','points_needed','rank_needed','gdate')
admin.site.register(gift,giftAdmin)
# Register your models here.
