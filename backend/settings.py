"""
Django settings for backend project.
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# load environment
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = []

# SECURITY WARNING: don't include unknown hosts
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http:\/\/localhost\:8080$",
]

CSRF_TRUSTED_ORIGINS = [
    "localhost:8080",
]

# Application definition

INTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_APPS = [
    "channels",
    "rest_framework",
    "rest_framework.authtoken",
    "phonenumber_field",
    "django_filters",
    "corsheaders",
]

LOCAL_APPS = [
    "account",
    "hashtag",
    "community",
    "publication",
    "comment",
    "notification",
]

INSTALLED_APPS = INTERNAL_APPS + EXTERNAL_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["account", "community"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# postgresql configuration
# -------------------------------------------------------------

# DATABASES = {
#     'default': {
#         'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
#         'NAME'    : os.getenv("DB_NAME"),
#         'USER'    : os.getenv("DB_USER"),
#         'PASSWORD': os.getenv("DB_PASSWORD"),
#         'HOST'    : 'localhost',
#         'PORT'    : '',
#     }
# }
# -------------------------------------------------------------


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Django REST Framework Configuration

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 15,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TIME_ZONE")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Email Server Configuration
# https://docs.djangoproject.com/en/3.2/topics/email/
# https://docs.djangoproject.com/en/3.2/topics/email/#email-backends

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_USE_TLS = True
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.getenv("HOST_EMAIL")
# EMAIL_HOST_PASSWORD = os.getenv("HOST_PASSWORD")
# -----------------------------------------------------
# temporary configuration for mailhog local mail server
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_HOST_USER = "foo@bar.com"
# -----------------------------------------------------

ALLOWED_IMAGES_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "JPG"]
MAX_UPLOAD_IMAGE_SIZE = 70000

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ASGI_APPLICATION = "backend.asgi.application"

# Channels Configuration
# https://channels.readthedocs.io/en/stable/

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
