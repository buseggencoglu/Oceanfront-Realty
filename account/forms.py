from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.forms import DateInput

from oceanf.models import EstatePersonal, Branch
from django.core.validators import RegexValidator

alphanumeric = RegexValidator('[A-Za-z ]', message='Only alpha characters are allowed.')


User = get_user_model()

USER_TYPES = (
    ('customer', 'Customer'),
    ('estate_person', 'Estate Person'),
)


# class RegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100, help_text='First Name')
#     last_name = forms.CharField(max_length=100, help_text='Last Name')
#     email = forms.EmailField(max_length=150, help_text='Email')
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class CustomerRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name',widget=forms.TextInput)
    last_name = forms.CharField(max_length=100, help_text='Last Name',widget=forms.TextInput)
    email = forms.EmailField(max_length=150, help_text='Email', widget=forms.EmailInput)
    birthDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EstatePersonRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name',widget=forms.TextInput)
    last_name = forms.CharField(max_length=100, help_text='Last Name',widget=forms.TextInput)
    email = forms.EmailField(max_length=150, help_text='Email',widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class RoleChooseForm(forms.Form):
    type = forms.ChoiceField(choices=USER_TYPES, help_text='User Type')


class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, help_text='First Name', widget=forms.TextInput, validators=[alphanumeric])
    last_name = forms.CharField(max_length=100, help_text='Last Name', widget=forms.TextInput, validators=[alphanumeric])
    email = forms.EmailField(max_length=150, help_text='Email', widget=forms.EmailInput)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',

        )