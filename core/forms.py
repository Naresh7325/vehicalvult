from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','role','firstName','lastName','phoneNumber','password1','password2']
        widgets = {
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }

class UserLoginForm(forms.Form):from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


# ✅ SIGNUP FORM
class UserSignupForm(UserCreationForm):

    username = forms.CharField(max_length=100)   # ✅ ADD THIS

    class Meta:
        model = User
        fields = [
            'username',     # ✅ IMPORTANT
            'email',
            'role',
            'firstName',
            'lastName',
            'phoneNumber',
            'password1',
            'password2'
        ]

        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    

# ✅ LOGIN FORM
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=100)   # ✅ must be username
    password = forms.CharField(widget=forms.PasswordInput)
    