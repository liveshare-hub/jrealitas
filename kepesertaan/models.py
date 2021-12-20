import os
from django.db import models
# from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# User = get_user_model()

NIK_VALIDATOR = RegexValidator("^\d{16}$","Format NIK Tidak Sesuai")
HP_VALIDATOR = RegexValidator("^(08+[1-9])([0-9]{7,10})$", "Format NO HP TIDAK SESUA!!!")

class Kantor(models.Model):
    kode_kantor = models.CharField(max_length=3)
    nama_kantor = models.CharField(max_length=100)
    alamat = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.kode_kantor} - {self.nama_kantor}'

class Bidang(models.Model):
    kode_bidang = models.CharField(max_length=3)
    nama_bidang = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.kode_bidang} - {self.nama_bidang}'

class Jabatan(models.Model):
    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE)
    kode_jabatan = models.CharField(max_length=3)
    nama_jabatan = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.kode_jabatan} - {self.nama_jabatan}'

    

class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    no_hp = models.CharField(max_length=13, validators=[HP_VALIDATOR])
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    kode_kantor = models.ForeignKey(Kantor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} - {self.nama}'

# class User_Profile(models.Model):
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     nama = models.CharField(max_length=100)
#     nik = models.CharField(max_length=16, validators=[NIK_VALIDATOR])
#     email = models.EmailField(max_length=100)
#     no_hp = models.CharField(max_length=13, validators=[HP_VALIDATOR])
#     Jabatan = models.CharField(default='HRD', max_length=10)

#     def __str__(self):
#         return f'{self.nama} - {self.Jabatan}'

class Perusahaan(models.Model):
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=16, validators=[NIK_VALIDATOR])
    jabatan = models.CharField(max_length=50, default="HRD")
    email = models.EmailField(max_length=100)
    no_hp = models.CharField(max_length=13, validators=[HP_VALIDATOR])
    npp = models.CharField(max_length=9)
    nama_perusahaan = models.CharField(max_length=200)
    alamat = models.CharField(max_length=250)
    desa_kel = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    kota_kab = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    pembina = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.npp} - {self.nama_perusahaan}'

    def total_npp(*args, **kwargs):
        
        npp = Perusahaan.objects.select_related('pembina').filter(pembina__username__username=kwargs['kwargs'])
        return npp.count()

# class Perusahaan_user(models.Model):
#     nama = models.CharField(max_length=100)
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
#     nik = models.CharField(max_length=16, validators=[NIK_VALIDATOR])
#     email = models.EmailField(max_length=100)
#     no_hp = models.CharField(max_length=13, validators=[HP_VALIDATOR])
#     jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.username} - {self.nama}'


class Tenaga_kerja(models.Model):
    npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    no_kartu = models.CharField(max_length=11)
    no_hp = models.CharField(max_length=13, validators=[HP_VALIDATOR])
    email = models.EmailField(max_length=100, blank=True, null=True)
    tgl_lahir = models.DateField()
    tgl_keps = models.DateField()
    tgl_na = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.no_kartu} - {self.nama}'

class Informasi(models.Model):
    npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='informasi/attachment/', blank=True, null=True)
    isi = models.TextField()
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.npp.npp} - {self.judul}'

    def filename(self):
        return os.path.basename(self.attachment.name)