from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreateUserForm, LoginForm
from .models import User


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('main:index')


class LoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'account/login.html'
