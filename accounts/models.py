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
    def is_manager(self):
        return self.groups.filter(name = 'Manager').exists()
    
    @property
    def is_chef(self):
        return self.groups.filter(name = 'Chef').exists()
    
    @property
    def is_waiter(self):
        return self.groups.filter(name = 'Waiter').exists()
    
    @property
    def is_cashier(self):
        return self.groups.filter(name = 'Cashier').exists()

    
    @property
    def is_rider_staff(self):
        return self.groups.filter(name = 'Rider Staff').exists()
    
    @property
    def is_customer(self):
        return self.groups.filter(name='Customer').exists()
    

