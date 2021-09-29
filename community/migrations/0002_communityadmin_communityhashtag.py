# Generated by Django 3.2.7 on 2021-09-29 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hashtags', to='community.community')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities', to='hashtag.hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='CommunityAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_community_admins', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_communities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]