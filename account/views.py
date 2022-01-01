from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.timezone import datetime, timedelta
from datetime import date

from oceanf.models import Customer, EstatePersonal, Profile
from .tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
)
from .forms import RoleChooseForm, CustomerRegisterForm, EstatePersonRegisterForm


def login_request(request):
    template = 'login.html'
    if request.method == 'POST':
        print(request.POST)
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.form")
    form = AuthenticationForm()
    return render(request=request,
                  template_name=template,
                  context={"form": form})


def register_customer(request):
    # if this is a POST request we need to process the form data
    template = 'register_customer.html'

    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            if (date.today() - form.cleaned_data['birthDate']) < timedelta(days=18 * 365):
                return render(request, template, {
                    'form': form,
                    'error_message': 'Age should be greater than 18.'
                })

            user = form.save()
            Customer.objects.create(user=user, birthDate=form.cleaned_data['birthDate'])
            user.is_active = True
            user.save()

            # Login the user
            login(request, user)
            return redirect('sent')

    else:
        form = CustomerRegisterForm()
    return render(request, template, {"form": form})


def register_estate_person(request):
    # if this is a POST request we need to process the form data
    template = 'register_estate_person.html'

    if request.method == "POST":
        form = EstatePersonRegisterForm(request.POST)
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })

            user = form.save()
            EstatePersonal.objects.create(user=user, rate=0)
            user.is_active = False
            user.save()

            return redirect('sent')

    else:
        form = EstatePersonRegisterForm()
    return render(request, template, {"form": form})


def role_choose(request):
    template = 'role_choose.html'

    if request.method == "POST":
        form = RoleChooseForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['type'] == 'customer':
                return HttpResponseRedirect('/register_customer')
            else:
                return HttpResponseRedirect('/register_estate_person')

        return redirect('sent')
    else:
        form = RoleChooseForm()
    return render(request, template, {"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')
