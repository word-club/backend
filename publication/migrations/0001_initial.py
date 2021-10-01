# Generated by Django 3.2.7 on 2021-10-01 16:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import publication.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hashtag', '0001_initial'),
        ('community', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False, editable=False)),
                ('published_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_pinned', models.BooleanField(default=False, editable=False)),
                ('view_count', models.PositiveBigIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PublicationImageUrl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_url', models.URLField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='image_urls', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PublicationImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=publication.models.upload_publication_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ReportPublication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reason', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reported_publications', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='PublicationUpVote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='up_voted_publications', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='up_votes', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='PublicationHashtag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hashtags', to='publication.publication')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='hashtag.hashtag')),
            ],
            options={
                'unique_together': {('publication', 'tag')},
            },
        ),
        migrations.CreateModel(
            name='PublicationDownVote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='down_voted_publications', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='down_votes', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='PublicationBookmark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_bookmarked', models.BooleanField(default=True, editable=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='HidePublication',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hidden_publications', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hides', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'created_by')},
            },
        ),
    ]
