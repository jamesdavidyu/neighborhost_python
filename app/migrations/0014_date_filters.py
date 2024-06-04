# Generated by Django 5.0.3 on 2024-05-08 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_calendar_filters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date_filters',
            fields=[
                ('date_filter_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('date_by', models.CharField(max_length=6)),
                ('filter_date', models.DateField()),
                ('date_filtered_when', models.DateTimeField()),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
    ]
