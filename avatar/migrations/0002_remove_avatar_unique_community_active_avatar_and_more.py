# Generated by Django 4.0.2 on 2022-03-17 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avatar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='avatar',
            name='unique_community_active_avatar',
        ),
        migrations.RemoveConstraint(
            model_name='avatar',
            name='unique_profile_active_avatar',
        ),
    ]