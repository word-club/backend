from backend.settings.base import *

# SECURITY WARNING: don't include unknown hosts
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# SECURITY WARNING: don't include unknown hosts
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http:\/\/localhost\:8080$",
    r"^http:\/\/127\.0\.0\.1\:8080$",
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Email Server Configuration
# https://docs.djangoproject.com/en/3.2/topics/email/
# https://docs.djangoproject.com/en/3.2/topics/email/#email-backends

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_HOST_USER = "foo@bar.com"
# -----------------------------------------------------

# Channels Configuration
# https://channels.readthedocs.io/en/stable/

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
