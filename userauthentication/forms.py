from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User, Profile

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"placeholder": "Image"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Bio"})) 
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone No"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']