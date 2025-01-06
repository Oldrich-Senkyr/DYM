#print("LoginForm is being imported")

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

# Dynamically get the custom user model
User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Your username'),
        'class': 'w-full py-4 rounded-xl'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Your password'),
        'class': 'w-full py-4 rounded-xl'
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User  # Use the dynamically retrieved user model
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(
        label=_("Username"), 
        widget=forms.TextInput(attrs={
            'placeholder': _('Your username'),
            'class': 'w-full py-4 rounded-xl'
        })
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': _('Your email address'),
        'class': 'w-full py-4 rounded-xl'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Your password'),
        'class': 'w-full py-4 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Repeat password'),
        'class': 'w-full py-4 rounded-xl'
    }))