import pandas as pd
from datetime import datetime
from csv import writer
from django.core.mail import send_mail, EmailMessage
from django.conf import settings






class HealthClassMiddleware : 
    def __init__(self , get_response):
        self.get_response = get_response
    
    def get_client_ip(self , request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        
        response = self.get_response(request)
        logs = [request.build_absolute_uri() , self.get_client_ip(request) ,  response.status_code , datetime.now()]
        
        with open('logs.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(logs)
            f_object.close()
        #check if its 500 error
        if response.status_code == 500 or response.status_code == 400 : 
            #send en email notification
            subject = 'IMPORTANT : An APP ERROR HAS OCCURED'
            message = f'the app is down right now at : {logs[2]} that has returned an error of {logs[1]}\n\nGood luck!!!'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["abdelatif.aitouche3@gmail.com"]
            send_mail( subject, message, email_from, recipient_list )
            print('fucked')
        #send an email notification
        return response