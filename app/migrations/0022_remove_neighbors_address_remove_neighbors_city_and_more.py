# Generated by Django 5.0.3 on 2024-05-21 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_friend_requests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='neighbors',
            name='address',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='city',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='state',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='verification_code',
        ),
        migrations.RemoveField(
            model_name='neighbors',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='events',
            name='event_private',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='none', max_length=255)),
                ('last_name', models.CharField(default='none', max_length=255)),
                ('address', models.CharField(default='none', max_length=50)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=35)),
                ('zipcode', models.CharField(default='none', max_length=10)),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('friend_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('friend_status', models.CharField(max_length=8)),
                ('friended_when', models.DateTimeField()),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
        migrations.CreateModel(
            name='Verifications',
            fields=[
                ('verification_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('verification_code', models.CharField(max_length=6)),
                ('code_generated_when', models.DateTimeField()),
                ('neighbor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.neighbors')),
            ],
        ),
    ]
