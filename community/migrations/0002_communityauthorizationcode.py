# Generated by Django 3.2.7 on 2021-09-29 20:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityAuthorizationCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='authorization_codes', to='community.community')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]