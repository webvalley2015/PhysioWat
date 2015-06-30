__author__ = 'federico'
from django import forms
class LoginForm(forms.Form):
    your_username = forms.CharField(label='Your Username', max_length=100)
    your_password = forms.PasswordInput(max_lenght=100)
