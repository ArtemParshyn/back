from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import ApiUser


class UserProfileForm(forms.Form):
    user_ava_img = forms.ImageField(
        label='Profile Picture',
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.png, .jpg, .jpeg'})
    )
    user_name = forms.CharField(
        label='Отображаемое имя',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input form-input--light'})
    )
    user_about = forms.CharField(
        label='О себе',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input form-input--light', 'cols': 30, 'rows': 10})
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if not user_name:
            raise forms.ValidationError('Это поле обязательно.')
        # Sanitize input
        return user_name

    def clean_user_about(self):
        user_about = self.cleaned_data.get('user_about')
        return user_about



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
