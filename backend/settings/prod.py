from backend.settings.base import *

ALLOWED_HOSTS = [
    "wordclub.foodswipe.com.np",
]

# SECURITY WARNING: don't include unknown hosts
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"https?:\/\/wc.foodswipe.com.np$",
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME") or "wordclub",
        "USER": os.getenv("DB_USER") or "wordclub",
        "PASSWORD": os.getenv("DB_PASSWORD") or "wordclub",
        "HOST": os.getenv("DB_HOST") or "localhost",
        "PORT": os.getenv("DB_PORT") or "5432",
    }
}
# -------------------------------------------------------------

# Email Server Configuration
# https://docs.djangoproject.com/en/3.2/topics/email/
# https://docs.djangoproject.com/en/3.2/topics/email/#email-backends

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("HOST_EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("HOST_PASSWORD")
