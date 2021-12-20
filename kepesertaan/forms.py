from django import forms
from django.forms import widgets

from .models import Profile, Jabatan, Bidang

class UploadForm(forms.Form):
    file = forms.FileField()

# class PembinaForm(forms.ModelForm):
#     bidang = forms.ModelChoiceField(queryset=Bidang.objects.all(),
#         widget=forms.Select(attrs={'class':'form-control'}))
    
#     class Meta:
#         model = Profile
#         exclude = ('username','kode_kantor',)

#         widgets = {
#             'nama':forms.TextInput(attrs={
#                 'class':'form-control', 'onkeyup':"this.value = this.value.toUpperCase()",
#                 'id':'nama',
#             }),
#             'email':forms.EmailInput(attrs={
#                 'class':'form-control'
#             }),
#             'no_hp':forms.TextInput(attrs={
#                 'class':'form-control'
#             }),

#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['jabatan'].queryset = Jabatan.objects.none()

#         if 'bidang' in self.data:
#             try:
#                 id_bidang = int(self.data.get('bidang'))
#                 self.fields['jabatan'].queryset = Jabatan.objects.filter(bidang_id=id_bidang).order_by('-kode_jabatan')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['jabatan'].queryset = self.instance.jabatan.bidang.order_by('-kode_jabatan')