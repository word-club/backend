# Generated by Django 4.0.3 on 2022-03-26 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('community', '0001_initial'),
        ('publication', '0001_initial'),
        ('account', '0001_initial'),
        ('comment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='comment.comment')),
                ('community', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_hides', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='account.profile')),
                ('publication', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='publication.publication')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='hide',
            constraint=models.UniqueConstraint(condition=models.Q(('publication__isnull', False)), fields=('publication', 'created_by'), name='unique_publication_user_hide'),
        ),
        migrations.AddConstraint(
            model_name='hide',
            constraint=models.UniqueConstraint(condition=models.Q(('comment__isnull', False)), fields=('comment', 'created_by'), name='unique_comment_user_hide'),
        ),
        migrations.AddConstraint(
            model_name='hide',
            constraint=models.UniqueConstraint(condition=models.Q(('profile__isnull', False)), fields=('profile', 'created_by'), name='unique_profile_user_hide'),
        ),
        migrations.AddConstraint(
            model_name='hide',
            constraint=models.UniqueConstraint(condition=models.Q(('community__isnull', False)), fields=('community', 'created_by'), name='unique_community_user_hide'),
        ),
    ]
