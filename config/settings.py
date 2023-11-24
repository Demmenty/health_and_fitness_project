from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

# DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG = True

DOMAIN_NAME = config("DOMAIN_NAME")

# ALLOWED_HOSTS = [DOMAIN_NAME]
ALLOWED_HOSTS = ["*"]


# CSRF

# CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN_NAME}"]
CSRF_TRUSTED_ORIGINS = ["https://*.loca.lt"]

CSRF_FAILURE_VIEW = "users.views.csrf_failure"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home.apps.HomeConfig",
    "users.apps.UsersConfig",
    "client.apps.ClientConfig",
    "expert.apps.ExpertConfig",
    "metrics.apps.MetricsConfig",
    "nutrition.apps.NutritionConfig",
    "chat.apps.ChatConfig",
    "django_cleanup",
]

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
        "DIRS": [],
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


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    (BASE_DIR / "home" / "static"),
    (BASE_DIR / "users" / "static"),
    (BASE_DIR / "client" / "static"),
    (BASE_DIR / "expert" / "static"),
    (BASE_DIR / "metrics" / "static"),
    (BASE_DIR / "nutrition" / "static"),
]


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Users

AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


# Emails

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = config("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


# Fatsecret

FS_CONSUMER_KEY = config("FS_CONSUMER_KEY")
FS_CONSUMER_SECRET = config("FS_CONSUMER_SECRET")
