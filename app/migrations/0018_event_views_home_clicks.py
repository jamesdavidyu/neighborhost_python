# Generated by Django 5.0.3 on 2024-05-15 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_events_event_zipcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_views',
            fields=[
                ('event_view_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('event_viewed_when', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.events')),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
        migrations.CreateModel(
            name='Home_clicks',
            fields=[
                ('home_click_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('home_clicked_when', models.DateTimeField()),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
    ]
