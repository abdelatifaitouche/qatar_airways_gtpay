from django.shortcuts import render , redirect, get_object_or_404
from .models import * 
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import * 
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .decorators import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .utils import send_otp
from datetime import datetime,timedelta



# Create your views here.


@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def home(request):
    employee = Employee.objects.all()
    files = Files.objects.all().order_by("-created_at")
    nbr_employee = len(employee)
    context = {'nombre' : nbr_employee , 'fiche_de_paie' : files}
    return render(request , 'app/dashboard.html' , context)


@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def employee(request):
    employee = Employee.objects.all()
    nbr_employee = len(employee)
    context = {'employee' : employee , 'nombre' : nbr_employee}
    return render(request , 'app/employe.html' , context)






@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def employee_details(request , pk):
    employee = Employee.objects.get(id = pk)
    files = Files.objects.filter(fiche__contains= employee.matricule).order_by("-created_at")
    total = files.count()
    context = {'employee' : employee , 'fiches':files , 'number':total}
    return render(request , 'app/employee_details.html' , context)











@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def upload_file(request):
    if request.method =='POST' :
        data = request.POST
        files = request.FILES.getlist('file')
        for file in files :
            instance = Files.objects.create(fiche=file)
            if instance : 
                instance.save()
            
        

        employee = Employee.objects.all()
        """
        for em in employee:
            subject = 'Ericsson : fiche de paie du mois '
            message = f'Bonjour {em.name}' + '\n Vous venez de recevoir votre fiche de paie sur votre platform https://gtpay.digital \n Merci.'
            from_email = settings.EMAIL_HOST_USER  # Sender's email address
            recipient_list = [em.email.strip()]  # List of recipient email addresses
            send_mail(subject, message, from_email, recipient_list)
        """

    context = {}
    return render(request , 'app/upload.html' , context)


""""
def loginPage(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username = username , password=password)
        if user is not None :
            login(request , user)
            if user.is_staff:
                return redirect('dashboard')
            else : 
                return redirect('user_page')
        else :
            messages.error(request , 'please check your informations')


    return render(request , 'app/login.html')
"""


def loginPage(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username = username , password=password)
        if user is not None : 
            
            send_otp(request , user.email)
            request.session['email'] = user.email
            request.session['username'] = username
            request.session['password'] = password
            return redirect('otp')
        else :
            messages.error(request , 'please check your informations')
    return render(request , 'app/login.html')

def otp_view(request):
    if request.method == "POST" :
        otp = request.POST.get('otp_code')
        
        if otp == str(request.session['otp']):
            print('here')
            user = User(username = request.session['username'])
            user = get_object_or_404(User , username = request.session['username'])    
            login(request , user)
            del request.session['username']
            del request.session['otp']
            if request.user.is_staff:
                return redirect('dashboard')
            else : 
                return redirect('user_page')
        else : 
            #RESEND OTP
            send_otp(request , request.session['email'])
            messages.error(request , "Incorrect code ")
            return redirect('otp')
    
    return render(request , 'app/otp.html')



@login_required(login_url='loginpage')
def logoutuser(request):
    logout(request)
    return redirect('loginpage')




@login_required(login_url='loginpage')
def userPage(request):
    current_user = request.user.employee
    user = Employee.objects.get(user = request.user)
    if user.first_login == True : 
        user.first_login = False
        user.save()
        return redirect('security_protocol')
    else : 
    #I need to check for the password update : start from 
    #https://stackoverflow.com/questions/41413423/detect-a-changed-password-in-django
        matricule = current_user.matricule
        files = Files.objects.filter(fiche__startswith= matricule).order_by("-created_at")
        
        context = {'files' : files}
    #context = {'files' : files , 'user' : current_user}
        return render(request , 'app/user_page.html' , context)


@login_required(login_url='loginpage')
def securityProtocol(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_page')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/security.html', {
        'form': form , 'user':request.user
    })



@login_required(login_url='loginpage')
def download_file(request , pk):
    obj = Files.objects.get(id=pk)
    response = HttpResponse(obj.fiche, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{obj.get_file_name()}"'
    return response



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def create_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name = 'employee')
            Employee.objects.create(user = user , name = user.username ,nom = form.cleaned_data['nom'],prenom = form.cleaned_data['prenom'] ,  matricule = form.cleaned_data['matricule'] , email=form.cleaned_data['email'])
            user.groups.add(group)
            messages.success(request, 'employee created successfully!')
            return redirect('create_user')
    context = {'form' : form}

    return render(request , 'app/create_user.html' , context)



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def updateUser(request , pk):
    employee = Employee.objects.get(id = pk)
    employee_form = UserCreationForm(instance = employee.user)
    if request.method == "POST":
        employee_form = UserCreationForm(request.POST)
        if employee_form.is_valid():
            form = employee_form.save()
            form.save()
            return redirect('app/employe_form.html')
    context = {'form' : employee_form}
    return render(request , 'app/employe_form.html',context)




@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def deleteUser(request , pk):
    employee = Employee.objects.get(id=pk)
    user = User.objects.get(username = employee.name)
    if request.method == "POST" :
        employee.delete()
        user.delete()
        return redirect('employee')
    context = {'employee' : employee}
    return render(request , 'app/delete_employee.html' , context)



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['employee'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/change_password.html', {
        'form': form , 'user':request.user
    })



@login_required(login_url='loginpage')
def persoInfo(request):
    user = Employee.objects.get(user = request.user)
    matricule = user.matricule
    files = Files.objects.filter(fiche__startswith= matricule).count
    context = {'user' : user , 'files' : files}
    return render(request , 'app/info_perso.html' , context)
