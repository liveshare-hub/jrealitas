from django import forms
from django.db.models import fields
from django.forms import widgets

from .models import Informasi, Profile

class UploadForm(forms.Form):
    file = forms.FileField()

class InformasiForm(forms.ModelForm):
    class Meta:
        model = Informasi
        # fields = '__all__'
        exclude = ('user',)

        widgets = {
            'judul':forms.TextInput(attrs={
                'class':'form-control','maxlength':'100'
            }),
            'isi':forms.Textarea(attrs={
                'class':'form-control', 'maxlength':'500'
            }),
            'attachment':forms.FileInput(attrs={
                'class':'from-control'
            }),
        }


class PembinaForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('username','kode_kantor')

        widgets = {
            'nama':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
            }),
            'no_hp':forms.TextInput(attrs={
                'class':'form-control'
            })
        }