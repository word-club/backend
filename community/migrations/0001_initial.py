# Generated by Django 4.0.2 on 2022-03-04 19:59

import community.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hashtag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=64, unique=True, validators=[community.models.validate_unique_id])),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=256, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_authorized', models.BooleanField(default=False, editable=False)),
                ('authorized_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('type', models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted'), ('private', 'Private')], max_length=64)),
                ('completed_registration_steps', models.BooleanField(default=False, editable=False)),
                ('contains_adult_content', models.BooleanField(default=False)),
                ('date_of_registration', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('quote', models.TextField(null=True)),
                ('welcome_text', models.TextField(null=True)),
                ('popularity', models.PositiveIntegerField(default=0, editable=False)),
                ('dislikes', models.PositiveIntegerField(default=0, editable=False)),
                ('discussions', models.PositiveIntegerField(default=0, editable=False)),
                ('supports', models.PositiveBigIntegerField(default=0, editable=False)),
                ('views', models.PositiveBigIntegerField(default=0, editable=False)),
                ('view_globally', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('primary', 'Primary'), ('orange', 'Orange'), ('red', 'Red'), ('pink', 'Pink'), ('teal', 'Teal'), ('green', 'Green'), ('indigo', 'Indigo'), ('grey', 'Grey'), ('deep-purple', 'Purple'), ('amber', 'Amber')], default='primary', max_length=32)),
                ('to_call_subscriber', models.CharField(default='Subscribers', max_length=64)),
                ('state_after_subscription', models.CharField(default='Awesome', max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='added_themes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityCreateProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('1', 'Display'), ('2', 'Rules'), ('3', 'Hashtags'), ('4', 'Authorization'), ('5', 'Administration')], max_length=64)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_skipped', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='create_progress', to='community.community')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunityAuthorizationCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='authorization_codes', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='requested_community_authorization_codes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='CommunitySubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disable_notification', models.BooleanField(default=False, editable=False)),
                ('is_approved', models.BooleanField(default=False, editable=False)),
                ('approved_at', models.DateTimeField(editable=False, null=True)),
                ('is_banned', models.BooleanField(default=False, editable=False)),
                ('banned_at', models.DateTimeField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='community.community')),
                ('subscriber', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('subscriber', 'community')},
            },
        ),
        migrations.CreateModel(
            name='CommunitySubAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sub_admins', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_community_sub_admins', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_managed_communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('user', 'community')},
            },
        ),
        migrations.CreateModel(
            name='CommunityRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_community_rules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
                'unique_together': {('community', 'title')},
            },
        ),
        migrations.CreateModel(
            name='CommunityHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hashtags', to='community.community')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities', to='hashtag.hashtag')),
            ],
            options={
                'unique_together': {('tag', 'community')},
            },
        ),
        migrations.CreateModel(
            name='CommunityAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False, editable=False)),
                ('accepted_at', models.DateTimeField(editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_community_admins', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('user', 'community')},
            },
        ),
    ]
