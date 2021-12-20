# Generated by Django 4.0 on 2021-12-19 04:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_bidang', models.CharField(max_length=3)),
                ('nama_bidang', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Jabatan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_jabatan', models.CharField(max_length=3)),
                ('nama_jabatan', models.CharField(max_length=100)),
                ('bidang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.bidang')),
            ],
        ),
        migrations.CreateModel(
            name='Kantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_kantor', models.CharField(max_length=3)),
                ('nama_kantor', models.CharField(max_length=100)),
                ('alamat', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nik', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{16}$', 'Format NIK Tidak Sesuai')])),
                ('jabatan', models.CharField(default='HRD', max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('no_hp', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^(08+[1-9])([0-9]{7,10})$', 'Format NO HP TIDAK SESUA!!!')])),
                ('npp', models.CharField(max_length=9)),
                ('nama_perusahaan', models.CharField(max_length=200)),
                ('alamat', models.CharField(max_length=250)),
                ('desa_kel', models.CharField(max_length=100)),
                ('kecamatan', models.CharField(max_length=100)),
                ('kota_kab', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tenaga_kerja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('no_kartu', models.CharField(max_length=11)),
                ('no_hp', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^(08+[1-9])([0-9]{7,10})$', 'Format NO HP TIDAK SESUA!!!')])),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('tgl_lahir', models.DateField()),
                ('tgl_keps', models.DateField()),
                ('tgl_na', models.DateField(blank=True, null=True)),
                ('npp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.perusahaan')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('no_hp', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^(08+[1-9])([0-9]{7,10})$', 'Format NO HP TIDAK SESUA!!!')])),
                ('jabatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.jabatan')),
                ('kode_kantor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.kantor')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='perusahaan',
            name='pembina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.profile'),
        ),
        migrations.AddField(
            model_name='perusahaan',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.CreateModel(
            name='Informasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=200)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='informasi/attachment/')),
                ('isi', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.profile')),
                ('npp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kepesertaan.perusahaan')),
            ],
        ),
    ]
