from django import forms
from .models import berita_kunjungan

class KunjunganForm(forms.ModelForm):
    class Meta:
        model = berita_kunjungan
        exclude = ('petugas',)

        widgets = {
            'to_nama':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'to_jabatan':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'to_alamat':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'to_no_hp':forms.TextInput(attrs={
                'class':'form-control','maxlength':'13'
            }),
            'hasil':forms.Textarea(attrs={
                'class':'form-control','rows':'20'
            }),
            'tujuan':forms.Select(attrs={
                'class':'form-control'
            }),
            'to_lokasi':forms.TextInput(attrs={
                'class':'form-control', 'maxlength':'100'
            })
        }