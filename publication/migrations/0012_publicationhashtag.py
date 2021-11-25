# Generated by Django 3.2.7 on 2021-11-24 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0014_alter_communitycreateprogress_options'),
        ('publication', '0011_auto_20211123_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('hashtag', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='community.communityhashtag')),
                ('publication', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hashtags', to='publication.publication')),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('publication', 'hashtag')},
            },
        ),
    ]