# Generated by Django 4.0 on 2022-01-06 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kunjungan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='berita_kunjungan',
            name='to_lokasi',
            field=models.CharField(default=1,max_length=100),
            preserve_default=False,
        ),
    ]
