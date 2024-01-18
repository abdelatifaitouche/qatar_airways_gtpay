from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .utils import * 
from django.contrib.auth.models import User
from .models import CustomUser
from .decorators import *
from django.contrib.auth.decorators import login_required


# Create your views here.





def custom_login(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        user = authenticate(request , email=email , password=password)
        if user is not None : 
            send_otp(request , user.email)
            request.session['email'] = user.email
            request.session['password'] = password
            return redirect('otp_verification')
        else : 
            messages.error(request , 'Please, check your informations')   
    return render(request , 'usermanagement/login.html')

def resendOtp(request):
    return send_otp(request , request.session['email'])

def OTP(request):
    if request.method == "POST":
        otp = request.POST['otp_code']
        if otp == str(request.session['otp']):
            user = get_object_or_404(CustomUser , email = request.session['email'])
            login(request , user)
            if user.is_staff:   
                return redirect('dashboard')
            else : 
                return redirect('userpage')
        else : 
            #RESEND OTP
            messages.error(request , 'Incorrect code, try again ') 
            send_otp(request , request.session['email'])
            return redirect('otp_verification')

    return render(request,'usermanagement/otp.html')

@login_required(login_url='login_screen')
def logoutuser(request):
    logout(request)
    return redirect('login_screen')