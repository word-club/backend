# Generated by Django 4.0.2 on 2022-03-19 22:25

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
