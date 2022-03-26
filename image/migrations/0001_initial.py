# Generated by Django 4.0.3 on 2022-03-26 17:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publication', '0001_initial'),
        ('comment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(null=True)),
                ('image', models.ImageField(null=True, upload_to=helpers.upload_path.upload_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='comment.comment')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='publication.publication')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
