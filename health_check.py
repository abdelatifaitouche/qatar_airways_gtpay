
import requests
from datetime import datetime
import pandas as pd
import time



#send a request to gtpay.digital 
#check its status
#report 

url = 'https://gtpay.digital/login/?next=/'
crm_url = "http://192.168.0.220/welcome.php"


def health_check(webapp_target):
    excel_data = pd.read_excel('log.xlsx')
    df = pd.DataFrame(excel_data)

    req = requests.get(webapp_target).status_code
    current_time = datetime.now()
    logs = {
        'WebApp' : webapp_target,
        'Time' : current_time,
        'Status' : req
    }
    df.loc[len(df)] = logs

    # Reset the index
    df = df.reset_index(drop=True)
    df.to_excel('log.xlsx')
    print(df)
    

def notifier(email):
    #send en email notification
    return 



#health_check(crm_url)


# importing the function from utils
from django.core.management.utils import get_random_secret_key

# generating and printing the SECRET_KEY
print(get_random_secret_key())




