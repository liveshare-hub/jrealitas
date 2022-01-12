from django import forms
from django.db.models import fields
from django.forms import widgets

from .models import Informasi

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


