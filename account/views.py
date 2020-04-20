from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import CreateUserForm, LoginForm
from .models import User


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('main:index')

    def form_invalid(self, form):
        messages.error(self.request, '아이디와 비밀번호를 다시 확인해주세요')
        return super().form_invalid(form)


class LoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.')
        return super().form_invalid(form)