# Generated by Django 5.0.3 on 2024-04-23 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_verify_id_verify_laters_later_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verifiers',
            fields=[
                ('verifier_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('neighbor_id', models.IntegerField()),
                ('verifier_when', models.DateTimeField()),
            ],
        ),
    ]
