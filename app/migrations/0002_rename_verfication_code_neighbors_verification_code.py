# Generated by Django 5.0.3 on 2024-04-23 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='neighbors',
            old_name='verfication_code',
            new_name='verification_code',
        ),
    ]
