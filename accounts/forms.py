from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': field.capitalize(),

                'class': 'auth-input'
            })
        

class LoginForm(AuthenticationForm):
   # username = forms.CharField()
    
    #passowrd = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'placeholder': field.capitalize(),
                'class': 'auth-input'
            })