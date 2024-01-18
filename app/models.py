from django.db import models
from usermanagement.models import CustomUser

# Create your models here.




class Document(models.Model):
    document = models.FileField(upload_to='documents/%Y/%m',null="True")
    employee = models.ForeignKey('usermanagement.CustomUser' , on_delete = models.CASCADE , null = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.document.name
    def getName(self):
        return self.document.name.split('/')[1]