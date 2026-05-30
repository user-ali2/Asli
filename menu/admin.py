from django.contrib import admin
from .models import Category, Food

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["slug", "name"]

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [
       # "id",
        "name",
        "category",
        "price",
        "available",
        "featured"
    ]

    list_filter = [
        "category",
        "available",
        "featured",
    ]

    search_fields = [
        "name",
        "description",
    ]

    list_editable = [
        "available",
        "featured"
    ]

    prepopulated_fields = {
        'slug': ('name',)
    }
