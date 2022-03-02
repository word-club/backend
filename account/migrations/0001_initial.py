# Generated by Django 4.0.2 on 2022-03-02 20:28

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(null=True)),
                ('birth_date', models.DateField(null=True)),
                ('is_authorized', models.BooleanField(default=False, editable=False)),
                ('authorized_at', models.DateTimeField(editable=False, null=True)),
                ('display_name', models.CharField(max_length=30, null=True)),
                ('allow_follow', models.BooleanField(default=True)),
                ('adult_content', models.BooleanField(default=True)),
                ('content_visibility', models.BooleanField(default=True)),
                ('communities_visibility', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('popularity', models.PositiveIntegerField(default=0, editable=False)),
                ('dislikes', models.PositiveIntegerField(default=0, editable=False)),
                ('discussions', models.PositiveIntegerField(default=0, editable=False)),
                ('supports', models.PositiveBigIntegerField(default=0, editable=False)),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ResetPasswordCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_password_codes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProfileCover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=account.models.upload_cover_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('profile', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='cover', to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=account.models.upload_profile_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('profile', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('created_by', 'user')},
            },
        ),
        migrations.CreateModel(
            name='BlockUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('created_by', 'user')},
            },
        ),
    ]
