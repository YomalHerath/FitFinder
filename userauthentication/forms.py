from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']