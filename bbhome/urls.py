from django.urls import path,include
from bbhome import views
from .views import ContinueWithGoogleView
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('home',views.home,name="home"),
      path('login',views.login,name='login'),
    # path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # path('social-auth/',include('social_django.urls',namespace='social')),
    path('signup/',views.signup,name='signup'),
    path('login_check/',views.login_check,name='login_check'),
    path('ContinueWithGoogleView/', ContinueWithGoogleView.as_view(), name='ContinueWithGoogleView'),
    path('profile',views.profile,name='profile'),
    path('verify/<str:token>/<str:profession>',views.verify,name='verify'),

    path('bioset/',views.bioset,name='bioset'),
    path('upload/',views.upload,name='upload'),
    path('intro/',views.intro,name='intro'),
    path('edu/',views.edu,name='edu'),
    path('quiz_html/',views.quiz_html,name='quiz_html'),
    path('quiz_java/',views.quiz_java,name='quiz_java'),
    path('quiz_python/',views.quiz_python,name='quiz_python'),
    path('quiz_cpp/',views.quiz_cpp,name='quiz_cpp'),
    path('quiz_clang',views.quiz_clang,name='quiz_clang'),
    path('quiz_javascript',views.quiz_javascript,name='quiz_javascript'),
    path('quiz_aptitude',views.quiz_aptitude,name='quiz_aptitude'),
    path('result/',views.result,name='result'),
    path('bbresult/<int:id>/<int:length>/',views.bbresult,name='bbresult'),
    path('gift',views.gift,name='gift'),
    path('send_otp',views.send_otp,name='send_otp'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    # path('ranking/',views.ranking,name='ranking'),
    path('check/',views.check,name='check'),
    path('add_address/',views.add_address,name='add_address'),
 path('logout/',views.logout,name='logout'),
 path('rank/',views.rank,name='rank'),
path('about/',views.about,name='about'),
path('contact/',views.contact,name="contact"),
 path('forget_pass/',views.forget_pass,name='forget_pass'),
 path('reset/<str:email>/<str:token>',views.reset,name='reset')



]