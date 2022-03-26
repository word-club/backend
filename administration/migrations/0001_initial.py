# Generated by Django 4.0.3 on 2022-03-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_update_limit', models.PositiveIntegerField(default=30, help_text='in days')),
                ('popularity_threshold', models.PositiveIntegerField(default=15)),
                ('comment_update_limit', models.PositiveIntegerField(default=30, help_text='in days')),
                ('top_count', models.PositiveIntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homepage', models.PositiveIntegerField(default=0)),
                ('publications', models.PositiveIntegerField(default=0)),
                ('community', models.PositiveIntegerField(default=0)),
                ('profile', models.PositiveIntegerField(default=0)),
                ('settings', models.PositiveIntegerField(default=0)),
                ('administration', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
