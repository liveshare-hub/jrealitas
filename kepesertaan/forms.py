from django import forms
from django.db.models import fields
from django.forms import widgets

from .models import Informasi

class UploadForm(forms.Form):
    file = forms.FileField()

class InformasiForm(forms.ModelForm):
    class Meta:
        model = Informasi
        fields = '__all__'

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
            'npp':forms.Select(attrs={
                'class':'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super(InformasiForm, self).__init__(*args, **kwargs)
        self.fields['npp'].required = False

