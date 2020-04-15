from django.shortcuts import render, reverse, HttpResponseRedirect, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import LoginForm
from .models import User


class CreateUserView(CreateView):
    model = User
    fields = ('username', 'password')


class LoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'account/login.html'
