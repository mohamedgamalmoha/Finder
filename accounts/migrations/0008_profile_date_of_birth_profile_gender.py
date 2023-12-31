# Generated by Django 4.2.2 on 2023-06-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_visitlog_is_scanned'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[(0, 'Male'), (1, 'Female'), (3, 'Other')], default=0, max_length=100, null=True, verbose_name='Gender'),
        ),
    ]
