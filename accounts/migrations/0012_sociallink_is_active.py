# Generated by Django 4.2.2 on 2023-07-11 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_sociallink'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallink',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, help_text='Designates whether this link is viewed at the profile', verbose_name='Active'),
        ),
    ]
