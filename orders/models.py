from django.db import models
from django.conf import settings
from menu.models import Food
from django.contrib.auth.models import User

class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        return total
    @property
    def total_items(self):
        total = sum(item.quantity for item in self.items.all())
        return total
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    

class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.food.price * self.quantity
    
    def __str__(self):
        return f"{self.food.name} x {self.quantity}"
    

class Order(models.Model):

    ORDER_TYPES = [
        ("takeout", "Takeout"),
        ("delivery", "Delivery"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("completed", "Completed"),
    ]

    PAYMENT_CHOICES = [
        ("cash", "Cash"),
        ("mpesa", "Mpesa"),

    ]

    order_type= models.CharField(max_length=20, choices=ORDER_TYPES, default="takeout")

    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    pickup_time = models.DateTimeField()

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order # {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    ) 

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.food.name}"
    

class DeliveryZone(models.Model):

    DELIVERY_TYPES = [
        ("foot", "On Foot"),
        ("restaurant_vehicle", "Restaurant Vehicle"),
        ("external_rider", "External Rider"),
    ]

    name = models.CharField(max_length=100)

    delivery_type = models.CharField(max_length=30, choices=DELIVERY_TYPES)

    external_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    estimated_time = models.CharField(max_length=50)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DeliveryStaff(models.Model):

    VEHICLE_CHOICES = [
        ("walking", "Walking"),
        ("bicycle", "Bicycle"),
        ("motorcycle", "Motorcycle"),

    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_CHOICES
    )

    is_available = models.BooleanField(
        default=True
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    
    
