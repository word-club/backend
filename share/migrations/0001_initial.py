# Generated by Django 4.0.2 on 2022-03-02 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publication', '0001_initial'),
        ('comment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='publication.publication')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='share',
            constraint=models.UniqueConstraint(condition=models.Q(('publication__isnull', False)), fields=('publication', 'created_by'), name='unique_publication_share'),
        ),
        migrations.AddConstraint(
            model_name='share',
            constraint=models.UniqueConstraint(condition=models.Q(('comment__isnull', False)), fields=('comment', 'created_by'), name='unique_comment_share'),
        ),
    ]
