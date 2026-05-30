from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    

    @property
    def is_owner(self):
        return self.groups.filter(name ='Owner').exists()
    
    @property
    def is_management(self):
        return self.groups.filter(name = 'Management').exists()
    
    @property
    def is_staff_member(self):
        return self.groups.filter(name = 'Staff').exists()
    
    @property
    def is_customer(self):
        return self.groups.filter(name='Customer').exists()
    

