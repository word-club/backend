# Generated by Django 3.2.7 on 2021-11-12 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_auto_20211112_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='completed_registration_steps',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]