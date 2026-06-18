from rest_framework import serializers
from .models import Food,Category

class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "available",
            "featured",
            "created_at",
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = [
            "id",
            "name",
            "slug",
            "created_at",
        ]