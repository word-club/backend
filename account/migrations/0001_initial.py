# Generated by Django 3.2.7 on 2021-10-17 12:00

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
                ('bio', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_authorized', models.BooleanField(default=False, editable=False)),
                ('authorized_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
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
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='covers', to='account.profile')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProfileAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=account.models.upload_profile_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='account.profile')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('to_follow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
