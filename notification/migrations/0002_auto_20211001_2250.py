# Generated by Django 3.2.7 on 2021-10-01 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
        ('publication', '0001_initial'),
        ('community', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='for_everyone',
            new_name='is_global',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='is_read',
            new_name='seen',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='comment_involved',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='community_involved',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='publication_involved',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='target',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user_involved',
        ),
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='PublicationNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('notification', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='notification.notification')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='NotificationTo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notification', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='receivers', to='notification.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='community.community')),
                ('notification', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='communities', to='notification.notification')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommentNotification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='comment.comment')),
                ('notification', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='notification.notification')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
