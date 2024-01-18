
from datetime import datetime,timedelta
import random
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


def send_otp(request , email):
    #check for the current time 
    #add the 2min validty 
    #if its valid, the code is working
    #if its passed the time, we need to generate another code

    otp = random.randint(100000 , 999999)
    request.session['otp'] = otp

    #add the send email functionality
    subject = 'welcome to GTPAY APP'
    message = f'Dear user,\n\nTo ensure the security of your account, we require you to verify your identity\nPlease enter this code on the verification page to complete the process {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )



    
    