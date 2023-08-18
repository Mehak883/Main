from django.urls import path,include
from bbquiz import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('create_ques/',views.create_ques,name="create_ques"),
    path('display_bbques/',views.display_bbques,name="display_bbques"),
    path('edit_bbques/<int:question_id>',views.edit_bbques,name="edit_bbques"),
    path('delete_bbques/<int:question_id>',views.delete_bbques,name="delete_bbques"),
    path('home_que/',views.main_que,name='home_que'),
    path('signup_emp/',views.signup_emp,name='signup_emp'),
    path('add_gifts/',views.add_gifts,name='add_gifts'),
    path('login_que/',views.login_que,name='login_que'),
    path('login_que1/',views.login_que1,name='login_que1'),
    path('signup_que/',views.signup_que,name='signup_que'),
    path('logout_que/',views.logout_que,name='logout_que'),
    path('reset_que/',views.reset_que,name='reset_que'),
    path('queries/',views.queries,name='queries'),
    path('forget_pass_que/',views.forget_pass_que,name='forget_pass_que')
    



    # path('login/',views.login,name='login'),
    # path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # path('social-auth/',include('social_django.urls',namespace='social')),
    
    ]