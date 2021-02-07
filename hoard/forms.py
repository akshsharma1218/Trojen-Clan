from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    message = forms.CharField(
        required=True
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class OwnerName(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name']
