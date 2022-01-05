# Generated by Django 4.0 on 2022-01-03 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=100)),
                ('pesan', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to='auth.user')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to='auth.user')),
            ],
        ),
    ]