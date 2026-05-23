from django.contrib import admin
from .models import Category, Food, SiteSettings

admin.site.register(Category)
admin.site.register(Food)
admin.site.register(SiteSettings)
