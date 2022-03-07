# Generated by Django 4.0.2 on 2022-03-07 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('popularity', models.PositiveIntegerField(default=0, editable=False)),
                ('dislikes', models.PositiveIntegerField(default=0, editable=False)),
                ('discussions', models.PositiveIntegerField(default=0, editable=False)),
                ('supports', models.PositiveBigIntegerField(default=0, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('created_by', 'user')},
            },
        ),
    ]
