from io import BytesIO
# from msilib.schema import File
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from kepesertaan.models import Perusahaan, Profile

import qrcode
from PIL import Image, ImageDraw

User = get_user_model()

TUJUAN = (
    ('1','SOSIALISASI'),
    ('2','KELENGKAPAN DATA KLAIM'),
    ('3','PENYELESAIAN KASUS JKK'),
    ('4','KUNJUNGAN LAPANGAN / CEK KASUS'),
    ('5','PEMBINAAN FASILITAS KESEHATAN (PLKK)')
)

STATUS = (
    ('0','PROSES'),
    ('1','SETUJU'),
    ('2','DITOLAK')
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
    # qrcode_pembina = models.ImageField(upload_to='media/kunjungan/pembina/')
    # qrcode_to_nama = models.ImageField(upload_to='media/kunjungan/toNama/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.petugas.username.username} - {self.to_perusahaan.npp} - {self.to_nama}'

    # def save(self, *args, **kwargs):
    #     qr =qrcode.QRCode(
    #         version=20,
    #         error_correction=qrcode.ERROR_CORRECT_M,
    #         box_size=50,
    #         border=2
    #     )

    #     data_pembina = """
    #     Nama : {}
    #     Kode Pembina : {}
    #     Jabatan : {}
    #     """.format(self.petugas.nama, self.petugas.username.username, self.petugas.jabatan.nama_jabatan)

    #     data_to_nama = """
    #     Nama : {}
    #     Jabatan/Sebagai : {}
    #     No Hp : {}
    #     """.format(self.to_nama, self.to_jabatan, self.to_no_hp)

    #     qr1_img = qrcode.make(data_pembina)
    #     qr2_img = qrcode.make(data_to_nama)

    #     canvas1 = Image.new('RGB', (300,300), 'white')
    #     draw1 = ImageDraw.Draw(canvas1)
    #     canvas1.paste(qr1_img)
    #     fname1 = f'{self.petugas.username.username}-{self.created}.PNG'
    #     buff1 = BytesIO()
    #     canvas1.save(buff1, 'PNG')
    #     self.qrcode_pembina.save(fname1, File(buff1), save=False)
    #     canvas1.close()

    #     canvas2 = Image.new('RGB',(300,300), 'white')
    #     draw2 = ImageDraw.Draw(canvas2)
    #     canvas2.paste(qr2_img)
    #     fname2 = f'{self.to_nama}-{self.created}.PNG'
    #     canvas2.save(buff1, 'PNG')
    #     self.qrcode_to_nama.save(fname2, File(buff1), save=False)
    #     canvas2.close()

        # return super().save(*args, **kwargs)

class approval_bak(models.Model):
    berita_acara = models.ForeignKey(berita_kunjungan, on_delete=models.CASCADE)
    # approved = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS, default='0')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.berita_acara.to_perusahaan.nama_perusahaan}'

@receiver(post_save, sender=berita_kunjungan, dispatch_uid="create_approval")
def kirim_approval(sender, instance, created, **kwargs):
    if created:
        approval_bak.objects.create(berita_acara=instance)
