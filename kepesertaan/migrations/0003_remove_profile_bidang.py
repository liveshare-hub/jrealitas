# Generated by Django 4.0 on 2021-12-19 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kepesertaan', '0002_profile_bidang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bidang',
        ),
    ]
