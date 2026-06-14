from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):

    payment_method = forms.ChoiceField(
        choices=[
            ("cash", "Cash"),
            ("mpesa", "Mpesa"),
            ("card", "Card"),
        ],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Order

        fields = ["pickup_time", 
                  "full_name",
                  "phone",
                  "area",
                  "house_name",
                  "plot_number",
                  "delivery_notes",
                  "zone",
                ]

        widgets = {
            "pickup_time": forms.DateTimeInput(attrs={
                "type": "datetime-local"
            }),

            "address": forms.Textarea(attrs={
                "rows": 3
            }),

            "delivery_notes": forms.Textarea(attrs={
                "rows": 3
            }),
        }