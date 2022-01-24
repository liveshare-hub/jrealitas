from django.db import models
from django.contrib.auth import get_user_model
from kepesertaan.models import Perusahaan, Profile

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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.petugas.username.username} - {self.to_perusahaan.npp}'

