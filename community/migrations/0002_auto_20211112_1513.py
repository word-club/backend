# Generated by Django 3.2.7 on 2021-11-12 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityavatar',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='communitycover',
            name='is_active',
        ),
    ]