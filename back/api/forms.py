from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import ApiUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    class Meta:
        model = ApiUser
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm password'}))

    class Meta:
        model = ApiUser
        fields = ('username', 'password1', 'password2')
