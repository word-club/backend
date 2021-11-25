from django.db import models
from django.core.exceptions import ValidationError

class Administration(models.Model):
    publication_update_limit = models.PositiveIntegerField(
        default=30, help_text="in days"
    )
    top_count = models.PositiveIntegerField(default=50)

    def save(self, *args, **kwargs):
        if not self.pk and Administration.objects.exists():
            raise ValidationError("Only one instance is allowed.")
        return super().save(*args, **kwargs)


class PageView(models.Model):
    homepage = models.PositiveIntegerField(default=0)
    publications = models.PositiveIntegerField(default=0)
    community = models.PositiveIntegerField(default=0)
    profile = models.PositiveIntegerField(default=0)
    settings = models.PositiveIntegerField(default=0)
    administration = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk and PageView.objects.exists():
            raise ValidationError("Only one instance is allowed.")
        return super().save(*args, **kwargs)
