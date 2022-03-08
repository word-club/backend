# Generated by Django 4.0.2 on 2022-03-08 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='comment.comment')),
                ('community', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_bookmarks', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='publication.publication')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(condition=models.Q(('publication__isnull', False)), fields=('publication', 'created_by'), name='unique_publication_user_bookmark'),
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(condition=models.Q(('comment__isnull', False)), fields=('comment', 'created_by'), name='unique_comment_user_bookmark'),
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(condition=models.Q(('community__isnull', False)), fields=('community', 'created_by'), name='unique_community_user_bookmark'),
        ),
    ]
