# Generated by Django 3.2.7 on 2021-11-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='discussions',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='community',
            name='dislikes',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='community',
            name='popularity',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='community',
            name='supports',
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='community',
            name='view_globally',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='community',
            name='views',
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
    ]