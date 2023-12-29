from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "healthfitness-demmenty.pythonanywhere.com",
]

CURRENT_DOMAIN = "http://healthfitness-demmenty.pythonanywhere.com"

# это добавлено из-за ошибки 'Origin checking failed'
CSRF_TRUSTED_ORIGINS = ["https://*.loca.lt"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authentication",
    "chat",
    "common",
    "homepage",
    "layouts",
    "client_overview",
    "mealjournal",
    "measurements",
    "fatsecret_app",
    "expert_overview",
    "expert_remarks",
    "expert_recommendations",
    "training",
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
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "health_and_fitness.urls"

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

WSGI_APPLICATION = "health_and_fitness.wsgi.application"

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATICFILES_DIRS = [
    (BASE_DIR / "chat" / "static"),
    (BASE_DIR / "common" / "static"),
    (BASE_DIR / "client_overview" / "static"),
    (BASE_DIR / "measurements" / "static"),
    (BASE_DIR / "expert_overview" / "static"),
    (BASE_DIR / "homepage" / "static"),
    (BASE_DIR / "training" / "static"),
]

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Users

LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/client_overview/"
LOGOUT_REDIRECT_URL = "/"

# Fatsecret

FS_CONSUMER_KEY = config("FS_CONSUMER_KEY")
FS_CONSUMER_SECRET = config("FS_CONSUMER_SECRET")
