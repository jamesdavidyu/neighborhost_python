# Generated by Django 4.2.6 on 2024-05-26 01:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_zipcodes_alter_addresses_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighborhoods',
            name='neighborhood_found_when',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 25, 21, 49, 40, 582381)),
        ),
    ]
