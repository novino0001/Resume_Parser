from django.db import models

# Create your models here.
from django.contrib.auth.models import User



# Create your models here.
class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=254)  
    Phone_number = models.CharField(max_length=100)
    Degree=models.CharField(max_length=50)
    Skills=models.TextField(max_length=500)
    created_date =  models.DateTimeField(auto_now_add=True)
    Experience=models.TextField(default=0)
    resume_file = models.FileField()


    def Contact_Details(self):
        return f"{self.Email} , {self.Phone_number}"
    Contact_Details.admin_order_field = 'email'
    Contact_Details.short_description = 'Contact Details'
    
    def __str__(self):
        return self.user.email

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_resume = models.FileField(upload_to='documents')
    created_date =  models.DateTimeField(auto_now_add=True)
    # date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True) 