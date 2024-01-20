from django.urls import path
from . import views
# from user import views as user_view
# app_name = "account"
from django.contrib.auth import views as auth
urlpatterns = [

    path('user_details/', views.PersonalDetails, name='user_details'),
    path('', views.Main, name='Main'),
    path('succes/', views.succes, name='succes'),
    path('signup/', views.Signup, name='Signup'),
    path('login/', views.Login, name='Login'),
    path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
    path('verify-otp/', views.VerifyOTP, name='VerifyOTP'),
    # path('', views.index, name='index'),
    
]
