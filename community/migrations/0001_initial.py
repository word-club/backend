# Generated by Django 4.0.2 on 2022-03-07 14:03

import community.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('unique_id', models.CharField(max_length=64, unique=True, validators=[community.validators.validate_unique_id])),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=256, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('quote', models.TextField(null=True)),
                ('welcome_text', models.TextField(null=True)),
                ('view_globally', models.BooleanField(default=True)),
                ('contains_adult_content', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted'), ('private', 'Private')], default='public', max_length=64)),
                ('is_authorized', models.BooleanField(default=False, editable=False)),
                ('authorized_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('popularity', models.PositiveIntegerField(default=0, editable=False)),
                ('dislikes', models.PositiveIntegerField(default=0, editable=False)),
                ('discussions', models.PositiveIntegerField(default=0, editable=False)),
                ('supports', models.PositiveBigIntegerField(default=0, editable=False)),
                ('views', models.PositiveBigIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_communities', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, related_name='communities', to='hashtag.Hashtag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('primary', 'Primary'), ('orange', 'Orange'), ('red', 'Red'), ('pink', 'Pink'), ('teal', 'Teal'), ('green', 'Green'), ('indigo', 'Indigo'), ('grey', 'Grey'), ('deep-purple', 'Purple'), ('amber', 'Amber')], default='primary', max_length=32)),
                ('subscriber_nickname', models.CharField(default='Subscribers', max_length=64)),
                ('state_after_subscription', models.CharField(default='Awesome', max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('community', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_community_themes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disable_notification', models.BooleanField(default=False, editable=False)),
                ('is_approved', models.BooleanField(default=False, editable=False)),
                ('approved_at', models.DateTimeField(editable=False, null=True)),
                ('is_banned', models.BooleanField(default=False, editable=False)),
                ('ban_reason', models.TextField(editable=False, null=True)),
                ('banned_at', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='community.community')),
                ('subscriber', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('subscriber', 'community')},
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_community_rules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('community', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('mod', 'Moderator'), ('sub', 'Sub Moderator')], max_length=3)),
                ('is_accepted', models.BooleanField(default=False, editable=False)),
                ('accepted_at', models.DateTimeField(editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='moderators', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_community_moderators', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_communities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('user', 'community', 'role')},
            },
        ),
    ]
