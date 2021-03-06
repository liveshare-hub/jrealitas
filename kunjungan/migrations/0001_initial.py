# Generated by Django 4.0 on 2022-03-28 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kepesertaan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='berita_kunjungan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_nama', models.CharField(max_length=50)),
                ('to_jabatan', models.CharField(max_length=50)),
                ('to_alamat', models.CharField(max_length=500)),
                ('to_no_hp', models.CharField(max_length=13)),
                ('to_lokasi', models.CharField(max_length=100)),
                ('tujuan', models.CharField(choices=[('1', 'SOSIALISASI'), ('2', 'KELENGKAPAN DATA KLAIM'), ('3', 'PENYELESAIAN KASUS JKK'), ('4', 'KUNJUNGAN LAPANGAN / CEK KASUS'), ('5', 'PEMBINAAN FASILITAS KESEHATAN (PLKK)')], max_length=2)),
                ('hasil', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('petugas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.profile')),
                ('to_perusahaan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.perusahaan')),
            ],
        ),
        migrations.CreateModel(
            name='approval_bak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'PROSES'), ('1', 'SETUJU'), ('2', 'DITOLAK')], default='0', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('berita_acara', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kunjungan.berita_kunjungan')),
            ],
        ),
    ]
