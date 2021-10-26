# Generated by Django 3.2.7 on 2021-10-26 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('orange', 'Orange'), ('red', 'Red'), ('pink', 'Pink'), ('teal', 'Teal'), ('green', 'Green'), ('indigo', 'Indigo'), ('grey', 'Grey'), ('deep-purple', 'Purple'), ('amber', 'Amber')], max_length=50)),
                ('community', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='added_themes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
