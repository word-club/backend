from django.apps import AppConfig


class UpvoteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vote"

    def ready(self):
        import vote.signals
