# Generated by Django 4.2.4 on 2023-08-20 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0003_location_remove_blooddemandprediction_population_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
