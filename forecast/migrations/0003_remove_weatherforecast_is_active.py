# Generated by Django 4.2.3 on 2023-07-28 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_weatherforecast_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherforecast',
            name='is_active',
        ),
    ]