# Generated by Django 4.2.2 on 2023-06-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='qr_code',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='QR Code'),
        ),
    ]
