# Generated by Django 3.2.7 on 2021-11-19 19:47

import comment.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('comment', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='CommentLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(editable=False, max_length=512, null=True)),
                ('image', models.URLField(editable=False, null=True)),
                ('description', models.TextField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('comment', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='link', to='comment.comment')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('comment', 'link')},
            },
        ),
        migrations.CreateModel(
            name='CommentShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('tags', models.CharField(blank=True, max_length=16, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='comment_share', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('comment', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='HideComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hides', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='comment_hidden_status', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('comment', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='HideReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reply_hidden_status', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hides', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('reply', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='ReplyBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('reply', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='ReplyImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=comment.models.upload_reply_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ReplyImageUrl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_url', models.URLField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='image_urls', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ReplyLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(editable=False, max_length=512, null=True)),
                ('image', models.URLField(editable=False, null=True)),
                ('description', models.TextField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('reply', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='link', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('reply', 'link')},
            },
        ),
        migrations.CreateModel(
            name='ReplyShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('tags', models.CharField(blank=True, max_length=16, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reply_share', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='comment.commentreply')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('reply', 'created_by')},
            },
        ),
        migrations.DeleteModel(
            name='CommentVideoUrl',
        ),
    ]
