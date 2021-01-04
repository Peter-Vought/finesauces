from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            )
        }
class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'postal_code', 'city', 'country')

        widgets = {
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'postal_code': forms. TextInput (
                attrs={'class': 'form-control'}
            ),
            'city': forms. TextInput (
                attrs={'class': 'form-control'}
            ),
            'country': forms. TextInput (
                attrs={'class': 'form-control'}
            )
        }

class UserRegistrationForm(forms.ModelForm):

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control'}
            ),
        }

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
