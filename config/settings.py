import os
from pathlib import Path
from storages.backends.s3boto3 import S3Boto3Storage
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ["*"]

# APPEND_SLASH = False


LOCAL_APPS = [
    "pages.apps.PagesConfig",
    "apps.cinema.apps.CinemaConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS += LOCAL_APPS
INSTALLED_APPS += THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME':     os.getenv("POSTGRESQL_DB_NAME"), 
        'USER':     os.getenv("POSTGRESQL_DB_USER"),
        'PASSWORD': os.getenv("POSTGRESQL_DB_PASS"),
        'HOST':     os.getenv("POSTGRESQL_DB_HOST"),
        'PORT':     os.getenv("POSTGRESQL_DB_PORT"),

    }
}

# DATABASES = {'default' : dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

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


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "static/"
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

OUTPUT_ABS_URL = MEDIA_URL + "output.pdf"
OUTPUT_FILE_PATH = os.path.join(MEDIA_ROOT, "output.pdf")
SELF_URL = os.getenv("SELF", "http://127.0.0.1:8000")

class Liara(S3Boto3Storage):
    def __init__(self, **settings):
        super().__init__(**settings)

        self.bucket_name = os.getenv("S3_BUCKET")
        self.endpoint_url = os.getenv("S3_ENDPOINT")
        self.access_key = os.getenv("S3_ACCESS_KEY")
        self.secret_key = os.getenv("S3_SECRET_KEY")
        self.querystring_auth = False
        self.default_acl = "public-read"

LIARA_STORAGE = Liara
