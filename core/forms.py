from django import forms

from django.contrib.auth.models import User
# from django.forms import widgets

class LoginForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username','password']
        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Username ...'
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control','placeholder':'Password'
            })
        }