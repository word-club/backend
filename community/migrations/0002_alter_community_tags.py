# Generated by Django 4.0.2 on 2022-03-05 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='tags',
            field=models.ManyToManyField(related_name='communities', to='hashtag.Hashtag'),
        ),
    ]
