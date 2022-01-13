# Generated by Django 4.0 on 2022-01-13 13:35

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
            ],
        ),
    ]
