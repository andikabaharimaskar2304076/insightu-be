# Generated by Django 4.2 on 2025-06-04 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_psychologistprofile_is_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
