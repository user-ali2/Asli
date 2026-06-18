from django.db import models
from django.conf import settings
from menu.models import Food


class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
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
    

class DeliveryZone(models.Model):

    DELIVERY_TYPES = [
        ("foot", "On Foot"),
        ("restaurant_vehicle", "Restaurant Vehicle"),
        ("external_rider", "External Rider"),
    ]

    name = models.CharField(max_length=100)

    delivery_type = models.CharField(max_length=30, choices=DELIVERY_TYPES)

    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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

    user = models.ForeignKey(
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
    

class Order(models.Model):

    ORDER_TYPES = [
        ("dine_in", "Dine In"),
        ("takeout", "Takeout"),
        ("delivery", "Delivery"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("picked_up", "Picked Up"),
        ("on_the_way", "On the Way"),
        ("delivered", "Delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("unable_to_proceed", "Unable To Proceed"),
    ]

    #PAYMENT_CHOICES = [
     #   ("cash", "Cash"),
      #  ("mpesa", "Mpesa"),

    #]

    

    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPES,
        default="takeout"
    )

    

   # payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    pickup_time = models.DateTimeField(null=True, blank=True)

    
    full_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    area = models.CharField(max_length=100, blank=True, null=True)
    house_name= models.CharField(max_length=100, blank=True, null=True)
    plot_number = models.CharField(max_length=50, blank=True, null=True)

    #address = models.TextField(blank=True,null=True)

    delivery_notes = models.TextField(
        blank=True,
        null=True
    )

    zone = models.ForeignKey(
        "DeliveryZone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    assigned_staff = models.ForeignKey(
    "DeliveryStaff",
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order #{self.id}"


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

    food_name = models.CharField(max_length=200)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return self.food_name
    


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("mpesa", "Mpesa"),
        ("card", "Card"),
    ]

    PAYMENT_STATUSES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ] 

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUSES,
        default="pending"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    mpesa_checkout_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    merchant_request_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    mpesa_receipt_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
    

class Refund(models.Model):
    payment = models.ForeignKey(
        "Payment",
        on_delete=models.CASCADE,
        related_name="refunds" 

    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    reason = models.TextField()

    refunded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    refunded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund #{self.id}"


class RefundRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="refund_requests"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund Request #{self.id}"    
    


class PaymentAttempt(models.Model):

    ATTEMPT_STATUSES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="attempts",

    )

    mpesa_checkout_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )

    mercahant_request_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    mpesa_receipt_number = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )

    status = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
