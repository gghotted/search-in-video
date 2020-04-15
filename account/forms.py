from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class CreateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), label='패스워드 확인'
    )


    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(
            widget=forms.PasswordInput(), label='패스워드'
        )
        self.label_suffix = ''


    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)
        self.fields['password'].label = '패스워드'
        self.label_suffix = ''