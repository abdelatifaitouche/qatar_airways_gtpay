from django.shortcuts import render,redirect
from .models import * 
from usermanagement.models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from usermanagement.decorators import allowed_user
from usermanagement.forms import CustomUserCreationForm
from django.contrib.auth.models import Group

# Create your views here.












@login_required(login_url='login_screen')
@allowed_user(allowed_roles=['admin' , 'staff'])
def dashboard(request):
    return render(request , 'app/dashboard.html')



@login_required(login_url='login_screen')
def userpage(request):
    return render(request , 'app/userpage.html')




@login_required(login_url='login_screen')
def upload_files(request):
    if request.method =='POST' :
        data = request.POST
        files = request.FILES.getlist('file')
        for file in files :
            instance = Document.objects.create(document=file)
            
            document_name = instance.document.name.split('/')[3][:8]
            
            try : 
                instance.employee = CustomUser.objects.get(matricule = document_name)
            except : 
                print('utilisateur non disponible')
            if instance : 
                    instance.save()
    return render(request , 'app/upload.html')



@login_required(login_url='login_screen')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            group = Group.objects.get(name = 'employee')
            user.groups.add(group)
            return redirect('create_user')
    else : 
        form = CustomUserCreationForm()
    context = {'form':form}
    return render(request , 'app/create_user.html' , context)



