# Generated by Django 4.0.3 on 2022-03-26 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_votes', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='publication.publication')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(condition=models.Q(('publication__isnull', False)), fields=('up', 'publication', 'created_by'), name='unique_publication_vote'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(condition=models.Q(('comment__isnull', False)), fields=('up', 'comment', 'created_by'), name='unique_comment_vote'),
        ),
    ]
