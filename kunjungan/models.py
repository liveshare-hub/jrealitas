from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from kepesertaan.models import Perusahaan, Profile

import PIL

User = get_user_model()

TUJUAN = (
    ('1','SOSIALISASI'),
    ('2','KELENGKAPAN DATA KLAIM'),
    ('3','PENYELESAIAN KASUS JKK'),
    ('4','KUNJUNGAN LAPANGAN / CEK KASUS'),
    ('5','PEMBINAAN FASILITAS KESEHATAN (PLKK)')
)

class berita_kunjungan(models.Model):
    petugas = models.ForeignKey(Profile, on_delete=models.CASCADE)
    to_perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
    to_nama = models.CharField(max_length=50)
    to_jabatan = models.CharField(max_length=50)
    to_alamat = models.CharField(max_length=500)
    to_no_hp = models.CharField(max_length=13)
    to_lokasi = models.CharField(max_length=100)
    tujuan = models.CharField(choices=TUJUAN, max_length=2)
    hasil = models.TextField()
    # qrcode_pembina = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.petugas.username.username} - {self.to_perusahaan.npp}'

    # def save(self, *args, **kwargs):

    #     return super().save(*args, **kwargs)

class approval_bak(models.Model):
    berita_acara = models.ForeignKey(berita_kunjungan, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.berita_acara.to_perusahaan.nama_perusahaan}'

@receiver(post_save, sender=berita_kunjungan, dispatch_uid="create_approval")
def kirim_approval(sender, instance, created, **kwargs):
    if created:
        approval_bak.objects.create(berita_acara=instance)
