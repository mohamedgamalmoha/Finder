# Generated by Django 4.2.2 on 2023-06-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitlog',
            name='is_scanned',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is scanned by qr code'),
        ),
    ]