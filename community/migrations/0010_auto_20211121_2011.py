# Generated by Django 3.2.7 on 2021-11-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_community_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitysubscription',
            name='disable_notification',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.DeleteModel(
            name='CommunityDisableNotifications',
        ),
    ]
