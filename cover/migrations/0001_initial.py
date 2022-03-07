# Generated by Django 4.0.2 on 2022-03-07 14:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=helpers.upload_path.upload_cover_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('is_active', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('community', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='covers', to='community.community')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_covers', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='covers', to='account.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='cover',
            constraint=models.UniqueConstraint(condition=models.Q(('community__isnull', False)), fields=('community', 'is_active'), name='unique_community_active_cover'),
        ),
        migrations.AddConstraint(
            model_name='cover',
            constraint=models.UniqueConstraint(condition=models.Q(('profile__isnull', False)), fields=('profile', 'is_active'), name='unique_profile_active_cover'),
        ),
    ]
