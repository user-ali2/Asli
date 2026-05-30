from django.db import models

class Category(models.Model):

    name = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Food(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='foods'
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    image = models.ImageField(
        upload_to='foods/'
    )

    featured = models.BooleanField(default=False)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class SiteSettings(models.Model):

    restaurant_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    email = models.EmailField()

    address = models.TextField()

    opening_hours = models.CharField(max_length=200)

    facebook = models.URLField(blank=True, null=True)

    instagram = models.URLField(blank=True, null=True)

    tiktok = models.URLField(blank=True, null=True)

    twitter=models.URLField(blank=True, null=True)

    def __str__(self):
        return self.restaurant_name