from django.contrib import admin
from django.urls import path,include
from .views import * 
urlpatterns = [
   path('userpage/' , userpage , name="userpage"),
   path('' ,dashboard , name="dashboard"),

   path('upload/' , upload_files , name = "upload_files"),
   path('create_user/' , create_user , name="create_user"),

]
