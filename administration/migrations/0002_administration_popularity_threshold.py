# Generated by Django 3.2.7 on 2021-11-29 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='administration',
            name='popularity_threshold',
            field=models.PositiveIntegerField(default=15),
        ),
    ]