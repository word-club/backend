# Generated by Django 4.0.3 on 2023-05-14 08:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=helpers.upload_path.upload_avatar_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('community', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_avatars', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to='account.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
