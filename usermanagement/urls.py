from django.contrib import admin
from django.urls import path
from .views import * 

urlpatterns = [
    
    path('login/' , custom_login , name="login_screen"),
    path('otp/' , OTP , name="otp_verification"),

    path('logout/' , logoutuser , name="logout"),
    path('resend_otp/' , resendOtp , name="resendOtp")

]
