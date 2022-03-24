from django import forms

from kepesertaan.models import Profile, Kantor, Bidang, Jabatan

class PembinaForm(forms.ModelForm):
    def __init__(self, bidang_id, *args, **kwargs):
        super(PembinaForm, self).__init__(*args, **kwargs)
        self.fields['jabatan'].queryset = self.fields['jabatan'].queryset.filter(bidang__kode_bidang=bidang_id)

    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control', 'disabled':'disabled','onkeyup':'this.value = this.value.toUpperCase()'
            }),
            'nama':forms.TextInput(attrs={
                'class':'form-control','onkeyup':'this.value = this.value.toUpperCase()'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control','onkeyup':'this.value = this.value.toUpperCase()'
            }),
            'no_hp':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'jabatan':forms.Select(attrs={
                'class':'form-control',
            }),
            'kode_kantor':forms.Select(attrs={
                'class':'form-control'
            })
        }

# class KantorForm(forms.ModelForm):
#     class Meta:
#         model = Kantor
#         fields = '__all__'

#         widgets = {
#             'kode_kantor':forms.TextInput(attrs={
#                 'class':'form-control','maxlength':'3'
#             }),
#             'nama_kantor':forms.TextInput(attrs={
#                 'class':'form-control','maxlength':'100'
#             }),
#             'alamat':forms.Textarea(attrs={
#                 'class':'form-control'
#             })
#         }

class BidangForm(forms.ModelForm):
    class Meta:
        model = Bidang
        fields = '__all__'

        widgets = {
            'kode_bidang':forms.TextInput(attrs={
                'class':'form-control','maxlength':'3'
            }),
            'nama_bidang':forms.TextInput(attrs={
                'class':'form-control','maxlength':'50'
            })
        }

class JabatanForm(forms.ModelForm):
    class Meta:
        model = Jabatan
        fields = '__all__'

        widgets = {
            'kode_jabatan':forms.TextInput(attrs={
                'class':'form-control','maxlength':'3'
            }),
            'nama_jabatan':forms.TextInput(attrs={
                'class':'form-control','maxlength':'100'
            }),
            'bidang':forms.Select(attrs={
                'class':'form-control'
            })
        }