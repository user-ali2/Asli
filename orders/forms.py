from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = ["pickup_time", "payment_method"]

        widgets = {
            "pickup_time": forms.DateTimeInput(attrs={
                "type": "datetime-local"
            })
        }